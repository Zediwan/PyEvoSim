package Main.Helper;

import java.util.function.Function;

public class Matrix {
    //TODO: write Test cases
    //TODO: couldn't we remove the rows and cols indicator and jsut use .length()
    private final int rows;
    private final int cols;
    private double[][] data;

    public Matrix(int rows, int cols){
        this.rows = rows;
        this.cols = cols;
        this.data = new double[rows][cols];
        for(int r = 0 ; r < this.rows; r++){
            for(int c = 0; c < this.cols; c++){
                this.data[r][c] = 0;
            }
        }
    }

    public Matrix copy() {
        Matrix m = new Matrix(this.rows, this.cols);
        for (int i = 0; i < this.rows; i++) {
            for (int j = 0; j < this.cols; j++) {
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
        double[] arr = new double[this.rows+this.cols];
        for(int r = 0 ; r < this.rows; r++){
            for(int c = 0; c < this.cols; c++){
                arr[r+c] = this.data[r][c];
            }
        }
        return arr;
    }


    public Matrix randomize(){
        for(int r = 0 ; r < this.rows; r++){
            for(int c = 0; c < this.cols; c++){
                this.data[r][c] = Math.floor(Math.random()*2 -1);
            }
        }
        return this;
    }
    public static Matrix randomize(Matrix m1){
        assert m1.data != null : "Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        for(int r = 0 ; r < m1.rows; r++){
            for(int c = 0; c < m1.cols; c++){
                m1.data[r][c] = Math.floor(Math.random()*2 -1);
            }
        }
        return m1;
    }


    public Matrix add(double scalar){
        for(int r = 0 ; r < this.rows; r++){
            for(int c = 0; c < this.cols; c++){
                this.data[r][c] += scalar;
            }
        }
        return this;
    }
    public static Matrix add(Matrix m1, double scalar){
        assert m1.data != null : "Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        Matrix result = new Matrix(m1.cols, m1.rows);
        for(int r = 0 ; r < m1.rows; r++){
            for(int c = 0; c < m1.cols; c++){
                result.data[r][c] = m1.data[r][c] + scalar;
            }
        }
        return result;
    }

    public Matrix add(Matrix oM){
        assert this.cols == oM.cols : "Cols don't match: " + this.cols + "!=" + oM.cols;
        assert this.rows == oM.rows : "Rows don't match: " + this.rows + "!=" + oM.rows;;
        assert oM.data != null : "Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        for(int r = 0 ; r < this.rows; r++){
            for(int c = 0; c < this.cols; c++){
                this.data[r][c] += oM.data[r][c];
            }
        }
        return this;
    }
    public static Matrix add(Matrix m1, Matrix m2){
        assert m1.data != null : "Main.NeuralNetwork.NeuralNetwork.Matrix is null";
        assert m2.data != null : "Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        Matrix result = new Matrix(m1.cols, m1.rows);
        for(int r = 0 ; r < m1.rows; r++){
            for(int c = 0; c < m1.cols; c++){
                result.data[r][c] = m1.data[r][c] + m2.data[r][c];
            }
        }
        return result;
    }

    public Matrix sub(Matrix oM){
        assert this.cols == oM.cols : "Cols don't match: " + this.cols + "!=" + oM.cols;
        assert this.rows == oM.rows : "Rows don't match: " + this.rows + "!=" + oM.rows;;
        assert oM.data != null : "Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        for(int r = 0 ; r < this.rows; r++){
            for(int c = 0; c < this.cols; c++){
                this.data[r][c] -= oM.data[r][c];
            }
        }
        return this;
    }
    public static Matrix sub(Matrix m1, Matrix m2){
        assert m1.data != null : "Main.NeuralNetwork.NeuralNetwork.Matrix is null";
        assert m2.data != null : "Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        Matrix result = new Matrix(m1.cols, m1.rows);
        for(int r = 0 ; r < m1.rows; r++){
            for(int c = 0; c < m1.cols; c++){
                result.data[r][c] = m1.data[r][c] - m2.data[r][c];
            }
        }
        return result;
    }


    public Matrix mult(double scalar){
        for(int r = 0 ; r < this.rows; r++){
            for(int c = 0; c < this.cols; c++){
                this.data[r][c] *= scalar;
            }
        }
        return this;
    }
    public static Matrix mult(Matrix m1, double scalar){
        assert m1.data != null : "Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        Matrix result = new Matrix(m1.cols, m1.rows);
        for(int r = 0 ; r < m1.rows; r++){
            for(int c = 0; c < m1.cols; c++){
                result.data[r][c] = m1.data[r][c] * scalar;
            }
        }
        return result;
    }

    public static Matrix mult(Matrix m1, Matrix m2){
        assert m1.cols == m2.rows : "Cols and Rows don't match; " + m1.cols + "!=" + m2.rows;
        assert m1.data != null : "Main.NeuralNetwork.NeuralNetwork.Matrix is null";
        assert m2.data != null : "Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        Matrix result = new Matrix(m1.rows, m2.cols);
        for(int r = 0 ; r < result.rows ; r++){
            for(int c = 0 ; c < result.cols ; c++){
                double sum = 0;
                for(int k = 0 ; k < m1.cols ; k++){
                    sum += m1.data[r][k] * m2.data[k][c];
                }
                result.data[r][c] = sum;
            }
        }
        return result;
    }


    public Matrix mult(Matrix oM){
        assert oM.data != null : "Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        for(int r = 0 ; r < this.rows; r++){
            for(int c = 0; c < this.cols; c++){
                this.data[r][c] *= oM.data[r][c];
            }
        }
        return this;
    }
    public static Matrix elemMult(Matrix m1, Matrix m2){
        assert m1.rows != m2.rows || m1.cols != m2.cols : "Columns and Rows of A must match Columns and Rows of B.";
        assert m1.data != null : "Main.NeuralNetwork.NeuralNetwork.Matrix is null";
        assert m2.data != null : "Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        Matrix result = new Matrix(m1.cols, m1.rows);
        for(int r = 0 ; r < m1.rows; r++){
            for(int c = 0; c < m1.cols; c++){
                result.data[r][c] = m1.data[r][c] * m2.data[c][r];
            }
        }
        return result;
    }


    public static Matrix transpose(Matrix m1) {
        assert m1.data != null : "Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        Matrix result = new Matrix(m1.cols, m1.rows);
        for(int r = 0 ; r < m1.rows; r++){
            for(int c = 0; c < m1.cols; c++){
                result.data[c][r] = m1.data[r][c];
            }
        }
        return result;
    }


    public Matrix map(Function<Double, Double> f){
        assert this.data != null : "Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        for(int r = 0 ; r < this.rows; r++){
            for(int c = 0; c < this.cols; c++){
                double val = this.data[r][c];
                this.data[r][c] = f.apply(val);
            }
        }
        return this;
    }
    public static Matrix map(Matrix m1, Function<Double, Double> f) {
        assert m1.data != null : "Main.NeuralNetwork.NeuralNetwork.Matrix is null";

        Matrix result = new Matrix(m1.rows, m1.cols);
        for(int r = 0 ; r < result.rows; r++){
            for(int c = 0; c < result.cols; c++){
                double val = m1.data[r][c];
                result.data[r][c] = f.apply(val);
            }
        }
        return result;
    }

    public String toString(){
        String s = "";
        for(int r = 0 ; r < this.rows; r++){
            s+= "| ";
            for(int c = 0; c < this.cols; c++){
                s += data[r][c];
                s += " ";
            }
            s += "|\n";
        }
        return s;
    }
}
