package components;

import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.table.DefaultTableModel;
import java.awt.Dimension;
import java.awt.GridLayout;


public class Table extends JPanel {
    IVR reddit = new IVR();


    public Table() {
        super(new GridLayout(1,0));
        String[] columnNames = {
                "Post_ID",
                "Subreddit_ID",
                "TimeStamp",
                "Author",
                "Title",
                "Body",
                "Comments",
                "Link"};

        Object[][] data = {};


        DefaultTableModel defTableModel = new DefaultTableModel(data,columnNames);
        JTable table = new JTable(defTableModel);
        table.setPreferredScrollableViewportSize(new Dimension(500, 70));
        table.setFillsViewportHeight(true);

        //Create the scroll pane and add the table to it.
        JScrollPane scrollPane = new JScrollPane(table);

        //Add the scroll pane to this panel.
        add(scrollPane);

        for (Entry ent:reddit.entryTable) {
            defTableModel.addRow(ent.toObject());
        }
    }
}