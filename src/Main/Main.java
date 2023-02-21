package Main;

import javax.swing.*;
import java.awt.*;

public class Main
{
    public static void main(String[] args)
    {
        /*
        JPanel statPanel = new JPanel();
        statPanel.setBackground(Color.white);
        statPanel.setPreferredSize(new Dimension(200,200));

        JPanel graphPanel = new JPanel();
        graphPanel.setBackground(Color.darkGray);
        graphPanel.setPreferredSize(new Dimension(200,200));
         */
        //CFrame frame2 = new CFrame();
        World w = new World(400,400,10,10);
        Simulation s = new Simulation(100,100,100,
                100,100,100,
                100,100,100,
                w);
        s.initiatePopulation();
        //JPanel simulationPanel = s.setUpVisuals();
        //simulationPanel.setBackground(Color.lightGray);
        /*
         JFrame frame = new JFrame("Simulation");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(1000,1000);
        frame.setLayout(new BorderLayout(0,0));

        //frame.add(new CFrame());
        frame.add(graphPanel, BorderLayout.SOUTH);
        frame.add(statPanel, BorderLayout.EAST);
        //frame.add(simulationPanel, BorderLayout.CENTER);
        frame.setVisible(true);
         */
    }
}
