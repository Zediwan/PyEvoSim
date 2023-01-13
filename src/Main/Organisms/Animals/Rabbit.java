package Main.Organisms.Animals;

import Main.CFrame;
import Main.NeuralNetwork.NeuralNetwork;
import Main.Organisms.Attributes.DNA;
import Main.Organisms.Attributes.Gender;
import Main.Helper.Transform;
import Main.Helper.Vector2D;
import Main.Organisms.Organism;
import Main.Organisms.Plants.Grass;
import java.awt.*;
import java.util.ArrayList;
import static Main.CFrame.*;

public class Rabbit extends Animal {
    public static DNA sumDNA = DNA.initiateSumDNA(5,
            new String[]{
            "NA","size", "maxSpeed", "maxForce", "viewDistance",
                    "desiredSepDist", "desiredAliDist", "desiredCohDist",
                    "sepWeight", "aliWeight", "cohWeight", "fleeWeight"
            }
    );
    public static int totalAmountOfRabbits = 0;                 //total amount of Rabbits naturally born

    public static final int MAX_HEALTH = 300;                   //maximum health for all Rabbits
    public static final int STARTING_HEALTH = MAX_HEALTH/2;              //starting health of a Rabbit
    public static final int MAX_HUNTING_HEALTH = MAX_HEALTH;           //above this threshold the Rabbit will stop looking food
    public static final double[][] HEALTH_REPRODUCTION_BONUS = new double[][]{
            new double[]{MAX_HEALTH*.75, MAX_HEALTH*.5, MAX_HEALTH*.25},    //health threshold at which there is a reproduction bonus
            new double[]{.01,.005,.0025}                                    //bonus to reproduction
    };

    public static final double BASE_REPRODUCTION_CHANCE = 0;    //Base reproduction chance
    public static final double MUTATION_CHANCE = .1;            //Chance for mutation of a Gene

    public static final double DAMAGE = 10;                     //damage an attack of a Rabbit does

    public static final double BASE_SIZE = 5;                   //Base size of a Rabbit
    public Color col = new Color(121, 83, 71, 200);
    public static final double DMG_PER_TICK = 5;                //Damage each Rabbit takes each tick

    public static final double ENERGY_FACTOR = 300;             //the factor that the eating of a Rabbit gives
    public static final double BASE_ENERGY_PROVIDED = 100;        //base energy that eating a Rabbit gives

    public static Organism typeOfFood = new Grass();
    public static Organism typeOfHunter = new Fox();

    //Neural Network
    /** Input Node Description
     * 1: (this.x)
     * 2: (this.y)
     * 3: closestPlant.x
     * 4: closestPlant.y
     * 5: closestHunter.x
     * 6: closestHunter.y
     * 7: this.health
     * 8: amount of food in sensory radius
     * 9: amount of hunters in sensory radius
     * 10: this.size
     * 11: distance to closest food
     * 12: distance to closest hunter
     * 13: distance to closest x-Axis border
     * 14: distance to closest y-Axis border
     * 15: distance to centre
     */
    public static final int input_nodes = 13;
    public static final int hidden_nodes = 36;
    public static final int output_nodes = 3;                   //two output nodes with the steer coordinates (x,y)

    //Constructors
    public Rabbit(Transform transform, float health, DNA dna, NeuralNetwork nn){
        super(transform, health, dna);
        this.decodeDNA();                                               //initialize DNA

        sumDNA.addToAVG(this.sumDNA,totalAmountOfRabbits, this.dna);    //add this DNA to the collection
        totalAmountOfRabbits++;                                         //increase counter

        //NN
        this.nn = nn;
    }
    public Rabbit(){
        super();
        this.dna = new DNA(5);
        this.dna.genes[2] += 1;
        this.dna.genes[3] += 1;
        this.dna.genes[4] += 1;
        this.decodeDNA();
        this.health = STARTING_HEALTH;

        sumDNA.addToAVG(this.sumDNA,totalAmountOfRabbits, this.dna);    //add this DNA to the collection
        totalAmountOfRabbits++;                                         //increase counter

        //NN
        this.nn = new NeuralNetwork(this.input_nodes, this.hidden_nodes,this.output_nodes);
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
        if(this.maxSpeed < 0) this.maxSpeed = 0;

        this.maxForce = this.dna.genes[3];                              //Define maxForce
        if(this.maxForce < 0) this.maxForce = 0;

        this.viewDistance = this.dna.genes[4] * this.transform.size;    //Define viewDistance
        if(this.viewDistance < 0) this.viewDistance = 0;

        /*
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
         */
    }

    /**
     * Updates the position of the Rabbit
     * PRE-CONDITION: this mustn't be dead
     */
    //TODO: an Animal moving slower than maxSpeed should take less tick-DMG
    public void update(){
        assert !this.dead() : "This is dead";

        this.think();

        this.transform.velocity.add(this.transform.acceleration);
        this.transform.velocity.limit(maxSpeed);
        this.transform.location.add(this.transform.velocity);
        this.transform.acceleration.mult(0);

        if(this.target != null) this.collision(this.target);

        this.reproduce();

        //TODO: remove and add an input to the NN with the closest border distance
        //this.borders2();
        this.health -= DMG_PER_TICK;

        assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" + Math.pow(this.maxSpeed,2);
    }

