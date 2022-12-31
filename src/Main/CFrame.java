package Main;
import Main.Helper.Vector2D;
import Main.NeuralNetwork.NeuralNetwork;
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

//TODO: make mating a thing
//TODO: update data output
//TODO: add legend to DNA
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

    private final int STARTING_RABBITS = 1000;
    private final int STARTING_FOXES = 50;
    private final int STARTING_PLANTS = 10000;

    public static int resolution = 10;              //total amount of fields in x and y direction not used right now
    public static int scale = 10;                   //width of a field
    static int numFieldsX = (int)(WIDTH/scale);     //amount of fields in x dir
    static int numFieldsY = (int)(HEIGHT/scale);    //amount of fields in y dir
    //Rabbits
    public static ArrayList<Animal> Rabbits = new ArrayList<>();
    public static ArrayList<Animal>[][] rGrid = new ArrayList[numFieldsY][numFieldsX];
    //Foxes
    public static ArrayList<Animal> Foxes = new ArrayList<>();
    public static ArrayList<Animal>[][] fGrid = new ArrayList[numFieldsY][numFieldsX];
    //Plants
    public static ArrayList<Plant> Plants = new ArrayList<>();
    public static ArrayList<Plant>[][] pGrid = new ArrayList[numFieldsY][numFieldsX];

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

    public void initiate(){
        for(int i=0;i<numFieldsY;i++) {
            for (int i2 = 0; i2 < numFieldsX; i2++) {
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
        for(int i = 0; i < numFieldsY; i++){
            for(int j = 0; j < numFieldsX; j++){
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
                int column = (int) Vector2D.map(p.getLocX(),0, WIDTH,0,numFieldsX);
                //int row = (int)(p.getLocY() / resolution);
                int row = (int)Vector2D.map(p.getLocY(), 0, HEIGHT, 0, numFieldsY);
                //Check for border cases
                if (column < 0) column = 0;
                else if (column >= numFieldsX) column = numFieldsX-1;
                if (row < 0) row = 0;
                else if (row >= numFieldsY) row = numFieldsY-1;
                //Add to the correct grid
                pGrid[row][column].add(p);
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
                int column = (int)Vector2D.map(r.getLocX(),0,WIDTH,0,numFieldsX);
                //int row = (int)(r.getLocY() / resolution);
                int row = (int)Vector2D.map(r.getLocY(), 0, HEIGHT, 0, numFieldsY);
                //Check for border cases
                if (column < 0) column = 0;
                else if (column >= numFieldsX) column = numFieldsX-1;
                if (row < 0) row = 0;
                else if (row >= numFieldsY) row = numFieldsY-1;
                //Add to the correct grid
                rGrid[row][column].add(r);

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
                int column = (int)Vector2D.map(f.getLocX(),0,WIDTH,0,numFieldsX);
                //int row = (int)(f.getLocY() / resolution);
                int row = (int)Vector2D.map(f.getLocY(), 0, HEIGHT, 0, numFieldsY);
                //Check for border cases
                if (column < 0) column = 0;
                else if (column >= numFieldsX) column = numFieldsX-1;
                if (row < 0) row = 0;
                else if (row >= numFieldsY) row = numFieldsY-1;
                //Add to the correct grid
                fGrid[row][column].add(f);

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
            //TODO: make auto-scaling a thing
            //Fox information
            //DNA
            //AVG DNA
            g.setColor(Color.BLACK);
            g.translate(CFrame.WIDTH, 15);
            if(Fox.totalAmountOfFoxes > 0) {
                g.setColor(Color.BLACK);
                g.drawString("Avg F:  ", 0,0);
                Fox.sumDNA.paint((Graphics2D) g, 50, 0);
            }
            g.setColor(Color.BLACK);
            g.translate(0,200);
            //Summary of Amount
            g.drawString("Amount of Foxes", 0, 0);
            g.drawString(": "+Foxes.size(), 150, 0);
            g.drawString("Tot num of born Foxes", 0, 15);
            g.drawString(": "+Fox.totalAmountOfFoxes,150,15);

            //Rabbit information
            //DNA
            //AVG DNA
            g.setColor(Color.BLACK);
            g.translate(250,-200);
            if(Rabbit.totalAmountOfRabbits > 0){
                g.setColor(Color.BLACK);
                g.drawString("Avg R:  ", 0,0);
                Rabbit.sumDNA.paint((Graphics2D) g, 50, 0);
            }
            g.setColor(Color.BLACK);
            g.translate(0,200);
            //Summary of Amount
            g.drawString("Amount of Rabbits", 0, 0);
            g.drawString(": "+Rabbits.size(), 150, 0);
            g.drawString("Tot num of born Rabbits", 0, 15);
            g.drawString(": "+Rabbit.totalAmountOfRabbits,150,15);

            //Plant information
            g.setColor(Color.BLACK);
            g.translate(250,0);
            //Summary of Amount
            g.drawString("Amount of Plants", 0, 0);
            g.drawString(": "+Plants.size(), 150, 0);
        }

        if(Foxes.size() <= 0) for(int i = 0; i< 1; i++) Foxes.add(new Fox());
        if(Rabbits.size() <= 0) for(int i = 0; i< 5; i++) Rabbits.add(new Rabbit());
        if(random.nextInt()<= 1 && Plants.size()<= 10000) for(int i = 0; i< 10; i++) Plants.add(new Grass());

        //NN
        //Generate inputs and targets
        double[] input = new double[2];
        double[] target = new double[1];
        input[0] = random.nextDouble(1);
        input[1] = random.nextDouble(1);
        target[0] = input[0] + input[1];
        //Train and paint
        nn1.train(input, target);
        nn1.paint((Graphics2D) g,1000,500, input, target);
        nn2.train(input,target);
        nn2.paint((Graphics2D) g,0,200, input, target);

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

