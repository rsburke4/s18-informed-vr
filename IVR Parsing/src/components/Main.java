package components;
import java.io.IOException;
import java.util.Scanner;

public class Main {
    public static void main(String[] args){

        System.out.println();

        Insert insert  = new Insert();
        try {
            insert.parseFile();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
