package Main.Helper;

import java.util.function.Function;

//TODO create tests for all the methods

/**
 * A Matrix class for performing various operations on matrices, such as addition, multiplication, and element-wise multiplication.
 *
 * @author Jeremy Moser
 * @since 02.04.2023
 */
public class Matrix implements mutable {
    //TODO: write Test cases
    //TODO: couldn't we remove the rows and cols indicator and just use .length()
    /**
     * The number of rows in the matrix.
     */
    private final int ROWS;

    /**
     * The number of columns in the matrix.
     */
    private final int COLS;

    /**
     * The data in the matrix represented as a two-dimensional array.
     */
    private double[][] data;

    /**
     * Constructs a matrix with the specified number of rows and columns.
     * All elements of the matrix are initialized to 0.
     *
     * @param rows the number of rows in the matrix.
     * @param cols the number of columns in the matrix.
     * @preCondition rows must be bigger than 0
     * @preCondition cols must be bigger than 0
     */
    public Matrix(int rows, int cols){
        assert rows > 0 : "invalid number of rows";
        assert cols > 0 : "invalid number of columns";

        this.ROWS = rows;
        this.COLS = cols;
        this.data = new double[rows][cols];
        for(int r = 0; r < this.ROWS; r++){
            for(int c = 0; c < this.COLS; c++){
                this.data[r][c] = 0;
            }
        }
    }

    /**
     * Returns a new Matrix object that is a copy of the current Matrix object.
     *
     * @return a new Matrix object that is a copy of the current Matrix object.
     */
    public Matrix copy() {
        Matrix m = new Matrix(this.ROWS, this.COLS);
        for (int i = 0; i < this.ROWS; i++) {
            for (int j = 0; j < this.COLS; j++) {
                m.data[i][j] = this.data[i][j];
            }
        }

        return m;
    }

    /**
     * Creates a new Matrix object from an array of double values.
     * The matrix has the same number of rows as the length of the array and 1 column.
     *
     * @param arr the array of double values.
     * @return a new Matrix object created from the array of double values.
     */
    public static Matrix fromArray(double[] arr){
        Matrix m = new Matrix(arr.length, 1);
        for(int r = 0 ; r < arr.length ; r++){
            m.data[r][0] = arr[r];
        }

        return m;
    }

    /**
     * Converts the matrix to a one-dimensional array.
     *
     * @return a one-dimensional array containing all elements of the matrix.
     */
    public double[] toArray(){
        double[] arr = new double[this.ROWS +this.COLS];
        for(int r = 0; r < this.ROWS; r++){
            for(int c = 0; c < this.COLS; c++){
                arr[r+c] = this.data[r][c];
            }
        }

        return arr;
    }

    /**
     * Randomizes the elements of the matrix using a random value between -0.5 and 0.5.
     *
     * @return the current Matrix object with its elements randomized.
     */
    public Matrix randomize(){
        for(int r = 0; r < this.ROWS; r++){
            for(int c = 0; c < this.COLS; c++){
                this.data[r][c] = Math.random()-.5;
            }
        }

        return this;
    }

    /**
     * Randomizes the values of the matrix by adding a random value within the given range to each element.
     *
     * @param range the range of the random values that will be added to each element.
     * @return the randomized matrix.
     */
    public Matrix randomize(double range) {
        for(int r = 0; r < this.ROWS; r++) {
            for(int c = 0; c < this.COLS; c++) {
                this.data[r][c] += (Math.random() * 2 * range) - range;
            }
        }

        return this;
    }

    /**
     * Randomly modifies the values of the current matrix by adding a random number
     * between -range and range to each element, with a given chance of modifying each element.
     *
     * @param chance The probability of modifying each element, between 0 (no element is modified) and 1 (all elements are modified).
     * @param range The maximum absolute value of the random number to add to each element.
     * @return This matrix, with the modified values.
     */
    public Matrix randomize(double chance, double range){
        for(int r = 0; r < this.ROWS; r++){
            for(int c = 0; c < this.COLS; c++){
                if(Math.random()< chance){
                    this.data[r][c] += (Math.random()* 2 * range)-range;
                }
            }
        }

        return this;
    }

