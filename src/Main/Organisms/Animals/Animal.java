package Main.Organisms.Animals;

import Main.CFrame;
import Main.NeuralNetwork.NeuralNetwork;
import Main.Organisms.Attributes.DNA.DNA;
import Main.Organisms.Attributes.DNA.Gene;
import Main.Organisms.Attributes.Gender;
import Main.Helper.Transform;
import Main.Helper.Vector2D;
import Main.Organisms.Organism;

import java.awt.*;
import java.util.ArrayList;
import java.util.Timer;
import java.util.TimerTask;

public class Animal extends Organism {
    public static long aniCount = 0;
    private static Animal blueprint;
    private static double baseExhaustDmg = 1;
    private static double allMaxSize = 4;
    private static double allMaxSpeed = 4;

    //TODO how should generations be handled when there are two parents?
    protected int generation = 0;
    protected Gender gender;
    protected double maxSpeed, maxForce;
    protected NeuralNetwork nn;
    protected double reproductiveUrge = 0;

    //------------------------------------------------DNA Variables----------------------------------------------------

    protected double speedRatio;                    //[9]
    protected double strength;                      //[10]  //TODO: make this depend on size, via a ration or something
    protected long gestationDuration;               //[11]
    protected double incubationTime;                //[12]
    protected double hatchTime;                     //[13]
    protected double viewAngle;                     //[14]
    protected double viewDistance;                  //[15]
    protected double timerFrequency;                //[16]
    protected double pheromoneSensibility;          //[17]
    protected static int numberAnimalGenes = 11;

    //-----------------------------------------------------------------------------------------------------------------

    //Constructors
    //Used for population by system
    public Animal() {
        super();

        Animal.aniCount++;
        this.id = Animal.aniCount;

        this.dna = new DNA();
        this.expressGenes();
    }

    //Used for population by reproduction
    public Animal(Animal father, Animal mother){
        super(father,mother);

        this.dna = DNA.crossover(father.getDna(), mother.getDna());
        this.dna.mutate(mother.getDna().getGene(5).getValue(), mother.getDna().getGene(4).getValue());

        this.nn = NeuralNetwork.crossover(father.getNn(), mother.getNn());
        this.nn.mutate(mother.getDna().getGene(7).getValue(), mother.getDna().getGene(6).getValue());

        Animal.aniCount++;
        this.id = Animal.aniCount;
        this.generation += Math.max(father.generation,mother.generation) + 1;

        this.expressGenes();
    }

    //Used for explicit creation
    public Animal(Transform transform, DNA dna, NeuralNetwork nn){
        super(transform,dna);

        Animal.aniCount++;
        this.id = Animal.aniCount;

        this.expressGenes();
        this.nn = nn;
    }

    //TODO Test
    //TODO write documentation
    //this is a singleton pattern
    public static Animal blueprint(){
        if(Animal.blueprint == null) {
            Transform t = new Transform();  //location is at (0,0)

            Gene[] genes = {
                    //TODO: set default parameters
                    new Gene(.1, "sizeRatio"),
                    new Gene(128, "colorRed"),
                    new Gene(128, "colorGreen"),
                    new Gene(128, "colorBlue"),
                    new Gene(.1, "mutSizeDNA"),
                    new Gene(.01, "mutProbDNA"),
                    new Gene(.1, "mutSizeNN"),
                    new Gene(.01, "mutProbNN"),
                    new Gene(1, "attractiveness"),
                    new Gene(.1, "speedRatio"),
                    new Gene(1, "strength"),
                    new Gene(5*1000, "gestationDuration"),
                    new Gene(1, "incubationTime"),
                    new Gene(1, "hatchTime"),
                    new Gene(45, "viewAngle"),
                    new Gene(4, "viewDistance"),
                    new Gene(1, "timerFrequency"),
                    new Gene(1, "pheromoneSensibility")
            };
            DNA dna = new DNA(genes);

            //TODO: check if these are the correct default amount of inputs
            NeuralNetwork nn = new NeuralNetwork(12, 36, 3);

            Animal blueprint = new Animal(t,dna,nn);
            Animal.aniCount--;  //to not increase the counter when not needed
            blueprint.id = 0;

            Animal.blueprint = blueprint;
        }
        return Animal.blueprint;
    }

