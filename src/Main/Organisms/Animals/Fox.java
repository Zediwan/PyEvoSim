package Main.Organisms.Animals;

import Main.CFrame;
import Main.Organisms.Attributes.DNA;
import Main.Organisms.Attributes.Gender;
import Main.Helper.Transform;
import Main.Helper.Vector2D;
import Main.Organisms.Organism;
import Main.Organisms.Plants.Grass;

import java.awt.*;
import java.util.ArrayList;

public class Fox extends Animal {
    public static DNA sumDNA = DNA.initiateSumDNA(11,
            new String[]{
            "NA","size", "maxSpeed", "maxForce", "viewDistance",
            "desiredSepDist", "desiredAliDist", "desiredCohDist",
            "sepWeight", "aliWeight", "cohWeight"
            }
    );
    public static int totalAmountOfFoxes = 0;                   //total amount of Foxes naturally born

    public static final int MAX_HEALTH = 1000;                  //maximum health for all Foxes
    public static final int STARTING_HEALTH = 500;              //starting health of a Fox
    public static final int MAX_HUNTING_HEALTH = 800;           //above this threshold the animal will stop hunting food
    public static final double[][] HEALTH_REPRODUCTION_BONUS = new double[][]{
            new double[]{MAX_HEALTH*.75, MAX_HEALTH*.5, MAX_HEALTH*.25},    //health threshold at which there is a reproduction bonus
            new double[]{.002,.001,.0005}                                   //bonus to reproduction
    };

    public static final double BASE_REPRODUCTION_CHANCE = 0;    //Base reproduction chance
    public static final double MUTATION_CHANCE = .5;            //Chance for mutation of a Gene

    public static final double DAMAGE = Rabbit.MAX_HEALTH;                    //damage an attack of a Fox does

    public static final double BASE_SIZE = 7;                   //Base size of a Fox
    public Color col = new Color(237, 150, 11, 200);
    public static final double DMG_PER_TICK = 3;                //Damage each Fox takes each tick

    public static final double ENERGY_FACTOR = 100;             //the factor that the eating of a Fox gives
    public static final double BASE_ENERGY_PROVIDED = 0;        //base energy that eating a Fox gives



    //Constructors
    public Fox(Transform transform, float health, DNA dna){
        super(transform, health, dna);
        this.decodeDNA();                                           //initialize DNA

        this.transform.velocity = Vector2D.randLimVec((Math.random()-.5)*5,
                (Math.random()-.5)*5).limit(this.maxSpeed);   //start with a random velocity

        sumDNA.addToAVG(this.sumDNA,totalAmountOfFoxes, this.dna);  //add this DNA to the collection
        totalAmountOfFoxes++;                                       //increase counter
    }
    public Fox(){
        super();
        this.dna = new DNA(11);
        this.decodeDNA();                                           //initialize DNA
        this.health = STARTING_HEALTH;

        this.transform.velocity = Vector2D.randLimVec((Math.random()-.5)*5,
                (Math.random()-.5)*5).limit(this.maxSpeed);   //start with a random velocity

        sumDNA.addToAVG(this.sumDNA,totalAmountOfFoxes, this.dna);  //add this DNA to the collection
        totalAmountOfFoxes++;                                       //increase counter
    }

    /**
     * genes[0] =
     * genes[1] = size
     * genes[2] = maxSpeed
     * genes[3] = maxForce
     * genes[4] = viewDistance
     * genes[5] = desiredSeparationDist
     * genes[6] = desiredAlignmentDist
     * genes[7] = desiredCohesionDist
     * genes[8] = separationWeight
     * genes[9] = alignmentWeight
     * genes[10] = cohesionWeight
     *
     * Decodes the DNA and sets the attributes according to it
     */
    //TODO: check what happens when values here are negative
    @Override
    public void decodeDNA() {
        if(Math.random() <= .5) this.gender = Gender.MALE;
        else this.gender = Gender.FEMALE;

        this.transform.size = this.dna.genes[1]+BASE_SIZE;              //Define size
        this.maxSpeed = this.dna.genes[2];                              //Define maxSpeed
        this.maxForce = this.dna.genes[3];                              //Define maxForce
        this.viewDistance = this.dna.genes[4] * this.transform.size;    //Define viewDistance
        if(this.viewDistance < 0) this.viewDistance = 0;

        //Define separation, alignment, cohesion distances
        this.desiredSepDist = this.dna.genes[5] * this.transform.size;
        this.desiredAliDist = this.dna.genes[6] * this.transform.size;
        this.desiredCohDist = this.dna.genes[7] * this.transform.size;

        //Define separation, alignment, cohesion weights
        this.sepWeight = this.dna.genes[8];
        this.aliWeight = this.dna.genes[9];
        this.cohWeight = this.dna.genes[10];

        assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" + Math.pow(this.maxSpeed,2);
    }

    /**
     * Updates the position of the Fox
     * PRE-CONDITION: this mustn't be dead
     */
    //TODO: an Animal moving slower than maxSpeed should take less tick-DMG
    public void update(){
        assert !this.dead() : "This is dead";

        this.transform.velocity.add(this.transform.acceleration);
        this.transform.velocity.limit(maxSpeed);
        this.transform.location.add(this.transform.velocity);
        this.transform.acceleration.mult(0);

        this.borders2();
        this.health -= DMG_PER_TICK;

        assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" + Math.pow(this.maxSpeed,2);
    }

