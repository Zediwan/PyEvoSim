package Main.Organisms.Animals;

import Main.Grid;
import Main.NeuralNetwork.NeuralNetwork;
import Main.Organisms.Attributes.DNA.DNA;
import Main.Organisms.Attributes.DNA.Gene;
import Main.Organisms.Attributes.Gender;
import Main.Helper.Transform;
import Main.Helper.Vector2D;
import Main.Organisms.Organism;
import Main.World;

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
    private double maturity;

    //TODO how should generations be handled when there are two parents?
    protected int generation = 0;
    protected Gender gender;
    protected double maxSpeed, maxForce;
    protected NeuralNetwork nn;
    protected double reproductiveUrge = 0;
    //protected double bodyPoints = 0;

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
    protected double separationWeight;              //[18]
    protected double alignmentWeight;               //[19]
    protected double cohesionWeight;                //[20]
    protected double velocityWeight;                //[21]
    protected double separationDistance;            //[22]
    protected double growthScaleFactor;             //[23]
    protected double growthMaturityFactor;          //[24]
    protected double growthMaturityExponent;        //[25]
    protected static int numberAnimalGenes = 14;

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
        this.maturity = 0 + mother.incubationTime / (10*1000);

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
                    new Gene(1, "pheromoneSensibility"),
                    new Gene(1, "separationWeight"),
                    new Gene(1, "alignmentWeight"),
                    new Gene(1, "cohesionWeight"),
                    new Gene(1, "velocityWeight"),
                    new Gene(1, "separationDistance")
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

        this.separationWeight = this.dna.getGene(shift+9).getValue();
        this.alignmentWeight = this.dna.getGene(shift+10).getValue();
        this.cohesionWeight = this.dna.getGene(shift + 11).getValue();
        this.velocityWeight = this.dna.getGene(shift+12).getValue();
        this.separationDistance = this.dna.getGene(shift + 13).getValue();

        this.transform.size = Animal.allMaxSize * this.sizeRatio * maturity;
        this.maxSpeed = Animal.allMaxSpeed * this.speedRatio;
    }

    //TODO Test
    //TODO write documentation
    @Override
    public void update(World w) {
        assert !this.isDead() : "this is dead";
        //TODO add physics so they can't run through into another and don't clip

        this.think(w);
            //use energy for thinking

        this.useEnergy(this.metabolismCost());      //use energy for acceleration

        //Movement
        //TODO check if this should be tweaked (relation to size, resistance, slipperiness, etc.)
        //TODO: maybe refactor this?
        this.transform.velocity.add(this.transform.acceleration.mult(this.healthRatio()));
        this.transform.velocity.limit(maxSpeed);
        this.transform.location.add(this.transform.velocity);
        this.transform.acceleration.mult(0);

        //update variables and states
            //use energy for existing
            //use energy for moving
    }

    @Override
    public void grow(double factor) {

    }

    //TODO Test
    //TODO write documentation
    public void think(World w){
        ArrayList<Animal> animals = w.getGrid().getGridFieldsA(this.getLoc(), this.viewDistance);
        Organism cPlant = this.searchClosestPlant(w);
        Organism cAnimal = this.searchClosestAnimal(w);

        double[] inputs = new double[]{
                1,
                this.energy,
                //Maturity,
                this.healthRatio(),
                this.speed(),
                this.getLoc().distSq(cAnimal.getLoc()),
                Vector2D.angleBetween(this.getLoc(), cAnimal.getLoc()),
                this.getLoc().distSq(cPlant.getLoc()),
                Vector2D.angleBetween(this.getLoc(), cPlant.getLoc()),
                animals.size(),
                w.getGrid().getGridFieldsP(this.getLoc(),this.viewDistance).size(),
                cAnimal.getColorRed(),
                cAnimal.getColorGreen(),
                cAnimal.getColorBlue(),
                //clkTic: Internal timer (1s on, 1s off (actual period decided by genes))
                //clkMinut: kind of like a chronometer, counts time, gets reset by an output neuron
                this.getAge(),
        };

        double[] outputs = this.nn.predict(inputs);

        /*
        Accelerate
        Rotate
         */
        this.transform.applyForce(this.transform.acceleration.rotate(outputs[0]-.5).setMag(outputs[1]-.5));

        //Herding Desire
        if(outputs[2] > .5){
            this.transform.applyForce(separate(animals).setMag(this.separationWeight).limit(this.maxForce));
            this.transform.applyForce(cohesion(animals).setMag(this.cohesionWeight).limit(this.maxForce));
            this.transform.applyForce(align(animals).setMag(this.alignmentWeight).limit(this.maxForce));
        }
        //Mate Desire
        if(outputs[3] > .5){
            this.reproductiveUrge = outputs[3];
            this.mate(this.searchClosestMate(w));
        }
        //Eat Desire
        if(outputs[4] > .5){
            if(collision(cPlant)){
                cPlant.takeDamage(this.strength);
                //TODO how much energy gets restored and based on what?
                //this.restoreEnergy(cPlant.);
            }
        }
        //Growth
        if(outputs[5] > .5){
            this.grow(outputs[5]);
        }
        //Healing
        if(outputs[6] > .5){
            this.restoreHealth(outputs[6] * 2);
        }
        //Attack
        if(outputs[7] > .5){
            if(collision(cAnimal)){
                //TODO consider strength of attacked animal
                cAnimal.takeDamage(this.strength * this.transform.velocity.magSq());
            }
        }
    }

    //TODO Test
    //TODO write documentation
    public void mate(Animal mate){
        if(this.maturity == 1 && mate.maturity == 1 && this.healthRatio() >= .5 && mate.healthRatio() >= .5){
            Animal self = this;
            //TODO: when do two organisms mate?

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
            }else{
                mate.mate(this);
            }
        }
    }

    //TODO Test
    //TODO write documentation
    @Override
    public Organism reproduce() {
        Organism child = null;
        if(this.gender.canBirth() && this.maturity == 1 && this.health >= .5) {
            child = new Animal(this, gender.getMate());
        }
        return child;
    }

    //TODO Test
    //TODO write documentation
    //Collision registration
    public boolean collision(Organism o){
        //check if this collides with something
        return this.getLoc().distSq(o.getLoc()) <= Math.pow(this.getR() + o.getR(), 2);
    }

    //TODO Test
    //TODO write documentation
    //Search for food
    public Organism searchClosestPlant(World w){
        assert !this.isDead() : "This is dead";

        ArrayList<Organism> foods = w.getGrid().getGridFieldsP(this.getLoc(), this.viewDistance);     //get all food in view Distance
        //calculate the closest organism
        return this.searchClosest(foods);
    }

    public Organism searchClosestAnimal(World w){
        assert !this.isDead() : "This is dead";

        ArrayList<Organism> animals = w.getGrid().getGridFieldsA(this.getLoc(), this.viewDistance);     //get all animals in view Distance
        //calculate the closest organism
        return this.searchClosest(animals);
    }

    public Animal searchClosestMate(World w){
        ArrayList<Animal> animals = w.getGrid().getGridFieldsA(this.getLoc(), this.viewDistance);

        Animal chosenMate = null;
        double mostAttractive = Double.NEGATIVE_INFINITY;

        for(Animal o : animals){
            double distance = this.getLoc().distSq(o.getLoc());
            double attractiveness = (1/distance) * o.getAttractiveness() * this.reproductiveUrge - this.attractiveness;
            //if the distance is smaller than the current closest distance and smaller than the viewDistance
            if((mostAttractive <= attractiveness) && (distance <= Math.pow(this.viewDistance,2))){
                mostAttractive = attractiveness;
                chosenMate = o;
            }
        }
        return chosenMate;
    }

    //TODO Test
    //TODO write documentation
    public Organism searchClosest(ArrayList<Organism> organisms){
        assert !this.isDead() : "This is dead";

        Organism closestOrganism = null;
        double closestDistance = Double.POSITIVE_INFINITY;

        //calculate the closest organism
        for(Organism o : organisms){
            double distance = this.getLoc().distSq(o.getLoc());
            //if the distance is smaller than the current closest distance and smaller than the viewDistance
            if((closestDistance >= distance) && (distance <= Math.pow(this.viewDistance,2))){
                closestDistance = distance;
                closestOrganism = o;
            }
        }
        return closestOrganism;
    }

    public double metabolismCost(){
        //TODO does this make sense? shouldn't more energy be used when bigger?
        return this.speed() / (2*this.size());
    }

    public double growthRate(){
        return this.growthScaleFactor/(1+this.growthMaturityFactor*Math.pow(this.maturity,this.growthMaturityExponent));
    }

    public double healthRatio(){
        return this.maxHealth/this.health;
    }

    public Vector2D seek(Vector2D target, int groupRatio){
        Vector2D desired = Vector2D.sub(target,this.transform.location);

        desired.setMag(this.maxSpeed * groupRatio);

        Vector2D steer = Vector2D.sub(desired,this.transform.velocity);
        steer.limit(this.maxForce);

        assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" +Math.pow(this.maxSpeed,2);
        return steer;
    }

    /**
     * Steer to avoid colliding with your neighbors
     * @param animals in the system
     * @return the steering vector
     */
    public Vector2D separate(ArrayList<Animal> animals){
        Vector2D sum = new Vector2D();
        Vector2D steer = new Vector2D();
        int count = 0; //of animals being too close

        for(Animal a : animals){
            //calculate distance of the two animals
            double distance = Vector2D.dist(this.getLoc(),a.getLoc());

            //here check distance > 0 to avoid an animal separation from itself
            if((distance>0) && (distance<this.separationDistance)){
                Vector2D difference = Vector2D.sub(this.getLoc(), a.getLoc());
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
        assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" + Math.pow(this.maxSpeed,2);
        return steer;
    }
    /**
     * Steer towards the center of your neighbors (stay within the group)
     * @param animals in the system
     * @return the steering vector
     */
    public Vector2D cohesion(ArrayList<Animal> animals){
        Vector2D sum = new Vector2D();
        int count = 0;
        int ratio = 0;

        for(Animal a : animals){
            double distance = Vector2D.dist(this.getLoc(),a.getLoc());
            if((distance > 0) && (distance < this.separationDistance*5)){
                if(distance < 0.5 * this.separationDistance*5) {
                    ratio++;
                }
                ratio++;
                sum.add(a.getLoc().negVectorCheck());
                count++;
            }
        }
        if(count > 0){
            sum.div(count);
            ratio/= count * 2;
            assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" + Math.pow(this.maxSpeed,2);
            return seek(sum,ratio);
        }else {
            assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" + Math.pow(this.maxSpeed,2);
            return new Vector2D();
        }
    }
    /**
     * Steer in the same direction as your neighbors
     * @param animals in the system
     * @return the steering vector
     */
    public Vector2D align(ArrayList<Animal> animals){
        Vector2D sum = new Vector2D();
        Vector2D steer = new Vector2D();
        int count = 0;

        for(Animal a : animals){
            double distance = Vector2D.dist(this.getLoc(),a.getLoc());
            if((distance > 0) && (distance < this.separationDistance*5)){
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
        assert this.invariant() : "Invariant is broken " + this.transform.velocity.magSq() + "/" + Math.pow(this.maxSpeed,2);
        return steer;
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

    public double getIncubationTime() {
        return incubationTime;
    }

    public void setIncubationTime(double incubationTime) {
        this.incubationTime = incubationTime;
    }

    public double getHatchTime() {
        return hatchTime;
    }

    public void setHatchTime(double hatchTime) {
        this.hatchTime = hatchTime;
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
