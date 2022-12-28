package Main.NeuralNetwork;
import java.awt.*;
import java.util.ArrayList;

public class Network {
    ArrayList<Neuron> neurons;

    public Network(double x, double y){
        this.neurons = new ArrayList();
    }

    public void addNeuron(Neuron neuron){
        neurons.add(neuron);
    }

    public void connect(Neuron a, Neuron b) {
        Connection c = new Connection(a,b,Math.random());
        a.addConnection(c);
    }

    public void connect(Neuron a, Neuron b, double weight) {
        Connection c = new Connection(a,b,weight);
        a.addConnection(c);
    }

    public void feedForward(double input) {
        Neuron start = neurons.get(0);
        start.feedForward(input);
    }

    public void update() {
        for(Neuron n : neurons) n.update();
    }

    public void paint(Graphics2D g, double x, double y) {
        g.translate(x, y);
        for(Neuron n : neurons) n.paint(g);
    }
}
