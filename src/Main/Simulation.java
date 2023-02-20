package Main;

import Main.Organisms.Animals.Animal;
import Main.Organisms.Animals.Rabbit;
import Main.Organisms.Organism;
import Main.Organisms.Plants.Plant;

import java.util.ArrayList;

public class Simulation {
    boolean paintNN = true;

    public static Animal currentTrackedR;
    public static Animal currentTrackedF;

    public double avgPHealth = 0;
    public double avgRHealth = 0;
    public double avgFHealth = 0;

    public double avgPAge;
    public double avgRAge = 0;
    public double avgFAge = 0;

    public static ArrayList<Animal> Rabbits = new ArrayList<>();
    public static ArrayList<Animal> Foxes = new ArrayList<>();
    public static ArrayList<Plant> Plants = new ArrayList<>();

    //SIMULATION VARIABLES
    //AMOUNT OF STARTING ENTITIES
    private int STARTING_RABBITS;
    private int STARTING_FOXES;
    private int STARTING_PLANTS;

    private int minNumRabbits;         //The amount at which the system starts spawning new Rabbits
    private int minNumFoxes;            //The amount at which the system starts spawning new Foxes
    private int maxNumPlants;//The maximum amount of Plants allowed in the simulation at once

    private int numNewPlants;          //The amount of new Plants being spawned each tick
    private int numNewRabbits;          //The amount of new Rabbits being spawned each tick
    private int numNewFoxes;            //The amount of new Foxes being spawned each tick

    public Simulation(){

    }

    /**
     * A method to calculate the current average Health of all Plants.
     * Maybe this can be refactored, so it is one method for all organisms and arguments can be given to choose.
     * @return the average health of all living Plants.
     */
    public double getAVGHealthPlants(){
        double count = 0;
        double avg = 0;
        for(Organism o : this.Plants){
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
        for(Organism o : this.Rabbits){
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
        for(Organism o : this.Foxes){
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
        for(Organism o : this.Plants){
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
        for(Organism o : this.Rabbits){
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
        for(Organism o : this.Foxes){
            count++;
            avg += o.getAge();
        }
        if(count != 0){
            avg /= count;
        }
        return avg;
    }
}
