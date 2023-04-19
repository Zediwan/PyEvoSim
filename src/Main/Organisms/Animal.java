package Main.Organisms;

import Main.GUI.SimulationGUI;
import Main.Helper.Transform;
import Main.Helper.Vector2D;
import Main.NeuralNetwork.NeuralNetwork;
import Main.Organisms.Attributes.DNA.DNA;
import Main.Organisms.Attributes.DNA.Gene;
import Main.Organisms.Attributes.DNA.GeneType;
import Main.Organisms.Attributes.Gender;
import Main.World.Simulation;
import Main.World.World;

import java.awt.*;
import java.awt.geom.AffineTransform;
import java.awt.geom.Arc2D;
import java.awt.geom.Ellipse2D;
import java.util.ArrayList;
import java.util.Timer;
import java.util.TimerTask;

//TODO create tests for all the methods
//TODO write class documentation
public class Animal extends Organism {
    /**
     * All time amount of animals
     */
    public static long aniCount = 0;
    /**
     * All time amount of animals born by other animals ((re-)population by system not included)
     */
    public static long aniBornCount = 0;

    /**
     * The blueprint for all animals spawned by the simulation
     * @see #blueprint()
     */
    private static Animal blueprint;

    //------------------------------------------------Statistics for simulation----------------------------------------
    public static double avgAge = 0;
    public static double avgAniKilled = 0;
    public static double avgPlaKilled = 0;
    public static double avgOffspringBirthed = 0;
    public static double avgMaxHealth = 0;
    public static double avgHealth = 0;
    public static double avgHealthRatio = 0;
    public static double avgMaxEnergy = 0;
    public static double avgEnergy = 0;
    public static double avgEnergyRatio = 0;

    //------------------------------------------------Simulation Setting Variables-------------------------------------
    public static double baseExhaustDmg = 1;
    public static double baseSize = 3;
    public static double allMaxSpeed = 4;
    public static double healthBodyRatio = 2;
    public static double bodyEnergyRatio = 3;
    public static double herdingThreshold = .5;
    public static double matingThreshold = .5;
    public static double eatingThreshold = .5;
    public static double growthThreshold = .5;
    public static double healingThreshold = .5;
    public static double attackThreshold = .5;
    public static double minHealthToReproduce = .5;
    public static double minMaturityToReproduce = .5;
    public static double reproductiveUrgeFactor = 50;
    public static double damageFactor = 4;
    public static double healingFactor = 2;
    public static double healingCostFactor = 2;
    public static double metabolismFactor = 3;
    //private static double baseSize = 1;

    private static double visualDirScale = 20;
    private static double visualAccScale = 10;

    //-----------------------------------------------------------------------------------------------------------------

    //TODO how should generations be handled when there are two parents?
    /**
     * The generation of an animal is equal the higher generation of its parents +1
     * @see #Animal(Animal, Animal)
     */
    protected int generation = 0;
    protected Gender gender;

    /**
     * flag to track if an animal is already pregnant
     * @see #reproduce(Simulation)
     */
    protected boolean isPregnant = false;
    /**
     * to keep track of the animal this has mated with
     * @see #reproduce(Simulation)
     */
    protected Animal mate;
    /**
     * Brain of this
     */
    protected NeuralNetwork nn;

    //TODO think if this is really needed or can be passed on through the methods
    protected double reproductiveUrge = 0;

    //------------------------------------------------DNA Variables----------------------------------------------------

    /**
     * Animal Gene number 0
     * <p>
     * TODO this may not be needed
     */
    protected double speedRatio;
    /**
     * Animal Gene number 1
     * <p> Represents the strength of this, this is used for fighting and defending </p>
     * <p> Positive value </p>
     * TODO: make this depend on size, via a ration or something
     */
    protected double strength;
    /**
     * Animal Gene number 2
     * <p> How long, in seconds, pregnancy takes,
     * the longer this period ist he more mature / developed an animal is at birth </p>
     * <p> Positive value </p>
     */
    protected long gestationDuration;
    /**
     * Animal Gene number 3
     * <p> The maximum steering force of this </p>
     * <p> Positive value </p>
     * TODO: make this depend on size, via a ration or something
     */
    protected double maxForce;
    /**
     * Animal Gene number 4
     * <p> The maximum speed of this </p>
     * <p> Positive value </p>
     */
    protected double maxSpeed;
    /**
     * Animal Gene number 5
     * <p> The view angle from heading direction </p>
     * <p> Value between 0 and 180 </p>
     * TODO implement
     */
    protected double viewAngle;
    /**
     * Animal Gene number 6
     * <p> How far this can see </p>
     * <p> Positive value</p>
     */
    protected double viewDistance;
    /**
     * Animal Gene number 7
     * <p> The seconds at which the inner timer runs </p>
     * <p> Positive value </p>
     * TODO implement in thinking
     */
    protected double timerFrequency;
    /**
     * Animal Gene number 8
     * <p> How sensible this is to pheromones </p>
     * TODO implement pheromones
     */
    protected double pheromoneSensibility;
    /**
     * Animal Gene number 9
     * <p> How much the separation vector is scaled by </p>
     */
    protected double separationWeight;
    /**
     * Animal Gene number 10
     * <p> How much the alignment vector is scaled by </p>
     */
    protected double alignmentWeight;
    /**
     * Animal Gene number 11
     * <p> How much the cohesion vector is scaled by </p>
     */
    protected double cohesionWeight;
    /**
     * Animal Gene number 12
     * <p> ? </p>
     * TODO check if this is needed
     */
    protected double velocityWeight;
    /**
     * Animal Gene number 13
     * <p> At what distance this want's to separate from others </p>
     * <p> Positive Value </p>
     */
    protected double separationDistance;

    /**
     * used as a shift value when expressing genes of children classes
     */
    protected static int numberAnimalGenes = 14;

    //-----------------------------------------------------------------------------------------------------------------

