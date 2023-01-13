package Main;
import Main.Helper.Vector2D;
import Main.Organisms.Animals.Animal;
import Main.Organisms.Animals.Fox;
import Main.Organisms.Animals.Rabbit;
import Main.Organisms.Plants.Grass;
import Main.Organisms.Plants.Plant;
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.Random;

//TODO: make mating a thing
//TODO: add graphs

public class CFrame extends JPanel implements ActionListener {
    public static Random random = new Random();
    //NeuralNetwork nn1 = new NeuralNetwork(2,12,1);
    //NeuralNetwork nn2 = new NeuralNetwork(2,12,1);
    public static Animal currentTrackedR;
    public static Animal currentTrackedF;

    public double avgPHealth = 0;
    public double avgRHealth = 0;
    public double avgFHealth = 0;

    public double avgPAge;
    public double avgRAge = 0;
    public double avgFAge = 0;

    //TODO: find out what this is for
    static final int TIME_PERIOD = 24;
    static int time = 0;

    //FRAME SIZES
    public static final int WIDTH = 800; //width of the frame
    public static final int HEIGHT = 800; //height of the frame

    //GRID HANDLING
    public static int resolution = 10;              //total amount of fields in x and y direction not used right now
    public static int scale = 10;                   //width of a field
    static int numFieldsX = (WIDTH/scale);          //amount of fields in x dir
    static int numFieldsY = (HEIGHT/scale);         //amount of fields in y dir

    //Rabbits
    public static ArrayList<Animal> Rabbits = new ArrayList<>();
    public static ArrayList<Animal>[][] rGrid = new ArrayList[numFieldsY][numFieldsX];
    //Foxes
    public static ArrayList<Animal> Foxes = new ArrayList<>();
    public static ArrayList<Animal>[][] fGrid = new ArrayList[numFieldsY][numFieldsX];
    //Plants
    public static ArrayList<Plant> Plants = new ArrayList<>();
    public static ArrayList<Plant>[][] pGrid = new ArrayList[numFieldsY][numFieldsX];

    //SIMULATION VARIABLES
    //AMOUNT OF STARTING ENTITIES
    private final int STARTING_RABBITS = 1000;
    private final int STARTING_FOXES = 50;
    private final int STARTING_PLANTS = 16000;

    private final int MIN_NUM_RABBITS = 100;         //The amount at which the system starts spawning new Rabbits
    private final int MIN_NUM_FOXES = 5;            //The amount at which the system starts spawning new Foxes
    private final int MAX_NUM_PLANTS = WIDTH*HEIGHT/40;//The maximum amount of Plants allowed in the simulation at once

    private final int NUM_NEW_PLANTS = 10;          //The amount of new Plants being spawned each tick
    private final int NUM_NEW_RABBITS = 20;          //The amount of new Rabbits being spawned each tick
    private final int NUM_NEW_FOXES = 5;            //The amount of new Foxes being spawned each tick


    public CFrame(){
        JFrame frame = new JFrame("Ecosystem");     //title of the frame
        frame.setSize(WIDTH, HEIGHT);                    //frame size
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        this.initiate();

        Timer t = new Timer(TIME_PERIOD,this);
        t.start();

        frame.add(this);
        frame.setVisible(true);
    }

    public void initiate(){
        //initiate the grids
        for(int i1=0;i1<numFieldsY;i1++) {
            for (int i2 = 0; i2 < numFieldsX; i2++) {
                rGrid[i1][i2] = new ArrayList<>();
                pGrid[i1][i2] = new ArrayList<>();
                fGrid[i1][i2] = new ArrayList<>();
            }
        }
        //initiate the organisms
        for(int i = 0; i < STARTING_RABBITS; i++) Rabbits.add(new Rabbit());
        for(int i = 0; i < STARTING_FOXES; i++) Foxes.add(new Fox());
        for(int j = 0; j < STARTING_PLANTS; j++) Plants.add(new Grass());
        this.currentTrackedR = Rabbits.get(random.nextInt(Rabbits.size()));
    }