    /**
     * Searches for possible Prey if the Fox is hungry enough and doesn't already have a target
     * PRE-CONDITION: this mustn't be dead
     * @param organisms that can be hunted
     * @return the Prey
     */
    //TODO: consider health of an animal too, if a Prey is lower health it should get prioritized
    @Override
    public Organism searchFood(ArrayList<Organism> organisms) {
        assert !this.dead() : "This is dead";

        Organism closestFood = null;

        //if there is a target and the Fox is hungry enough to look for food
        if(target != null && this.health <= MAX_HUNTING_HEALTH) {
            this.transform.applyForce(seek(target.getLocation()));          //seek the target
            if (collision(target)) target = searchFood(organisms);          //if the target is dead
        }
        //else look for food
        else{
            double closestDistance = Double.POSITIVE_INFINITY;
            for(Organism o : organisms){
                //TODO: create a Prey variable that holds the class of all huntable / eatable / fightable organisms
                assert o.getClass() == Rabbit.class;                                //check if the target is a Rabbit

                double distance = Vector2D.sub(o.transform.location, this.transform.location).magSq();
                //if the distance is smaller than the current closest distance and smaller than the viewDistance
                if((closestDistance >= distance) && (distance <= Math.pow(this.viewDistance,2))){
                    closestDistance = distance;
                    closestFood = o;
                }
            }
            if(closestFood != null) assert closestFood.getClass() == Rabbit.class;  //check if the target is a Rabbit
            this.target = closestFood;
        }

        assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" + Math.pow(this.maxSpeed,2);
        return closestFood;
    }

    /**
     * This method checks if a Fox collides with his Prey and if so deal damage and gain health if the prey is dead
     * PRE-CONDITION: the Prey needs to be of the correct class, this mustn't be dead
     * @param Prey the target that should be checked for a collision with
     * @return true if the prey is dead
     */
    @Override
    public boolean collision(Organism Prey) {
        //TODO: create a Prey variable that holds the class of all huntable / eatable / fightable organisms
        assert !this.dead() : "This is dead";                                            //check if this is dead
        assert Prey.getClass() == Rabbit.class;                                         //check if the target is a Rabbit

        //check if the two collide
        if(this.transform.getRectangle().intersects(Prey.transform.getRectangle())){
            Prey.takeDamage(DAMAGE);                       //reduce plants health to 0
            this.health += (Prey.transform.size * Rabbit.ENERGY_FACTOR) + Rabbit.BASE_ENERGY_PROVIDED;     //gain health
            if(Prey.dead()) target = null;            //remove target
        }
        /*
        if(this.transform.location.dist(Prey.transform.location) <= this.transform.getR() + Prey.transform.getR()){
            //TODO: maybe make this dependant on attributes of the Fox (size, ect)
            Prey.health -= DAMAGE;                                                      //reduce Preys health by dmg
            //TODO: rework so that once an animal is dead it leaves a corpse that then can be consumed
            //TODO: make damaged animals walk slower for a short period of time
            if(Prey.health <= 0) {                                                      //if the prey is dead
                this.health += (Prey.transform.size * Rabbit.ENERGY_FACTOR) + Rabbit.BASE_ENERGY_PROVIDED;                               //adds health if the rabbit is dead
                target = null;                                                          //remove target
            }
        }
         */


        assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" + Math.pow(this.maxSpeed,2);
        return target == null;                                                          //return true if the prey has been killed
    }

    /**
     * Calculates the Chance to give birth and adds boni according to this Foxes health
     * Then gives birth if the Chance occurs and creates a new Fox
     * PRE-CONDITION: this mustn't be dead
     */
    @Override
    public void reproduce(){
        assert !this.dead() : "This is dead";

        double birthChance = BASE_REPRODUCTION_CHANCE;
        //Adds all Boni that for each threshold that has been met
        for(int i = 0; i < HEALTH_REPRODUCTION_BONUS[0].length; i++){
            if(this.health >= HEALTH_REPRODUCTION_BONUS[0][i]) birthChance += HEALTH_REPRODUCTION_BONUS[1][i];
        }
        if(Math.random() <= birthChance){
            DNA childDNA = dna.copy();                              //copy this DNA
            childDNA.mutate(MUTATION_CHANCE);                       //mutate DNA if MUTATION_CHANCE occurs
            Transform t = this.transform.clone();                   //Copy this transform
            CFrame.Foxes.add(new Fox(t,MAX_HEALTH, childDNA));      //Add a new Fox
        }

        assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" + Math.pow(this.maxSpeed,2);
    }

    //right now there aren't any animals that a fox needs to flee of so this is currently empty
    @Override
    public void flee(ArrayList<Organism> organisms) {
    }

    //right now this isn't implemented
    //TODO: implement growth of an Animal
    @Override
    public void grow() {

    }

    /**
     * Corrects if an Animal has too much health
     * @return if the current speed is bigger than the maxSpeed
     */
    public boolean invariant(){
        if(this.health >= MAX_HEALTH) this.health = MAX_HEALTH;
        return (this.transform.velocity.magSq() <= (this.maxSpeed*this.maxSpeed) + .01) ||
                (this.transform.velocity.magSq() >= (this.maxSpeed*this.maxSpeed) - .01);
    }

    //Visualization
    @Override
    public void paint(Graphics2D g) {
        assert !this.dead() : "This is dead";

        int alpha = 55+(int)Vector2D.map(this.health,0,MAX_HEALTH,0,200);
        assert alpha <= 255 : alpha;

        this.col = new Color(237, 150, 11, alpha);

        g.setColor(this.col);
        g.fill(this.transform.getRectangle());

        assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" + Math.pow(this.maxSpeed,2);
    }
}
