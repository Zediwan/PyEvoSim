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

import static Main.CFrame.Foxes;
import static Main.CFrame.Rabbits;

public class Rabbit extends Animal {
    public static DNA sumDNA = DNA.initiateSumDNA(12,
            new String[]{
            "NA","size", "maxSpeed", "maxForce", "viewDistance",
                    "desiredSepDist", "desiredAliDist", "desiredCohDist",
                    "sepWeight", "aliWeight", "cohWeight", "fleeWeight"
            }
    );
    public static int totalAmountOfRabbits = 0;                 //total amount of Rabbits naturally born

    public static final int MAX_HEALTH = 300;                   //maximum health for all Rabbits
    public static final int STARTING_HEALTH = 150;              //starting health of a Rabbit
    public static final int MAX_HUNTING_HEALTH = 250;           //above this threshold the Rabbit will stop looking food
    public static final double[][] HEALTH_REPRODUCTION_BONUS = new double[][]{
            new double[]{MAX_HEALTH*.75, MAX_HEALTH*.5, MAX_HEALTH*.25},    //health threshold at which there is a reproduction bonus
            new double[]{.01,.005,.0025}                                    //bonus to reproduction
    };

    public static final double BASE_REPRODUCTION_CHANCE = 0;    //Base reproduction chance
    public static final double MUTATION_CHANCE = .1;            //Chance for mutation of a Gene

    public static final double DAMAGE = 10;                     //damage an attack of a Rabbit does

    public static final double BASE_SIZE = 2;                   //Base size of a Rabbit
    public Color col = new Color(121, 83, 71, 200);
    public static final double DMG_PER_TICK = 5;                //Damage each Fox takes each tick

    public static final double ENERGY_FACTOR = 100;             //the factor that the eating of a Rabbit gives
    public static final double BASE_ENERGY_PROVIDED = 0;        //base energy that eating a Rabbit gives

