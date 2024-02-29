package Main.NeuralNetwork;

import Main.Helper.Vector2D;
import java.awt.*;

public class Connection {
    Neuron a;
    Neuron b;
    double weight;
    boolean sending = false;
    Vector2D sender;
    double output;
    Vector2D senderStep;
    private static double baseSize = 1;
    private static double weightSizeFactor = 1;

    public Connection(Neuron from, Neuron to, double weight){
        this.a = from;
        this.b = to;
        this.weight = weight;
    }

    public void feedForward(double value) {
        this.sending = true;
        this.sender = new Vector2D(this.a.location.getX(), this.a.location.getY());
        this.senderStep = Vector2D.sub(this.b.location,this.sender).div(100);
        this.output = value * this.weight;
    }

    public void update(){
        if(this.sending){
            this.sender.add(senderStep);

            double d = Vector2D.dist(this.sender,this.b.location);

            if(d < 8){
                this.b.feedForward(this.output);
                this.sending = false;
            }
        }
    }

    public void paint(Graphics2D g) {
        if(this.weight > 0) g.setColor(Color.GREEN);
        else if(this.weight < 0) g.setColor(Color.RED);
        else return; // do not paint if weight is zero
        g.setStroke(new BasicStroke(Math.round(baseSize+Math.abs(this.weight)*weightSizeFactor)));
        g.drawLine((int)Math.round(this.a.location.getX()),(int)Math.round(this.a.location.getY()),(int)Math.round(this.b.location.getX()),(int)Math.round(this.b.location.getY()));
    }

}