    /**
     * Creates a new Animal object by crossing over the genes and neural network of the father and mother.
     * The resulting animal has a mutated combination of the father's and mother's DNA and neural network.
     * The animal's ID, generation, and maturity are set based on the father and mother's properties.
     *
     * @param father The Animal object representing the father of the new animal
     * @param mother The Animal object representing the mother of the new animal
     * @throws AssertionError if father is female or mother is male (if they are not the same animal)
     */
    public Animal(Animal father, Animal mother){
        super(father,mother);

        if(father.id != mother.id){
            assert father.gender == Gender.MALE : "father is wrong gender";
            assert mother.gender == Gender.FEMALE : "mother is wrong gender";
        }
        this.dna = DNA.crossover(father.getDna(), mother.getDna());
        //mutate by the mother's gene values
        this.dna.percentageMutate(mother.getMutProbDNA(), mother.getMutSizeDNA());

        this.nn = NeuralNetwork.crossover(father.getNn(), mother.getNn());
        //mutate by the mother's gene values
        this.nn.rangedMutate(mother.getMutProbNN(), mother.getMutSizeNN());

        Animal.aniCount++;
        this.id = Animal.aniCount;

        //calculate this generation
        this.generation += Math.max(father.generation,mother.generation) + 1;

        //calculate maturity of this
        //TODO think about this function
        this.maturity = (mother.gestationDuration / (6*1000.0));
        //this.maturity = 1;

        this.health *= Animal.minHealthToReproduce * .9;

        this.expressGenes();
    }

    /**
     * Creates a new Animal instance with genetic material from a single ancestor.
     *
     * @param ancestor of this animal
     * @see #Animal(Animal, Animal)
     */
    public Animal(Animal ancestor) {
        this(ancestor,ancestor);
    }

    /**
     * Create a new Animal from the blueprint Animal
     * <p>
     *     Used for (re-)population of the simulation
     * </p>
     *
     * @see #blueprint()
     */
    public Animal(){
        this(Animal.blueprint());
    }

    /**
     * Constructs a new animal with the given Transform and DNA.
     *
     * @param transform of this animal
     * @param dna of this animal
     * @param nn brain of this animal
     */
    public Animal(Transform transform, DNA dna, NeuralNetwork nn){
        super(transform,dna);

        Animal.aniCount++;
        this.id = Animal.aniCount;

        this.expressGenes();
        this.nn = nn;
    }

    /**
     * Returns a blueprint Animal with default parameters for use in creating new animals.
     * <p>
     *     <a href = "https://en.wikipedia.org/wiki/Singleton_pattern"> Singleton pattern </a>
     * </p>
     *
     * @return an Animal object with default DNA and NeuralNetwork parameters
     */
    public static Animal blueprint(){
        //if blueprint hasn't been generated already create it
        if(Animal.blueprint == null) {
            Transform t = new Transform();  //location is at (0,0)

            Gene[] genes = {
                    //TODO: set default parameters
                    new Gene(10, "sizeRatio", GeneType.SMALLER),
                    new Gene(128, "colorRed", GeneType.COLOR),
                    new Gene(128, "colorGreen", GeneType.COLOR),
                    new Gene(128, "colorBlue", GeneType.COLOR),
                    new Gene(.01, "mutSizeDNA", GeneType.PROBABILITY),
                    new Gene(.1, "mutProbDNA", GeneType.PROBABILITY),
                    new Gene(5, "mutSizeNN", GeneType.PROBABILITY),
                    new Gene(.5, "mutProbNN", GeneType.PROBABILITY),
                    new Gene(5, "attractiveness", GeneType.SMALLER),
                    new Gene(1, "growthScaleFactor", GeneType.SMALLER),
                    new Gene(20, "growthMaturityFactor", GeneType.BIGGER),
                    new Gene(1, "growthMaturityExponent", GeneType.SMALLER),
                    new Gene(.05, "speedRatio", GeneType.SMALLER),
                    new Gene(20, "strength", GeneType.BIGGER),
                    new Gene(2*1000, "gestationDuration", GeneType.TIME),
                    new Gene(.2, "maxForce", GeneType.SMALLER),
                    new Gene(.5, "maxSpeed", GeneType.SMALLER),
                    new Gene(45, "viewAngle", GeneType.ANGLE),
                    new Gene(100, "viewDistance", GeneType.DISTANCE),
                    new Gene(3 * 1000, "timerFrequency", GeneType.TIME),
                    new Gene(0, "pheromoneSensibility", GeneType.SMALLER),
                    new Gene(1, "separationWeight", GeneType.SMALLER),
                    new Gene(.5, "alignmentWeight", GeneType.SMALLER),
                    new Gene(.5, "cohesionWeight", GeneType.SMALLER),
                    new Gene(1, "velocityWeight", GeneType.SMALLER),
                    new Gene(50, "separationDistance", GeneType.DISTANCE)
            };
            DNA dna = new DNA(genes);

            //TODO: check if these are the correct default amount of inputs
            NeuralNetwork nn = new NeuralNetwork(22, 36, 8);

            Animal blueprint = new Animal(t,dna,nn);

            //to not increase the counter when not needed, because this will be increased in the expressGenes method
            Animal.aniCount--;
            blueprint.id = 0;

            Animal.blueprint = blueprint;
        }
        return Animal.blueprint;
    }

    /**
     * sets the new blueprint
     * @param blueprint that should from now on be used
     */
    public static void setBlueprint(Animal blueprint){
        Animal.blueprint = blueprint;
    }


