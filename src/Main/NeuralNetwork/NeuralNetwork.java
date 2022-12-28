package Main.NeuralNetwork;
import Main.Helper.Matrix;
import java.awt.*;
import java.util.function.Function;

public class NeuralNetwork{
    //TODO: add toString method
    //TODO: add paint visualization

    //Amount of nodes
    public final int output_nodes;
    public final int input_nodes;
    public final int hidden_nodes;
    //Weights
    public Matrix weights_ih;
    public Matrix weights_ho;
    //Biases
    public Matrix bias_h;
    public Matrix bias_o;

    public double learning_rate;
    public ActivationFunction activation_function;
    private Matrix output_errors;

    //Painting
    Network n;

    public NeuralNetwork(int input_nodes, int hidden_nodes, int output_nodes){
        //Amount of notes in each part
        this.input_nodes = input_nodes;
        this.hidden_nodes = hidden_nodes;
        this.output_nodes = output_nodes;

        //Weights
        this.weights_ih = new Matrix(this.hidden_nodes, this.input_nodes);
        this.weights_ho = new Matrix(this.output_nodes, this.hidden_nodes);
        //Use random weights at the start
        this.weights_ih.randomize();
        this.weights_ho.randomize();

        //Biases
        this.bias_h = new Matrix(this.hidden_nodes, 1);
        this.bias_o = new Matrix(this.output_nodes,1);
        //Use random biases at the start
        this.bias_h.randomize();
        this.bias_o.randomize();

        this.setLearning_rate(.1);
        this.setActivation_function(new ActivationFunction(ActivationFunction.sigmoid, ActivationFunction.dSigmoid));
    }

    public NeuralNetwork(NeuralNetwork nn) {
        this.input_nodes = nn.input_nodes;
        this.hidden_nodes = nn.hidden_nodes;
        this.output_nodes = nn.output_nodes;

        this.weights_ih = nn.weights_ih.copy();
        this.weights_ho = nn.weights_ho.copy();

        this.bias_h = nn.bias_h.copy();
        this.bias_o = nn.bias_o.copy();
    }

    private void setActivation_function(ActivationFunction af) {
        this.activation_function = af;
    }
    private void setLearning_rate(double lr) {
        this.learning_rate = lr;
    }

    public double[] predict(double[] input_array) {
        // Generating the Hidden Outputs
        Matrix inputs = Matrix.fromArray(input_array);
        Matrix hidden = Matrix.mult(this.weights_ih, inputs);
        hidden.add(this.bias_h);
        // activation function!
        hidden.map(this.activation_function.func);

        // Generating the output's output!
        Matrix output = Matrix.mult(this.weights_ho, hidden);
        output.add(this.bias_o);
        output.map(this.activation_function.func);

        // Sending back to the caller!
        return output.toArray();
    }

    public void train(double[] input_array, double[] target_array) {
        // Generating the Hidden Outputs
        Matrix inputs = Matrix.fromArray(input_array);
        Matrix hidden = Matrix.mult(this.weights_ih, inputs);
        hidden.add(this.bias_h);
        // activation function!
        hidden.map(this.activation_function.func);

        // Generating the output's output!
        Matrix outputs = Matrix.mult(this.weights_ho, hidden);
        outputs.add(this.bias_o);
        outputs.map(this.activation_function.func);

        // Convert array to matrix object
        Matrix targets = Matrix.fromArray(target_array);

        // Calculate the error
        // ERROR = TARGETS - OUTPUTS
        this.output_errors = Matrix.sub(targets, outputs);

        // let gradient = outputs * (1 - outputs);
        // Calculate gradient
        Matrix gradients = Matrix.map(outputs, this.activation_function.dfunc);
        gradients.mult(output_errors);
        gradients.mult(this.learning_rate);

        // Calculate deltas
        Matrix weight_ho_deltas = Matrix.mult(gradients, Matrix.transpose(hidden));

        // Adjust the weights by deltas
        this.weights_ho.add(weight_ho_deltas);
        // Adjust the bias by its deltas (which is just the gradients)
        this.bias_o.add(gradients);

        // Calculate the hidden layer errors
        Matrix hidden_errors = Matrix.mult(Matrix.transpose(this.weights_ho), output_errors);

        // Calculate hidden gradient
        Matrix hidden_gradient = Matrix.map(hidden, this.activation_function.dfunc);
        hidden_gradient.mult(hidden_errors);
        hidden_gradient.mult(this.learning_rate);

        // Calculate input->hidden deltas
        Matrix weight_ih_deltas = Matrix.mult(hidden_gradient, Matrix.transpose(inputs));

        this.weights_ih.add(weight_ih_deltas);
        // Adjust the bias by its deltas (which is just the gradients)
        this.bias_h.add(hidden_gradient);

        //System.out.print("Input: \n" + inputs);
        //System.out.print("Output: " + outputs);
        //System.out.print("Target: " + targets);
        System.out.println("Error: \n" + output_errors);
    }