    /**
     *
     * @param g
     */
    public void paint(Graphics g) {
        time += TIME_PERIOD;
        super.paintComponent(g);

        //update tracked organisms if needed
        if(currentTrackedR.dead()) Rabbits.get(random.nextInt(Rabbits.size()));
        //if(currentTrackedF.dead()) Foxes.get(random.nextInt(Foxes.size()));

        //clear all the grids
        for(int i = 0; i < numFieldsY; i++){
            for(int j = 0; j < numFieldsX; j++){
                pGrid[i][j].clear();
                rGrid[i][j].clear();
                fGrid[i][j].clear();
            }
        }

        //Reset avg
        avgPHealth = 0;
        avgRHealth = 0;
        avgFHealth = 0;

        avgPAge = 0;
        avgRAge = 0;
        avgFAge = 0;

        //TODO: refactor these into a method or something
        for(int i = Plants.size()-1; i >= 0; i--){
            Plant p = Plants.get(i);
            if(p.dead()) {
                Grass.totalAvgAge = (Grass.totalAmount*Grass.totalAvgAge + p.age())/(Grass.totalAmount+1);
                Plants.remove(i);
            }
            else{
                //add to avg
                avgPHealth += p.getHealth();
                avgPAge += p.age();

                //Define Grid position
                int[] grid = getGrid(p.transform.location);

                //Add to the correct grid
                pGrid[grid[1]][grid[0]].add(p);

                p.paint((Graphics2D) g);
                p.update();
            }
        }
        //calc avg
        avgPAge /= Plants.size();
        avgPHealth /= Plants.size();

        for(int i = Rabbits.size()-1; i >= 0; i--){
            Animal r = Rabbits.get(i);
            //Remove if rabbit is dead
            if(r.dead()) {
                Rabbit.totalAvgAge = (Rabbit.totalAmount*Rabbit.totalAvgAge + r.age())/(Rabbit.totalAmount+1);
                Rabbits.remove(i);
            }
            else{
                //add to avg
                avgRHealth += r.getHealth();
                avgRAge += r.age();

                //Define Grid position
                int[] grid = getGrid(r.transform.location);
                //Add to the correct grid
                rGrid[grid[1]][grid[0]].add(r);

                r.paint((Graphics2D)g);
                r.update();
            }
        }
        //calc avg
        avgRAge /= Rabbits.size();
        avgRHealth /= Rabbits.size();


        for(int i = Foxes.size()-1; i >= 0; i--){
            Animal f = Foxes.get(i);
            //Remove if rabbit is dead
            if(f.dead()) {
                Fox.totalAvgAge = (Fox.totalAmount*Fox.totalAvgAge + f.age())/(Fox.totalAmount+1);
                Foxes.remove(i);
            }
            else{
                //add to avg
                avgFHealth += f.getHealth();
                avgFAge += f.age();

                //Define Grid position
                int[] grid = getGrid(f.transform.location);

                //Add to the correct grid
                fGrid[grid[1]][grid[0]].add(f);

                //Behavior
                f.paint((Graphics2D)g);
                f.update();
            }
        }
        //calc avg
        avgFAge /= Foxes.size();
        avgFHealth /= Foxes.size();

        //Spawning Foxes and Rabbits if less than the MIN are alive
        if(Foxes.size() <= MIN_NUM_FOXES) {
            //improve the base Foxes if all have died to give them a better chance of survival
            //Fox.baseMaxSpeed += .1;
            //Fox.baseMaxForce += .1;
            for(int i = 0; i< NUM_NEW_FOXES; i++) {
                Foxes.add(new Fox());
            }
        }
        if(Rabbits.size() <= MIN_NUM_RABBITS) {
            for(int i = 0; i< NUM_NEW_RABBITS; i++) {
                Rabbits.add(new Rabbit());
            }
        }
        //Spawns new plants if there are less than MAX_NUM_PLANTS
        if(Plants.size()<= MAX_NUM_PLANTS){
            for(int i = 0; i< NUM_NEW_PLANTS; i++) {
                Plants.add(new Grass());
            }
        }

        //Interface
        paintStats(g);

        //NN
        //Generate inputs and targets
        //currentTrackedR.nn.paint((Graphics2D) g,0,400);
        /*
        double[] input = new double[2];
        double[] target = new double[1];
        input[0] = random.nextDouble(1);
        input[1] = random.nextDouble(1);
        target[0] = input[0] + input[1];
        //Train and paint
        nn1.train(input, target);
        nn1.paint((Graphics2D) g,-200,400, input, target);
        nn2.train(input,target);
        nn2.paint((Graphics2D) g,-200,400, input, target);x
         */
    }

