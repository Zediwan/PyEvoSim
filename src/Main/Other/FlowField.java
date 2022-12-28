/*
import java.awt.*;
import java.util.Random;

public class FlowField {
    Main.Main.NeuralNetwork.NeuralNetwork.Vector2D[][] field;
    int rows, cols; //Columns and Rows
    int resolution; //How large is each cell in the flow field

    public FlowField(int resolution, Main.Main.NeuralNetwork.NeuralNetwork.CFrame frame){
        this.resolution = resolution;
        //Determine the number of columns and rows
        this.cols = frame.WIDTH/this.resolution;
        this.rows = frame.HEIGHT/this.resolution;

        field = new Main.Main.NeuralNetwork.NeuralNetwork.Vector2D[cols][rows];
        this.init(frame);
    }

    private void init(Main.Main.NeuralNetwork.NeuralNetwork.CFrame frame) {
        //Reseed noise so we can get a new flow field every time
        float xoff = 0;
        for(int i = 0; i < this.cols; i++){
            float yoff = 0;
            for(int j = 0; j < this.rows; j++){
                //System.out.println(new PerlinNoise(10).noise(xoff,yoff));
                //float theta = Main.Main.NeuralNetwork.NeuralNetwork.Vector2D.map(Math.round(frame.pNoise.noise2(xoff,yoff)*100),0,1,0,Math.round(2*Math.PI));
                float theta = 90;
                theta += frame.random.nextFloat(4)-2;
                field[i][j] = Main.Main.NeuralNetwork.NeuralNetwork.Vector2D.fromAngle(theta);
                yoff += .1;
            }
            xoff += .1;
        }
    }

    public Main.Main.NeuralNetwork.NeuralNetwork.Vector2D lookup(Main.Main.NeuralNetwork.NeuralNetwork.Vector2D lookup) {
        int col = (int)(this.constrain(lookup.x / this.resolution,0,cols-1));
        int row = (int)(this.constrain(lookup.y / this.resolution, 0 ,rows-1));
        return field[col][row];
    }

    private double constrain(float value, int lowerBound, int upperBound) {
        double newValue = value;
        if(newValue > upperBound) newValue = upperBound;
        else if(newValue < lowerBound) newValue = lowerBound;
        return newValue;
    }

    public void paint(Graphics g){
        for(int i = 0; i < this.cols; i++){
            for(int j = 0; j < this.rows; j++){
                g.setColor(Color.GRAY);
                int startX = i*this.resolution;
                int startY = j*this.resolution;
                int endX = (int)(startX + (this.field[i][j].x * this.resolution));
                int endY = (int)(startY + (this.field[i][j].y * this.resolution));
                g.drawLine(startX,startY,endX, endY);
            }
        }
    }

    public String toString(){
        String s = "";
        for(int i = 0; i < this.cols; i++){
            for(int j = 0; j < this.rows; j++){
                s += field[i][j] + " | ";
            }
            s += "\n";
        }
        return s;
    }
}

 */