    /**
     * Randomize the values of a given Matrix object.
     *
     * @param m1 the Matrix object to randomize
     * @return the same Matrix object with randomized data
     * @preCondition parameter matrix is not null
     */
    public static Matrix randomize(Matrix m1){
        assert m1.data != null : "Matrix is null";

        for(int r = 0; r < m1.ROWS; r++){
            for(int c = 0; c < m1.COLS; c++){
                m1.data[r][c] = Math.random()-.5;
            }
        }

        return m1;
    }

    /**
     * Add a value to each element of this matrix.
     *
     * @param value to be added to each element of the matrix
     * @return the resulting matrix after the addition
     */
    public Matrix add(double value){
        for(int r = 0; r < this.ROWS; r++){
            for(int c = 0; c < this.COLS; c++){
                this.data[r][c] += value;
            }
        }

        return this;
    }

    /**
     * Adds a scalar value to every element in a matrix.
     *
     * @param m1 the matrix to which the scalar will be added
     * @param value the value to add
     * @return a new matrix with the same dimensions as m1, where every element is the sum of the corresponding
     * element in m1 and the value
     * @preCondition the input matrix is null
     */
    public static Matrix add(Matrix m1, double value){
        assert m1.data != null : "Matrix is null";

        Matrix result = new Matrix(m1.COLS, m1.ROWS);
        for(int r = 0; r < m1.ROWS; r++){
            for(int c = 0; c < m1.COLS; c++){
                result.data[r][c] = m1.data[r][c] + value;
            }
        }

        return result;
    }

    /**
     * Adds the values of another Matrix object to the current Matrix object.
     *
     * @param oM the other Matrix object to add to the current Matrix
     * @return the resulting Matrix object after addition
     * @preCondition the cols and rows of the matrices match and given matrix is not null
     */
    public Matrix add(Matrix oM){
        assert this.COLS == oM.COLS : "Cols don't match: " + this.COLS + "!=" + oM.COLS;
        assert this.ROWS == oM.ROWS : "Rows don't match: " + this.ROWS + "!=" + oM.ROWS;;
        assert oM.data != null : "Matrix is null";

        for(int r = 0; r < this.ROWS; r++){
            for(int c = 0; c < this.COLS; c++){
                this.data[r][c] += oM.data[r][c];
            }
        }

        return this;
    }

    /**
     * Returns a new Matrix object which is the result of element-wise addition of the two input matrices.
     *
     * @param m1 The first Matrix object to be added.
     * @param m2 The second Matrix object to be added.
     * @return A new Matrix object which is the result of element-wise addition of the two input matrices.
     * @preCondition given matrices are not null
     */
    public static Matrix add(Matrix m1, Matrix m2){
        assert m1.data != null : "Matrix is null";
        assert m2.data != null : "Matrix is null";

        Matrix result = new Matrix(m1.COLS, m1.ROWS);
        for(int r = 0; r < m1.ROWS; r++){
            for(int c = 0; c < m1.COLS; c++){
                result.data[r][c] = m1.data[r][c] + m2.data[r][c];
            }
        }

        return result;
    }

    /**
     * Subtracts the values of another matrix from the values of this matrix.
     *
     * @param oM the other matrix to subtract from this matrix
     * @return the resulting matrix after the subtraction
     * @preCondition the cols and rows of the matrices match and given matrix is not null
     */
    public Matrix sub(Matrix oM){
        assert this.COLS == oM.COLS : "Cols don't match: " + this.COLS + "!=" + oM.COLS;
        assert this.ROWS == oM.ROWS : "Rows don't match: " + this.ROWS + "!=" + oM.ROWS;;
        assert oM.data != null : "Matrix is null";

        for(int r = 0; r < this.ROWS; r++){
            for(int c = 0; c < this.COLS; c++){
                this.data[r][c] -= oM.data[r][c];
            }
        }

        return this;
    }

