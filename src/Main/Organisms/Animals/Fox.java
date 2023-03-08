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

import static Main.CFrame.*;
import static Main.CFrame.HEIGHT;

public class Fox extends Animal {
    //TODO: maybe make food view distance and hunter viewDistance different?
    //Summary
    public static DNA sumDNA = DNA.initiateSumDNA(4,
            new String[]{
            "size", "maxSpeed", "maxForce", "viewDistance"
            }
    );
    public static int totalAmount = 0;                      //total amount of Foxes ever born
    public static double totalAvgAge = 0;                     //total avg age

    //Physical attributes
    public Color col = new Color(237, 150, 11, 200);    //Standard color
    public static final double BASE_SIZE = 5;                       //Base size
    public static double baseMaxSpeed = 1;                  //Base max speed
    public static double baseMaxForce = 1;                  //Base max force
    public static final double BASE_VIEW_DISTANCE_FACTOR = 10;       //Base view Distance

    //Health
    public static final double MAX_HEALTH = 180 * scale;                      //maximum health for all Foxes
    public static final double STARTING_HEALTH = MAX_HEALTH / 2;       //starting health of a Fox
    public static final double MAX_HUNTING_HEALTH = (MAX_HEALTH * 2)/3;//above this threshold the animal will stop hunting food
    public static final double DMG_PER_TICK = .2 * scale;                    //Damage each Fox takes each tick

    //Reproduction
    /** Holds the health amounts and the according reproduction bonuses gained by them (being added up) */
    //TODO: make this a new class
    public static final double[][] HEALTH_REPRODUCTION_BONUS = new double[][]{
            new double[]{MAX_HEALTH*.75, MAX_HEALTH*.5, MAX_HEALTH*.25},    //health threshold at which there is a reproduction bonus
            new double[]{.009,.0005,.00025}                                   //bonus to reproduction
    };
    public static final double BASE_REPRODUCTION_CHANCE = .00001;        //Base reproduction chance
    public static final double DNA_MUTATION_CHANCE = .5;            //Chance for mutation of a Gene
    public static double DNA_MUTATION_RANGE = 2;
    public static double DNA_STARTING_MUTATION_RANGE = .5;
    public static double NN_MUTATION_RANGE = .1;
    public static final double NN_MUTATION_CHANCE = .5;            //Chance for the whole NN to mutate

    //Hunting
    public static final double DAMAGE = Rabbit.MAX_HEALTH/4;        //damage an attack of a Fox does
    //TODO: transform this into a list to allow multiple food types
    public static Organism typeOfFood = new Rabbit();               //eatable Organisms

    //Nutrition
    //TODO: transform into a list to allow multiple hunters
    public static Organism typeOfHunter = null;                     //animals this is hunted by
    public static final double ENERGY_FACTOR = 100;                 //the factor that the eating of a Fox gives
    public static final double BASE_ENERGY_PROVIDED = 0;            //base energy that eating a Fox gives

    //Neural Network
    //TODO: reorder
    /** Input Node Description
     * In relation to this position:
     * closestRabbit.x
     * closestRabbit.y
     * -------------------------------------
     * this.health
     * amount of food in sensory radius
     * amount of other foxes in sensory radius
     * this.size
     * distance to closest food
     * distance to closest x-Axis border
     * distance to closest y-Axis border
     * distance to centre
     */
    public static final int input_nodes = 8;
    public static final int hidden_nodes = 40;
    /**
     * Output Node Description
     * 1: x coodrinate steer
     * 2: y coordinate steer
     * 3: strength of steer
     */
    public static final int output_nodes = 3;

    //Constructors
    //this is being used when a fox is born by its parent
    public Fox(Transform transform, double health, DNA dna, NeuralNetwork nn){
        super(transform, health, dna);
        this.expressGenes();                                       //initialize DNA

        //start with a random velocity
        this.transform.velocity = Vector2D.randLimVec((Math.random()-.5),
                (Math.random()-.5)).setMag(this.maxSpeed);

        sumDNA.addToAVG(this.sumDNA, totalAmount, this.dna);    //add this DNA to the collection
        totalAmount++;                                          //increase counter

        //NN
        this.nn = nn;
    }
    //this is being used for repopulation by the system
    //TODO: maybe refactor this to just take in a parent?
    public Fox(){
        super();
        this.dna = new DNA(4, DNA_STARTING_MUTATION_RANGE);
        this.dna.genes[0] += BASE_SIZE;
        this.dna.genes[1] += baseMaxSpeed;
        this.dna.genes[2] += baseMaxForce;
        this.dna.genes[3] += BASE_VIEW_DISTANCE_FACTOR;
        this.expressGenes();                                       //initialize DNA

        this.health = STARTING_HEALTH;                          //set starting health

        //start with a random velocity
        this.transform.velocity = Vector2D.randLimVec((Math.random()-.5),
                (Math.random()-.5)).setMag(this.maxSpeed);

        sumDNA.addToAVG(this.sumDNA, totalAmount, this.dna);    //add this DNA to the collection
        totalAmount++;                                          //increase counter

        //NN
        this.nn = new NeuralNetwork(this.input_nodes, this.hidden_nodes,this.output_nodes);
    }

