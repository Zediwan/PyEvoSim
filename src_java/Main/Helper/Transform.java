package Main.Helper;

import java.awt.*;
import java.awt.geom.Ellipse2D;
import java.awt.geom.Line2D;
import java.awt.geom.Rectangle2D;

//TODO create tests for all the methods

/**
 * The `Transform` class represents the position, velocity, and acceleration of an object in 2D space.
 * It also includes methods for moving the object, applying forces to it, and getting information about its shape.
 * <p>
 * A `Transform` object is constructed with a `Vector2D` representing its initial location, velocity, and acceleration,
 * as well as a size and shape.
 * @author Jeremy Moser
 * @since 02.04.2023
 * @see Vector2D
 * @see Shape
 */
public class Transform {
    //TODO: add scale everywhere for zooming functions
    public static double scale = 1;
    /** a vector representing the location */
    private Vector2D location;
    /** a vector representing the direction of movement */
    private Vector2D velocity;
    /** a vector representing the change of movement */
    private Vector2D acceleration;
    /**
     * the size of the object
     * <p>
     * TODO maybe this will be changed and handled via the Shape object
     * */
    private double size;
    private Shape shape;

    /**
     * Constructs a new `Transform` object with the specified parameters.
     *
     * @param location representing position
     * @param velocity representing current movement
     * @param acceleration representing wanted change in movement
     * @param size width of the object
     * @param shape of the object
     * @preCondition the given vector are not null
     */
    public Transform(Vector2D location, Vector2D velocity, Vector2D acceleration, double size, Shape shape){
        assert location != null : "location is null";
        assert velocity != null : "velocity is null";
        assert acceleration != null : "acceleration is null";

        this.location = location;
        this.velocity = velocity;
        this.acceleration = acceleration;
        this.size = size;
        this.shape = shape;
    }

    /**
     * Constructs a new `Transform` object with the specified location and size.
     * The velocity and acceleration vectors are set to zero, and the shape is null.
     *
     * @param location representing position
     * @param size width of the object
     * @see #Transform(Vector2D)
     */
    public Transform(Vector2D location, float size){
        this(location);
        this.size = size;
    }

    /**
     * Constructs a new `Transform` object with the specified location.
     * The velocity and acceleration vectors are set to zero, and the size and shape are null.
     *
     * @param location representing position
     * @see Vector2D#copy()
     * @see Vector2D#Vector2D()
     */
    public Transform(Vector2D location){
        this.location = location.copy(); //important here to copy otherwise unwanted bugs may occur
        this.velocity = new Vector2D();
        this.acceleration = new Vector2D();
    }

    /**
     * Constructs a new `Transform` object with the specified x and y coordinates.
     * The velocity and acceleration vectors are set to zero, and the size and shape are null.
     *
     * @param x x-coordinate of the position vector
     * @param y y-coordinate of the position vector
     * @see #Transform(Vector2D)
     * @see Vector2D#Vector2D(double, double)
     */
    public Transform(float x, float y){
        this(new Vector2D(x,y));
    }

    /**
     * Constructs a new `Transform` object with a position vector at the origin.
     * The velocity and acceleration vectors are set to zero, and the size and shape are null.
     *
     * @see Vector2D#Vector2D()
     */
    public Transform(){
        this(new Vector2D());
    }

    /**
     * Constructs a new Transform object by copying another Transform object.
     *
     * @param transform the Transform object to be copied
     * @preCondition the given Transform object is not null
     */
    public Transform(Transform transform) {
        assert transform != null;

        this.location = transform.getLocation().copy();
        this.velocity = transform.getVelocity().copy();
        this.acceleration = transform.getAcceleration().copy();
        this.size = transform.getSize();
        this.shape = transform.getShape();  //TODO check if this is working correct maybe need to .copy()
    }

    /**
     * Updates the Transform object's location by adding the current velocity vector
     * multiplied by the specified maximum speed and then resets the acceleration vector to zero.
     *
     * @param maxSpeed the maximum speed that the object can move
     * @see Vector2D#limit(double)
     * TODO what if maxSpeed is negative or zero? where should this be handled
     * TODO add something that reduces velocity to resemble friction
     */
    public void move(double maxSpeed){
        assert maxSpeed >= 0 : "maxSpeed is negative";

        if(maxSpeed == 0){
            return;
        }else{
            /*
            double frictionMagnitude = 0.01; // adjust this to control the strength of the friction force
            Vector2D frictionForce = Vector2D.mult(this.velocity, -frictionMagnitude);
            if(this.acceleration.mag() - frictionForce.mag() >= 0){
                this.acceleration.add(frictionForce);
            }
             */
            this.velocity.add(this.acceleration);
            this.velocity.limit(maxSpeed);

            this.location.add(this.velocity);
            this.acceleration.mult(0);  //TODO think more about this, if it is needed everytime...
        }
    }