    /**
     * Expresses the genes of the animal, retrieving and setting values for the different DNA genes.
     * The genes are stored in the DNA object, which is an attribute of the animal.
     * Each gene is accessed and its value is checked and set within specific bounds, and then used to set the values of
     * the corresponding attributes of the animal.
     * <p>
     *     Genes:
     *     <ul>
     *         <li>[0] speedRatio: speed ratio of the organism</li>
     *         <li>[1] strength: strength of the organism (>=0)</li>
     *         <li>[2] gestationDuration: duration of pregnancy in seconds (>=0)</li>
     *         <li>[3] maxForce: The maximum steering force of this (>=0)</li>
     *         <li>[4] maxSpeed: The maximum speed of this (>=0)</li>
     *         <li>[5] viewAngle: The view angle from heading direction (0-180)</li>
     *         <li>[6] viewDistance: How far this can see (>=0)</li>
     *         <li>[7] timerFrequency: The seconds at which the inner timer runs (>=0)</li>
     *         <li>[8] pheromoneSensibility: How sensible this is to pheromones</li>
     *         <li>[9] separationWeight: How much the separation vector is scaled by</li>
     *         <li>[10] alignmentWeight: How much the alignment vector is scaled by</li>
     *         <li>[11] cohesionWeight: How much the cohesion vector is scaled by</li>
     *         <li>[12] velocityWeight: ?</li>
     *         <li>[13] separationDistance: At what distance this want's to separate from others</li>
     *     </ul>
     * </p>
     * The size is set by multiplying the maturity and size Ratio
     * @see DNA
     * @see Organism#expressGenes()
     */
    @Override
    public void expressGenes() {
        super.expressGenes();
        int shift = Organism.numberOrganismGenes;

        this.gender = Gender.getRandomGender();

        this.speedRatio = this.dna.getGene(shift+0).getValue();

        this.dna.getGene(shift+1).genePositiveCheck();
        this.strength = this.dna.getGene(shift+1).getValue();

        this.dna.getGene(shift+2).geneBoundCheck(1000, Double.POSITIVE_INFINITY);
        this.gestationDuration = Math.round(this.dna.getGene(shift+2).getValue());

        this.dna.getGene(shift+3).genePositiveCheck();
        this.maxForce = this.dna.getGene(shift+3).getValue();

        this.dna.getGene(shift+4).genePositiveCheck();
        this.maxSpeed = this.dna.getGene(shift+4).getValue();

        this.dna.getGene(shift+5).geneBoundCheck(0,180);
        this.viewAngle = this.dna.getGene(shift+5).getValue();

        this.dna.getGene(shift+6).genePositiveCheck();
        this.viewDistance = this.dna.getGene(shift+6).getValue();

        this.timerFrequency = this.dna.getGene(shift+7).getValue();

        this.pheromoneSensibility = this.dna.getGene(shift+8).getValue();

        this.separationWeight = this.dna.getGene(shift+9).getValue();
        this.alignmentWeight = this.dna.getGene(shift+10).getValue();
        this.cohesionWeight = this.dna.getGene(shift + 11).getValue();
        this.velocityWeight = this.dna.getGene(shift+12).getValue();
        this.dna.getGene(shift+13).geneBoundCheck(Double.NEGATIVE_INFINITY, this.viewDistance);
        this.separationDistance = this.dna.getGene(shift + 13).getValue();

        this.transform.setSize(Animal.baseSize * this.sizeRatio * this.maturity + 1);

        if(this.maxSpeed > Animal.allMaxSpeed){
            this.maxSpeed = Animal.allMaxSpeed;
        }
    }


    /**
     * Updates the state of the organism based on the current simulation.
     *
     * <p>This method is responsible for executing the organism's behaviors and updating its position and state.
     * First, the organism thinks and uses energy for this process. Then, the organism uses energy for acceleration and
     * moves according to its maximum speed. Finally, the organism updates its variables and states and uses energy for
     * existing and moving.</p>
     *
     * <p>The organism's energy is used during the thinking and acceleration processes.</p>
     *
     * <p>TODO: add physics so the organism cannot run through another one and cannot clip.</p>
     *
     * @param s the current simulation context
     *
     * @see #think(Simulation)
     * @see #metabolismCost()
     * @throws AssertionError if this is dead
     */
    @Override
    public void update(Simulation s) {
        assert !this.isDead() : "this is dead";


        this.think(s);
        //TODO use energy for thinking

        //use energy for acceleration
        this.useEnergy(this.metabolismCost());

        //Movement
        //TODO check if this should be tweaked (relation to size, resistance, slipperiness, etc.)
        this.transform.getAcceleration().limit(this.maxForce).mult(this.healthRatio());
        this.transform.move(this.maxSpeed);

        //update variables and states
        //TODO use energy for existing
        //TODO use energy for moving
    }

