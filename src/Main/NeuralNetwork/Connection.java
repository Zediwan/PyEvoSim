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
    private static double baseSize = .5;
    private static double weightSizeFactor = .1;

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
        if(this.weight >= 0) g.setColor(Color.BLACK);
        else g.setColor(Color.RED);
        g.setStroke(new BasicStroke(Math.round(baseSize+Math.abs(this.weight)*weightSizeFactor)));
        g.drawLine((int)Math.round(this.a.location.x),(int)Math.round(this.a.location.y),(int)Math.round(this.b.location.x),(int)Math.round(this.b.location.y));

        /*
        if(this.sending) {
            g.setColor(new Color(0,0,0,100));
            g.fillOval((int)this.sender.x-8,(int)this.sender.y-8,16,16);
        }
         */
    }
}
