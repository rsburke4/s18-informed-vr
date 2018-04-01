package components;


import java.time.Instant;
import java.util.Date;

public class Entry {
    String Post_ID;
    String Subreddit_ID;
    Date TimeStamp;
    String Author;
    String Title;
    String Body;
    String Comments;
    String Link;


    Entry(){
        Post_ID ="Post_ID";
        Subreddit_ID = "Subreddit_ID";
        TimeStamp = new Date();
        Author = "Author";
        Title = "Title";
        Body = "Body";
        Comments = "Comments";
        Link = "Link";
    }

    @Override
    public String toString() {
        return Post_ID + ", " + Subreddit_ID + ", " + TimeStamp + ", " + Author + ", " + Title + ", " + Body + ", " + Comments + ", " + Link + "\n";
    }

    public Object[] toObject(){
        return new String[]{Post_ID, Subreddit_ID, TimeStamp.toString(), Author, Title, Body, Comments, Link};
    }
}
