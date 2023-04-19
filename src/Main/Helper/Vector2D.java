package Main.Helper;

import java.awt.*;

//TODO create tests for all the methods

/**
 * A vector represents a point in two-dimensional space
 * @author Jeremy Moser
 * @since 02.04.2023
 */
public class Vector2D {
    /**
     * @param x the x coordinate of the point
     * @param y the y coordinate of the point
     */
    private double x;
    private double y;

    /**
     * Constructor
     * @param x coordinate
     * @param y coordinate
     */
    public Vector2D(double x, double y) {
        this.x = x;
        this.y = y;
    }

    /**
     * Constructor
     * <p>
     * If no arguments are given, the null-vector will be created
     */
    public Vector2D(){
        this.x = 0;
        this.y = 0;
    }

    /**
     * @return a copy of the vector
     */
    public Vector2D copy() {
        return new Vector2D(this.x, this.y);
    }

    /**
     * Creates a vector within a radius
     * @param surrounding the range where the vector should lie in
     * @return the vector
     * @preCondition surrounding must be positive
     */
    public static Vector2D randSurroundingVec(double surrounding){
        assert surrounding >= 0 : "surrounding must be positive";

        return new Vector2D(Math.random()*surrounding - (surrounding/2), Math.random()*surrounding- (surrounding/2));
    }

    /**
     * Generates a random vector from 0 to the limits
     * @param maxX maximal x value of the vector
     * @param maxY maximal y value of the vector
     * @return a random Vector in the rang from 0 to (maxX and maxY)
     */
    public static Vector2D randLimVec(double maxX, double maxY){
        return new Vector2D(Math.random()*maxX, Math.random()*maxY);
    }

    /**
     * Regular vector addition
     * NOTE: Changes the vector on which this method is called
     * @param v the vector that should be added
     * @return the changed vector
     * @preCondition vector must not be null
     */
    public Vector2D add(Vector2D v) {
        assert v != null : "given vector is null";

        this.x += v.x;
        this.y += v.y;

        return this;
    }

    /**
     * Regular vector addition
     * NOTE: Doesn't change the vector(s), instead a new one is generated
     * @param v1 first vector
     * @param v2 second vector
     * @return the sum of the regular vector addition
     * @preCondition none of the two vectors should be null
     */
    public static Vector2D add(Vector2D v1, Vector2D v2){
        assert v1 != null : "given vector is null";
        assert v2 != null : "given vector is null";

        double newX = v1.x + v2.x;
        double newY = v1.y + v2.y;
        Vector2D vector = new Vector2D(newX,newY);

        return vector;
    }

    /**
     * Regular vector subtraction
     * NOTE: Changes the vector on which this method is called
     * @param v that should be subtracted
     * @return the changed vector
     * @preCondition vector must not be null
     */
    public Vector2D sub(Vector2D v) {
        assert v != null : "given vector is null";

        this.x -= v.x;
        this.y -= v.y;

        return this;
    }

    /**
     * Regular vector subtraction
     * NOTE: Doesn't change the vector(s), instead a new one is generated
     * @param v1 first vector
     * @param v2 second vector
     * @return the difference of the two vectors
     * @preCondition none of the two vectors should be null
     */
    public static Vector2D sub(Vector2D v1, Vector2D v2){
        assert v1 != null : "given vector is null";
        assert v2 != null : "given vector is null";

        double newX = v1.x - v2.x;
        double newY = v1.y - v2.y;
        Vector2D vector = new Vector2D(newX,newY);

        return vector;
    }

    /**
     * Regular scalar multiplication
     * NOTE: Changes the vector on which this method is called
     * @param scalar that the vector should be scaled by
     * @return the scaled vector
     */
    public Vector2D mult(double scalar){
        this.x *= scalar;
        this.y *= scalar;

        return this;
    }

    /**
     * Regular scalar multiplication
     * NOTE: Doesn't change the vector(s), instead a new one is generated
     * @param v vector that should be scaled
     * @param scalar that the vector should be scaled by
     * @return the scaled vector
     * @preCondition vector should not be null
     */
    public static Vector2D mult(Vector2D v, double scalar){
        assert v != null : "given vector is null";

        Vector2D vector = new Vector2D(v.x * scalar, v.y * scalar);
        return vector;
    }

    /**
     * Inverse of the vector multiplication
     * NOTE: Changes the vector on which this method is called
     * @param scalar that the vector should be shrunk by
     * @return the changed vector
     * @preCondition scalar mustn't be zero
     */
    public Vector2D div(double scalar){
        assert scalar != 0 :  "scalar is zero";

        this.x /= scalar;
        this.y /= scalar;

        return this;
    }

    /**
     * Inverse of the vector multiplication
     * NOTE: Doesn't change the vector(s), instead a new one is generated
     * @param v vector that should be shrunk
     * @param scalar that the vector should be shrunk by
     * @return a new vector
     * @preCondition the given vector shouldn't be null and the scalar cannot be zero
     */
    public static Vector2D div(Vector2D v, double scalar){
        assert v != null : "given vector is null";
        assert scalar != 0 : "scalar is zero";

        Vector2D vector = new Vector2D(v.x / scalar, v.y / scalar);

        return vector;
    }

