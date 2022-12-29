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
    NeuralNetwork nn1 = new NeuralNetwork(2,3,1);
    NeuralNetwork nn2 = new NeuralNetwork(2,4,1);

    public static final int WIDTH = 600; //width of the frame
    public static final int HEIGHT = 800; //height of the frame

    //TODO: find out what this is for
    static final int TIME_PERIOD = 24;
    static int time = 0;

    private final int STARTING_RABBITS = 100;
    private final int STARTING_FOXES = 5;
    private final int STARTING_PLANTS = 5000;

    public static int resolution = 4;
    public static int scale = 4;
    static int amountOfFieldsX = (int)(WIDTH/scale);
    static int amountOfFieldsY = (int)(HEIGHT/scale);
    //Rabbits
    public static ArrayList<Animal> Rabbits = new ArrayList<>();
    public static ArrayList<Animal>[][] rGrid = new ArrayList[resolution][resolution];
    //Foxes
    public static ArrayList<Animal> Foxes = new ArrayList<>();
    public static ArrayList<Animal>[][] fGrid = new ArrayList[resolution][resolution];
    //Plants
    public static ArrayList<Plant> Plants = new ArrayList<>();
    public static ArrayList<Plant>[][] pGrid = new ArrayList[resolution][resolution];

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
    /*
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
     */

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
        //TODO: refactor the grid updating
        time += TIME_PERIOD;
        super.paintComponent(g);

        //clear all the grids
        for(int i = 0; i < resolution; i++){
            for(int j = 0; j < resolution; j++){
                pGrid[i][j].clear();
                rGrid[i][j].clear();
                fGrid[i][j].clear();
            }
        }

        for(int j = 0; j < Plants.size(); j++){
            Plant p = Plants.get(j);
            if(p.dead()) Plants.remove(p);
            else{
                //int column = (int)(p.getLocX() / resolution);
                int column = (int) Vector2D.map(p.getLocX(),0, WIDTH,0,resolution);
                //int row = (int)(p.getLocY() / resolution);
                int row = (int)Vector2D.map(p.getLocY(), 0, HEIGHT, 0, resolution);
                //Check for border cases
                if (column < 0) column = 0;
                else if (column >= resolution) column = resolution-1;
                if (row < 0) row = 0;
                else if (row >= resolution) row = resolution-1;
                //Add to the correct grid
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
                //int column = (int)(r.getLocX() / resolution);
                int column = (int)Vector2D.map(r.getLocX(),0,WIDTH,0,resolution);
                //int row = (int)(r.getLocY() / resolution);
                int row = (int)Vector2D.map(r.getLocY(), 0, HEIGHT, 0, resolution);
                //Check for border cases
                if (column < 0) column = 0;
                else if (column >= resolution) column = resolution-1;
                if (row < 0) row = 0;
                else if (row >= resolution) row = resolution-1;
                //Add to the correct grid
                rGrid[column][row].add(r);

                //Behavior
                r.flock(getGridFields(r.transform.location, rGrid));
                r.flee(getGridFields(r.transform.location, fGrid));
                r.searchFood(getGridFields(r.transform.location, pGrid));
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
                //int column = (int)(f.getLocX() / resolution);
                int column = (int)Vector2D.map(f.getLocX(),0,WIDTH,0,resolution);
                //int row = (int)(f.getLocY() / resolution);
                int row = (int)Vector2D.map(f.getLocY(), 0, HEIGHT, 0, resolution);
                //Check for border cases
                if (column < 0) column = 0;
                else if (column >= resolution) column = resolution-1;
                if (row < 0) row = 0;
                else if (row >= resolution) row = resolution-1;
                //Add to the correct grid
                fGrid[column][row].add(f);

                //Behavior
                f.flock(getGridFields(f.transform.location, fGrid));
                f.searchFood(getGridFields(f.transform.location, rGrid));
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
        //Generate inputs and targets
        double[] input = new double[2];
        double[] target = new double[1];
        input[0] = random.nextDouble(1);
        input[1] = random.nextDouble(1);
        target[0] = input[0] + input[1];
        //Train and paint
        nn1.train(input, target);
        nn1.paint((Graphics2D) g,1000,300, input, target);
        nn2.train(input,target);
        nn2.paint((Graphics2D) g,0,400, input, target);

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

    public ArrayList getGridFields(Vector2D location, ArrayList[][] grid){
        ArrayList list = new ArrayList();

        //int column = (int)(location.x / resolution);
        int column = (int)Vector2D.map(location.x, 0, HEIGHT, 0, resolution);
        //int row = (int)(location.y / resolution);
        int row = (int)Vector2D.map(location.y, 0, HEIGHT, 0, resolution);

        //String radius = "";

        for(int x = -1; x <= 1; x++){
            for(int y = -1;y <= 1; y++){
                int newCol = column+x;
                int newRow = row+y;
                if (((newCol >= 0 && newCol < resolution) &&
                        (newRow >= 0 && newRow < resolution))) list.addAll(grid[newCol][newRow]);
                //radius += "("+newCol+","+newRow+")";
            }
        }
        //System.out.println(radius);
        return list;
    }
    //TODO: this needs to be updated / does not work correctly right now!!!
    /*
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
     */


    /**
     * don't really know what this does
     * @param e
     */
    public void actionPerformed(ActionEvent e){
        repaint();
    }
}

