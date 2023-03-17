package Main.Helper;

import java.util.function.Function;

public class Matrix implements mutable {
    //TODO: write Test cases
    //TODO: couldn't we remove the rows and cols indicator and jsut use .length()
    private final int ROWS;
    private final int COLS;
    public double[][] data;

    public Matrix(int rows, int cols){
        this.ROWS = rows;
        this.COLS = cols;
        this.data = new double[rows][cols];
        for(int r = 0; r < this.ROWS; r++){
            for(int c = 0; c < this.COLS; c++){
                this.data[r][c] = 0;
            }
        }
    }

    public Matrix copy() {
        Matrix m = new Matrix(this.ROWS, this.COLS);
        for (int i = 0; i < this.ROWS; i++) {
            for (int j = 0; j < this.COLS; j++) {
                m.data[i][j] = this.data[i][j];
            }
        }
        return m;
    }

    public static Matrix fromArray(double[] arr){
        Matrix m = new Matrix(arr.length, 1);
        for(int r = 0 ; r < arr.length ; r++){
            m.data[r][0] = arr[r];
        }
        return m;
    }

    public double[] toArray(){
        double[] arr = new double[this.ROWS +this.COLS];
        for(int r = 0; r < this.ROWS; r++){
            for(int c = 0; c < this.COLS; c++){
                arr[r+c] = this.data[r][c];
            }
        }
        return arr;
    }


    public Matrix randomize(){
        for(int r = 0; r < this.ROWS; r++){
            for(int c = 0; c < this.COLS; c++){
                this.data[r][c] = Math.random()-.5;
            }
        }
        return this;
    }

    public Matrix randomize(double range){
        for(int r = 0; r < this.ROWS; r++){
            for(int c = 0; c < this.COLS; c++){
                this.data[r][c] += (Math.random()*range)-(range/2);
            }
        }
        return this;
    }