    //Constructors
    public Rabbit(Transform transform, float health, DNA dna){
        super(transform, health, dna);
        this.decodeDNA();                                               //initialize DNA

        this.transform.velocity = Vector2D.randLimVec((Math.random()-.5)*5,
                (Math.random()-.5)*5).limit(this.maxSpeed);       //start with a random velocity

        sumDNA.addToAVG(this.sumDNA,totalAmountOfRabbits, this.dna);    //add this DNA to the collection
        totalAmountOfRabbits++;                                         //increase counter
    }
    public Rabbit(){
        super();
        this.dna = new DNA(12);
        this.decodeDNA();

        this.health = STARTING_HEALTH;
        this.transform.velocity = Vector2D.randLimVec((Math.random()-.5)*5,
                (Math.random()-.5)*5).limit(this.maxSpeed);        //start with a random velocity
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
     * genes[11] = fleeWeight
     *
     * Decodes the DNA and sets the attributes according to it
     */
    //TODO: check what happens when values here are negative
    @Override
    public void decodeDNA() {
        if(Math.random() <= .5) this.gender = Gender.MALE;
        else this.gender = Gender.FEMALE;

        this.transform.size = this.dna.genes[1] + BASE_SIZE;            //Define size
        this.maxSpeed = this.dna.genes[2];                              //Define maxSpeed
        this.maxForce = this.dna.genes[3];                              //Define maxForce
        this.viewDistance = this.dna.genes[4] + this.transform.size;    //Define viewDistance

        //Define separation, alignment, cohesion distances
        this.desiredSepDist = this.dna.genes[5] * this.transform.size;
        this.desiredAliDist = this.dna.genes[6] * this.transform.size;
        this.desiredCohDist = this.dna.genes[7] * this.transform.size;

        //Define separation, alignment, cohesion weights
        this.sepWeight = this.dna.genes[8];
        this.aliWeight = this.dna.genes[9];
        //newborn rabbits stick together more when they're outnumbered by foxes
        if(Rabbits.size() <= 0){
            this.cohWeight = this.dna.genes[10];
        }else{
        this.cohWeight = this.dna.genes[10] * Math.sqrt(10*Foxes.size()/ Rabbits.size());}
        this.fleeWeight = this.dna.genes[11];                           //Define flee weight
    }

    /**
     * Updates the position of the Rabbit
     * PRE-CONDITION: this mustn't be dead
     */
    //TODO: an Animal moving slower than maxSpeed should take less tick-DMG
    public void update(){
        assert !this.dead() : "This is dead";

        this.transform.velocity.add(this.transform.acceleration);
        this.transform.velocity.limit(maxSpeed);
        this.transform.location.add(this.transform.velocity);
        this.transform.acceleration.mult(0);

        this.borders1();
        this.health -= DMG_PER_TICK;

        assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" + Math.pow(this.maxSpeed,2);
    }

    /**
     * Searches for possible Food if the Rabbit is hungry enough and doesn't already have a target
     * PRE-CONDITION: this mustn't be dead
     * @param organisms that can be eaten
     * @return the Food
     */
    //TODO: consider health of an animal too, if a Prey is lower health it should get prioritized
    @Override
    public Organism searchFood(ArrayList<Organism> organisms) {
        assert !this.dead() : "This is dead";

        Organism closestFood = null;

        //if there is a target and the Rabbit is hungry enough to look for food
        if(target != null && this.health <= MAX_HUNTING_HEALTH) {
            this.transform.applyForce(seek(target.getLocation()));
            if (collision(target)) target = searchFood(organisms);
        }
        //else look for food
        else{
            double closestDistance = Double.POSITIVE_INFINITY;
            for(Organism o : organisms){
                //TODO: create a Prey variable that holds the class of all huntable / eatable / fightable organisms
                assert o.getClass() == Grass.class;             //check if the target is a Grass

                double distance = Vector2D.sub(o.transform.location, this.transform.location).magSq();                //if the distance is smaller than the current closest distance and smaller than the viewDistance
                //if the distance is smaller than the current closest distance and smaller than the viewDistance
                if((closestDistance >= distance) && (distance <= Math.pow(this.viewDistance,2))){
                    closestDistance = distance;
                    closestFood = o;
                }
            }
            if(closestFood != null) assert closestFood.getClass() == Grass.class;   //check if the target is a Grass
            this.target = closestFood;
        }

        assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" + Math.pow(this.maxSpeed,2);
        return closestFood;
    }

    /**
     * This method checks if a Rabbit collides with his target and if so deal damage and gain health
     * PRE-CONDITION: the target needs to be of the correct class, this mustn't be dead
     * @param grass the target that should be checked for a collision with
     * @return true if the target is consumed
     */
    @Override
    public boolean collision(Organism grass) {
        //TODO: create a Prey variable that holds the class of all huntable / eatable / fightable organisms
        assert !this.dead() : "This is dead";                //check if this is dead
        assert grass.getClass() == Grass.class;            //check if the target is a Rabbit

        //check if the two collide
        if(this.transform.location.dist(grass.transform.location) <= this.transform.getR() + grass.transform.getR()){
            //TODO: maybe make this dependant on attributes of the Fox (size, ect)
            grass.health -= DAMAGE;                         //reduce plants health to 0
            this.health += (grass.transform.size * Grass.ENERGY_FACTOR) + Grass.BASE_ENERGY_PROVIDED;     //gain health
            if(grass.health <= 0) target = null;            //remove target
        }

        assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" + Math.pow(this.maxSpeed,2);
        return target == null;
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
            CFrame.Rabbits.add(new Rabbit(t,MAX_HEALTH, childDNA)); //Add a new Rabbit
        }

        assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" + Math.pow(this.maxSpeed,2);
    }

    /**
     * Calculates the fleeing force
     * PRE-CONDITION: this mustn't be dead
     * @param organisms that the Animal should consider fleeing from
     */
    public void flee(ArrayList<Organism> organisms) {
        assert !this.dead() : "This is dead";

        Vector2D sum = new Vector2D();
        Vector2D steer = new Vector2D();
        int count = 0;                              //of animals scaring the rabbit

        for (Organism o : organisms) {
            //TODO: create a Hunter variable that holds the class of all organisms this has to be afraid of
            assert o.getClass() == Fox.class;                                       //assert this is fleeing from a Fox
            double distance = Vector2D.dist(this.getLocation(), o.getLocation());   //calculate distance of the two animals
            //here check distance > 0 to avoid an animal fleeing from itself
            if ((distance > 0) && (distance < this.viewDistance)) {
                Vector2D difference = Vector2D.sub(this.getLocation(), o.getLocation());
                difference.normalize();
                difference.div(distance);           //the closer an animal the more we should flee
                sum.add(difference);                //add all the vectors together
                count++;                            //increment count
            }
        }
        //avoid division by zero
        if (count > 0) {
            sum.div(count);                         //get the average vector
            sum.setMag(this.maxSpeed);              //set its magnitude to maxSpeed
            steer = Vector2D.sub(sum, this.transform.getVelocity());
            steer.limit(this.maxForce);
        }
        steer.mult(this.fleeWeight);
        this.transform.applyForce(steer);

        assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" + Math.pow(this.maxSpeed,2);
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

        this.col = new Color(121, 83, 71,55+(int)Vector2D.map(this.health,0,MAX_HEALTH,0,200));

        g.setColor(this.col);
        g.fill(this.transform.getRectangle());

        assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" + Math.pow(this.maxSpeed,2);
    }
}