    /**
     * Dot product of two vectors, multiplication of the x values and the y values separately
     * @param v vector that should be multiplied with
     * @return the dot product
     * @preCondition the given vector is not null
     */
    public double dot(Vector2D v){
        assert v != null : "given vector is null";

        return this.x * v.x + this.y * v.y;
    }

    /**
     * Dot product of two vectors, multiplication of the x values and the y values separately
     * @param v1 first vector
     * @param v2 second vector
     * @return the dot product
     * @preCondition vectors mustn't be null
     */
    public static double dot(Vector2D v1, Vector2D v2){
        assert v1 != null : "first given vector is null";
        assert v2 != null : "second given vector is null";

        return v1.x * v2.x + v1.y * v2.y;
    }

    /**
     * normalizes a vector by dividing the values with the length of the vector
     * NOTE: Changes the vector on which this method is called
     * NOTE: if the magnitude is 0 then return the normal vector
     * @return the normalized vector
     * @see #magSq()
     * @postCondition checking if normalization worked correctly, needs overhaul and testing
     */
    public Vector2D normalize(){
        //first check is to avoid division by 0
        //second part is that if the magnitude squared is 1 then the vector is already normalized
        if(this.magSq()!=0 && this.magSq() != 1){
            this.x = Math.pow(this.x,2) / this.magSq();
            this.y = Math.pow(this.y,2) / this.magSq();

            //assertion for floating point errors
            //TODO check if this is still needed or think about better ways to check that
            //assert (this.mag() >= .9 || this.mag() <= 1.1): "Magnitude is not relative close to 1 but: " + this.mag();
        }

        return this;
    }

    /**
     * The normalized vector is calculated by the x,y variables divided by the vector's length.
     * NOTE: Doesn't change the vector(s), instead a new one is generated
     * NOTE: if the magnitude is 0 then return the normal vector
     * @return a normalized vector
     * @see #copy()
     * @see #normalize(Vector2D)
     * @preCondition given vector mustn't be null
     * TODO check if this works correctly
     */
    public static Vector2D normalize(Vector2D v) {
        assert v != null : "given vector is null";

        return v.copy().normalize();
    }

    /**
     * The length is calculated by the square root of the coordinates by the power of 2.
     * NOTE: this method is computationally heavier, if possible use {@link Vector2D#magSq()} for better performance
     * @return the length of the vector
     * @postCondition length of the vector isn't smaller than zero
     */
    public double mag(){
        double mag = Math.sqrt(Math.pow(this.x,2) + Math.pow(this.y,2));

        assert mag >= 0 : "Magnitude is negative (" + mag+")";

        return mag;
    }

    /**
     * Works like {@link Vector2D#mag()} but is computationally better
     * @return the squared length of a vector
     * @postCondition magnitude squared is greater than zero
     */
    public double magSq(){
        double magSq = this.x*this.x + this.y*this.y;

        assert magSq >= 0 : "Magnitude is negative (" + magSq +")";

        return magSq;
    }

    /**
     * scales the vector to a given magnitude, by first {@link #normalize normalizing} it
     * and the {@link #mult multiplying} by the factor
     * NOTE: Changes the vector on which this method is called
     * @param m the magnitude the vector should have
     * @return the vector changed vector
     * @see #normalize()
     * @see #mult(double)
     * @postCondition checking if normalization worked correctly, needs overhaul and testing
     */
    public Vector2D setMag(double m){
        Vector2D v = this.normalize().mult(m);

        //TODO check if this is still needed or think about better ways to check that
        assert (this.mag() >= m-.001 || this.mag() <= m+.001): "Magnitude is not "+ m +" but: " + this.mag();

        return v;
    }

    /**
     * Calculates the distance between two vectors
     * @param v the other vector
     * @return the distance
     * @see #sub(Vector2D, Vector2D)
     * @see #mag()
     */
    public double dist(Vector2D v){
        return Vector2D.sub(v,this).mag();
    }

    /**
     * Calculates the distance between two vectors
     * Use {@link #distSq(Vector2D, Vector2D)} for better performance
     * @param v1 first vector
     * @param v2 second vector
     * @return the distance between the vectors
     * @see #sub(Vector2D, Vector2D)
     * @see #mag()
     */
    public static double dist(Vector2D v1, Vector2D v2){
        return Vector2D.sub(v1,v2).mag();
    }

    /**
     * Calculates the distance squared between two vectors
     * Works like {@link #dist(Vector2D)} but is computationally better
     * @param v the other vector
     * @return the distance
     * @see #sub(Vector2D, Vector2D)
     * @see #magSq()
     */
    public double distSq(Vector2D v){
        return Vector2D.sub(v,this).magSq();
    }

    /**
     * Calculates the distance squared between two vectors
     * Works like {@link #dist(Vector2D, Vector2D)} but is computationally better
     * Used for better performance
     * @param v1 first vector
     * @param v2 second vector
     * @return the distance between the vectors
     * @see #sub(Vector2D, Vector2D)
     * @see #magSq()
     */
    public static double distSq(Vector2D v1, Vector2D v2){
        return Vector2D.sub(v1,v2).magSq();
    }