    /**
     * Applies the given force to the object, adding it to the current acceleration.
     *
     * @param force the force to apply
     * @preCondition the given force vector is not null
     */
    public void applyForce(Vector2D force) {
        assert force != null : "force is null";

        this.acceleration.add(force);
    }

    /**
     * Returns a new `Transform` object that is a copy of this object.
     * <P>
     * Only the location is copied the other vectors are the null-vector, size and shape are null
     * @return a new `Transform` object that is a copy of this object
     * @see #Transform(Transform)
     */
    public Transform clone(){
        Transform t = new Transform(location);

        return t;
    }

    /**
     * Creates a full clone of this `Transform` object with a new instance of all its properties.
     *
     * @return a new `Transform` object with the same properties as this object.
     * @see #Transform(Transform)
     */
    public Transform fullClone(){
        Transform clone = new Transform(this);

        return clone;
    }

    /**
     * Calculates the center of the Transform's shape.
     * <p>The center is half the size added in x and y direction</p>
     * @return a Vector2D representing the center location of this
     * @see #getR()
     * TODO maybe deprecated???
     */
    public Vector2D getCenter(){
        return Vector2D.add(this.location, new Vector2D(this.getR(), this.getR()));
    }

    /**
     * Returns a new `Ellipse2D` object that represents a circle with this transform's location as its center and its size as its diameter.
     * @return a new `Ellipse2D` object representing a circle with this transform's location as its center and its size as its diameter.
     * @see Ellipse2D.Double
     */

    public Ellipse2D getCircle(){
        return new Ellipse2D.Double(this.getLocX() - this.getR(), this.getLocY() - this.getR(), this.size, this.size);
    }

    /**
     * Returns a rectangle with the location of the Transform object as its center and the size of the object.
     * @return a Rectangle object representing the bounds of the Transform object.
     * @see Rectangle
     */
    public Rectangle2D.Double getRectangle(){

        Rectangle2D.Double rec = new Rectangle2D.Double(
                this.location.getX()- this.getR(),
                this.location.getY() - this.getR(),
                this.size, this.size
        );

        return rec;
    }

    /**
     * Returns a Rectangle2D.Double object that is centered around the object's location.
     * The rectangle's width and height are twice the object's radius.
     *
     * @return a Rectangle2D.Double object centered around the object's location.
     */
    public Rectangle2D.Double getTranslatedRectangle(){
        double r = this.getR();
        return new Rectangle2D.Double(-r,-r,r*2,r*2);
    }

    /**
     * Returns the rotation of the object in radians, based on its velocity vector and the positive X-axis.
     *
     * @return the rotation of the object in radians
    */
    public double getRotation(){
        double angle = Vector2D.angleBetween(this.velocity, new Vector2D(1,0));
        //if (this.velocity.getY() < 0) {
        //    angle += 180;
        //}
        return angle;
    }

    //------------------------------------------------Getter and Setter------------------------------------------------

    /**
     * Returns the radius of the object, which is half of the width/height of the object.
     * @return the radius of the object
     */
    public double getR(){
        return this.size/2;
    }

    public Vector2D getLocation() {
        return this.location;
    }

    public void setLocation(Vector2D location) {
        this.location = location;
    }

    public double getLocX(){
        return this.location.getX();
    }

    public void setLocX(float x) {
        this.location.setX(x);
    }

    public double getLocY(){
        return this.location.getY();
    }

    public void setLocY(float y){
        this.location.setY(y);
    }

    public Vector2D getVelocity() {
        return this.velocity;
    }

    public void setVelocity(Vector2D velocity) {
        this.velocity = velocity;
    }

    public Vector2D getAcceleration() {
        return this.acceleration;
    }

    public void setAcceleration(Vector2D acceleration) {
        this.acceleration = acceleration;
    }

    public double getSize() {
        return this.size;
    }

