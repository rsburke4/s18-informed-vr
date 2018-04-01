package components;

import javax.swing.*;

public class Main
{

    public static void main(String[] args)
    {
        //Create and set up the window.
        JFrame frame = new JFrame("Informed Virtual Reality");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        //Create and set up the content pane.
        Table newContentPane = new Table();
        newContentPane.setOpaque(true); //content panes must be opaque
        frame.setContentPane(newContentPane);

        //Display the window.
        frame.setSize(1000, 100);
        frame.setVisible(true);
    }
}