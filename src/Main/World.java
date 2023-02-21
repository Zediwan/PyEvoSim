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

    public void updateRabbit(Organism o) {
        this.grid.updateGridR(o);
    }

    public void updateFox(Organism o) {
        this.grid.updateGridF(o);
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
