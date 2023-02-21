package Main;

import Main.Organisms.Animals.Animal;
import Main.Organisms.Animals.Fox;
import Main.Organisms.Animals.Rabbit;
import Main.Organisms.Organism;
import Main.Organisms.Plants.Grass;
import Main.Organisms.Plants.Plant;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.util.ArrayList;

public class Simulation extends JPanel {
    //static final int TIME_PERIOD = 24;  //TODO: find out what this is for
    //private int time = 0;

    //TODO: implement a button to toggle this on and off
    private boolean paintNN = true;                 //enables displaying a NN

    //TODO: this should be chosen by clicking an organism and then displaying their stats
    private Animal currentTrackedR;   //the currently tracked Rabbit
    private Animal currentTrackedF;   //the currently tracked Fox

    //Lists containing the organisms
    //TODO: think if there is a better way to handle these organisms
    private ArrayList<Rabbit> rabbits = new ArrayList<>();
    private ArrayList<Fox> foxes = new ArrayList<>();
    private ArrayList<Plant> plants = new ArrayList<>();

    //SIMULATION VARIABLES-------------------------------------------------------
    //amount of stating organisms
    //TODO: make these choose-able in a menu before starting a simulation
    private int startingPlants;
    private int startingRabbits;
    private int startingFoxes;

    //TODO: implement a slider to control this during the simulation
    private int maxNumPlants;           //The maximum amount of Plants allowed in the simulation at once
    private int minNumRabbits;          //The amount at which the system starts spawning new Rabbits
    private int minNumFoxes;            //The amount at which the system starts spawning new Foxes

    //TODO: implement a slider to control this during the simulation
    private int numNewPlants;          //The amount of new Plants being spawned each tick
    private int numNewRabbits;         //The amount of new Rabbits being spawned each tick
    private int numNewFoxes;           //The amount of new Foxes being spawned each tick

    private World world;
    private static int simNum = 0;
    private int simID;

    public Simulation(int stP, int stR, int stF,
                      int maxP, int minR, int minF,
                      int newP, int newR, int newF,
                      World w){
        this.startingPlants = stP;
        this.startingRabbits = stR;
        this.startingFoxes = stF;

        this.maxNumPlants = maxP;
        this.minNumRabbits = minR;
        this.minNumFoxes = minF;

        this.numNewPlants = newP;
        this.numNewRabbits = newR;
        this.numNewFoxes = newF;

        this.world = w;

        this.simID = simNum;    //set this simulations ID
        simNum++;               //increment simulation counter

        JFrame simFrame = new JFrame("Simulation " + this.simID);
        simFrame.setSize(this.world.getWorldDimension());
        simFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        simFrame.add(this);
        simFrame.setVisible(true);
    }

