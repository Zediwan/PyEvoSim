package Main;

import Main.Helper.Vector2D;
import Main.Organisms.Animal;
import Main.Organisms.Organism;
import Main.Organisms.Plant;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;

public class Simulation extends JPanel implements ActionListener {
    //static final int TIME_PERIOD = 24;  //TODO: find out what this is for
    //private int time = 0;

    //TODO: implement a button to toggle this on and off
    private boolean paintNN = true;                 //enables displaying a NN
    private boolean paintAnimalQuadTree = true;
    private boolean paintPlantQuadTree = true;

    //TODO: this should be chosen by clicking an organism and then displaying their stats
    private Animal currentTrackedA;   //the currently tracked Animal

    //Lists containing the organisms
    //TODO: think if there is a better way to handle these organisms
    private ArrayList<Animal> animals = new ArrayList<>();
    private ArrayList<Plant> plants = new ArrayList<>();

    //SIMULATION VARIABLES-------------------------------------------------------
    //amount of stating organisms
    //TODO: make these choose-able in a menu before starting a simulation
    private int startingPlants;
    private int startingAnimals;

    //TODO: implement a slider to control this during the simulation
    private int maxNumPlants;           //The maximum amount of Plants allowed in the simulation at once
    private int minNumPlants;
    private int maxNumAnimals;
    private int minNumAnimals;          //The amount at which the system starts spawning new Animals

    //TODO: implement a slider to control this during the simulation
    private int numNewPlants;          //The amount of new Plants being spawned each tick
    private int numNewAnimals;         //The amount of new animals being spawned each tick

    private static int simNum = 0;
    private int simID;

    private World world;
    public Timer repaintTimer;

    private long lastFrameTime;
    private int fps;

    public long startTime;

    public Simulation(int stP, int stA,
                      int maxP, int minP, int maxA, int minA,
                      int newP, int newA,
                      World w){
        this.startingPlants = stP;
        this.startingAnimals = stA;

        this.maxNumPlants = maxP;
        this.minNumPlants = minP;
        this.maxNumAnimals = maxA;
        this.minNumAnimals = minA;

        this.numNewPlants = newP;
        this.numNewAnimals = newA;

        this.world = w;

        this.simID = simNum;    //set this simulations ID
        simNum++;               //increment simulation counter

        /*
        JFrame frame = new JFrame("Simulation " + this.simID);
        frame.setSize(this.world.getWorldDimension());
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.add(this);
        frame.setVisible(true);
         */

        this.initiatePopulation();
        this.repaintTimer = new Timer(10, this);
        this.lastFrameTime = System.currentTimeMillis();
        this.repaintTimer.start();

        this.startTime = this.lastFrameTime;
    }

    /**
     * Makes the simulation run by updating all the organisms in it
     */
    public void paint(Graphics g){
        super.paintComponent(g);

        this.updatePlants(g);
        this.updateAnimals(g);

        if(this.paintAnimalQuadTree){
            g.setColor(Color.BLACK);
            this.world.getAnimalQuadTree().paint((Graphics2D) g);
        }
        if(this.paintPlantQuadTree){
            g.setColor(Color.BLACK);
            this.world.getPlantQuadTree().paint((Graphics2D) g);
        }

        //this.world.getGrid().clearGrid();
        this.world.clearQuadTrees();

        this.controlPops();
    }

    /**
     * Setup method, initiates the simulation frame
     * @return the simulation frame
     */
    public JPanel setUpVisuals(){
        JPanel simPanel = new JPanel();
        simPanel.setSize(this.world.getWorldDimension());
        simPanel.setVisible(true);
        return simPanel;
    }

    /**
     * Initializes the Population according to the set variables
     */
    public void initiatePopulation(){
        for(int i = 0; i < this.startingPlants; i++){
            Plant p = new Plant();
            p.setLocation(Vector2D.randLimVec(this.world.getWorldDimension().width,this.world.getWorldDimension().height));
            this.plants.add(p);
        }

        for(int i = 0; i < this.startingAnimals; i++){
            Animal a = new Animal();
            a.setLocation(Vector2D.randLimVec(this.world.getWorldDimension().width,this.world.getWorldDimension().height));
            a.setColorRed((int)Math.round(Math.random() * 255));
            a.setColorGreen((int)Math.round(Math.random() * 255));
            a.setColorBlue((int)Math.round(Math.random() * 255));
            a.refreshColor();
            this.animals.add(a);
        }
    }