    /**
     * Determines the actions to take based on the current state and environment.
     *
     * @param s the simulation in which the animal exists
     */
    public void think(Simulation s){
        World w = s.getWorld();

        //get animals and plants in sight
        ArrayList<Animal> animalsInSight = w.getAnimalQuadTree().query(this.getFieldOfView());
        ArrayList<Plant> plantsInSight = w.getPlantQuadTree().query(this.getFieldOfView());

        //search the closest entity of each
        Plant cPlant = this.searchClosestPlant(plantsInSight);
        Animal cAnimal = this.searchClosestAnimal(animalsInSight);

        double[] inputs = new double[]{
                //constant
                1,
                this.energy,
                this.getMaturity(),
                this.attractiveness,
                this.healthRatio(),
                this.speed(),
                this.getAge(),
                this.canMate() ? 1 : 0,

                // 1/distance to the closest Animal
                cAnimal != null && this.getLocation().distSq(cAnimal.getLocation()) != 0 ? 1/this.getLocation().distSq(cAnimal.getLocation()) : 0,
                // angle to the closest Animal
                cAnimal != null ? Vector2D.angleBetween(this.getLocation(), cAnimal.getLocation()) : 0,

                // 1/distance to the closest Plant
                cPlant != null && this.getLocation().distSq(cPlant.getLocation()) != 0 ? 1/this.getLocation().distSq(cPlant.getLocation()) : 0,
                // angle to the closest Plant
                cPlant != null ? Vector2D.angleBetween(this.getLocation(), cPlant.getLocation()) : 0,

                //how many animals / plants are in sight
                animalsInSight.size(),
                plantsInSight.size(),

                //color of the closest animal
                cAnimal != null ? cAnimal.getColorRed() : 0,
                cAnimal != null ? cAnimal.getColorGreen() : 0,
                cAnimal != null ? cAnimal.getColorBlue() : 0,

                //gender of the closest animal
                //TODO figure out a smart way to transmit this

                /*
                cAnimal != null ?
                        (cAnimal.getGender() == Gender.MALE ? 1 : -1)
                        : 0,
                 */
                cAnimal != null ? (this.correctGenderComb(cAnimal) ? 1 : 0) : 0,
                cAnimal != null ? (cAnimal.canMate() ? 1 : 0) : 0,

                cAnimal != null ? cAnimal.healthRatio() : 0,
                cAnimal != null ? cAnimal.getMaturity() : 0,
                cAnimal != null ? cAnimal.attractiveness : 0,
                //direction of movement of the animal
                //cAnimal.getTransform().getVelocity().getX(),
                //cAnimal.getTransform().getVelocity().getY(),


                //clkTic: Internal timer (1s on, 1s off (actual period decided by genes))
                //clkMinute: kind of like a chronometer, counts time, gets reset by an output neuron
        };

        double[] outputs = this.nn.predict(inputs);

        Vector2D direction = new Vector2D(1,0); //current direction of movement
        //if this doesn't have any direction choose a unit vector
        if(!this.transform.getAcceleration().isNullVector()){
            direction = this.transform.getAcceleration();
        }
        //Accelerate, Rotate
        this.transform.applyForce(
                //"choose" direction to move
                Vector2D.fromAngle((outputs[0])*360, direction)
                        //how fast
                        .setMag(outputs[1] * this.maxForce)
        );

        //Herding Desire TODO check if the handling of the vectors is correct
        if(outputs[2] > Animal.herdingThreshold) {
            this.transform.applyForce(separate(animalsInSight).mult(this.separationWeight).limit(this.maxForce));
            this.transform.applyForce(cohesion(animalsInSight).mult(this.cohesionWeight).limit(this.maxForce));
            this.transform.applyForce(align(animalsInSight).mult(this.alignmentWeight).limit(this.maxForce));
        }

        //Mate Desire TODO implement attractiveness into the mating
        if(outputs[3] > Animal.matingThreshold && cAnimal != null && !cAnimal.isDead()){
            //this.reproductiveUrge = outputs[3] * Animal.reproductiveUrgeFactor;

            if(this.correctGenderComb(cAnimal) &&
                    this.canMate() &&
                    cAnimal.canMate() &&
                    this.collision(cAnimal)){
                this.mate(cAnimal, s);
            }
            else{
                //TODO implement asexual reproduction
                if(this.canMate() & Math.random() <= this.healthRatio() * .005 & this.gender == Gender.FEMALE && !this.isPregnant){
                    this.mate = this;
                    this.reproduce(s);
                }
            }
        }

        //Eat Desire TODO rework and implement different diet types
        if(outputs[4] > Animal.eatingThreshold && cPlant != null && !cPlant.isDead()){
            if(collision(cPlant)){
                double damage = this.strength * Animal.damageFactor;    //calculate damage
                double energyGained = damage;   //TODO add a factor to scale energyGained in the settings

                //if damage is bigger than rest of health obtainable energy is limited
                if(damage > cPlant.getHealth()){
                    energyGained = cPlant.getHealth();
                }

                cPlant.takeDamage(damage);  //deal damage

                //TODO how much energy gets restored and based on what?
                //TODO add a factor to scale
                this.restoreEnergy(energyGained * 3);

                if(cPlant.getHealth() <= 0){
                    this.plantsKilled++;
                }

            }
        }

        //Growth
        if(outputs[5] > Animal.growthThreshold && outputs[5] > 0){
            this.grow(outputs[5]);
        }

        //Healing TODO rework
        if(outputs[6] > Animal.healingThreshold){
            this.useEnergy(outputs[6] * Animal.healingFactor);//Animal.healingCostFactor);
            this.restoreHealth(outputs[6] * Animal.healingFactor);
        }

        //Attack TODO rework
        if(outputs[7] > Animal.attackThreshold && cAnimal != null && !cAnimal.isDead()){
            if(collision(cAnimal)){
                //TODO consider strength of attacked animal as defence
                //TODO consider speed of animals
                if(this.strength >= cAnimal.strength){
                    cAnimal.takeDamage(this.strength); //* this.transform.getVelocity().magSq());
                }
                //System.out.println("Dealt damage: " + this.strength);
                if(cAnimal.getHealth() <= 0){
                    this.animalsKilled++;
                }
            }
        }
    }

    //------------------------------------------------Herding----------------------------------------------------------
    /**
     * Calculates and returns the steering force required to separate the current animal from other animals that are
     * too close according to the separation distance.
     *
     * @param animals an ArrayList of Animal objects representing the other animals in the environment
     * @return a Vector2D object representing the steering force required to separate the current animal from the other animals
     * @throws AssertionError if an animal is not in sight
     */
    public Vector2D separate(ArrayList<Animal> animals){
        Vector2D sum = new Vector2D();
        Vector2D steer = new Vector2D();
        int count = 0; //of animals being too close

        for(Animal a : animals){
            //calculate distance of the two animals
            double distance = Vector2D.distSq(this.getLocation(),a.getLocation());

            //TODO check
            //assert distance < Math.pow(this.viewDistance,2) : "animal not in sight";

            //here check distance > 0 to avoid an animal separation from itself
            if((distance>0) && (distance < Math.pow(this.separationDistance,2))){
                Vector2D difference = Vector2D.sub(this.getLocation(), a.getLocation());
                difference.normalize();
                //the closer an animal the more we should flee
                difference.div(distance);
                //add all the vectors together
                sum.add(difference);
                count++;
            }
        }

        //avoid division by zero
        if(count > 0){
            sum.div(count);
            sum.setMag(this.maxSpeed);
            steer = Vector2D.sub(sum,this.transform.getVelocity());
            steer.limit(this.maxForce);
        }

        assert this.invariant() : "Invariant is broken " + this.transform.getVelocity().magSq() + "/" + Math.pow(this.maxSpeed,2);
        return steer;
    }

    /**
     * Calculates and returns the steering force required to separate the current animal from other animals that are
     * too close according to the separation distance.
     *
     * @param animals an ArrayList of Animal objects representing the other animals in the environment
     * @return a Vector2D object representing the steering force required to separate the current animal from the other animals
     * @throws AssertionError if an animal is not in sight
     */
    public Vector2D cohesion(ArrayList<Animal> animals){
        Vector2D sum = new Vector2D();
        int count = 0;
        int ratio = 0;

        for(Animal a : animals){
            double distance = Vector2D.distSq(this.getLocation(),a.getLocation());

            //TODO check why this assertion is thrown
            //assert distance < Math.pow(this.viewDistance,2) : "animal not in sight";

            //TODO implement cohesion distance?
            if((distance > 0) && (distance < Math.pow(this.separationDistance*5,2))){
                if(distance < Math.pow(0.5 * this.separationDistance*5,2)) {
                    ratio++;
                }
                ratio++;
                sum.add(a.getLocation());
                count++;
            }
        }
        if(count > 0){
            sum.div(count);
            ratio/= count * 2;
            assert this.invariant() : "Invariant is broken " + this.transform.getVelocity().magSq() + "/" + Math.pow(this.maxSpeed,2);
            return seek(sum,ratio);
        }
        else {
            assert this.invariant() : "Invariant is broken " + this.transform.getVelocity().magSq() + "/" + Math.pow(this.maxSpeed,2);
            return new Vector2D();
        }
    }