    public void think(){
        //search the closest Food
        ArrayList foods = CFrame.getGridFields(this.transform.location, pGrid);
        Organism closestFood = this.searchFood(foods);

        //TODO: think of a better solution / placeholder when there is no food in sensory radius
        Vector2D closestFoodPosition = new Vector2D();      //if there is no food in sensory radius just return the null vector
        double distanceClosestFood = 0;                     //if there is no food set distance to 0

        if (closestFood != null)  {
            closestFoodPosition = Vector2D.sub(closestFood.transform.location,this.transform.location); //put the vector in relation to the position
            distanceClosestFood = closestFoodPosition.mag();
        }

        //search the closest Food
        ArrayList hunters = CFrame.getGridFields(this.transform.location, fGrid);
        Organism closestHunter = this.searchHunter(hunters);

        //TODO: think of a better solution / placeholder when there is no hunter in sensory radius
        Vector2D closestHunterPosition = new Vector2D();    //if there is no hunter in sensory radius just return the null vector
        double distanceClosestHunter = 0;                   //if there is no hunter distance is 0

        if (closestHunter != null)  {
            closestHunterPosition = Vector2D.sub(closestHunter.transform.location,this.transform.location); //put the vector in relation to the position
            distanceClosestHunter = closestHunterPosition.mag();
        }

        //calculate distance to borders
        //calculate closest x Border
        double distanceXB = Double.POSITIVE_INFINITY;
        if(this.transform.location.x >= WIDTH/2) distanceXB = WIDTH-this.transform.location.x;
        else distanceXB = this.transform.location.x;
        //calculate closest y Border
        double distanceYB = Double.POSITIVE_INFINITY;
        if(this.transform.location.y >= HEIGHT/2) distanceXB = HEIGHT-this.transform.location.y;
        else distanceXB = this.transform.location.y;


        //set inputs
        double[] inputs = new double[]{
                //this.transform.getLocX(), this.transform.getLocY(),
                closestFoodPosition.x, closestFoodPosition.y,
                closestHunterPosition.x, closestHunterPosition.y,
                this.health,
                foods.size(),
                hunters.size(),
                this.transform.size,
                distanceClosestFood,
                distanceClosestHunter,
                distanceXB,distanceYB,
                Vector2D.sub(this.transform.location, new Vector2D(WIDTH,HEIGHT)).mag()
        };
        double[] outputs = this.nn.predict(inputs);
        this.transform.applyForce(new Vector2D(outputs[0]-.5, outputs[1]-.5).setMag(outputs[2]*this.maxForce).limit(this.maxForce));
    }

    /**
     * Searches for possible Food
     * PRE-CONDITION: this mustn't be dead
     * @param organisms that can be eaten
     * @return the Food
     */
    //TODO: consider health of an animal too, if a Prey is lower health it should get prioritized
    @Override
    public Organism searchFood(ArrayList<Organism> organisms) {
        assert !this.dead() : "This is dead";

        Organism closestFood = null;
        double closestDistance = Double.POSITIVE_INFINITY;
        for(Organism o : organisms){
            assert o.getClass() == typeOfFood.getClass();         //check if the target is possible food

            double distance = Vector2D.sub(o.transform.location, this.transform.location).magSq();
            //if the distance is smaller than the current closest distance and smaller than the viewDistance
            if((closestDistance >= distance) && (distance <= Math.pow(this.viewDistance,2))){
                closestDistance = distance;
                closestFood = o;
            }
        }
        this.target = closestFood;

        assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" + Math.pow(this.maxSpeed,2);
        return closestFood;
    }
    public Organism searchHunter(ArrayList<Organism> hunters) {
        assert !this.dead() : "This is dead";

        Organism closestHunter = null;
        double closestDistance = Double.POSITIVE_INFINITY;
        for(Organism o : hunters){
            assert o.getClass() == typeOfHunter.getClass();             //check if the organism is a possible hunter

            double distance = Vector2D.sub(o.transform.location, this.transform.location).magSq();
            //if the distance is smaller than the current closest distance and smaller than the viewDistance
            if((closestDistance >= distance) && (distance <= Math.pow(this.viewDistance,2))){
                closestDistance = distance;
                closestHunter = o;
            }
        }

        assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" + Math.pow(this.maxSpeed,2);
        return closestHunter;
    }

    /**
     * This method checks if a Rabbit collides with his target and if so deal damage and gain health
     * PRE-CONDITION: the target needs to be of the correct class, this mustn't be dead
     * @param food the target that should be checked for a collision with
     * @return true if the target is consumed
     */
    @Override
    public boolean collision(Organism food) {
        assert !this.dead() : "This is dead";               //check if this is dead
        assert food.getClass() == typeOfFood.getClass();   //check if the target is eatable

        //check if the two collide
        if(this.transform.location.dist(food.transform.location) <= this.transform.getR() + food.transform.getR()){
            //TODO: maybe make this dependant on attributes of the Rabbit (size, ect)
            food.takeDamage(DAMAGE);                     //reduce plants health to 0
            this.health += (food.transform.size * Grass.ENERGY_FACTOR) + Grass.BASE_ENERGY_PROVIDED;     //gain health
            if(food.dead()){
                target = null;            //remove target
            }
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
            //DNA
            DNA childDNA = dna.copy();                              //copy this DNA
            childDNA.mutate(MUTATION_CHANCE);                       //mutate DNA if MUTATION_CHANCE occurs

            //NN
            NeuralNetwork childNN = this.nn.copy();
            //if(Math.random() <= MUTATION_CHANCE*)
            childNN.mutate();

            Transform t = this.transform.clone();                           //Copy this transform
            Rabbit child = new Rabbit(t,MAX_HEALTH, childDNA,childNN);
            CFrame.Rabbits.add(child); //Add a new Rabbit
            CFrame.currentTrackedR = child;
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