    /**
     * Gene order:
     * size
     * maxSpeed
     * maxForce
     * viewDistance
     *
     * Decodes the DNA and sets the attributes according to it.
     * If any values are below 0 they will just be put to 0
     */
    //TODO: check what happens when values here are negative
    @Override
    public void expressGenes() {
        if(Math.random() <= .5) this.gender = Gender.MALE;              //Define Gender
        else this.gender = Gender.FEMALE;

        this.transform.size = this.dna.genes[0];                        //Define size
        this.desiredSepDist = this.transform.size;

        this.maxSpeed = this.dna.genes[1];                              //Define maxSpeed
        if(this.maxSpeed < 0) this.maxSpeed = 0;

        this.maxForce = this.dna.genes[2];                              //Define maxForce
        if(this.maxForce < 0) this.maxForce = 0;

        this.viewDistance = this.dna.genes[3] * this.transform.size;    //Define viewDistance
        if(this.viewDistance < 0) this.viewDistance = 0;

        assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" + Math.pow(this.maxSpeed,2);
    }

    /**
     * Updates the position of the Fox
     * PRE-CONDITION: this mustn't be dead
     */
    //TODO: an Animal moving slower than maxSpeed should take less tick-DMG
    public void update(){
        assert !this.isDead() : "This is dead";

        this.think();                                           //make a decision where to move (by the NN)
        this.transform.applyForce(this.separate(CFrame.getGridFields(this.getLocation(), fGrid)));


        //Movement
        //TODO: maybe refactor this?
        this.transform.velocity.add(this.transform.acceleration);
        this.transform.velocity.limit(maxSpeed);
        this.transform.location.add(this.transform.velocity);
        this.transform.acceleration.mult(0);

        if(this.target != null) this.collision(this.target);    //if this is chasing something then check for collision

        this.reproduce();                                       //handle reproduction if necessary

        //TODO: check if the rabbits can learn when to move back to not die in the no mans land and if so then remove this
        //this.borders2();

        this.health -= DMG_PER_TICK;                            //take damage

        assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" + Math.pow(this.maxSpeed,2);
    }