    /**
     * Calculates the steering force required for the animal to align its velocity with the average velocity of neighboring animals.
     * Only animals within the view distance and alignment distance will be considered.
     *
     * @param animals an ArrayList of Animal objects representing the neighboring animals
     * @return a Vector2D representing the steering force required for the animal to align its velocity with neighboring animals
     * @throws AssertionError if an animal is not in sight
     */
    public Vector2D align(ArrayList<Animal> animals){
        Vector2D sum = new Vector2D();
        Vector2D steer = new Vector2D();
        int count = 0;

        for(Animal a : animals){
            double distance = Vector2D.distSq(this.getLocation(),a.getLocation());

            //TODO check why this assertion is thrown
            //assert distance < Math.pow(this.viewDistance,2) : "animal not in sight";

            //TODO implement alignment distance?
            if((distance > 0) && (distance < Math.pow(this.separationDistance*5,2))){
                sum.add(a.getTransform().getVelocity());
                count++;
            }
        }
        if(count > 0){
            sum.div(count);
            sum.normalize();
            sum.mult(this.maxSpeed);
            steer = Vector2D.sub(sum,this.transform.getVelocity());
            steer.limit(this.maxForce);
        }
        assert this.invariant() : "Invariant is broken " + this.transform.getVelocity().magSq() + "/" + Math.pow(this.maxSpeed,2);
        return steer;
    }

    /**
     * Calculates a steering force towards a target location.
     * The force is calculated as the difference between the desired velocity (which points from the animal's current location
     * towards the target) and the animal's current velocity.
     * The magnitude of the desired velocity is adjusted based on the groupRatio parameter, which should be an integer value representing
     * the ratio of nearby animals to the maximum number of animals allowed within a certain range.
     * The steering force is then limited by the animal's maximum force.
     *
     * @param target the target location to seek
     * @param groupRatio the ratio of nearby animals to the maximum number of animals allowed within a certain range
     * @return a Vector2D representing the steering force towards the target location
     */
    public Vector2D seek(Vector2D target, int groupRatio){
        Vector2D desired = Vector2D.sub(target,this.transform.getLocation());

        desired.setMag(this.maxSpeed * groupRatio);

        Vector2D steer = Vector2D.sub(desired,this.transform.getVelocity());
        steer.limit(this.maxForce);

        assert this.invariant() : "Invariant is broken " + this.transform.getVelocity().magSq() + "/" +Math.pow(this.maxSpeed,2);
        return steer;
    }

    //------------------------------------------------Reproduction-----------------------------------------------------

    /**
     * Searches for the closest mate within the given world.
     *
     * @param w The world in which the animal is searching for a mate.
     * @return The closest animal that is a suitable mate, or null if no mate is found.
     * @throws AssertionError If the chosen mate is not of the correct gender combination or the animal tries to mate with itself.
     */
    public Animal searchClosestMate(World w){
        ArrayList<Animal> animals = w.getAnimalQuadTree().query(this.getFieldOfView());

        Animal chosenMate = null;
        double mostAttractive = Double.NEGATIVE_INFINITY;

        for(Animal o : animals){
            double distance = this.getLocation().distSq(o.getLocation());
            double attractiveness = (1/distance) * o.getAttractiveness() * this.reproductiveUrge - this.attractiveness;

            //TODO rework
            if(this.id != o.id
                    && distance <= Math.pow(this.viewDistance,2)
                    && this.correctGenderComb(o) && this.canMate() && o.canMate()
                    && o.wantsToMate(this)
                    && mostAttractive <= attractiveness
            )
            {
                mostAttractive = attractiveness;
                chosenMate = o;
            }
        }
        assert (chosenMate != null ? this.correctGenderComb(chosenMate) : true) : "Wrong gender combination";
        assert this != chosenMate : "Wants to mate with itself";

        return chosenMate;
    }


    /**
     * Returns whether this animal wants to mate with another animal.
     *
     * @param a the other animal
     * @return true if this animal wants to mate with the other animal, false otherwise
     * @throws AssertionError if the other animal is the same as this animal
     //TODO rework
     */
    public boolean wantsToMate(Animal a) {
        assert this != a : "wantsToMate on itself";

        if(this.reproductiveUrge <= 0){
            return false;
        }
        else{
            //TODO rethink this formula with some examples and see if they make sense
            return this.attractiveness * (1 / this.reproductiveUrge) <= a.attractiveness;
        }
    }

    /**
     * Checks if the gender combination of this animal and its mate is valid for mating.
     *
     * @param mate the animal to mate with
     * @return true if the gender combination is valid for mating, false otherwise
     * @see Gender#correctGenderForReproduction(Gender)
     */
    public boolean correctGenderComb(Animal mate){
        return this.gender.correctGenderForReproduction(mate.gender);
    }

    /**
     * Checks whether the animal can mate or not based on its health ratio and maturity.
     *
     * @return boolean value indicating whether the animal can mate or not.
     */
    public boolean canMate(){
        return this.healthRatio() >= Animal.minHealthToReproduce && this.maturity >= Animal.minMaturityToReproduce;
    }

