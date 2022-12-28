package Main;
import Main.Helper.Vector2D;
import Main.NeuralNetwork.Network;
import Main.NeuralNetwork.NeuralNetwork;
import Main.NeuralNetwork.Neuron;
import Main.Organisms.Animals.Animal;
import Main.Organisms.Animals.Fox;
import Main.Organisms.Animals.Rabbit;
import Main.Organisms.Attributes.DNA;
import Main.Organisms.Plants.Grass;
import Main.Organisms.Plants.Plant;
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.Random;

//TODO: use grid in food search
//TODO: make mating a thing
//TODO: update data output
//TODO: add legend to Main.NeuralNetwork.NeuralNetwork.DNA
//TODO: add graphs

public class CFrame extends JPanel implements ActionListener {
    public static Random random = new Random();
    NeuralNetwork nn = new NeuralNetwork(2,10,1);
    Network n;

    public static final int WIDTH = 800; //width of the frame
    public static final int HEIGHT = 800; //height of the frame

    //TODO: find out what this is for
    static final int TIME_PERIOD = 24;
    static int time = 0;
    int newSend = 100;
    int time_ = 10;

    private final int STARTING_RABBITS = 100;
    private final int STARTING_FOXES = 5;
    private final int STARTING_PLANTS = 5000;

    static double resolution = 10;
    static int amountOfFieldsX = (int)(WIDTH/resolution);
    static int amountOfFieldsY = (int)(HEIGHT/resolution);
    //Rabbits
    public static ArrayList<Animal> Rabbits = new ArrayList<>();
    public static ArrayList<Animal>[][] rGrid = new ArrayList[amountOfFieldsX][amountOfFieldsY];
    //Foxes
    public static ArrayList<Animal> Foxes = new ArrayList<>();
    public static ArrayList<Animal>[][] fGrid = new ArrayList[amountOfFieldsX][amountOfFieldsY];
    //Plants
    public static ArrayList<Plant> Plants = new ArrayList<>();
    public static ArrayList<Plant>[][] pGrid = new ArrayList[amountOfFieldsX][amountOfFieldsY];

    public CFrame(){
        JFrame frame = new JFrame("Ecosystem");     //title of the frame
        frame.setSize(WIDTH, HEIGHT);                    //frame size
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        this.initiate();
        //this.initiateNetwork();

        Timer t = new Timer(TIME_PERIOD,this);
        t.start();

        frame.add(this);
        frame.setVisible(true);
    }

    //TEST
    public void initiateNetwork(){
        n = new Network(1100,500);

        Neuron a = new Neuron(-200,0);
        Neuron b = new Neuron(0,100);
        Neuron c = new Neuron(0,-100);
        Neuron d = new Neuron(200,0);

        n.addNeuron(a);
        n.addNeuron(b);
        n.addNeuron(c);
        n.addNeuron(d);

        n.connect(a,b);
        n.connect(a,c);
        n.connect(b,d);
        n.connect(c,d);
    }

    public void initiate(){
        for(int i=0;i<rGrid.length;i++) {
            for (int i2 = 0; i2 < rGrid[i].length; i2++) {
                rGrid[i][i2] = new ArrayList<>();
                pGrid[i][i2] = new ArrayList<>();
                fGrid[i][i2] = new ArrayList<>();
            }
        }
        for(int i = 0; i < STARTING_RABBITS; i++) Rabbits.add(new Rabbit());
        for(int i = 0; i < STARTING_FOXES; i++) Foxes.add(new Fox());
        for(int j = 0; j < STARTING_PLANTS; j++) Plants.add(new Grass());
    }


