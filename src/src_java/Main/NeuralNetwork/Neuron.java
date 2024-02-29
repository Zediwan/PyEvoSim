package Main.NeuralNetwork;
import Main.Helper.Vector2D;
import java.awt.*;
import java.util.ArrayList;

public class Neuron {
    Vector2D location;
    ArrayList<Connection> connections;
    double sum = 0;
    double bias = 0;
    private static double baseSize = 20;
    private static double biasSizeFactor = 3;

    public Neuron(double x, double y){
        this.location = new Vector2D(x,y);
        connections = new ArrayList();
    }

    public Neuron(double x, double y, double bias){
        this.location = new Vector2D(x,y);
        connections = new ArrayList();
        this.bias = bias;
    }

    public void addConnection(Connection c) {
        connections.add(c);
    }

    public void feedForward(double input) {
        this.sum += input;
        if(this.sum > 1) {
            fire();
            sum = 0;
        }
    }

    private void fire() {
        for(Connection con : connections) con.feedForward(sum);
    }

    public void paint(Graphics2D g) {
        for(Connection con : connections) con.paint(g);
        if(this.bias > 0) g.setColor(Color.GREEN);
        else if(this.bias < 0) g.setColor(Color.RED);
        //else return; // do not paint if bias is zero
        int size = (int)Math.round(baseSize + biasSizeFactor * Math.abs(this.bias));
        g.fillOval((int)Math.round(this.location.getX()-size/2),(int)Math.round(this.location.getY()-size/2),size,size);
    }


    public void update() {
        for(Connection c : connections) c.update();
    }
}
