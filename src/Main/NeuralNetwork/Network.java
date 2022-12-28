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

    public void feedForward(double input) {
        Neuron start = neurons.get(0);
        start.feedForward(input);
    }

    public void update() {
        for(Neuron n : neurons) n.update();
    }

    /*
    public static Main.NeuralNetwork.NeuralNetwork.Network transformNN(double x, double y, NeuralNetwork.NeuralNetwork nn, Graphics2D g){
        Main.NeuralNetwork.NeuralNetwork.Network n = new Main.NeuralNetwork.NeuralNetwork.Network(x,y);
        g.translate(x,y);
    }
     */

    public void paint(Graphics2D g, double x, double y) {
        g.translate(x, y);
        for(Neuron n : neurons) n.paint(g);
    }
}
