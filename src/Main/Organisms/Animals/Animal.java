package Main.Organisms.Animals;

import Main.CFrame;
import Main.NeuralNetwork.NeuralNetwork;
import Main.Organisms.Attributes.DNA.DNA;
import Main.Organisms.Attributes.Gender;
import Main.Helper.Transform;
import Main.Helper.Vector2D;
import Main.Organisms.Organism;

import java.awt.*;
import java.util.ArrayList;

public class Animal extends Organism {
    public static long aniCount = 0;

    protected Gender gender;
    protected double maxSpeed, maxForce;
    protected NeuralNetwork nn;

    //------------------------------------------------DNA Variables----------------------------------------------------

    protected double speedRatio;                    //[9]
    protected double strength;                      //[10]  //TODO: make this depend on size, via a ration or something
    protected double layTime;                       //[11]
    protected double incubationTime;                //[12]
    protected double hatchTime;                     //[13]
    protected double viewAngle;                     //[14]
    protected double viewDistance;                  //[15]
    protected double timerFrequency;                //[16]
    protected double pheromoneSensibility;          //[17]
    protected static int numberAnimalGenes = 11;

    //-----------------------------------------------------------------------------------------------------------------

    //Constructors
    public Animal(Transform transform, DNA dna){
        super(transform,dna);

        Animal.aniCount++;
        this.id = Animal.aniCount;

        this.expressGenes();
    }

    public Animal(){
        super();

        Animal.aniCount++;
        this.id = Animal.aniCount;

        this.dna = new DNA();
        this.expressGenes();

        this.invariant();
    }

    @Override
    public void expressGenes() {
        super.expressGenes();
        int shift = Organism.numberOrganismGenes;
        this.gender = Gender.getRandomGender();
        this.speedRatio = (int)Math.round(this.dna.getGene(shift+0).getValue());
        this.strength = (int)Math.round(this.dna.getGene(shift+1).getValue());
        this.layTime = (int)Math.round(this.dna.getGene(shift+2).getValue());
        this.incubationTime = (int)Math.round(this.dna.getGene(shift+3).getValue());
        this.hatchTime = (int)Math.round(this.dna.getGene(shift+4).getValue());
        this.viewAngle = (int)Math.round(this.dna.getGene(shift+5).getValue());
        this.viewDistance = (int)Math.round(this.dna.getGene(shift+6).getValue());
        this.timerFrequency = (int)Math.round(this.dna.getGene(shift+7).getValue());
        this.pheromoneSensibility = (int)Math.round(this.dna.getGene(shift+8).getValue());
    }

    @Override
    public void update() {
        //update position
        //update variables and states
    }

    public void think(){
        //collect input for nn
        //think
    }

    @Override
    public void grow() {
        //when should an animal be able to grow? what does grow actually mean?
    }

    public boolean mate(Organism mate){
        boolean doMate = false; //TODO: when do two organisms mate?
        if(doMate){
            if(this.gender == Gender.FEMALE){
                //what happens if female
            }else{
                //what happens if male
            }
        }
        return doMate;
    }

    @Override
    public Organism reproduce(DNA mateDNA) {
        Organism child = null;
        if(this.gender == Gender.FEMALE){
            //what happens if female
        }else{
            //what happens if male
        }
        return child;
    }

    //Collision registration
    public boolean collision(Organism o){
        //check if this collides with something
        return false;
    }

    //Search for food
    public Organism searchFood(ArrayList<Organism> organisms){
        return null;
    }

    //Border handling
    public void borders1(){
        if(this.transform.location.x < -this.transform.getR())this.transform.location.x = CFrame.WIDTH;
        if(this.transform.location.y < -this.transform.getR())this.transform.location.y = CFrame.HEIGHT;
        if(this.transform.location.x > CFrame.WIDTH + this.transform.getR())this.transform.location.x = 0;
        if(this.transform.location.y > CFrame.HEIGHT + this.transform.getR())this.transform.location.y = 0;
    }
    public void borders2(){
        Vector2D desired = new Vector2D();

        //check the x Axis
        if(this.getLocX() < 0){
            desired = new Vector2D(this.maxSpeed, this.transform.velocity.getY());
        }else if (this.getLocX() > CFrame.WIDTH){
            desired = new Vector2D(-this.maxSpeed, this.transform.velocity.getY());
        }
        desired.normalize();
        desired.mult(this.maxSpeed);

        Vector2D steer = Vector2D.sub(desired,this.transform.getVelocity());
        steer.limit(this.maxForce);
        this.transform.applyForce(steer);

        //check the y Axis
        if(this.getLocY() < 0){
            desired = new Vector2D(this.transform.velocity.getX(), this.maxSpeed);
        }else if (this.getLocY() > CFrame.HEIGHT){
            desired = new Vector2D(this.transform.velocity.getX(), -this.maxSpeed);
        }
        desired.normalize();
        desired.mult(this.maxSpeed);

        steer = Vector2D.sub(desired,this.transform.getVelocity());
        steer.limit(this.maxForce);
        this.transform.applyForce(steer);
    }

    public double metabolismCost(){
        return this.speed() / (2*this.size());
    }

    //------------------------------------------------Getter and Setter------------------------------------------------

    public Gender getGender() {
        return gender;
    }

    public void setGender(Gender gender) {
        this.gender = gender;
    }

    public double getMaxSpeed() {
        return maxSpeed;
    }

    public void setMaxSpeed(double maxSpeed) {
        this.maxSpeed = maxSpeed;
    }

    public double getMaxForce() {
        return maxForce;
    }

    public void setMaxForce(double maxForce) {
        this.maxForce = maxForce;
    }

    public double getViewDistance() {
        return viewDistance;
    }

    public void setViewDistance(double viewDistance) {
        this.viewDistance = viewDistance;
    }

    public NeuralNetwork getNn() {
        return nn;
    }

    public void setNn(NeuralNetwork nn) {
        this.nn = nn;
    }

    public double size(){
        return this.transform.size;
    }

    public double speed(){
        //TODO: check if velocity changes when no acceleration is applied
        return this.transform.acceleration.mag();
    }

    //------------------------------------------------toString and paint-----------------------------------------------

    @Override
    public void paint(Graphics2D g) {

    }

    //------------------------------------------------invariant--------------------------------------------------------

    /**
     * @return if the current speed is bigger than the maxSpeed
     */
    public boolean invariant(){
        return (this.transform.velocity.magSq() <= (this.maxSpeed*this.maxSpeed) + .01) ||
                (this.transform.velocity.magSq() >= (this.maxSpeed*this.maxSpeed) - .01);
    }
}
