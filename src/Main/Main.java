package Main;

public class Main
{
    public static void main(String[] args)
    {
        World w = new World(400,400,10,10);
        Simulation s = new Simulation(100,100,100,
                100,100,100,
                100,100,100,
                w);
        s.initiatePopulation();
    }
}