    //TODO: Test
    /**
     * Checks if the population of each organism is within the given values and adjusts them
     */
    private void controlPops() {
        //control plant pop
        if(this.plants.size() < minNumPlants && this.plants.size() + this.numNewPlants < this.maxNumPlants){
            for(int i = 0; i < numNewPlants; i++){
                Plant p = new Plant();
                p.setLocation(Vector2D.randLimVec(this.world.getWorldDimension().width,this.world.getWorldDimension().height));
                this.plants.add(p);
            }
        }
        //control animal pop
        if(this.animals.size() < minNumAnimals && this.animals.size() + this.numNewAnimals < this.maxNumAnimals){
            for(int i = 0; i < numNewAnimals; i++){
                Animal a = new Animal();
                a.setLocation(Vector2D.randLimVec(this.world.getWorldDimension().width,this.world.getWorldDimension().height));
                a.setColorRed((int)Math.round(Math.random() * 255));
                a.setColorGreen((int)Math.round(Math.random() * 255));
                a.setColorBlue((int)Math.round(Math.random() * 255));
                a.refreshColor();
                this.animals.add(a);
            }
        }
    }

    //TODO: Test

    /**
     * Updates all the plants in the simulation, removing any dead, updating and painting any that are not
     */
    private void updatePlants(Graphics g) {
        for(int i = this.plants.size()-1; i >= 0; i--){
            Plant p = this.plants.get(i);
            if(p.isDead()) {
                this.plants.remove(p);      //if the plant is dead, then remove it
            }
            else{
                this.world.updatePlant(p);
                p.paint((Graphics2D) g);
                p.update(this);
            }
        }
    }

    //TODO: Test
    /**
     * Updates all the Rabbits in the simulation, removing any dead, updating and painting any that are not
     */
    private void updateAnimals(Graphics g) {
        for(int i = this.animals.size()-1; i >= 0; i--){
            Animal a = this.animals.get(i);
            if(a.isDead()) {
                this.animals.remove(a);      //if the plant is dead, then remove it
            }
            else{
                this.world.updateAnimal(a);
                a.paint((Graphics2D) g);
                a.update(this);
                this.borders1(a);
            }
        }
    }

    //Border handling
    public void borders1(Animal a){
        //TODO implement the needed methods in the world and animal classes
        double locX = a.getLocX();
        double locY = a.getLocY();
        double rad = a.getR();
        double worldWidth = this.world.getWorldDimension().width;
        double worldHeight = this.world.getWorldDimension().height;

        if(locX < -rad){
            a.setLocX(Math.round(worldWidth));
        }else if(locX > worldWidth + rad){
            a.setLocX(0);
        }
        if(locY < -rad){
            a.setLocY(Math.round(worldHeight));
        }else if(locY > worldHeight + rad){
            a.setLocY(0);
        }
    }

    /**
     * A method to calculate the current average Age of all Rabbits.
     * Maybe this can be refactored, so it is one method for all organisms and arguments can be given to choose.
     * @return the average age of all living Rabbits.
     */
    public double getAVGAgeAnimals(){
        double count = 0;
        double avg = 0;
        for(Organism o : this.animals){
            count++;
            avg += o.getAge();
        }
        if(count != 0){
            avg /= count;
        }
        return avg;
    }

    public double getAVGAnimalsKilled(){
        double count = 0;
        double avg = 0;
        for(Animal a : this.animals){
            count++;
            avg += a.getAnimalsKilled();
        }
        if(count != 0){
            avg /= count;
        }
        return avg;
    }

    public double getAVGPlantsKilled(){
        double count = 0;
        double avg = 0;
        for(Animal a : this.animals){
            count++;
            avg += a.getPlantsKilled();
        }
        if(count != 0){
            avg /= count;
        }
        return avg;
    }

    public double getAVGOffspringBirthed(){
        double count = 0;
        double avg = 0;
        for(Animal a : this.animals){
            count++;
            avg += a.getOffspringBirthed();
        }
        if(count != 0){
            avg /= count;
        }
        return avg;
    }

    public double getAVGMaxHealthAnimals(){
        double count = 0;
        double avg = 0;
        for(Animal a : this.animals){
            count++;
            avg += a.maxHealth();
        }
        if(count != 0){
            avg /= count;
        }
        return avg;
    }

    /**
     * A method to calculate the current average Health of all Rabbits.
     * Maybe this can be refactored, so it is one method for all organisms and arguments can be given to choose.
     * @return the average health of all living Rabbits.
     */
    public double getAVGHealthAnimals(){
        double count = 0;
        double avg = 0;
        for(Organism o : this.animals){
            count++;
            avg += o.getHealth();
        }
        if(count != 0){
            avg /= count;
        }
        return avg;
    }

    public double getAVGHealthRatioAnimals(){
        double count = 0;
        double avg = 0;
        for(Animal a : this.animals){
            count++;
            avg += a.healthRatio();
        }
        if(count != 0){
            avg /= count;
        }
        return avg;
    }

