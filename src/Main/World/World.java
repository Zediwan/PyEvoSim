package Main.World;

import Main.Organisms.Animal;
import Main.Organisms.Plant;

import java.awt.*;
import java.awt.geom.Rectangle2D;

public class World {
    private Dimension worldDimension;     //world size
    //private Grid grid;
    private QuadTree.Animals animalQuadTree;
    private QuadTree.Plants plantQuadTree;

    public World(int width, int height, int capacityA, int capacityB){
        this.worldDimension = new Dimension(width, height);
        Rectangle2D.Double worldRect = new Rectangle2D.Double(0,0, width, height);

        this.worldDimension = new Dimension(width, height);
        this.animalQuadTree = new QuadTree.Animals(worldRect, capacityA, this);
        this.plantQuadTree = new QuadTree.Plants(worldRect, capacityB, this);
        //this.grid = new Grid(gridFieldWidth, gridFieldHeight, this); //initiate the grid
    }

    public void clearQuadTrees(){
        this.plantQuadTree.clear();
        this.animalQuadTree.clear();
    }

    public void updatePlant(Plant p) {
        //this.grid.updateGridP(o);
        this.plantQuadTree.insert(p);
    }

    public void updateAnimal(Animal a) {
        //this.grid.updateGridA(o);
        this.animalQuadTree.insert(a);
    }

    public Dimension getWorldDimension() {
        return worldDimension;
    }

    public void setWorldDimension(Dimension worldDimension) {
        this.worldDimension = worldDimension;
    }

    public QuadTree.Animals getAnimalQuadTree() {
        return animalQuadTree;
    }

    public void setAnimalQuadTree(QuadTree.Animals animalQuadTree) {
        this.animalQuadTree = animalQuadTree;
    }

    public QuadTree.Plants getPlantQuadTree() {
        return plantQuadTree;
    }

    public void setPlantQuadTree(QuadTree.Plants plantQuadTree) {
        this.plantQuadTree = plantQuadTree;
    }

    /*
    public Grid getGrid() {
        return grid;
    }

    public void setGrid(Grid grid) {
        this.grid = grid;
    }
     */
}
