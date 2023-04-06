package Main.NeuralNetwork;

import Main.Helper.Matrix;
import Main.Helper.mutable;

import java.awt.*;
import java.util.function.Function;

/**
 * <a href = https://youtube.com/playlist?list=PLRqwX-V7Uu6aCibgK1PTWWu9by6XFdCfh>Youtube Series for understanding</a>
 */
public class NeuralNetwork implements mutable {
    //TODO: add toString method
    //TODO: add paint visualization
    //TODO: remove the activation function (as it should not be needed for this?)


    private final int OUTPUT_NODES;
    private final int INPUT_NODES;
    private final int HIDDEN_NODES;

    private Matrix weights_ih;
    private Matrix weights_ho;

    private Matrix bias_h;
    private Matrix bias_o;

    private double learning_rate;
    private ActivationFunction activation_function;
    private Matrix output_errors;
    private static double visualLayerOffset = 200;


    Network n;

    /**
     * Constructs a new neural network with the given number of input, hidden, and output nodes.
     * Initializes the weights and biases randomly.
     *
     * @param input_nodes   the number of input nodes
     * @param hidden_nodes  the number of hidden nodes
     * @param output_nodes  the number of output nodes
     */
    public NeuralNetwork(int input_nodes, int hidden_nodes, int output_nodes){
        //Amount of notes in each part
        this.INPUT_NODES = input_nodes;
        this.HIDDEN_NODES = hidden_nodes;
        this.OUTPUT_NODES = output_nodes;

        //Weights
        this.weights_ih = new Matrix(this.HIDDEN_NODES, this.INPUT_NODES);
        this.weights_ho = new Matrix(this.OUTPUT_NODES, this.HIDDEN_NODES);

        //Use random weights at the start
        this.weights_ih.randomize();
        this.weights_ho.randomize();

        //Biases
        this.bias_h = new Matrix(this.HIDDEN_NODES, 1);
        this.bias_o = new Matrix(this.OUTPUT_NODES,1);

        //Use random biases at the start
        this.bias_h.randomize();
        this.bias_o.randomize();

        this.setLearning_rate(.1);
        this.setActivation_function(new ActivationFunction(ActivationFunction.sigmoid, ActivationFunction.dSigmoid));
    }

    /**
     * @param wih The weights for the input layer to hidden layer.
     * @param who The weights for the hidden layer to output layer.
     * @param bh The biases for the hidden layer.
     * @param bo The biases for the output layer.
     * @throws AssertionError if the sizes of weights and biases don't match.
     */
    public NeuralNetwork(Matrix wih, Matrix who, Matrix bh, Matrix bo){
        assert bh.getROWS() == wih.getROWS() : "Sizes of hidden layer don't match (bias and weights)";
        assert bo.getROWS() == who.getROWS() : "Sizes of output layer don't match (bias and weights)";
        assert wih.getROWS() == who.getCOLS() : "Sizes of hidden layer don't match (weights)";

        //Amount of notes in each part
        this.INPUT_NODES = wih.getCOLS();
        this.HIDDEN_NODES = wih.getROWS();
        this.OUTPUT_NODES = who.getROWS();

        //Weights
        this.weights_ih = wih;
        this.weights_ho = who;

        //Biases
        this.bias_h = bh;
        this.bias_o = bo;

        this.setLearning_rate(.1);
        this.setActivation_function(new ActivationFunction(ActivationFunction.sigmoid, ActivationFunction.dSigmoid));
    }

    /**
     * Creates a new NeuralNetwork object that is a copy of an existing NeuralNetwork object.
     *
     * @param nn the NeuralNetwork object to copy
     */
    public NeuralNetwork(NeuralNetwork nn) {
        this.INPUT_NODES = nn.INPUT_NODES;
        this.HIDDEN_NODES = nn.HIDDEN_NODES;
        this.OUTPUT_NODES = nn.OUTPUT_NODES;

        this.weights_ih = nn.weights_ih.copy();
        this.weights_ho = nn.weights_ho.copy();

        this.bias_h = nn.bias_h.copy();
        this.bias_o = nn.bias_o.copy();

        this.setLearning_rate(nn.learning_rate);
        this.setActivation_function(nn.activation_function);
    }