    /**
     * Returns a new matrix whose elements are the difference between the corresponding elements of the input matrices.
     *
     * @param m1 the first input matrix
     * @param m2 the second input matrix
     * @return a new matrix whose elements are the difference between the corresponding elements of the input matrices
     * @preCondition given matrices are not null
     */
    public static Matrix sub(Matrix m1, Matrix m2){
        assert m1.data != null : "Matrix is null";
        assert m2.data != null : "Matrix is null";

        Matrix result = new Matrix(m1.COLS, m1.ROWS);
        for(int r = 0; r < m1.ROWS; r++){
            for(int c = 0; c < m1.COLS; c++){
                result.data[r][c] = m1.data[r][c] - m2.data[r][c];
            }
        }

        return result;
    }

    /**
     * Multiplies all elements of the matrix by a scalar value.
     *
     * @param scalar the scalar value to multiply by
     * @return the modified matrix
     */
    public Matrix mult(double scalar){
        for(int r = 0; r < this.ROWS; r++){
            for(int c = 0; c < this.COLS; c++){
                this.data[r][c] *= scalar;
            }
        }
        return this;
    }

    /**
     * Multiplies a matrix by a scalar value.
     *
     * @param m1 the matrix to multiply
     * @param scalar the scalar value to multiply each element of the matrix by
     * @return a new matrix that is the result of the multiplication
     * @throws AssertionError if the input matrix is null
     */
    public static Matrix mult(Matrix m1, double scalar){
        assert m1.data != null : "Matrix is null";

        Matrix result = new Matrix(m1.COLS, m1.ROWS);
        for(int r = 0; r < m1.ROWS; r++){
            for(int c = 0; c < m1.COLS; c++){
                result.data[r][c] = m1.data[r][c] * scalar;
            }
        }

        return result;
    }

