package Main.NeuralNetwork;

import java.util.function.Function;

public class ActivationFunction {
    public Function<Double, Double> func;
    public Function<Double, Double> dfunc;
    public static Function<Double, Double> sigmoid = e -> 1 / (1 + Math.exp(-e));
    public static Function<Double, Double> dSigmoid = e -> e * (1 - e);
    public static Function<Double, Double> tanh = e -> Math.tanh(e);
    public static Function<Double, Double> dTanh = e -> 1 - (e * e);

    public ActivationFunction(Function<Double, Double> func, Function<Double, Double> dfunc) {
        this.func = func;
        this.dfunc = dfunc;
    }
}