    /**
     * Initiates a mating process with another animal, given they are of the correct gender combination and both are able to mate.
     * If this animal is female and able to give birth, and is not already pregnant, it will become pregnant and start gestating for a certain amount of time before reproducing.
     * Otherwise, the mate() method is called on the other animal, initiating the mating process on its end.
     *
     * @param mate the other animal to mate with
     * @param s the simulation instance
     * @throws AssertionError if the gender combination is incorrect or if either animal is unable to mate
     * @see #reproduce(Simulation)
     */
    public void mate(Animal mate, Simulation s){
        assert this.correctGenderComb(mate) : "Wrong gender combination";
        assert this.canMate() : "this can't mate";
        assert mate.canMate() : "partner is not able to mate";

        Animal self = this;

        if (this.gender.canBirth()) {
            if (!this.isPregnant) { // check if not already pregnant
                //this.gender.getPregnant(mate); // set pregnant flag
                this.mate = mate;
                this.isPregnant = true;
                new Timer().schedule(new TimerTask() {
                    @Override
                    public void run() {
                        self.reproduce(s);
                    }
                }, this.gestationDuration);
            }
        }
        else {
            //if this cannot getPregnant then the other animal should be female and call this method on the other animal
            mate.mate(this, s);
        }
    }

    /**
     * Overrides the reproduce method of the Organism class to create a new Animal that inherits
     * its gender from the mate of the parent animal, and its genes from the parent. The child is
     * then added to the simulation. The count of animals born is incremented and the birth is
     * recorded in the parent animal's gender object.
     *
     * @param s The simulation that the animal is added to.
     * @return The new Animal object.
     * @throws AssertionError If the parent animal can't give birth or has not had a mate.
     * TODO add the possibility of multiple children to be birthed and a way to control it or define it
     */
    @Override
    public Organism reproduce(Simulation s) {
        assert this.gender.canBirth() : "this can't birth";
        assert this.mate != null;

        Animal child = new Animal(this.mate,this);
        //TODO add a toggle for this
        s.getGraphics().drawOval((int)child.getLocX()-20,(int)child.getLocY()-20,40,40);
        s.addAnimal(child);

        Animal.aniBornCount++;
        if(this != this.mate){
            this.mate.offspringBirthed++;
        }
        this.offspringBirthed++;
        this.mate = null;

        Animal self = this;
        //TODO make this a variable maybe in genes? settings?
        //TODO also use another tag than isPregnant, maybe canGetPregnant or something like that
        int timeTillCanBirthAgain = 10000;
        new Timer().schedule(new TimerTask() {
            @Override
            public void run() {
                self.isPregnant = false;
            }
        }, timeTillCanBirthAgain);
        //this.isPregnant = false;

        return child;
    }

    //------------------------------------------------Eating-----------------------------------------------------------

    //------------------------------------------------Growth-----------------------------------------------------------
    /**
     * Increases the maturity of the animal by a certain factor, based on its growth rate and size ratio.
     * Uses energy based on the increase in basal metabolic rate (BMR) caused by the growth.
     *
     * @param factor the factor by which to increase the animal's maturity (must be greater than 0)
     * @throws AssertionError if factor is 0 or less
     */
    @Override
    public void grow(double factor) {
        assert factor > 0 : "factor is 0 or less";
        double oldMaturity = this.maturity;

        double growth = this.growthRate() * factor;
        this.setMaturity(this.maturity+growth);
        double BPIncrease = 100 * growth * Math.pow(this.sizeRatio,2);
        this.useEnergy(BPIncrease * Animal.bodyEnergyRatio * (1+(1.0/Animal.healthBodyRatio)));

        assert oldMaturity <= this.maturity;
    }

    //------------------------------------------------Healing----------------------------------------------------------

    //------------------------------------------------Attacking--------------------------------------------------------

    //------------------------------------------------Searching--------------------------------------------------------
    /**
     * Searches for the closest plant in the given list of plants within the animal's view distance.
     *
     * @param plantsInSight the list of plants within the animal's view distance
     * @return the closest plant, or null if no plants are within the view distance
     * @throws AssertionError if the animal is dead
     */
    public Plant searchClosestPlant(ArrayList<Plant> plantsInSight){
        assert !this.isDead() : "This is dead";

        //calculate the closest organism

        Plant closestOrganism = null;
        double closestDistance = Double.POSITIVE_INFINITY;

        //calculate the closest organism
        for(Plant p : plantsInSight){
            double distance = this.getLocation().distSq(p.getLocation());
            //if the distance is smaller than the current closest distance and smaller than the viewDistance
            if((closestDistance >= distance) && (distance <= Math.pow(this.viewDistance,2))
                    && (p.getId() != this.id) && (!p.isDead())){
                closestDistance = distance;
                closestOrganism = p;
            }
        }
        return closestOrganism;
    }

    public Plant searchClosestPlant(World w){
        return this.searchClosestPlant(w.getPlantQuadTree().query(this.getFieldOfView()));
    }

    /**
     * Searches for the closest animal in the given list of animals in sight.
     *
     * @param animalsInSight the list of animals in sight
     * @return the closest animal, or null if no animal is in sight
     * @throws IllegalStateException if this animal is dead
     */
    public Animal searchClosestAnimal(ArrayList<Animal> animalsInSight){
        assert !this.isDead() : "This is dead";

        //calculate the closest organism
        Animal closestAnimal = null;
        double closestDistance = Double.POSITIVE_INFINITY;

        //calculate the closest organism
        for(Animal a : animalsInSight){
            double distance = this.getLocation().distSq(a.getLocation());
            //if the distance is smaller than the current closest distance and smaller than the viewDistance
            if((closestDistance >= distance) && (distance <= Math.pow(this.viewDistance,2))
                    && (a.getId() != this.id) && (!a.isDead())){
                closestDistance = distance;
                closestAnimal = a;
            }
        }
        return closestAnimal;
    }

    public Animal searchClosestAnimal(World w){
        return this.searchClosestAnimal(w.getAnimalQuadTree().query(this.getFieldOfView()));
    }

    /**
     * Searches for the closest organism within the given list of organisms.
     * Throws an assertion error if the organism invoking this method is dead.
     *
     * @param organisms the list of organisms to search within
     * @return the closest organism found, or null if the list is empty
     */
    public Organism searchClosest(ArrayList<Organism> organisms){
        assert !this.isDead() : "This is dead";

        Organism closestOrganism = null;
        double closestDistance = Double.POSITIVE_INFINITY;

        //calculate the closest organism
        for(Organism o : organisms){
            double distance = this.getLocation().distSq(o.getLocation());
            //if the distance is smaller than the current closest distance and smaller than the viewDistance
            if((closestDistance >= distance) && (distance <= Math.pow(this.viewDistance,2)) && (o.getId() != this.id)){
                closestDistance = distance;
                closestOrganism = o;
            }
        }
        return closestOrganism;
    }

