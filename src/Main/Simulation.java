package Main;

import Main.Organisms.Animals.Animal;
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
        this.updateAnimals(g);
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
        for(int i = 0; i < this.startingAnimals; i++){
            this.animals.add(new Animal());
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
        //control animal pop
        if(this.animals.size() < minNumAnimals){
            for(int i = 0; i < numNewAnimals; i++){
                this.animals.add(new Animal());
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
                p.update();
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
                a.update();
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
}