    /**
     * Performs matrix multiplication between two matrices.
     * The number of columns in the first matrix must match the number of rows in the second matrix.
     * If this condition is not met, an AssertionError is thrown.
     *
     * @param m1 the first matrix to be multiplied
     * @param m2 the second matrix to be multiplied
     * @return a new Matrix that is the result of multiplying m1 and m2
     * @throws AssertionError if the number of columns in m1 does not match the number of rows in m2, or if either matrix is null
     */
    public static Matrix mult(Matrix m1, Matrix m2){
        assert m1.COLS == m2.ROWS : "Cols and Rows don't match; " + m1.COLS + "!=" + m2.ROWS;
        assert m1.data != null : "Matrix is null";
        assert m2.data != null : "Matrix is null";

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

    /**
     * Multiplies this matrix with the given matrix element-wise and updates the values in this matrix.
     *
     * @param oM the matrix to multiply with
     * @return this matrix after element-wise multiplication with oM
     * @throws AssertionError if the given matrix is null
     */
    public Matrix mult(Matrix oM){
        assert oM.data != null : "Matrix is null";

        for(int r = 0; r < this.ROWS; r++){
            for(int c = 0; c < this.COLS; c++){
                this.data[r][c] *= oM.data[r][c];
            }
        }

        return this;
    }

    /**
     * Performs element-wise multiplication of two matrices.
     *
     * @param m1 the first matrix
     * @param m2 the second matrix
     * @return a new matrix that is the element-wise multiplication of m1 and m2
     * @throws AssertionError if the columns and rows of m1 do not match the columns and rows of m2, or if either matrix is null
     */
    public static Matrix elemMult(Matrix m1, Matrix m2){
        assert m1.ROWS != m2.ROWS || m1.COLS != m2.COLS : "Columns and Rows of m1 must match Columns and Rows of m2.";
        assert m1.data != null : "Matrix is null";
        assert m2.data != null : "Matrix is null";

        Matrix result = new Matrix(m1.COLS, m1.ROWS);
        for(int r = 0; r < m1.ROWS; r++){
            for(int c = 0; c < m1.COLS; c++){
                result.data[r][c] = m1.data[r][c] * m2.data[c][r];
            }
        }

        return result;
    }

    /**
     * Returns a new matrix that is the transpose of the given matrix.
     *
     * @param m1 the matrix to be transposed
     * @return a new matrix that is the transpose of the given matrix
     * @throws AssertionError if the matrix is null
     */
    public static Matrix transpose(Matrix m1) {
        assert m1.data != null : "Matrix is null";

        Matrix result = new Matrix(m1.COLS, m1.ROWS);
        for(int r = 0; r < m1.ROWS; r++){
            for(int c = 0; c < m1.COLS; c++){
                result.data[c][r] = m1.data[r][c];
            }
        }

        return result;
    }

    /**
     * Performs mutation on the matrix object by adding a new matrix object with random values multiplied by a mutation chance and range.
     * The resulting matrix is added to the original matrix object using the add() method. The original matrix object is mutated in place.
     *
     * @param mutationChance The chance of a given value being mutated.
     * @param range The range of the mutation.
     * @see Matrix#rangedMutate(double, double)
     */
    @Override
    public void rangedMutate(double mutationChance, double range) {
        Matrix mutation = new Matrix(this.ROWS,this.COLS).randomize(mutationChance,range);
        this.add(mutation);
    }

    /**
     * Adds a random value to each element in the matrix, with a mutation chance of 1 and range of 1.
     *
     * @see #rangedMutate(double, double)
     */
    @Override
    public void rangedMutate() {
        this.rangedMutate(1,1);
    }

    /**
     * Randomly mutates the weights by a percentage amount, with a specified mutation chance.
     * @param mutationChance The probability that a weight will be mutated
     * @param percent The percentage amount by which to mutate the weight
     */
    @Override
    public void percentageMutate(double mutationChance, double percent){
        for(int r = 0; r < this.ROWS; r++){
            for(int c = 0; c < this.COLS; c++){
                // If the mutationChance is greater than a random number between 0 and 1, then mutate the weight
                if(Math.random()< mutationChance){
                    // Mutate the weight by the given percentage amount
                    this.data[r][c] += (this.data[r][c] * percent) - ((this.data[r][c] * percent)/2);
                }
            }
        }
    }

    /**
     * Randomly mutates the weights by a default percentage amount and mutation chance.
     * The default values are 1.
     */
    @Override
    public void percentageMutate(){
        this.percentageMutate(1,1);
    }

    /**
     * Performs a crossover operation between two matrices of the same size, creating a new matrix with values
     * randomly selected from both input matrices.
     *
     * @param m1 the first input matrix
     * @param m2 the second input matrix
     * @return a new matrix resulting from the crossover operation
     * @throws AssertionError if the input matrices have different number of rows or columns
     */
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

    /**
     * Applies the given function to each element in the matrix and returns the result as a new Matrix object.
     *
     * @param f the function to apply to each element in the matrix
     * @return a new Matrix object with each element being the result of applying the function to the corresponding element in the original matrix
     * @throws AssertionError if the matrix is null
     */
    public Matrix map(Function<Double, Double> f){
        assert this.data != null : "Matrix is null";

        for(int r = 0; r < this.ROWS; r++){
            for(int c = 0; c < this.COLS; c++){
                double val = this.data[r][c];
                this.data[r][c] = f.apply(val);
            }
        }

        return this;
    }

    /**
     * Applies a given function to each element of this matrix.
     *
     * @param f the function to apply
     * @return this matrix after the function has been applied to each element
     * @throws AssertionError if this matrix is null
     */
    public static Matrix map(Matrix m1, Function<Double, Double> f) {
        assert m1.data != null : "Matrix is null";

        Matrix result = new Matrix(m1.ROWS, m1.COLS);
        for(int r = 0; r < result.ROWS; r++){
            for(int c = 0; c < result.COLS; c++){
                double val = m1.data[r][c];
                result.data[r][c] = f.apply(val);
            }
        }
        return result;
    }

    //------------------------------------------------Getter and Setter------------------------------------------------

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

    //------------------------------------------------toString and paint-----------------------------------------------

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
