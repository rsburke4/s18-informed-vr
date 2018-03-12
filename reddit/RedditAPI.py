import requests
import datetime
import json

# This class uses the pushshift.io API to download Reddit data
# Two main types of data can be accessed
# - Submissions: top level threads
# - Comments: content of posts added to threads

# JSON submission format
# {
#  id: {}
#  subreddit_id: {}
#  created: {}
#  author: {}
#  title: {}
#  body: {}
#  comments: {}
#  link: {}
# }

# JSON comment format
# {
#  id: {}
#  created: {}
#  author: {}
#  body: {}
#  comments: {}
# }


# To download a subreddit, we need to fetch all of the submissions in that subreddit,
# and then fetch all the comments within these submissions
def fetch_subreddit(subreddit_name, size=250, utc_start_date=None, utc_end_date=None, print_to_file=False):
    # Create a list within which we will store all the comments
    submissions = {}
    
    end = int(utc_start_date)+86400
    
    # create the first URL we'll use to start the process
    url = "https://api.pushshift.io/reddit/search/submission/?subreddit=" + subreddit_name + \
          "&sort=asc" + \
          "&size=" + str(size)
    if utc_start_date is not None:
        url += "&after=" + str(utc_start_date)
    if utc_end_date is not None:
        url += "&before=" + str(utc_end_date)

    if print_to_file:
        f = open(subreddit_name + '_submissions_'+ datetime.datetime.fromtimestamp(int(utc_start_date)).strftime('%Y-%m-%d') +'.txt', 'w', encoding='utf-8')
        f.write("[")

    # Begin fetching responses
    continue_fetching = True
    while continue_fetching:
        response = requests.get(url)
        try:
            # Get the response from the server
            j = response.json()
            # Check to make sure we got valid data
            if "data" in j:
                # Iterate through each returned response and process it
                for submission in j["data"]:
                    sub = parse_submission(submission)
                    submissions[sub["id"]] = sub

                    if print_to_file:
                        json.dump(sub, f, sort_keys=True, indent=4)
                        f.write(",\n")

                # Fetch the datetime of the last comment
                next_datetime = j["data"][-1]["created_utc"]
                
                sub_time = int(next_datetime)
                if int(created_utc) >= end:
                    continue_fetching = False
                # Update the URL to fetch the next batch
                url = "https://api.pushshift.io/reddit/search/submission/?subreddit=" + subreddit_name + \
                      "&sort=asc" + \
                      "&size=" + str(size) + \
                      "&after=" + str(next_datetime)
                if utc_end_date is not None:
                    url += "&before=" + str(utc_end_date)

                if len(submissions) % size * 100 == 0:
                    print("Fetched " + str(len(submissions)) + " submissions... Current datetime is " + \
                          datetime.datetime.fromtimestamp(int(next_datetime)).strftime('%Y-%m-%d %H:%M:%S'))
        
            else:
                continue_fetching = False

        except json.decoder.JSONDecodeError:
            print("Could not parse JSON document")
            print(response.content)

    if print_to_file:
        f.write("]")
        f.close()

    return submissions


def parse_submission(submission):
    sub = {}
    sub["id"] = submission["id"]
    sub["subreddit_id"] = submission["subreddit_id"]
    sub["created"] = submission["created_utc"]
    sub["author"] = submission["author"]
    sub["title"] = submission["title"]
    if "selftext" in submission:
        sub["body"] = submission["selftext"]
    else:
        sub["body"] = ""
    sub["link"] = submission["full_link"]
    sub["comments"] = fetch_comments_for_submission(sub["id"])
    return sub


def fetch_comments_for_submission(submission_id, max_comments_in_request = 500):
    url="https://api.pushshift.io/reddit/submission/comment_ids/"+submission_id
    response = requests.get(url)
    j = response.json()

    # If we request too many comments at once, we'll get an error because the request string will exceed 4096 characters
    # As such, we split the comments into multiple sets. Allowing no more than 500 comments per request will avoid this error
    comment_count = 0
    comment_ids = []
    for submission in j["data"]:
        # Determine which set we're adding this comment to
        index = comment_count // max_comments_in_request
        # Check to make sure this set exists, if not, create it
        if len(comment_ids) == index:
            comment_ids.append("")
        # Append the comment request
        comment_ids[index] += submission + ","
        comment_count += 1

    if comment_ids:
        return fetch_comments(comment_ids)
    else:
        return {}