    public void paintStats(Graphics g){
        //TODO: make auto-scaling a thing
        //Fox information
        //DNA
        //AVG DNA
        g.setColor(Color.BLACK);
        g.translate(CFrame.WIDTH, 15);
        g.drawString("Avg F:  ", 0,0);
        Fox.sumDNA.paint((Graphics2D) g, 50, 0);

        g.setColor(Color.BLACK);
        g.translate(0,200);
        //Summary of Amount
        g.drawString("Amount of Foxes", 0, 0);          //amount of foxes
        g.drawString(": "+Foxes.size(), 150, 0);
        g.drawString("Total num of Foxes", 0, 15);      //total amount of foxes
        g.drawString(": "+Fox.totalAmount,150,15);
        g.drawString("Average current Age", 0, 30);     //avg current age
        g.drawString(": "+Math.round(avgFAge),150,30);
        g.drawString("Average total Age", 0, 45);       //avg total age
        g.drawString(": "+Math.round(Fox.totalAvgAge),150,45);
        g.drawString("Average Health", 0, 60);          //avg health
        g.drawString(": "+Math.round(avgFHealth),150,60);
        g.drawString(": "+Math.round(avgFHealth/Fox.MAX_HEALTH*100) + "%",150,75);


        //Rabbit information
        //DNA
        //AVG DNA
        g.setColor(Color.BLACK);
        g.translate(200,-200);
        g.drawString("Avg R:  ", 0,0);
        Rabbit.sumDNA.paint((Graphics2D) g, 50, 0);

        g.setColor(Color.BLACK);
        g.translate(0,200);
        //Summary of Amount
        g.drawString("Amount of Rabbits", 0, 0);        //amt of rabbits
        g.drawString(": "+Rabbits.size(), 150, 0);
        g.drawString("Total num of Rabbits", 0, 15);    //tot amt of rabbits
        g.drawString(": "+Rabbit.totalAmount,150,15);
        g.drawString("Average current Age", 0, 30);     //avg current age
        g.drawString(": "+Math.round(avgRAge),150,30);
        g.drawString("Average total Age", 0, 45);       //avg total age
        g.drawString(": "+Math.round(Rabbit.totalAvgAge),150,45);
        g.drawString("Average Health", 0, 60);          //avg health
        g.drawString(": "+Math.round(avgRHealth),150,60);
        g.drawString(": "+Math.round(avgRHealth/Rabbit.MAX_HEALTH*100) + "%",150,75);

        //Plant information
        g.setColor(Color.BLACK);
        g.translate(200,0);
        //Summary of Amount
        g.drawString("Amount of Plants", 0, 0);         //amt of plants
        g.drawString(": "+Plants.size(), 150, 0);
        g.drawString("Total num of Rabbits", 0, 15);    //tot amt of plants
        g.drawString(": "+Grass.totalAmount,150,15);
        g.drawString("Average current Age", 0, 30);     //avg current age
        g.drawString(": "+Math.round(avgPAge),150,30);
        g.drawString("Average total Age", 0, 45);       //avg total age
        g.drawString(": "+Math.round(Grass.totalAvgAge),150,45);
        g.drawString("Average Health", 0, 60);          //avg health
        g.drawString(": "+Math.round(avgPHealth),150,60);
        g.drawString(": "+Math.round(avgPHealth/Grass.MAX_HEALTH*100) + "%",150,75);
    }

    public int[] getGrid(Vector2D loc){
        //Define Grid position

        int column = (int)Vector2D.map(loc.x,0,WIDTH,0,numFieldsX);
        int row = (int)Vector2D.map(loc.y, 0, HEIGHT, 0, numFieldsY);

        //Check for border cases
        if (column < 0) column = 0;
        else if (column >= numFieldsX) column = numFieldsX-1;
        if (row < 0) row = 0;
        else if (row >= numFieldsY) row = numFieldsY-1;
        int[] grid = new int[]{column,row};
        return grid;
    }

    public static ArrayList getGridFields(Vector2D location, ArrayList[][] grid){
        ArrayList list = new ArrayList();

        //int column = (int)(location.x / resolution);
        int column = (int)Vector2D.map(location.x, 0, WIDTH, 0, numFieldsX);
        //int row = (int)(location.y / resolution);
        int row = (int)Vector2D.map(location.y, 0, HEIGHT, 0, numFieldsY);

        //String radius = "";

        for(int x = -1; x <= 1; x++){
            for(int y = -1;y <= 1; y++){
                int newCol = column+x;
                int newRow = row+y;
                //TODO: can be improve to not add duplicates into the grids
                if (((newCol >= 0 && newCol < numFieldsX) &&
                        (newRow >= 0 && newRow < numFieldsY))) list.addAll(grid[newRow][newCol]);
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

