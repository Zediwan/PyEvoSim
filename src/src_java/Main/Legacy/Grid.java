package Main.Legacy;

import Main.Helper.Vector2D;
import Main.Organisms.Animal;
import Main.Organisms.Organism;
import Main.World.World;

import java.util.ArrayList;

public class Grid {
    //TODO: implement gridCell types
    private int gridCellWidth;          //height of a grid cell
    private int gridCellHeight;         //width of a grid cell
    private int numCellsX;              //amount of cells in x dir
    private int numCellsY;              //amount of cells in y dir

    private World world;

    private ArrayList<Organism>[][] pGrid; //Plants
    private ArrayList<Organism>[][] aGrid;  //Animals

    public Grid(int gridCellWidth, int gridCellHeight, World w){
        this.world = w;
        //calculate the amount of grid cells
        this.gridCellWidth = gridCellWidth;
        this.gridCellHeight = gridCellHeight;
        this.numCellsX = this.world.getWorldDimension().width / this.gridCellWidth;
        this.numCellsY = this.world.getWorldDimension().height / this.gridCellHeight;

        //initiate the grids
        this.pGrid = new ArrayList[numCellsY][numCellsX];
        this.aGrid = new ArrayList[numCellsY][numCellsX];

        for(int i1=0;i1<numCellsY;i1++) {
            for (int i2 = 0; i2 < numCellsX; i2++) {
                this.aGrid[i1][i2] = new ArrayList<>();
                this.pGrid[i1][i2] = new ArrayList<>();
            }
        }
    }

    //TODO: Test
    public void clearGrid(){
        for(int i = 0; i < numCellsY; i++){
            for(int j = 0; j < numCellsX; j++){
                pGrid[i][j].clear();
                aGrid[i][j].clear();
            }
        }
    }

    //TODO: Test
    public void updateGridP(Organism o){
        //assert o.getClass().equals(Plant.class);

        int[] gridCell = this.getGrid(o.getLocation());
        this.pGrid[gridCell[1]][gridCell[0]].add(o);
    }

    //TODO: Test
    public void updateGridA(Organism o){
        assert o.getClass().equals(Animal.class);

        int[] gridCell = this.getGrid(o.getLocation());
        this.aGrid[gridCell[1]][gridCell[0]].add(o);
    }

    //TODO: Test
    public int[] getGrid(Vector2D loc){
        int width = this.world.getWorldDimension().width;
        int height = this.world.getWorldDimension().height;

        //Define Grid position
        int column = (int)Math.round(Vector2D.map(loc.getX(),0, width,0, this.numCellsX));
        int row = (int)Math.round(Vector2D.map(loc.getY(), 0, height, 0, this.numCellsY));

        //Check for border cases
        if (column < 0) column = 0;
        else if (column >= this.numCellsX) column = this.numCellsX-1;
        if (row < 0) row = 0;
        else if (row >= this.numCellsY) row = this.numCellsY-1;

        //TODO: refactor so this is a class
        int[] grid = new int[]{column,row};     //grid position
        return grid;
    }

    //TODO: Test
    public ArrayList getGridFieldsP(Vector2D location, double range){
        if(range <= 0) return new ArrayList();  //if the range is <= 0 then return an empty list
        ArrayList list = new ArrayList();       //the list containing the plants in range

        //int[] gridPosition = this.getGrid(location);
        //int column = gridPosition[0];
        //int row =  gridPosition[1];

        for(double x = location.getX() - range; x <= location.getX() +range; x += this.gridCellWidth){
            for(double y = location.getY() - range; y <= location.getY() + range; y += this.gridCellHeight){
                int[] gridCell = this.getGrid(new Vector2D(x,y));
                //TODO: check if the values are the right way around
                list.addAll(this.pGrid[gridCell[1]][gridCell[0]]);
            }
        }
        return list;
    }

    //TODO: Test
    public ArrayList getGridFieldsA(Vector2D location, double range){
        if(range <= 0) return new ArrayList();  //if the range is <= 0 then return an empty list
        ArrayList list = new ArrayList();       //the list containing the plants in range

        //int[] gridPosition = this.getGrid(location);
        //int column = gridPosition[0];
        //int row =  gridPosition[1];

        for(double x = location.getX() - range; x <= location.getX() +range; x += this.gridCellWidth){
            for(double y = location.getY() - range; y <= location.getY() + range; y += this.gridCellHeight){
                int[] gridCell = this.getGrid(new Vector2D(x,y));
                //TODO: check if the values are the right way around
                list.addAll(this.aGrid[gridCell[1]][gridCell[0]]);
            }
        }
        return list;
    }
}
