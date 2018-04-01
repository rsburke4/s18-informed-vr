package components;

import java.sql.*;
import java.util.ArrayList;
import java.util.Date;

public class IVR {
    String out;
    Entry temp = new Entry();
    ArrayList <Entry> entryTable = new ArrayList<>();
    Date date = new Date(1425349529);
    {
        try
        {
            // create our mysql database connection
            String myDriver = "com.mysql.jdbc.Driver";
            String myUrl = "jdbc:mysql://mysql1.cs.clemson.edu/reddit_informed_virtual_reality";
            Class.forName(myDriver);
            Connection conn = DriverManager.getConnection(myUrl, "ivr", "ivrreddit!");

            // our SQL SELECT query.
            // if you only need a few columns, specify them by name instead of using "*"
            String query = "SELECT * FROM Posts";

            // create the java statement
            Statement st = conn.createStatement();

            // execute the query, and get a java resultset
            ResultSet rs = st.executeQuery(query);

            // iterate through the java resultset
            int i = 0;
            while (rs.next())
            {
                temp.Post_ID = rs.getString("Post_ID");
                temp.Subreddit_ID = rs.getString("Subreddit_ID");
                temp.TimeStamp = new Timestamp(1425349529);//rs.getDate("TimeStamp");
                temp.Author = rs.getString("Author");
                temp.Title = rs.getString("Title");
                temp.Body = rs.getString("Body");
                temp.Comments = rs.getString("Comments");
                temp.Link = rs.getString("Link");

                out = temp.toString();

                entryTable.add(i,temp);

                // print the results
                //System.out.format(temp.toString());

                temp = new Entry();

                i++;
            }

            st.close();
        }
        catch (Exception e)
        {
            System.err.println("Got an exception! ");
            System.err.println(e.getMessage());
            e.printStackTrace();
        }
    }
}
