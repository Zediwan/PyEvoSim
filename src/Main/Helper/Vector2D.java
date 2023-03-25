package Main.Helper;

public class Vector2D {
    //TODO: change variables to private
    public double x; //x coordinate
    public double y; //y coordinate

    public Vector2D(double x, double y) {
        this.x = x;
        this.y = y;
    }

    /**
     * Convention if no values are given just generate the null vector
     */
    public Vector2D(){
        this.x = 0;
        this.y = 0;
    }
    /**
     * Transforms a "negative vector" into the null vector
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

    public static Vector2D randSurroundingVec(double surrounding){
        return new Vector2D(Math.random()*surrounding - (surrounding/2), Math.random()*surrounding- (surrounding/2));
    }


    /**
     * Generates a random vector within 0 to the limits
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
     */
    public Vector2D add(Vector2D v) {
        assert v != null;

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
     */
    public static Vector2D add(Vector2D v1, Vector2D v2){
        assert v1 != null;
        assert v2 != null;

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
     */
    public Vector2D sub(Vector2D v) {
        assert v != null;

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
     */
    public static Vector2D sub(Vector2D v1, Vector2D v2){
        assert v1 != null;
        assert v2 != null;

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
     */
    public static Vector2D mult(Vector2D v, double scalar){
        assert v != null;

        Vector2D vector = new Vector2D(v.x * scalar, v.y * scalar);
        return vector;
    }

    /**
     * Inverse of the vector multiplication
     * NOTE: Changes the vector on which this method is called
     * @param scalar that the vector should be shrunk by
     * @return the changed vector
     */
    public Vector2D div(double scalar){
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
     */
    public static Vector2D div(Vector2D v, double scalar){
        assert v != null;
        assert scalar != 0;

        Vector2D vector = new Vector2D(v.x / scalar, v.y / scalar);
        return vector;
    }

    /**
     * Dot product of two vectors, multiplication of the x values and the y values separately
     * @param v vector that should be multiplied with
     * @return the dot product
     */
    public double dot(Vector2D v){
        return this.x * v.x + this.y * v.y;
    }

    /**
     * Dot product of two vectors, multiplication of the x values and the y values separately
     * @param v1 first vector
     * @param v2 second vector
     * @return the dot product
     */
    public static double dot(Vector2D v1, Vector2D v2){
        return v1.x * v2.x + v1.y * v2.y;
    }

    /**
     * normalizes a vector by dividing the values with the length of the vector
     * NOTE: Changes the vector on which this method is called
     * NOTE: if the magnitude is 0 then return the normal vector
     * @return the normalized vector
     */
    public Vector2D normalize(){
        if(this.mag()!=0){
            this.x /= this.mag();
            this.y /= this.mag();
            assert (this.mag() >= .9 || this.mag() <= 1.1): "Magnitude is not 1 but: " + this.mag();
        }
        return this;
    }

    /**
     * The normalized vector is calculated by the x,y variables divided by the vector's length.
     * NOTE: Doesn't change the vector(s), instead a new one is generated
     * NOTE: if the magnitude is 0 then return the normal vector
     * @return a normalized vector
     */
    public static Vector2D normalize(Vector2D v) {
        assert v != null;
        Vector2D normalizedVector = v;
        if(v.mag() != 0) normalizedVector = new Vector2D(v.x/v.mag(), v.y/v.mag());
        return normalizedVector;
    }

    /**
     * The length is calculated by the square root of the coordinates by the power of 2.
     * Post-condition: length is never smaller than 0.
     * @return the length of the vector
     */
    public double mag(){
        double mag = Math.sqrt(Math.pow(this.x,2) + Math.pow(this.y,2));
        assert mag >= 0 : "Magnitude is negative (" + mag+")";
        return mag;
    }

    /**
     * Post-condition: length is never smaller than 0.
     * @return the squared length of a vector
     */
    public double magSq(){
        double magSq = this.x*this.x + this.y*this.y;
        assert !(magSq < 0) : "Magnitude is negative (" + magSq +")";
        return magSq;
    }

    /**
     * scales the vector to a given magnitude
     * @param m the magnitude the vector should have
     * @return the vector
     */
    public Vector2D setMag(double m){
        Vector2D v = this.normalize().mult(m);
        assert (this.mag() >= m-.001 || this.mag() <= m+.001): "Magnitude is not "+ m +" but: " + this.mag();
        return v;
    }

    /**
     * Calculates the distance between two vectors
     * @param v the other vector
     * @return the distance
     */
    public double dist(Vector2D v){
        return Vector2D.sub(v,this).mag();
    }

    /**
     * Calculates the distance between two vectors
     * @param v1 first vector
     * @param v2 second vector
     * @return the distance between the vectors
     */
    public static double dist(Vector2D v1, Vector2D v2){
        return Vector2D.sub(v1,v2).mag();
    }

    /**
     * Calculates the distance squared between two vectors
     * Used for better performance
     * @param v the other vector
     * @return the distance
     */
    public double distSq(Vector2D v){
        /*
        double dist = Vector2D.sub(v,this).magSq();
        if(dist == Double.POSITIVE_INFINITY || dist == Double.NEGATIVE_INFINITY){
            dist = 0;
        }
        return dist;
         */
        return Vector2D.sub(v,this).magSq();
    }

    /**
     * Calculates the distance squared between two vectors
     * Used for better performance
     * @param v1 first vector
     * @param v2 second vector
     * @return the distance between the vectors
     */
    public static double distSq(Vector2D v1, Vector2D v2){
        return Vector2D.sub(v1,v2).magSq();
    }

    /**
     * Limit the magnitude of this vector to the value used for the max parameter.
     * NOTE: Changes the vector on which this method is called
     * @param max magnitude of the vector
     * @return the vector
     */
    public Vector2D limit(double max) {
        if (this.magSq() > (max*max)) this.setMag(max);
        //assert (this.magSq() <= (max*max)+.5) : "Magnitude (" + this.mag() + ") is bigger than maximum (" + max+")";
        return this;
    }

    /**
     * Calculates and returns the angle (in radians) between two vectors.
     *
     * @param v1 the x, y components of a Vector
     * @param v2 the x, y components of a Vector
     * @brief Calculate and return the angle between two vectors
     */
    static public double angleBetween(Vector2D v1, Vector2D v2) {

        // We get NaN if we pass in a zero vector which can cause problems
        // Zero seems like a reasonable angle between a (0,0,0) vector and something else
        if (v1.x == 0 && v1.y == 0) return 0.0f;
        if (v2.x == 0 && v2.y == 0) return 0.0f;

        double dot = v1.x * v2.x + v1.y * v2.y;
        double v1mag = Math.sqrt(v1.x * v1.x + v1.y * v1.y);
        double v2mag = Math.sqrt(v2.x * v2.x + v2.y * v2.y);
        // This should be a number between -1 and 1, since it's "normalized"
        double amt = dot / (v1mag * v2mag);
        // But if it's not due to rounding error, then we need to fix it
        // Otherwise if outside the range, acos() will return NaN
        if (amt <= -1) {
            return Math.PI;
        } else if (amt >= 1) {
            return 0;
        }
        return Math.acos(amt);
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

    //TODO: doesnt really belong in this class
    public static float map(float value, float isStart, float isStop, float oStart, float oStop){
        return oStart + (oStop-oStart) * ((value-isStart)/(isStop-isStart));
    }
    public static double map(double value, double isStart, double isStop, double oStart, double oStop){
        return oStart + (oStop-oStart) * ((value-isStart)/(isStop-isStart));
    }

    public String toString(){
        return this.x + ", " + this.y;
    }

    public Vector2D copy() {
        return new Vector2D(this.x, this.y);
    }
}

