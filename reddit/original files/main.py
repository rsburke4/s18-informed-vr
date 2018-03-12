import numpy as np

import RedditAPI
import RedditNLP

# Download an entire subreddit
RedditAPI.fetch_subreddit("Vive", size=499, print_to_file=True, utc_start_date=1462278632)

# Apply tf-idf to a subreddit
#submissions, documents = RedditNLP.load_reddit_dump("Vive_submissions - 1st Part.txt")
#submission_weeks, weeks = RedditNLP.group_submissions_by_date(submissions)

#Xtr, vec = RedditNLP.compute_tfidf_for_submissions(documents)

#dfs = []
#for week in weeks:
#    filter = [x == week for x in submission_weeks]
#    dat = RedditNLP.top_mean_feats(Xtr, vec.get_feature_names(), np.where(filter)[0])
#    print("### " + week + " ###################################################")
#    print(dat)
#    dat.label = weeks
#    dfs.append(dat)

#RedditNLP.plot_tfidf_classfeats_h(dfs)