    /**
     * Makes the simulation run by updating all the organisms in it
     */
    public void paint(Graphics g){
        super.paintComponent(g);

        this.updatePlants(g);
        this.updateRabbits(g);
        this.updateFoxes(g);
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
            this.plants.add(new Grass());
        }
        for(int i = 0; i < this.startingRabbits; i++){
            this.rabbits.add(new Rabbit());
        }
        for(int i = 0; i < this.startingFoxes; i++){
            this.foxes.add(new Fox());
        }
    }

    //TODO: Test
    /**
     * Checks if the population of each organism is within the given values and adjusts them
     */
    private void controlPops() {
        //control plant pop
        if(this.plants.size() < maxNumPlants){
            for(int i = 0; i < numNewPlants; i++){
                this.plants.add(new Grass());
            }
        }
        //control rabbit pop
        if(this.rabbits.size() < minNumRabbits){
            for(int i = 0; i < numNewRabbits; i++){
                this.rabbits.add(new Rabbit());
            }
        }
        //control fox pop
        if(this.foxes.size() < minNumFoxes){
            for(int i = 0; i < numNewFoxes; i++){
                this.foxes.add(new Fox());
            }
        }
    }

    //TODO: Test

    /**
     * Updates all the plants in the simulation, removing any dead, updating and painting any that are not
     */
    private void updatePlants(Graphics g) {
        for(int i = this.plants.size()-1; i >= 0; i--){
            Organism o = this.plants.get(i);
            if(o.dead()) {
                this.plants.remove(o);      //if the plant is dead, then remove it
            }
            else{
                this.world.updatePlant(o);
                o.paint((Graphics2D) g);
                o.update();
            }
        }
    }

    //TODO: Test
    /**
     * Updates all the Rabbits in the simulation, removing any dead, updating and painting any that are not
     */
    private void updateRabbits(Graphics g) {
        for(int i = this.rabbits.size()-1; i >= 0; i--){
            Organism o = this.rabbits.get(i);
            if(o.dead()) {
                this.rabbits.remove(o);      //if the plant is dead, then remove it
            }
            else{
                this.world.updateRabbit(o);
                o.paint((Graphics2D) g);
                o.update();
            }
        }
    }

    //TODO: Test
    /**
     * Updates all the Foxes in the simulation, removing any dead, updating and painting any that are not
     */
    private void updateFoxes(Graphics g) {
        for(int i = this.foxes.size()-1; i >= 0; i--){
            Organism o = this.foxes.get(i);
            if(o.dead()) {
                this.foxes.remove(o);      //if the plant is dead, then remove it
            }
            else{
                this.world.updateFox(o);
                o.paint((Graphics2D) g);
                o.update();
            }
        }
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

    /**
     * A method to calculate the current average Health of all Rabbits.
     * Maybe this can be refactored, so it is one method for all organisms and arguments can be given to choose.
     * @return the average health of all living Rabbits.
     */
    public double getAVGHealthRabbits(){
        double count = 0;
        double avg = 0;
        for(Organism o : this.rabbits){
            count++;
            avg += o.getHealth();
        }
        if(count != 0){
            avg /= count;
        }
        return avg;
    }

    /**
     * A method to calculate the current average Health of all Foxes.
     * Maybe this can be refactored, so it is one method for all organisms and arguments can be given to choose.
     * @return the average health of all living Foxes.
     */
    public double getAVGHealthFoxes(){
        double count = 0;
        double avg = 0;
        for(Organism o : this.foxes){
            count++;
            avg += o.getHealth();
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
     * A method to calculate the current average Age of all Rabbits.
     * Maybe this can be refactored, so it is one method for all organisms and arguments can be given to choose.
     * @return the average age of all living Rabbits.
     */
    public double getAVGAgeRabbits(){
        double count = 0;
        double avg = 0;
        for(Organism o : this.rabbits){
            count++;
            avg += o.getAge();
        }
        if(count != 0){
            avg /= count;
        }
        return avg;
    }

    /**
     * A method to calculate the current average Age of all Foxes.
     * Maybe this can be refactored, so it is one method for all organisms and arguments can be given to choose.
     * @return the average age of all living Foxes.
     */
    public double getAVGAgeFoxes(){
        double count = 0;
        double avg = 0;
        for(Organism o : this.foxes){
            count++;
            avg += o.getAge();
        }
        if(count != 0){
            avg /= count;
        }
        return avg;
    }

    /**
     * don't really know what this does
     * @param e
     */
    public void actionPerformed(ActionEvent e){
        repaint();
    }

    //Getter and Setter--------------------------------------------------------------------------

    public boolean isPaintNN() {
        return paintNN;
    }

    public void setPaintNN(boolean paintNN) {
        this.paintNN = paintNN;
    }

    public Animal getCurrentTrackedR() {
        return this.currentTrackedR;
    }

    public void setCurrentTrackedR(Animal currentTrackedR) {
        this.currentTrackedR = currentTrackedR;
    }

    public Animal getCurrentTrackedF() {
        return this.currentTrackedF;
    }

    public void setCurrentTrackedF(Animal currentTrackedF) {
        this.currentTrackedF = currentTrackedF;
    }

    public int getStartingPlants() {
        return startingPlants;
    }

    public void setStartingPlants(int startingPlants) {
        this.startingPlants = startingPlants;
    }

    public int getStartingRabbits() {
        return startingRabbits;
    }

    public void setStartingRabbits(int startingRabbits) {
        this.startingRabbits = startingRabbits;
    }

    public int getStartingFoxes() {
        return startingFoxes;
    }

    public void setStartingFoxes(int startingFoxes) {
        this.startingFoxes = startingFoxes;
    }

    public int getMaxNumPlants() {
        return maxNumPlants;
    }

    public void setMaxNumPlants(int maxNumPlants) {
        this.maxNumPlants = maxNumPlants;
    }

    public int getMinNumRabbits() {
        return minNumRabbits;
    }

    public void setMinNumRabbits(int minNumRabbits) {
        this.minNumRabbits = minNumRabbits;
    }

    public int getMinNumFoxes() {
        return minNumFoxes;
    }

    public void setMinNumFoxes(int minNumFoxes) {
        this.minNumFoxes = minNumFoxes;
    }

    public int getNumNewPlants() {
        return numNewPlants;
    }

    public void setNumNewPlants(int numNewPlants) {
        this.numNewPlants = numNewPlants;
    }

    public int getNumNewRabbits() {
        return numNewRabbits;
    }

    public void setNumNewRabbits(int numNewRabbits) {
        this.numNewRabbits = numNewRabbits;
    }

    public int getNumNewFoxes() {
        return numNewFoxes;
    }

    public void setNumNewFoxes(int numNewFoxes) {
        this.numNewFoxes = numNewFoxes;
    }
}