# fetch_comments expects a comma separated list of comment ids
# e.g. "dlrezc8,dlrawgw,dlrhbkq"
def fetch_comments(comment_ids):
    url="https://api.pushshift.io/reddit/comment/search?ids="
    all_comments = []
    for comments in comment_ids:
        response = requests.get(url + comments)
        j = response.json()
        if "data" in j:
            all_comments.extend(j["data"])
    if len(all_comments) > 0:
        return organize_comments(all_comments)
    else:
        return {}


# Organize the fetched comments into the appropriate hierarchy
def organize_comments(comments):
    top_level_comments = {}
    all_comments = {}
    unorganized_comments = []

    # First, we iterate through all of the comments and add them to a few lists
    # Add all comments to the all_comments dictionary
    # If the parent_id == link_id, then it's a top level comment, and add it to that dictionary
    # If the parent_id == a comment in all_comments, add it to the child list of that comment
    # Otherwise, add it to the unorganized comment list, and we'll assign it later
    for c in comments:
        # Create a comment object
        com = {}
        com["id"] = c["id"]
        com["created"] = c["created_utc"]
        com["author"] = c["author"]
        com["body"] = c["body"]
        com["comments"] = {}

        # Add this comment to the list of all comments
        all_comments[com["id"]] = com

        # This is a top-level comment
        if c["parent_id"] == c["link_id"]:
            top_level_comments[com["id"]] = com
        # This is a child comment
        # Strip off the first three characters, as those tell us what type of entity the parent comment is
        # See https://www.reddit.com/dev/api/#fullnames
        elif c["parent_id"][3:] in all_comments:
            all_comments[c["parent_id"][3:]]["comments"][com["id"]] = com
        else:
            com["parent_id"] = c["parent_id"][3:]
            unorganized_comments.append(com)

    # Now go through and assign all unorganized comments possible
    try:
        for c in unorganized_comments:
            if c["parent_id"] in all_comments:
                all_comments[c["parent_id"]]["comments"][c["id"]] = c
                c.pop('parent_id', None)
            else:
                print("!! Orphaned comment !!")
    except:
        pass

    return top_level_comments




########################################################################################################################
def fetch_all_comments_in_subreddit(subreddit_name, size=250, utc_start_date=None, utc_end_date=None, print_to_file=False):
    # Create a list within which we will store all the comments
    comments = []

    # create the first URL we'll use to start the process
    url = "https://api.pushshift.io/reddit/comment/search?subreddit=" + subreddit_name + \
          "&sort=asc" + \
          "&size=" + str(size)
    if utc_start_date != None:
        url += "&after="+str(utc_start_date)
    if utc_end_date != None:
        url += "&before="+str(utc_end_date)

    if print_to_file:
        f = open(subreddit_name + '.txt', 'w', encoding='utf-8')

    # Begin fetching responses
    continue_fetching = True
    while continue_fetching:
        response = requests.get(url)
        try:
            j = response.json()

            if len(j["data"]) > 0:
                # Record these comments
                comments.extend(j["data"])

                if print_to_file:
                    for comment in j["data"]:
                        f.write(str(comment["body"].encode("utf-8"))[2:-1])
                        f.write('\n')

                # Fetch the datetime of the last comment
                next_datetime = j["data"][-1]["created_utc"]

                # Update the URL to fetch the next batch
                url = "https://api.pushshift.io/reddit/comment/search?subreddit=" + subreddit_name + \
                      "&sort=asc" + \
                      "&size=" + str(size) + \
                      "&after=" + str(next_datetime)
                if utc_end_date != None:
                    url += "&before=" + str(utc_end_date)

                if len(j["data"]) % size * 1000 == 0:
                    print("Fetched " + str(len(comments)) + " comments... Current datetime is " + \
                          datetime.datetime.fromtimestamp(int(next_datetime)).strftime('%Y-%m-%d %H:%M:%S'))
            else:
                continue_fetching = False

        except json.decoder.JSONDecodeError:
            print("Could not parse JSON document")
            print(response.content)

    if print_to_file:
        f.close()

    return comments