    public void think(){
        //search the closest Food
        //TODO: maybe refactor the two search parts?
        ArrayList foods = CFrame.getGridFields(this.transform.location, rGrid);     //get all food in view Distance
        Organism closestFood = this.searchClosestOrganism(foods,typeOfFood);        //choose the closest if any
        //TODO: think of a better solution / placeholder when there is no food in sensory radius
        Vector2D closestFoodPosition = new Vector2D();      //if there is no food in sensory radius just return the null vector
        double distanceClosestFood = 0;                     //if there is no food set distance to 0
        if (closestFood != null)  {
            //TODO: check if this calculates the right thing
            this.target = closestFood;
            closestFoodPosition = Vector2D.sub(closestFood.transform.location,this.transform.location); //put the vector in relation to the position
            distanceClosestFood = closestFoodPosition.mag();
        }

        //Get the amount of foxes around this
        ArrayList foxes = CFrame.getGridFields(this.transform.location, fGrid);   //get all foxes in viewDistance



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
                closestFoodPosition.x, closestFoodPosition.y,
                this.health,
                foods.size(),
                foxes.size(),
                this.transform.size,
                distanceClosestFood,
                //distanceXB,distanceYB,
                this.transform.location.distSq(new Vector2D(WIDTH,HEIGHT))
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
    //TODO: check if these methods cannot be refactored
    @Override
    public Organism searchFood(ArrayList<Organism> organisms) {
        assert !this.isDead() : "This is dead";

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
     * Searches for the closest organism of a specified type
     * PRE-CONDITION: this mustn't be dead
     * @param organisms that should be considered
     * @return the closest of those organisms
     */
    //TODO: consider health of an animal too, if a Prey is lower health it should get prioritized
    public Organism searchClosestOrganism(ArrayList<Organism> organisms, Organism typeOfOrganism){
        assert !this.isDead() : "This is dead";

        Organism closestOrganism = null;
        double closestDistance = Double.POSITIVE_INFINITY;

        //calculate the closest organism
        for(Organism o : organisms){
            assert o.getClass() == typeOfOrganism.getClass(); //check if the organism is the correct type of organism

            double distance = this.transform.location.distSq(o.transform.location);
            //if the distance is smaller than the current closest distance and smaller than the viewDistance
            if((closestDistance >= distance) && (distance <= Math.pow(this.viewDistance,2))){
                closestDistance = distance;
                closestOrganism = o;
            }
        }

        assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" + Math.pow(this.maxSpeed,2);
        return closestOrganism;
    }

    /**
     * This method checks if a Rabbit collides with his target and if so deal damage and gain health
     * PRE-CONDITION: the target needs to be of the correct class, this mustn't be dead
     * @param food the target that should be checked for a collision with
     * @return true if the target is consumed
     */
    //TODO: check if this really only returns true if the target is dead
    @Override
    public boolean collision(Organism food) {
        assert !this.isDead() : "This is dead";           //check if this is dead
        assert food.getClass() == typeOfFood.getClass();//check if the target is eatable

        //check if the two collide
        if(this.transform.location.distSq(food.transform.location) <= Math.pow(this.transform.getR() + food.transform.getR(), 2)){
            //TODO: maybe make the damage dependant on attributes of the Fox (size, ect)
            food.takeDamage(DAMAGE);                    //reduce plants health to 0
            //remove target if it is dead
            if(food.isDead()){
                this.health += (food.transform.size * Rabbit.ENERGY_FACTOR) + Rabbit.BASE_ENERGY_PROVIDED;     //gain health
                target = null;
            }
        }

        assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" + Math.pow(this.maxSpeed,2);
        return target == null;
    }

    /**
     * Calculates the chance to give birth according to bonuses gained in relation to it's health
     * Then gives birth if the chance occurs and creates a new Child
     * PRE-CONDITION: this mustn't be dead
     */
    @Override
    public void reproduce(){
        assert !this.isDead() : "This is dead";

        double birthChance = BASE_REPRODUCTION_CHANCE;
        //Adds all bonuses that for each threshold that has been met
        //TODO: refactor this by making it a separate data class
        for(int i = 0; i < HEALTH_REPRODUCTION_BONUS[0].length; i++){
            if(this.health >= HEALTH_REPRODUCTION_BONUS[0][i]) birthChance += HEALTH_REPRODUCTION_BONUS[1][i];
        }

        //if chance occurs give birth and mutate
        //TODO: maybe make this a separate method? (refactor)
        if(Math.random() <= birthChance){
            //DNA
            DNA childDNA = dna.copy();                                  //copy this DNA
            childDNA.mutate(DNA_MUTATION_CHANCE, DNA_MUTATION_RANGE);       //mutate DNA if chance occurs

            //NN
            NeuralNetwork childNN = this.nn.copy();                     //copy this NN
            //if(Math.random() <= NN_MUTATION_CHANCE) childNN.mutate(NN_MUTATION_RANGE);   //mutate NN if chance occurs
            childNN.mutate(NN_MUTATION_RANGE,NN_MUTATION_CHANCE);       //mutate NN if chance occurs


            Transform t = this.transform.clone();                       //Copy this transform
            Fox child = new Fox(t,STARTING_HEALTH, childDNA,childNN);        //Create child
            Foxes.add(child);                                           //Add a new organism
            CFrame.currentTrackedF = child;                             //make this the tracked organism
        }

        assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" + Math.pow(this.maxSpeed,2);
    }

    //right now there aren't any animals that a fox needs to flee of so this is currently empty
    @Override
    public void flee(ArrayList<Organism> organisms) {
    }

    //TODO: implement growth of an Animal
    @Override
    public void grow() {

    }

    /**
     * Corrects if this has too much health
     * @return if the current speed is bigger than the maxSpeed
     */
    //TODO: maybe refactor the assertion in here
    public boolean invariant(){
        if(this.health >= MAX_HEALTH) this.health = MAX_HEALTH;
        //margins for rounding error
        return (this.transform.velocity.magSq() <= (this.maxSpeed*this.maxSpeed) + .01) ||
                (this.transform.velocity.magSq() >= (this.maxSpeed*this.maxSpeed) - .01);
    }

    //Visualization
    @Override
    public void paint(Graphics2D g) {
        assert !this.isDead() : "This is dead";

        //set opacity according to the health of this
        int alpha = 55+(int)Vector2D.map(this.health,0,MAX_HEALTH,0,200);
        assert alpha <= 255 : alpha;
        this.col = new Color(237, 150, 11, alpha);

        g.setColor(this.col);
        //TODO: implement proper shape
        g.fill(this.transform.getRectangle());

        assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" + Math.pow(this.maxSpeed,2);
    }
}
