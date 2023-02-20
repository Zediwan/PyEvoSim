package Main;

import javax.swing.*;
import java.awt.*;

public class Main
{
    public static void main(String[] args)
    {
        JPanel simulationPanel = new JPanel();
        simulationPanel.setBackground(Color.lightGray);
        simulationPanel.setPreferredSize( new Dimension(1200,600));

        JPanel statPanel = new JPanel();
        statPanel.setBackground(Color.white);
        statPanel.setPreferredSize(new Dimension(200,200));

        JPanel graphPanel = new JPanel();
        graphPanel.setBackground(Color.darkGray);
        graphPanel.setPreferredSize(new Dimension(200,200));

        JFrame frame = new JFrame("Simulation");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(1000,1000);
        frame.setLayout(new BorderLayout(0,0));

        //frame.add(new CFrame());
        frame.add(graphPanel, BorderLayout.SOUTH);
        frame.add(statPanel, BorderLayout.EAST);
        frame.add(simulationPanel, BorderLayout.CENTER);
        frame.setVisible(true);


        CFrame frame2 = new CFrame();
        //CFrame frame1 = new CFrame(3200, 0 ,0);
        //CFrame frame2 = new CFrame(3200, 0, 2);
        //CFrame frame3 = new CFrame(1600, 2, 2);
    }
}
