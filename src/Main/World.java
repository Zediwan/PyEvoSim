package Main;

import Main.Organisms.Organism;

import java.awt.*;

public class World {
    private Dimension worldDimension;     //world size
    private Grid grid;

    public World(int width, int height, int gridFieldWidth, int gridFieldHeight){
        this.worldDimension = new Dimension(width, height);
        this.grid = new Grid(gridFieldWidth, gridFieldHeight, this); //initiate the grid
    }

    public void updatePlant(Organism o) {
        this.grid.updateGridP(o);
    }

    public void updateAnimal(Organism o) {
        this.grid.updateGridA(o);
    }

    public Dimension getWorldDimension() {
        return worldDimension;
    }

    public void setWorldDimension(Dimension worldDimension) {
        this.worldDimension = worldDimension;
    }

    public Grid getGrid() {
        return grid;
    }

    public void setGrid(Grid grid) {
        this.grid = grid;
    }
}
