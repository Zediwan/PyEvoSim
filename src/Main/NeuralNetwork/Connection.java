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

    public Connection(Neuron from, Neuron to, double weight){
        this.a = from;
        this.b = to;
        this.weight = weight;
    }

    public void feedForward(double value) {
        this.sending = true;
        this.sender = new Vector2D(this.a.location.x, this.a.location.y);
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
        Color c = new Color(0,0,0);
        g.setColor(c);
        g.setStroke(new BasicStroke(Math.round(1+4*this.weight)));
        g.drawLine((int)Math.round(this.a.location.x),(int)Math.round(this.a.location.y),(int)Math.round(this.b.location.x),(int)Math.round(this.b.location.y));

        if(this.sending) {
            g.setColor(new Color(0,0,0,100));
            g.fillOval((int)this.sender.x-8,(int)this.sender.y-8,16,16);
        }
    }
}