    public void setSize(double size) {
        this.size = size;
    }

    public static double getScale() {
        return scale;
    }

    public static void setScale(double scale) {
        Transform.scale = scale;
    }

    public Shape getShape() {
        return shape;
    }

    public void setShape(Shape shape) {
        this.shape = shape;
    }

    //------------------------------------------------toString and paint-----------------------------------------------

    //TODO think about th utilization of the shape
    public void paint(Graphics2D g){
        g.fill(this.shape);
    }

    /**
     * Returns a line representing the velocity vector of this animal,
     * scaled by the specified factor, relative to the animal's position.
     *
     * @param scale the scaling factor for the velocity vector
     * @return a Line2D object representing the scaled velocity vector relative to the animal's position
     */
    public Line2D getVelocityLine(double scale){
        // Calculate the moved velocity vector by adding the current location and the scaled velocity vector.
        Vector2D movedVelocity = Vector2D.add(this.location, this.velocity.copy().mult(scale));

        // Create a new Line2D object from the animal's current location to the location of the moved velocity vector.
        return new Line2D.Double(
                this.location.getRoundedX(), this.location.getRoundedY(),
                movedVelocity.getRoundedX(), movedVelocity.getRoundedY());
    }

    /**
     * Returns a Line2D object representing the translated velocity vector of this object.
     * The Line2D object is scaled by the specified factor and rotated by the object's current rotation angle.
     *
     * @param scale the scale factor by which to scale the velocity vector
     * @return a Line2D object representing the translated velocity vector of this object
     * @since 12.04.2023
     */
    public Line2D getTranslatedVelocityLine(double scale) {
        // Scale the velocity vector
        Vector2D scaledVelocity = this.velocity.copy().mult(scale);

        // Rotate the scaled velocity vector by the negative rotation angle of the object
        scaledVelocity.rotate(-this.getRotation());

        // Create and return a Line2D object from (0, 0) to the scaled and rotated velocity vector
        return new Line2D.Double(0, 0, scaledVelocity.getRoundedX(), scaledVelocity.getRoundedY());
    }

    /**
     * Paints the acceleration vector drawn from the center of this
     * @param g the graphics object to paint on
     * @deprecated Use {@link #getAccelerationLine(double)} or {@link #getTranslatedAccelerationLine(double)}
     */
    public void paintAcceleration(Graphics2D g){
        //TODO add scaling to the length
        //TODO how can this be painted if acceleration is reset each timestep
        Vector2D movedVelocity = Vector2D.add(this.location, this.acceleration.copy().mult(20));

        g.drawLine(
                this.location.getRoundedX(), this.location.getRoundedY(),
                movedVelocity.getRoundedX(), movedVelocity.getRoundedY()
        );
    }

    /**
     * Returns a line representing the acceleration vector of this animal,
     * scaled by the specified factor, relative to the animal's position.
     *
     * @param scale the scaling factor for the acceleration vector
     * @return a Line2D object representing the scaled acceleration vector relative to the animal's position
     */
    public Line2D getAccelerationLine(double scale){
        // Calculate the moved acceleration vector by adding the current location and the scaled acceleration vector.
        Vector2D movedAcceleration = Vector2D.add(this.location, this.acceleration.copy().mult(scale));

        // Create a new Line2D object from the animal's current location to the location of the moved acceleration vector.
        return new Line2D.Double(
                this.location.getRoundedX(), this.location.getRoundedY(),
                movedAcceleration.getRoundedX(), movedAcceleration.getRoundedY());
    }

    /**
     * Returns a Line2D object representing the translated acceleration vector of this object.
     * The Line2D object is scaled by the specified factor and rotated by the object's current rotation angle.
     *
     * @param scale the scale factor by which to scale the acceleration vector
     * @return a Line2D object representing the translated acceleration vector of this object
     * @since 12.04.2023
     */
    public Line2D getTranslatedAccelerationLine(double scale) {
        // Scale the acceleration vector
        Vector2D scaledAcceleration = this.acceleration.copy().mult(scale);

        // Rotate the scaled acceleration vector by the negative rotation angle of the object
        scaledAcceleration.rotate(-this.getRotation());

        // Create and return a Line2D object from (0, 0) to the scaled and rotated acceleration vector
        return new Line2D.Double(0, 0, scaledAcceleration.getRoundedX(), scaledAcceleration.getRoundedY());
    }

}