    public double getAVGMaxEnergyAnimals(){
        double count = 0;
        double avg = 0;
        for(Animal a : this.animals){
            count++;
            avg += a.maxEnergy();
        }
        if(count != 0){
            avg /= count;
        }
        return avg;
    }

    public double getAVGEnergyAnimals(){
        double count = 0;
        double avg = 0;
        for(Animal a : this.animals){
            count++;
            avg += a.getEnergy();
        }
        if(count != 0){
            avg /= count;
        }
        return avg;
    }

    public double getAVGEnergyRatioAnimals(){
        double count = 0;
        double avg = 0;
        for(Animal a : this.animals){
            count++;
            avg += a.getEnergy()/a.maxEnergy();
        }
        if(count != 0){
            avg /= count;
        }
        return avg;
    }

    /**
     * A method to calculate the current average Age of all Plants.
     * Maybe this can be refactored, so it is one method for all organisms and arguments can be given to choose.
     * @return the average age of all living Plants.
     */
    public double getAVGAgePlants(){
        double count = 0;
        double avg = 0;
        for(Organism o : this.plants){
            count++;
            avg += o.getAge();
        }
        if(count != 0){
            avg /= count;
        }
        return avg;
    }

    /**
     * A method to calculate the current average Health of all Plants.
     * Maybe this can be refactored, so it is one method for all organisms and arguments can be given to choose.
     * @return the average health of all living Plants.
     */
    public double getAVGHealthPlants(){
        double count = 0;
        double avg = 0;
        for(Organism o : this.plants){
            count++;
            avg += o.getHealth();
        }
        if(count != 0){
            avg /= count;
        }
        return avg;
    }

    public void actionPerformed(ActionEvent e){
        this.updateFPS();
        this.repaint();
    }

    private void updateFPS() {
        long currentTime = System.currentTimeMillis();
        if(currentTime-this.lastFrameTime > 0){
            this.fps = (int) (1000/(currentTime-this.lastFrameTime));
        }
        this.lastFrameTime = currentTime;
    }

    //Getter and Setter--------------------------------------------------------------------------

    public boolean isPaintNN() {
        return paintNN;
    }

    public void setPaintNN(boolean paintNN) {
        this.paintNN = paintNN;
    }

    public Animal getCurrentTrackedA() {
        return this.currentTrackedA;
    }

    public void setCurrentTrackedA(Animal currentTrackedA) {
        this.currentTrackedA = currentTrackedA;
    }

    public int getStartingPlants() {
        return startingPlants;
    }

    public void setStartingPlants(int startingPlants) {
        this.startingPlants = startingPlants;
    }

    public int getStartingAnimals() {
        return startingAnimals;
    }

    public void setStartingAnimals(int startingAnimals) {
        this.startingAnimals = startingAnimals;
    }

    public int getMaxNumPlants() {
        return maxNumPlants;
    }

    public void setMaxNumPlants(int maxNumPlants) {
        this.maxNumPlants = maxNumPlants;
    }

    public int getMinNumAnimals() {
        return minNumAnimals;
    }

    public void setMinNumAnimals(int minNumAnimals) {
        this.minNumAnimals = minNumAnimals;
    }

    public int getNumNewPlants() {
        return numNewPlants;
    }

    public void setNumNewPlants(int numNewPlants) {
        this.numNewPlants = numNewPlants;
    }

    public int getNumNewAnimals() {
        return numNewAnimals;
    }

    public void setNumNewAnimals(int numNewAnimals) {
        this.numNewAnimals = numNewAnimals;
    }

    public World getWorld() {
        return this.world;
    }

    public void addPlant(Plant p) {
        if(this.plants.size() + 1 >= this.maxNumPlants){
            this.plants.add(p);
        }
    }

    public void addAnimal(Animal child) {
        if(this.animals.size() + 1 >= this.maxNumAnimals){
            this.animals.add(child);
        }
    }

    public void setMaxPlants(int maxPlants) {
        this.maxNumPlants = maxPlants;
    }

    public void setMaxAnimals(int maxAnimals) {
        this.maxNumAnimals = maxAnimals;
    }

    public int getMinNumPlants() {
        return minNumPlants;
    }

    public void setMinNumPlants(int minNumPlants) {
        this.minNumPlants = minNumPlants;
    }

    public int getMaxNumAnimals() {
        return maxNumAnimals;
    }

    public void setTimerDelay(int simulationSpeed) {
        this.repaintTimer.setDelay(simulationSpeed);
    }

    public int getFps() {
        return this.fps;
    }

    public ArrayList getAnimals() {
        return this.animals;
    }
}
