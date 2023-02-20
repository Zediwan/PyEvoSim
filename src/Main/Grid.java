package Main;

import Main.Organisms.Animals.Animal;
import Main.Organisms.Plants.Plant;
import java.util.ArrayList;

public class Grid {
    private int scale;      //width of a field
    private int numFieldsX; //amount of fields in x dir
    private int numFieldsY; //amount of fields in y dir

    private ArrayList<Animal>[][] rGrid;//Rabbits
    private ArrayList<Animal>[][] fGrid;//Foxes
    private ArrayList<Plant>[][] pGrid; //Plants

}