    public Matrix randomize(double range, double chance){
        for(int r = 0; r < this.ROWS; r++){
            for(int c = 0; c < this.COLS; c++){
                if(Math.random()< chance){
                    this.data[r][c] += (Math.random()*range)-(range/2);
                }
            }
        }
        return this;
    }
    public static Matrix randomize(Matrix m1){
        assert m1.data != null : "Main.Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        for(int r = 0; r < m1.ROWS; r++){
            for(int c = 0; c < m1.COLS; c++){
                m1.data[r][c] = Math.random()-.5;
            }
        }
        return m1;
    }


    public Matrix add(double scalar){
        for(int r = 0; r < this.ROWS; r++){
            for(int c = 0; c < this.COLS; c++){
                this.data[r][c] += scalar;
            }
        }
        return this;
    }
    public static Matrix add(Matrix m1, double scalar){
        assert m1.data != null : "Main.Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        Matrix result = new Matrix(m1.COLS, m1.ROWS);
        for(int r = 0; r < m1.ROWS; r++){
            for(int c = 0; c < m1.COLS; c++){
                result.data[r][c] = m1.data[r][c] + scalar;
            }
        }
        return result;
    }

    public Matrix add(Matrix oM){
        assert this.COLS == oM.COLS : "Cols don't match: " + this.COLS + "!=" + oM.COLS;
        assert this.ROWS == oM.ROWS : "Rows don't match: " + this.ROWS + "!=" + oM.ROWS;;
        assert oM.data != null : "Main.Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        for(int r = 0; r < this.ROWS; r++){
            for(int c = 0; c < this.COLS; c++){
                this.data[r][c] += oM.data[r][c];
            }
        }
        return this;
    }
    public static Matrix add(Matrix m1, Matrix m2){
        assert m1.data != null : "Main.Main.NeuralNetwork.NeuralNetwork.Matrix is null";
        assert m2.data != null : "Main.Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        Matrix result = new Matrix(m1.COLS, m1.ROWS);
        for(int r = 0; r < m1.ROWS; r++){
            for(int c = 0; c < m1.COLS; c++){
                result.data[r][c] = m1.data[r][c] + m2.data[r][c];
            }
        }
        return result;
    }

    public Matrix sub(Matrix oM){
        assert this.COLS == oM.COLS : "Cols don't match: " + this.COLS + "!=" + oM.COLS;
        assert this.ROWS == oM.ROWS : "Rows don't match: " + this.ROWS + "!=" + oM.ROWS;;
        assert oM.data != null : "Main.Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        for(int r = 0; r < this.ROWS; r++){
            for(int c = 0; c < this.COLS; c++){
                this.data[r][c] -= oM.data[r][c];
            }
        }
        return this;
    }
    public static Matrix sub(Matrix m1, Matrix m2){
        assert m1.data != null : "Main.Main.NeuralNetwork.NeuralNetwork.Matrix is null";
        assert m2.data != null : "Main.Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        Matrix result = new Matrix(m1.COLS, m1.ROWS);
        for(int r = 0; r < m1.ROWS; r++){
            for(int c = 0; c < m1.COLS; c++){
                result.data[r][c] = m1.data[r][c] - m2.data[r][c];
            }
        }
        return result;
    }


    public Matrix mult(double scalar){
        for(int r = 0; r < this.ROWS; r++){
            for(int c = 0; c < this.COLS; c++){
                this.data[r][c] *= scalar;
            }
        }
        return this;
    }
    public static Matrix mult(Matrix m1, double scalar){
        assert m1.data != null : "Main.Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        Matrix result = new Matrix(m1.COLS, m1.ROWS);
        for(int r = 0; r < m1.ROWS; r++){
            for(int c = 0; c < m1.COLS; c++){
                result.data[r][c] = m1.data[r][c] * scalar;
            }
        }
        return result;
    }

    public static Matrix mult(Matrix m1, Matrix m2){
        assert m1.COLS == m2.ROWS : "Cols and Rows don't match; " + m1.COLS + "!=" + m2.ROWS;
        assert m1.data != null : "Main.Main.NeuralNetwork.NeuralNetwork.Matrix is null";
        assert m2.data != null : "Main.Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        Matrix result = new Matrix(m1.ROWS, m2.COLS);
        for(int r = 0; r < result.ROWS; r++){
            for(int c = 0; c < result.COLS; c++){
                double sum = 0;
                for(int k = 0; k < m1.COLS; k++){
                    sum += m1.data[r][k] * m2.data[k][c];
                }
                result.data[r][c] = sum;
            }
        }
        return result;
    }


    public Matrix mult(Matrix oM){
        assert oM.data != null : "Main.Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        for(int r = 0; r < this.ROWS; r++){
            for(int c = 0; c < this.COLS; c++){
                this.data[r][c] *= oM.data[r][c];
            }
        }
        return this;
    }
    public static Matrix elemMult(Matrix m1, Matrix m2){
        assert m1.ROWS != m2.ROWS || m1.COLS != m2.COLS : "Columns and Rows of A must match Columns and Rows of B.";
        assert m1.data != null : "Main.Main.NeuralNetwork.NeuralNetwork.Matrix is null";
        assert m2.data != null : "Main.Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        Matrix result = new Matrix(m1.COLS, m1.ROWS);
        for(int r = 0; r < m1.ROWS; r++){
            for(int c = 0; c < m1.COLS; c++){
                result.data[r][c] = m1.data[r][c] * m2.data[c][r];
            }
        }
        return result;
    }


    public static Matrix transpose(Matrix m1) {
        assert m1.data != null : "Main.Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        Matrix result = new Matrix(m1.COLS, m1.ROWS);
        for(int r = 0; r < m1.ROWS; r++){
            for(int c = 0; c < m1.COLS; c++){
                result.data[c][r] = m1.data[r][c];
            }
        }
        return result;
    }

    @Override
    public void mutate() {
        this.mutate(1,1);
    }

    @Override
    public void mutate(double mutationChance, double range) {
        Matrix mutation = new Matrix(this.ROWS,this.COLS).randomize(mutationChance,range);
        this.add(mutation);
    }

    //TODO should this only be done with same size matrices? or how would different sized matrices be handled?
    public static Matrix crossover(Matrix m1, Matrix m2){
        assert(m1.ROWS == m2.ROWS) : "Different amount of Rows";
        assert(m1.COLS == m2.COLS) : "Different amount of Cols";

        Matrix m3 = m1.copy();
        for(int r = 0; r < m1.ROWS; r++){
            for(int c = 0; c < m1.COLS; c++){
                /*
                Select randomly one of the two matrices values
                Here as we start with m1's values we only need to choose m2's values 50% of the time
                 */
                if(Math.random() < .5) {
                    m3.data[r][c] = m2.data[r][c];
                }
            }
        }
        return m3;
    }

    public Matrix map(Function<Double, Double> f){
        assert this.data != null : "Main.Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        for(int r = 0; r < this.ROWS; r++){
            for(int c = 0; c < this.COLS; c++){
                double val = this.data[r][c];
                this.data[r][c] = f.apply(val);
            }
        }
        return this;
    }
    public static Matrix map(Matrix m1, Function<Double, Double> f) {
        assert m1.data != null : "Main.Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        Matrix result = new Matrix(m1.ROWS, m1.COLS);
        for(int r = 0; r < result.ROWS; r++){
            for(int c = 0; c < result.COLS; c++){
                double val = m1.data[r][c];
                result.data[r][c] = f.apply(val);
            }
        }
        return result;
    }

    public int getROWS() {
        return ROWS;
    }

    public int getCOLS() {
        return COLS;
    }

    public double[][] getData() {
        return data;
    }

    public void setData(double[][] data) {
        this.data = data;
    }

    public String toString(){
        String s = "";
        for(int r = 0; r < this.ROWS; r++){
            s+= "| ";
            for(int c = 0; c < this.COLS; c++){
                s += data[r][c];
                s += " ";
            }
            s += "|\n";
        }
        return s;
    }
}
