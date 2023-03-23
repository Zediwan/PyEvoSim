package Main;

public class Main
{
    public static void main(String[] args)
    {
        World w = new World(1000,800,10,10);
        Simulation s = new Simulation(10000,100,100000,
                80000,100000,10,
                100,100,
                w);
        s.initiatePopulation();
        while(true){
            //s.simFrame.getGraphics().fillOval(500,500,10,10);
            s.paint(s.simFrame.getGraphics());
        }
    }
}