    //TODO Test
    //TODO write documentation
    @Override
    public void expressGenes() {
        super.expressGenes();
        int shift = Organism.numberOrganismGenes;

        this.gender = Gender.getRandomGender();

        this.dna.getGene(shift+0).gene0to1Check();
        this.speedRatio = this.dna.getGene(shift+0).getValue();

        this.strength = this.dna.getGene(shift+1).getValue();

        this.gestationDuration = Math.round(this.dna.getGene(shift+2).getValue());

        //TODO this may be deleted
        this.incubationTime = this.dna.getGene(shift+3).getValue();
        //TODO this may be delete
        this.hatchTime = this.dna.getGene(shift+4).getValue();

        this.viewAngle = this.dna.getGene(shift+5).getValue();

        this.viewDistance = this.dna.getGene(shift+6).getValue();

        this.timerFrequency = this.dna.getGene(shift+7).getValue();

        this.pheromoneSensibility = this.dna.getGene(shift+8).getValue();

        this.transform.size = Animal.allMaxSize * this.sizeRatio;
        this.maxSpeed = Animal.allMaxSpeed * this.speedRatio;
    }

    //TODO Test
    //TODO write documentation
    @Override
    public void update() {
        assert !this.isDead() : "this is dead";
        //TODO add physics so they can't run through into another and don't clip

        this.think();
            //use energy for thinking

        //Movement
        //TODO: maybe refactor this?
        //TODO check if this should be tweaked (relation to size, resistance, slipperiness, etc.)
        this.transform.velocity.add(this.transform.acceleration);
        this.transform.velocity.limit(maxSpeed);
        this.transform.location.add(this.transform.velocity);
        this.transform.acceleration.mult(0);

        //update variables and states
            //this.energy -= this.metabolismCost();   //use energy to move
            //use energy for existing
            //use energy for moving
        if(this.energy <= 0){
            this.takeDamage(this.energy - Animal.baseExhaustDmg);
        }

        this.borders1();
    }

    //TODO Test
    //TODO write documentation
    public void think(){
        //collect input for nn
            //variables
        double healthRatio;
        double energyRatio;
        this.speed();
            //TODO challenge how to animals detect what animals are hunter and prey?
            //search closest food
                //get coordinates
                //get angle
                //amount of food visable
            //search closest animal
                //get coordinates
                //get angle
                //amount of animals visable
        //think

        /*
        ----OUTPUS----
        Accelerate
        Rotate
        Herding Desire
        Mate Desire
        Eat Desire
        Growth
        Healing Strength
        Want to Attack (aggressiveness)
         */
    }

    //TODO Test
    //TODO write documentation
    @Override
    public void grow() {
        //when should an animal be able to grow? what does grow actually mean?
    }

    //TODO Test
    //TODO write documentation
    public boolean mate(Animal mate){
        Animal self = this;
        //TODO: when do two organisms mate?
        boolean doMate = this.attractiveness <= mate.getAttractiveness() * this.reproductiveUrge;
        if(doMate){
            if(gender.canBirth()){
                //what happens if female
                this.gender.setMate(mate);

                new Timer().schedule(
                        new TimerTask() {
                            @Override
                            public void run() {
                                self.reproduce();
                            }
                        },
                        this.gestationDuration
                );
            }
        }
        return doMate;
    }

    //TODO Test
    //TODO write documentation
    @Override
    public Organism reproduce() {
        Organism child = null;
        if(this.gender.canBirth()) {
            child = new Animal(this, gender.getMate());
        }
        return child;
    }

    //TODO Test
    //TODO write documentation
    //Collision registration
    public boolean collision(Organism o){
        //check if this collides with something
        return this.getLocation().distSq(o.getLocation()) <= Math.pow(this.getR() + o.getR(), 2);
    }

    //TODO Test
    //TODO write documentation
    //Search for food
    public Organism searchClosest(ArrayList<Organism> organisms){
        assert !this.isDead() : "This is dead";

        Organism closestOrganism = null;
        double closestDistance = Double.POSITIVE_INFINITY;

        //calculate the closest organism
        for(Organism o : organisms){
            double distance = this.getLocation().distSq(o.getLocation());
            //if the distance is smaller than the current closest distance and smaller than the viewDistance
            if((closestDistance >= distance) && (distance <= Math.pow(this.viewDistance,2))){
                closestDistance = distance;
                closestOrganism = o;
            }
        }
        return closestOrganism;
    }

    //TODO Test
    //TODO write documentation
    //Border handling
    public void borders1(){
        if(this.transform.location.x < -this.transform.getR())this.transform.location.x = CFrame.WIDTH;
        if(this.transform.location.y < -this.transform.getR())this.transform.location.y = CFrame.HEIGHT;
        if(this.transform.location.x > CFrame.WIDTH + this.transform.getR())this.transform.location.x = 0;
        if(this.transform.location.y > CFrame.HEIGHT + this.transform.getR())this.transform.location.y = 0;
    }

    //TODO Test
    //TODO write documentation
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
        //TODO does this make sense? shouldn't more energy be used when bigger?
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