    // Adding function for neuro-evolution
    public NeuralNetwork copy() {
        return new NeuralNetwork(this);
    }

    // Accept an arbitrary function for mutation
    public void mutate(Function<Double, Double> func) {
        this.weights_ih.map(func);
        this.weights_ho.map(func);
        this.bias_h.map(func);
        this.bias_o.map(func);
    }

    public void initializeVisualNetwork(double x, double y) {
        n = new Network(x,y);
        //add input Neurons
        for(int i = 0; i < this.input_nodes; i++){
            n.addNeuron(new Neuron(x,y + i * 50));
        }
        //add hidden Neurons
        for(int i = 0; i < this.hidden_nodes; i++){
            n.addNeuron(new Neuron(x + 100,y + i * 50, this.bias_h.data[i][0]));
        }
        //add output Neurons
        for(int i = 0; i < this.output_nodes; i++){
            n.addNeuron(new Neuron(x + 100 * 2,y + i * 50, this.bias_o.data[i][0]));
        }
        //connect input to hidden Neurons
        for(int i = 0; i < this.input_nodes; i++){
            for(int j = 0; j < this.hidden_nodes; j++){
                n.connect(n.neurons.get(i), n.neurons.get(j+this.input_nodes), weights_ih.data[j][i]);
            }
        }
        //connect hidden to output Neurons
        for(int i = 0; i < this.hidden_nodes; i++) {
            for (int j = 0; j < this.output_nodes; j++) {
                n.connect(n.neurons.get(i+this.input_nodes), n.neurons.get(j+this.hidden_nodes+this.input_nodes), weights_ho.data[j][i]);
            }
        }
    }

    public void update() {
        for(Neuron n : n.neurons) n.update();
    }

    public void paint(Graphics2D g, double x, double y) {
        //g.translate(x, y);
        this.initializeVisualNetwork(x,y);
        for(Neuron n : n.neurons) n.paint(g);
    }

    public void paint(Graphics2D g, double x, double y, double[] input_array, double[] target_array) {
        //g.translate(x, y);
        this.initializeVisualNetwork(x,y);
        g.setColor(Color.BLACK);
        //Draw Input
        for(int i = 0; i<input_array.length; i++)g.drawString(String.format("%.2f",input_array[i]) + "-->",(int)x-50,(int)y + i * 50);
        //Draw output
        for(int i = 0; i<target_array.length; i++){
            g.drawString("-->"+String.format("%.2f",this.predict(input_array)[i]),(int)x+200,(int)y + i * 50);
            if(this.output_errors.data[0][i] >= 0) g.setColor(Color.BLACK);
            else g.setColor(Color.RED);
            g.drawString("      " + String.format("%.2f",Math.abs(this.output_errors.data[0][i])), (int)x+200,(int)y + i * 50 + 15);
        }
        //Paint the graph
        for(Neuron n : n.neurons) n.paint(g);
    }
}