    /**
     * Limit the magnitude of this vector to the value used for the max parameter.
     * NOTE: Changes the vector on which this method is called
     * @param max magnitude of the vector
     * @return the vector
     * @see #magSq()
     * @see #setMag(double)
     */
    public Vector2D limit(double max) {
        if (this.magSq() > (max*max)){
            this.setMag(max);
        }
        return this;
    }

    /**
     * Calculates and returns the angle (in radians) between two vectors.
     *
     * @param v1 the first vector
     * @param v2 the second vector
     * @return the angle (in radians) between the two vectors
     */
    public static double angleBetween(Vector2D v1, Vector2D v2) {
        double v1mag = v1.mag();
        double v2mag = v2.mag();

        if (v1mag == 0 || v2mag == 0) {
            return 0.0; // return 0 if either vector is a zero vector
        }

        double dot = v1.dot(v2);
        double cosTheta = dot / (v1mag * v2mag);

        if (cosTheta < -1.0) {
            cosTheta = -1.0;
        } else if (cosTheta > 1.0) {
            cosTheta = 1.0;
        }

        return Math.acos(cosTheta);
    }


    /**
     * Make a new 2D unit vector from an angle
     * @param target the target vector (if null, a new vector will be created)
     * @return the vector
     */
    static public Vector2D fromAngle(double angle, Vector2D target) {
        if (target == null) {
            target = new Vector2D(Math.cos(angle),Math.sin(angle));
        } else {
            target.set(Math.cos(angle),Math.sin(angle));
        }
        return target;
    }

    /**
     * * Make a new 2D unit vector from an angle.
     *
     * @brief Make a new 2D unit vector from an angle
     * @param angle the angle in radians
     * @return the new unit PVector
     */
    static public Vector2D fromAngle(double angle) {
        return fromAngle(angle,null);
    }

    /**
     * Rotate the vector by an angle (only 2D vectors), magnitude remains the same
     *
     * @brief Rotate the vector by an angle (2D only)
     * @param theta the angle of rotation
     */
    public Vector2D rotate(double theta) {
        double temp = x;
        // Might need to check for rounding errors like with angleBetween function?
        x = x*Math.cos(theta) - y*Math.sin(theta);
        y = temp*Math.sin(theta) + y*Math.cos(theta);
        return this;
    }

    /**
     * Calculate the angle of rotation for this vector (only 2D vectors)
     *
     * @return the angle of rotation
     * @brief Calculate the angle of rotation for this vector
     */
    public float heading() {
        float angle = (float) Math.atan2(y, x);
        return angle;
    }

    /**
     * Checks if this vector is the null vector
     *
     * @return if the vector is the null vector (if x and y are 0)
     */
    //TODO add a variance so that a vector (.00001,.000001) is also seen as the null vector
    public boolean isNullVector(){
        return this.x == 0 && this.y == 0;
    }

    //------------------------------------------------Getter and Setter------------------------------------------------

    /**
     * @param x the x component of the vector
     * @param y the y component of the vector
     */
    public Vector2D set(double x, double y) {
        this.x = x;
        this.y = y;
        return this;
    }

    public void setX(double x){
        this.x = x;
    }

    public void setY(double y){
        this.y = y;
    }

    public double getX() {
        return x;
    }

    public double getY() {
        return y;
    }

    /**
     * This is used for painting
     * @return the rounded x coordinates
     * @see #paint(Graphics2D)
     */
    public int getRoundedX(){
        return (int)Math.round(this.x);
    }

    /**
     * This is used for painting
     * @return the rounded y coordinates
     * @see #paint(Graphics2D)
     */
    public int getRoundedY(){
        return (int)Math.round(this.y);
    }

    /**
     * This is used for some Shape methods that use Points as variables
     * @return a Point representing the vector
     */
    public Point toPoint(){
        return new Point((int)Math.round(this.x), (int)Math.round(this.y));
    }


    /**
     * Transforms a "negative vector" into the null-vector
     * @return the vector only with values >= 0
     * @Deprecated
     */
    public Vector2D negVectorCheck(){
        if(this.x < 0){
            this.x = 0;
        }
        if(this.y < 0){
            this.y = 0;
        }
        return this;
    }

    //------------------------------------------------toString and paint-----------------------------------------------

    /**
     * @return the vectors x and y coordinates as a string
     */
    public String toString(){
        return this.x + ", " + this.y;
    }

    /**
     * Used for displaying the vector as a point
     * @param g the Graphics variable used for panting
     * @see #getRoundedX()
     * @see #getRoundedY()
     */
    public void paint(Graphics2D g){
        g.fillOval(this.getRoundedX(),this.getRoundedY(),1,1);
    }

    //TODO: doesnt really belong in this class, maybe create a new class
    public static float map(float value, float isStart, float isStop, float oStart, float oStop){
        return oStart + (oStop-oStart) * ((value-isStart)/(isStop-isStart));
    }
    public static double map(double value, double isStart, double isStop, double oStart, double oStop){
        return oStart + (oStop-oStart) * ((value-isStart)/(isStop-isStart));
    }
}