    /**
     *
     * @param g
     */
    public void paint(Graphics g) {
        time += TIME_PERIOD;
        super.paintComponent(g);

        for(int j = 0; j < Plants.size(); j++){
            Plant p = Plants.get(j);
            if(p.dead()) Plants.remove(p);
            else{
                int column = (int)Math.round(p.getLocX() / resolution);
                int row = (int)Math.round(p.getLocY() / resolution);
                if (column < 0) column = 0;
                else if (column >= amountOfFieldsX) column = amountOfFieldsX-1;
                if (row < 0) row = 0;
                else if (row >= amountOfFieldsY) row = amountOfFieldsY-1;
                pGrid[column][row].add(p);

                p.update();
                p.paint((Graphics2D) g);
            }
        }

        for(int i = 0; i < Rabbits.size(); i++){
            Animal r = Rabbits.get(i);
            //Remove if rabbit is dead
            if(r.dead()) Rabbits.remove(i);
            else{
                //Define Grid position
                int column = (int)Math.round(r.getLocX() / resolution);
                int row = (int)Math.round(r.getLocY() / resolution);
                if (column < 0) column = 0;
                else if (column >= amountOfFieldsX) column = amountOfFieldsX-1;
                if (row < 0) row = 0;
                else if (row >= amountOfFieldsY) row = amountOfFieldsY-1;
                rGrid[column][row].add(r);

                //Behavior
                r.flock(getGridFields(r.transform.location, rGrid));
                r.flee(getGridFields(r.transform.location, fGrid));
                r.update();
                r.paint((Graphics2D)g);

                //Reproduction
                r.reproduce();
            }
        }

        for(int i = 0; i < Foxes.size(); i++){
            Animal f = Foxes.get(i);
            //Remove if rabbit is dead
            if(f.dead()) Foxes.remove(i);
            else{
                //Define Grid position
                int column = (int)(f.getLocX() / resolution);
                int row = (int)(f.getLocY() / resolution);
                if (column < 0) column = 0;
                else if (column >= amountOfFieldsX) column = amountOfFieldsX-1;
                if (row < 0) row = 0;
                else if (row >= amountOfFieldsY) row = amountOfFieldsY-1;
                fGrid[column][row].add(f);

                //Behavior
                f.flock(getGridFields(f.transform.location, fGrid));
                f.update();
                f.paint((Graphics2D)g);

                //Reproduction
                f.reproduce();
            }

            //Interface
            //TODO: make a class or something better here
            g.setColor(Color.BLACK);
            if(Fox.totalAmountOfFoxes > 0) g.drawString("Avg F:  "+
                    DNA.div(Fox.totalAmountOfFoxes, Fox.sumDNA), CFrame.WIDTH,15);
            if(Rabbit.totalAmountOfRabbits > 0) g.drawString("Avg R: " +
                    DNA.div(Rabbit.totalAmountOfRabbits, Rabbit.sumDNA), CFrame.WIDTH,30);
            g.drawString("Amount of Foxes:       " +
                    Foxes.size(), CFrame.WIDTH, 45);
            g.drawString("Amount of Rabbits:    " +
                    Rabbits.size(), CFrame.WIDTH, 60);
            g.drawString("Amount of Plants:      " +
                    Plants.size(), CFrame.WIDTH, 75);
            g.drawString("Total amount of Foxes (naturally born):   " +
                    Fox.totalAmountOfFoxes, CFrame.WIDTH, 90);
            g.drawString("Total amount of Rabbits (naturally born): " +
                    Rabbit.totalAmountOfRabbits, CFrame.WIDTH, 105);

            //n.paint((Graphics2D) g, 1100, 500);
        }

        if(Foxes.size() <= 0) for(int i = 0; i< 1; i++) Foxes.add(new Fox());
        if(Rabbits.size() <= 0) for(int i = 0; i< 5; i++) Rabbits.add(new Rabbit());
        if(random.nextInt()<= 1 && Plants.size()<= 5000) for(int i = 0; i< 10; i++) Plants.add(new Grass());

        //NN
        double[] input = new double[2];
        double[] target = new double[1];
        input[0] = random.nextInt(2);
        input[1] = random.nextInt(2);
        if(input[0] + input[1] > 0) target[0] = 1;
        else target[0] = 0;
        nn.train(input, target);
        nn.paint((Graphics2D) g,1200,500);

        //Network
        /*
        this.time_ -= 1;
        if(this.time_ <= 0){
            this.time_ = this.newSend;
            n.feedForward(Math.random());
        }
        n.update();
         */
    }

    //TODO: this needs to be updated / does not work correctly right now!!!
    public ArrayList getGridFields(Animal a, ArrayList[][] grid){
        ArrayList list = new ArrayList();
        int column = (int)(a.transform.location.x / resolution);
        int row = (int)(a.transform.location.x / resolution);

        String radius = "";

        int fieldViewDistanceX = (int)(a.viewDistance / amountOfFieldsX);
        int fieldViewDistanceY = (int)(a.viewDistance / amountOfFieldsY);

        for(int x = -fieldViewDistanceX; x <= fieldViewDistanceX; x++){
            for(int y = -fieldViewDistanceY;y <= fieldViewDistanceY; y++){
                int newCol = column+x;
                int newRow = row+y;
                if (((newCol >= 0 && newCol < amountOfFieldsX) && (newRow >= 0 && newRow < amountOfFieldsY))) list.addAll(grid[newCol][newRow]);
                radius += "("+newCol+","+newRow+")";
            }
        }
        System.out.println(radius);
        return list;
    }
    public ArrayList getGridFields(Vector2D location, ArrayList[][] grid){
        ArrayList list = new ArrayList();

        int column = (int)(location.x / resolution);
        int row = (int)(location.x / resolution);

        //String radius = "";

        for(int x = -1; x <= 1; x++){
            for(int y = -1;y <= 1; y++){
                int newCol = column+x;
                int newRow = row+y;
                if (((newCol >= 0 && newCol < amountOfFieldsX) && (newRow >= 0 && newRow < amountOfFieldsY))) list.addAll(grid[newCol][newRow]);
                //radius += "("+newCol+","+newRow+")";
            }
        }
        //System.out.println(radius);
        return list;
    }

    /**
     * don't really know what this does
     * @param e
     */
    public void actionPerformed(ActionEvent e){
        repaint();
    }
}

