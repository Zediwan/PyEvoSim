package Main.NeuralNetwork;

import Main.Helper.Vector2D;

import java.awt.*;
import java.util.ArrayList;

public class Neuron {
    Vector2D location;
    ArrayList<Connection> connections;
    double sum = 0;

    public Neuron(double x, double y){
        this.location = new Vector2D(x,y);
        connections = new ArrayList();
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
        Color c = new Color(0,0,0);
        g.setColor(c);
        g.fillOval((int)Math.round(this.location.x-8),(int)Math.round(this.location.y-8),16,16);
        for(Connection con : connections) con.paint(g);
    }

    public void update() {
        for(Connection c : connections) c.update();
    }
}