    //------------------------------------------------Other------------------------------------------------------------
    /**
     * Checks whether this organism collides with another organism.
     *
     * @param o the other organism to check for collision with
     * @return true if this organism collides with the other organism, false otherwise
     */
    public boolean collision(Organism o){
        //check if this collides with something
        if(o == null){
            return false;
        }
        else{
            return this.transform.getRectangle().intersects(o.getTransform().getRectangle());
            //return this.getLocation().distSq(o.getLocation()) <= Math.pow(this.getR() + o.getR(), 2);
        }
    }

    /**
     * Calculates the metabolic cost of this organism based on its speed and size.
     * The larger and faster the organism is, the more energy it requires to sustain itself.
     *
     * @return the metabolic cost of this organism
     */
    public double metabolismCost(){
        //TODO does this make sense? shouldn't more energy be used when bigger?
        return ((this.speed()+3)*Animal.metabolismFactor) / (2*this.size());
    }

    /**
     * Returns an Ellipse2D object that represents the sensory radius of the organism.
     * The sensory radius is a circular area that extends a distance of half the view distance beyond the
     * radius of the organism, centered on its location.
     *
     * @return an Ellipse2D object representing the sensory radius of the organism
     * TODO maybe refactor into Transform class?
     */
    public Ellipse2D getSensoryRadius(){
        return new Ellipse2D.Double(this.getLocX() - this.getR() - this.viewDistance/2, this.getLocY() - this.getR() - this.viewDistance/2, this.size() + this.viewDistance, this.size() + this.viewDistance);
    }

    /**
     * Returns an Arc2D.Double object representing the translated field of view of the animal.
     * The arc is created with the current location of the animal as its center.
     *
     * @return Arc2D.Double object representing the translated field of view of the animal.
     * TODO extend documentation maybe add pre conditions
     * TODO find a bug where the field of view is not correct
     */
    public Arc2D.Double getTranslatedFieldOfView(){
        return new Arc2D.Double(
                -this.viewDistance/2, -this.viewDistance/2,
                this.viewDistance, this.viewDistance,
                -this.viewAngle, 2*this.viewAngle, Arc2D.PIE);
    }

    /**
     * Returns an Arc2D.Double object representing the field of view of the animal.
     *
     * @return Arc2D.Double object representing the field of view of the animal.
     * @since 11.04.2023
     * TODO find a bug where the field of view is not correct
     */
    public Arc2D.Double getFieldOfView(){
        return new Arc2D.Double(
                this.getLocX()-this.viewDistance/2, this.getLocY()-this.viewDistance/2,
                this.viewDistance, this.viewDistance,
                -this.viewAngle, 2*this.viewAngle, Arc2D.PIE);
    }

    //TODO think about a good function
    //TODO write documentation with examples and maybe a link to a visual drawing of the function
    public double getFitnessScore(){
        return (this.healthRatio() + this.energyRatio())*(this.plantsKilled);//Math.pow(this.offspringBirthed,2) + this.maturity) * ;
    }

    /**
     * Returns the on-screen position of the animal based on its current location and the position of the scroll pane's viewport.
     *
     * @return a Point object representing the on-screen position of the animal
     */
    public Point getScreenPosition() {
        // calculate the animal's position on the screen
        // based on its current position and the position
        // of the viewport in the scroll pane
        int x = (int)(this.getLocX() - SimulationGUI.scrollPane.getViewport().getViewPosition().getX());
        int y = (int)(this.getLocY() - SimulationGUI.scrollPane.getViewport().getViewPosition().getY());
        return new Point(x, y);
    }

    /**
     * Overrides the parent method to add rotation to the graphics context.
     * It first calls the parent method to translate the graphics to the location of the object,
     * and then rotates the graphics context based on the rotation angle of the object's transform.
     *
     * @param g the graphics context to be translated and rotated
     * @since 11.04.2023
     */
    @Override
    protected void translateGraphics(Graphics2D g) {
        super.translateGraphics(g);
        g.rotate(this.transform.getRotation(),0,0);
    }

    //------------------------------------------------Getter and Setter------------------------------------------------

    public Gender getGender() {
        return gender;
    }

    public void setGender(Gender gender) {
        this.gender = gender;
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
        return this.transform.getSize();
    }

    /**
     * Returns the current speed of the organism, which is the magnitude of its acceleration vector.
     *
     * @return the current speed of the organism
     */
    public double speed(){
        //TODO: check if velocity changes when no acceleration is applied
        return this.transform.getAcceleration().mag();
    }

    public int getGeneration() {
        return generation;
    }

    public void setGeneration(int generation) {
        this.generation = generation;
    }

    public double getReproductiveUrge() {
        return reproductiveUrge;
    }

    public void setReproductiveUrge(double reproductiveUrge) {
        this.reproductiveUrge = reproductiveUrge;
    }

    public double getSpeedRatio() {
        return speedRatio;
    }

    public void setSpeedRatio(double speedRatio) {
        this.speedRatio = speedRatio;
    }

    public double getStrength() {
        return strength;
    }

    public void setStrength(double strength) {
        this.strength = strength;
    }

    public long getGestationDuration() {
        return gestationDuration;
    }

    public void setGestationDuration(long gestationDuration) {
        this.gestationDuration = gestationDuration;
    }

    public double getMaxForce() {
        return maxForce;
    }

    public void setMaxForce(double maxForce) {
        this.maxForce = maxForce;
    }

    public double getMaxSpeed() {
        return maxSpeed;
    }

    public void setMaxSpeed(double maxSpeed) {
        this.maxSpeed = maxSpeed;
    }

    public double getViewAngle() {
        return viewAngle;
    }

    public void setViewAngle(double viewAngle) {
        this.viewAngle = viewAngle;
    }

    public double getTimerFrequency() {
        return timerFrequency;
    }

    public void setTimerFrequency(double timerFrequency) {
        this.timerFrequency = timerFrequency;
    }

    public double getPheromoneSensibility() {
        return pheromoneSensibility;
    }

