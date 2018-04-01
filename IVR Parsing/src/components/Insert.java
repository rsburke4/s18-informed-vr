package components;

import java.io.*;
import java.util.ArrayList;
import java.util.Date;

public class Insert {


    ArrayList <String> lines = new ArrayList<>();
    ArrayList <Entry> entryTable = new ArrayList<>();
    ArrayList <Entry> Comments = new ArrayList<>();
    File input = new File("Vive_submissions.txt");

    public void parseFile() throws  IOException{
        try(BufferedReader br = new BufferedReader(new FileReader(input))) {
            for(String line; (line = br.readLine()) != null; ) {
                line = line.trim();



                if (line.charAt(0) == '['){
                    lines.add("INSERT INTO Posts");
                    lines.add("    (Post_ID, Subreddit_ID, TimeStamp, Author, Title, Body, Comments, Link)");
                    lines.add("VALUES");
                }
                Entry temp = postParser(line);

                lines.add("    " + temp.toString() + ",\n");
            }
            // line is not visible here.
        }
        catch (FileNotFoundException e)
        {
            System.err.println("Got an exception! ");
            System.err.println(e.getMessage());
            e.printStackTrace();
        }
        //write lines to output file
        FileWriter writer  = new FileWriter("mysql_instructions.txt");
        for (Entry tmp:entryTable) {
            writer.write(tmp.toString());
        }


    }

    public Entry postParser(String input){
        Entry temp = new Entry();
        if (input.contains("\"author\"")){
            temp.Author = authorParser(input);
        }
        if (input.contains("\"body\"")){
            temp.Body = bodyParser(input);
        }
        if (input.contains("\"created\"")){
            temp.TimeStamp = createdParser(input);
        }
        if (input.contains("\"id\"")){
            temp.Post_ID = idParser(input);
        }
        if (input.contains("\"subreddit_id\"")){
            temp.Subreddit_ID = sub_idParser(input);
        }
        if (input.contains("\"title\"")){
            temp.Title = titleParser(input);
        }
        if (input.contains("\"comments\"")){
            if (input.contains("}")){
                temp.Comments = "None";
            }
            else{
                commentParser(input);
            }
        }
        return temp;
    }

    public void commentParser(String input){
        Entry temp = new Entry();

    }
    public String  authorParser(String input){
        return  input.substring(input.indexOf(": \"") + 3, input.indexOf("\","));
    }
    public String bodyParser(String input){
        return  input.substring(input.indexOf(": \"") + 3, input.indexOf("\","));
    }
    public Date createdParser(String input){
        String date  = input.substring(input.indexOf(": ") + 2, input.indexOf(","));
        long epoch = Long.parseLong(date);
        return new Date(epoch*1000);
    }
    public String idParser(String input){
        return  input.substring(input.indexOf(": \"") + 3, input.indexOf("\","));
    }
    public String sub_idParser(String input){
        return  input.substring(input.indexOf(": \"") + 3, input.indexOf("\","));
    }
    public String titleParser(String input){
        return  input.substring(input.indexOf(": \"") + 3, input.indexOf("\","));
    }
}