    /**
     * Predicts the output values for the given input values.
     * @param input_array an array of input values to the neural network
     * @return an array of output values predicted by the neural network
     */

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

    /**
     * Trains the neural network with a given input and target array.
     *
     * @param input_array an array of doubles representing the input values for the network
     * @param target_array an array of doubles representing the desired output values for the network
     */
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
        //System.out.println("Error: \n" + output_errors);
    }

    /**
     * This method returns a deep copy of the current neural network object.
     * A deep copy means that all the instance variables of the object are duplicated and separate from the original object, so that changes made to the copy do not affect the original.
     *
     * @return a new NeuralNetwork object that is a deep copy of the current NeuralNetwork instance.
     */
    public NeuralNetwork copy() {
        return new NeuralNetwork(this);
    }

    /**
     * Mutates the weights and biases of the neural network using the specified function.
     *
     * @param func a function that takes a double as input and returns a double as output, used to modify each weight and bias value.
     */
    public void rangedMutate(Function<Double, Double> func) {
        this.weights_ih.map(func);
        this.weights_ho.map(func);
        this.bias_h.map(func);
        this.bias_o.map(func);
    }

    /**
     * Randomly mutates the weights and biases of the neural network according to the given range and mutationChance.
     * Each weight and bias value has a mutationChance to be mutated, and if selected, it will be mutated by a random value
     * within the given range.
     *
     * @param mutationChance The mutationChance that a weight or bias value will be mutated. Should be between 0 and 1.
     * @param range The range within which each weight and bias can be mutated.
     * @see Matrix#rangedMutate(double, double)
     */
    @Override
    public void rangedMutate(double mutationChance, double range){
        this.weights_ih.rangedMutate(mutationChance, range);
        this.weights_ho.rangedMutate(mutationChance, range);
        this.bias_h.rangedMutate(mutationChance, range);
        this.bias_o.rangedMutate(mutationChance, range);
    }

    /**
     * Randomly mutates the weights and biases of the neural network with a range of 1 and a chance of 1.
     * Each weight and bias value has a chance of 100% to be mutated by a random value within the range of -1 to 1.
     */
    @Override
    public void rangedMutate(){
        this.rangedMutate(1,1);
    }

    /**
     * Randomly mutates the weights and biases of the neural network according to the given range and a default chance of 1.
     * Each weight and bias value has a chance of 100% to be mutated by a random value within the given range.
     *
     * @param range The range within which each weight and bias can be mutated.
     */
    public void rangedMutate(double range){
        this.rangedMutate(1, range);
    }

    /**
     * Mutates the weights and biases of the neural network by the given percentage.
     *
     * @param mutationChance The probability that a weight or bias will be mutated.
     * @param percent        The percentage by which to mutate the weights and biases.
     */
    public void percentageMutate(double mutationChance, double percent){
        // Mutate the weights and biases of the input-hidden layer
        this.weights_ih.percentageMutate(mutationChance, percent);
        this.bias_h.percentageMutate(mutationChance, percent);

        // Mutate the weights and biases of the hidden-output layer
        this.weights_ho.percentageMutate(mutationChance, percent);
        this.bias_o.percentageMutate(mutationChance, percent);
    }

    /**
     * Mutates the weights and biases of the neural network by 100% with a probability of 1.0.
     */
    @Override
    public void percentageMutate(){
        // Mutate the weights and biases with a mutation chance of 1.0 and a percentage of 100%
        this.percentageMutate(1,1);
    }

    /**
     * Performs crossover between two neural networks by randomly selecting matrices from each parent network.
     *
     * @param n1 The first parent neural network.
     * @param n2 The second parent neural network.
     * @return A new neural network created from the crossover of the two parent networks.
     * @see Matrix#crossover(Matrix, Matrix)
     */
    public static NeuralNetwork crossover(NeuralNetwork n1, NeuralNetwork n2){
        Matrix wih = Matrix.crossover(n1.weights_ih,n2.weights_ih);
        Matrix who = Matrix.crossover(n1.weights_ho,n2.weights_ho);
        Matrix bh = Matrix.crossover(n1.bias_h,n2.bias_h);
        Matrix bo = Matrix.crossover(n1.bias_o,n2.bias_o);

        NeuralNetwork n3 = new NeuralNetwork(wih,who,bh,bo);

        return n3;
    }

    public void initializeVisualNetwork() {
        n = new Network(0,0);
        //TODO: add biases to the nodes
        //TODO: idea just use an offset to place the nodes centred (look up the highest amount of nodes and just offset according to that)
        //add input Neurons
        n.generateCentralizedNodes(-visualLayerOffset, this.INPUT_NODES);
        //for(int i = 0; i < this.input_nodes; i++) n.addNeuron(new Neuron(-50,i * 50));

        //add hidden Neurons
        n.generateCentralizedNodes(0, this.HIDDEN_NODES, this.bias_h.toArray());
        //for(int i = 0; i < this.hidden_nodes; i++) n.addNeuron(new Neuron(0,  i * 50, this.bias_h.data[i][0]));

        //add output Neurons
        n.generateCentralizedNodes(visualLayerOffset, this.OUTPUT_NODES, this.bias_o.toArray());
        //for(int i = 0; i < this.output_nodes; i++) n.addNeuron(new Neuron(50 * 2,i * 50, this.bias_o.data[i][0]));

        //add all weights

        //connect input to hidden Neurons
        for(int i = 0; i < this.INPUT_NODES; i++){
            for(int j = 0; j < this.HIDDEN_NODES; j++){
                n.connect(n.neurons.get(i), n.neurons.get(j+this.INPUT_NODES), weights_ih.getData()[j][i]);
            }
        }
        //connect hidden to output Neurons
        for(int i = 0; i < this.HIDDEN_NODES; i++) {
            for (int j = 0; j < this.OUTPUT_NODES; j++) {
                n.connect(n.neurons.get(i+this.INPUT_NODES), n.neurons.get(j+this.HIDDEN_NODES +this.INPUT_NODES), weights_ho.getData()[j][i]);
            }
        }
    }

    public void update() {
        for(Neuron n : n.neurons) n.update();
    }

    private void setActivation_function(ActivationFunction af) {
        this.activation_function = af;
    }
    private void setLearning_rate(double lr) {
        this.learning_rate = lr;
    }

    public void paint(Graphics2D g, double x, double y) {
        g.translate(x, y);
        this.initializeVisualNetwork();
        for(Neuron n : n.neurons) n.paint(g);
    }

    public void paint(Graphics2D g, double x, double y, double[] input_array, double[] target_array) {
        g.translate(x, y);
        this.initializeVisualNetwork();
        g.setColor(Color.BLACK);
        //Draw Input
        for(int i = 0; i<input_array.length; i++)g.drawString(String.format("%.2f",input_array[i]) + "->",-150,-25+i * 50);
        //Draw output
        for(int i = 0; i<target_array.length; i++){
            g.drawString("->"+String.format("%.2f",this.predict(input_array)[i]),110, i * 50);
            if(this.output_errors.getData()[0][i] >= 0) g.setColor(Color.BLACK);
            else g.setColor(Color.RED);
            g.drawString("    " + String.format("%.2f",Math.abs(this.output_errors.getData()[0][i])), 110,i * 50 + 15);
        }
        //Paint the graph
        for(Neuron n : n.neurons) n.paint(g);
    }
}