    public void setPheromoneSensibility(double pheromoneSensibility) {
        this.pheromoneSensibility = pheromoneSensibility;
    }

    public double getSeparationWeight() {
        return separationWeight;
    }

    public void setSeparationWeight(double separationWeight) {
        this.separationWeight = separationWeight;
    }

    public double getAlignmentWeight() {
        return alignmentWeight;
    }

    public void setAlignmentWeight(double alignmentWeight) {
        this.alignmentWeight = alignmentWeight;
    }

    public double getCohesionWeight() {
        return cohesionWeight;
    }

    public void setCohesionWeight(double cohesionWeight) {
        this.cohesionWeight = cohesionWeight;
    }

    public double getVelocityWeight() {
        return velocityWeight;
    }

    public void setVelocityWeight(double velocityWeight) {
        this.velocityWeight = velocityWeight;
    }

    public double getSeparationDistance() {
        return separationDistance;
    }

    public void setSeparationDistance(double separationDistance) {
        this.separationDistance = separationDistance;
    }

    public double getGrowthScaleFactor() {
        return growthScaleFactor;
    }

    public void setGrowthScaleFactor(double growthScaleFactor) {
        this.growthScaleFactor = growthScaleFactor;
    }

    public double getGrowthMaturityFactor() {
        return growthMaturityFactor;
    }

    public void setGrowthMaturityFactor(double growthMaturityFactor) {
        this.growthMaturityFactor = growthMaturityFactor;
    }

    public double getGrowthMaturityExponent() {
        return growthMaturityExponent;
    }

    public void setGrowthMaturityExponent(double growthMaturityExponent) {
        this.growthMaturityExponent = growthMaturityExponent;
    }

    public static int getNumberAnimalGenes() {
        return numberAnimalGenes;
    }

    public static void setNumberAnimalGenes(int numberAnimalGenes) {
        Animal.numberAnimalGenes = numberAnimalGenes;
    }

    //------------------------------------------------toString and paint-----------------------------------------------

    //TODO needs rework, think about unnecessary multiple calculation
    @Override
    public void paint(Graphics2D g) {
        super.paint(g);
        AffineTransform old = g.getTransform(); //save transform to reset later

        this.translateGraphics(g);  //set the center of the graphics to this center

        //TODO rework so this works with the animals shape via getCenteredShape and getShape
        g.fill(this.transform.getTranslatedRectangle());  //paint the shape

        this.paintFemale(g); //mark if female (and if pregnant)

        this.paintFieldOfView(g); //paint the field of view

        this.paintAcceleration(g); //paint the acceleration vector

        this.paintDirection(g); //paint the direction vector

        g.setTransform(old); //Reset Transform

        this.paintStats(g); //paint stats
    }

    /**
     * Paints any statistics that should be displayed for this animal onto the graphics context.
     *
     * @param g the graphics context to paint onto
     * @since 12.04.2023
     */
    @Override
    protected void paintStats(Graphics2D g) {
        super.paintStats(g);
    }

    /**
     * Paints a line indicating the animal's direction of movement.
     * The length of the line is proportional to the magnitude of the animal's velocity vector.
     *
     * @param g the Graphics2D object to paint on
     * @since 12.04.2023
     */
    private void paintDirection(Graphics2D g) {
        if(SimulationGUI.showDirection){
            g.setColor(Color.BLACK);
            g.draw(this.transform.getTranslatedVelocityLine(Animal.visualDirScale));
        }
    }

    /**
     * Paints the acceleration vector of this animal onto the given Graphics2D object, if the
     * SimulationGUI flag "showSteering" is set to true.
     *
     * @param g the Graphics2D object on which to paint the acceleration vector
     * @since 12.04.2023
     */
    private void paintAcceleration(Graphics2D g) {
        if (SimulationGUI.showSteering) {
            // Set the color of the acceleration vector to light gray
            g.setColor(Color.lightGray);

            // Draw the translated acceleration line of the animal on the Graphics2D object
            g.draw(this.transform.getTranslatedAccelerationLine(Animal.visualAccScale));
        }
    }

    /**
     * Paints the field of view of the animal.
     * If SimulationGUI.showSensoryRadius is true, the sensory radius of the animal is shown.
     * The color of the field of view depends on the status of the animal:
     * red if it is pregnant, green if it can mate, yellow if it is mature, and gray if it is immature.
     *
     * @param g the Graphics2D object used for painting
     * @since 11.04.2023
     */
    private void paintFieldOfView(Graphics2D g) {
        //show the sensory radius
        if(SimulationGUI.showSensoryRadius){
            //paint red if this is pregnant
            if(this.isPregnant){
                g.setColor(new Color(200,0,0,100));
            }
            //paint green if this can mate
            else if(this.canMate()){
                g.setColor(new Color(0,200,0,100));
            }
            //paint yellow if this is mature
            else if(this.maturity >= 1){
                g.setColor(new Color(200,200,0,100));
            }
            else{
                g.setColor(new Color(200,200,200,30));
            }

            g.fill(this.getTranslatedFieldOfView());
        }
    }

    /**
     * Marks the female animal with a circle or filled oval, depending on whether it is pregnant or not.
     * The circle/oval is drawn around the animal's location.
     *
     * @param g The graphics object on which to draw the mark
     * @since 11.04.2023
     */
    private void paintFemale(Graphics2D g) {
        //specially mark females
        if(this.gender == Gender.FEMALE){
            int offset = 2;
            int x = (int)Math.round(-this.getR() -offset);
            int y = (int)Math.round(-this.getR() -offset);
            int s = (int)this.size() + (2*offset);

            //if pregnant fill the oval
            if(this.isPregnant){
                g.fillOval(x,y,s,s);
            }
            //otherwise, just a circle surrounding the animal
            else{
                g.drawOval(x,y,s,s);
            }
        }
    }

    //------------------------------------------------invariant--------------------------------------------------------

    /**
     * @return if the current speed is bigger than the maxSpeed
     */
    public boolean invariant(){
        return (this.transform.getVelocity().magSq() <= (this.maxSpeed*this.maxSpeed) + .01) ||
                (this.transform.getVelocity().magSq() >= (this.maxSpeed*this.maxSpeed) - .01);
    }
}
