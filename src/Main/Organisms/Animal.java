package Main.Organisms;

import Main.Helper.Transform;
import Main.Helper.Vector2D;
import Main.NeuralNetwork.NeuralNetwork;
import Main.Organisms.Attributes.DNA.DNA;
import Main.Organisms.Attributes.DNA.Gene;
import Main.Organisms.Attributes.Gender;
import Main.Simulation;
import Main.SimulationGUI;
import Main.World;

import java.awt.*;
import java.awt.geom.Ellipse2D;
import java.util.ArrayList;
import java.util.Timer;
import java.util.TimerTask;

public class Animal extends Organism {
    public static long aniCount = 0;
    public static long aniBornCount = 0;
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
    private static Animal blueprint;

    public static double baseExhaustDmg = 1;
    public static double baseSize = 4;
    public static double allMaxSpeed = 4;
    public static double healthBodyRatio = 2;
    public static double bodyEnergyRatio = 2;
    public static double herdingThreshold = .5;
    public static double matingThreshold = .2;
    public static double eatingThreshold = .2;
    public static double growthThreshold = .5;
    public static double healingThreshold = .5;
    public static double attackThreshold = .5;
    public static double reproductiveUrgeFactor = 50;
    public static double damageFactor = 30;
    public static double healingFactor = 2;
    public static double healingCostFactor = 2;
    public static double metabolismFactor = 1;
    //private static double baseSize = 1;

    //TODO how should generations be handled when there are two parents?
    protected int generation = 0;
    protected Gender gender;
    protected NeuralNetwork nn;
    protected double reproductiveUrge = 0;
    //protected double bodyPoints = 0;

    //------------------------------------------------DNA Variables----------------------------------------------------

    protected double speedRatio;                    //[9]
    protected double strength;                      //[10]  //TODO: make this depend on size, via a ration or something
    protected long gestationDuration;               //[11]
    protected double maxForce;                      //[12]
    protected double maxSpeed;                      //[13]
    protected double viewAngle;                     //[14]
    protected double viewDistance;                  //[15]
    protected double timerFrequency;                //[16]
    protected double pheromoneSensibility;          //[17]
    protected double separationWeight;              //[18]
    protected double alignmentWeight;               //[19]
    protected double cohesionWeight;                //[20]
    protected double velocityWeight;                //[21]
    protected double separationDistance;            //[22]
    protected static int numberAnimalGenes = 14;

    //-----------------------------------------------------------------------------------------------------------------

    //Constructors
    //Used for population by system
    /*
    public Animal() {
        super();

        Animal.aniCount++;
        this.id = Animal.aniCount;

        this.dna = new DNA();
        this.expressGenes();
    }
     */
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

        this.maturity = 0 + mother.gestationDuration / (5*1000);

        this.expressGenes();
    }

    public Animal(Animal ancestor) {
        this(ancestor,ancestor);
    }

    public Animal(){
        this(Animal.blueprint());
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
                    new Gene(1, "sizeRatio"),
                    new Gene(128, "colorRed"),
                    new Gene(128, "colorGreen"),
                    new Gene(128, "colorBlue"),
                    new Gene(.5, "mutSizeDNA"),
                    new Gene(1, "mutProbDNA"),
                    new Gene(.1, "mutSizeNN"),
                    new Gene(1, "mutProbNN"),
                    new Gene(.5, "attractiveness"),
                    new Gene(.5, "growthScaleFactor"),
                    new Gene(.5, "growthMaturityFactor"),
                    new Gene(.5, "growthMaturityExponent"),
                    new Gene(.05, "speedRatio"),
                    new Gene(5, "strength"),
                    new Gene(5*1000, "gestationDuration"),
                    new Gene(.2, "maxForce"),
                    new Gene(1, "maxSpeed"),
                    new Gene(45, "viewAngle"),
                    new Gene(100, "viewDistance"),
                    new Gene(1, "timerFrequency"),
                    new Gene(1, "pheromoneSensibility"),
                    new Gene(.1, "separationWeight"),
                    new Gene(.1, "alignmentWeight"),
                    new Gene(.1, "cohesionWeight"),
                    new Gene(.1, "velocityWeight"),
                    new Gene(4, "separationDistance")
            };
            DNA dna = new DNA(genes);

            //TODO: check if these are the correct default amount of inputs
            NeuralNetwork nn = new NeuralNetwork(14, 36, 8);

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

        this.speedRatio = this.dna.getGene(shift+0).getValue();

        this.strength = this.dna.getGene(shift+1).getValue();

        this.gestationDuration = Math.round(this.dna.getGene(shift+2).getValue());

        this.maxForce = this.dna.getGene(shift+3).getValue();

        this.maxSpeed = this.dna.getGene(shift+4).getValue();

        this.viewAngle = this.dna.getGene(shift+5).getValue();

        this.viewDistance = this.dna.getGene(shift+6).getValue();

        this.timerFrequency = this.dna.getGene(shift+7).getValue();

        this.pheromoneSensibility = this.dna.getGene(shift+8).getValue();

        this.separationWeight = this.dna.getGene(shift+9).getValue();
        this.alignmentWeight = this.dna.getGene(shift+10).getValue();
        this.cohesionWeight = this.dna.getGene(shift + 11).getValue();
        this.velocityWeight = this.dna.getGene(shift+12).getValue();
        this.separationDistance = this.dna.getGene(shift + 13).getValue();

        this.transform.size = Animal.baseSize * this.sizeRatio * this.maturity+1;
        if(this.maxSpeed > Animal.allMaxSpeed){
            this.maxSpeed = Animal.allMaxSpeed;
        }
    }

    //TODO Test
    //TODO write documentation
    @Override
    public void update(Simulation s) {
        assert !this.isDead() : "this is dead";
        //TODO add physics so they can't run through into another and don't clip

        //System.out.println(this.healthRatio());

        this.think(s);
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

    //TODO Test
    //TODO write documentation
    public void think(Simulation s){
        World w = s.getWorld();
        ArrayList<Animal> animals = w.getAnimalQuadTree().query(this);
        Organism cPlant = this.searchClosestPlant(w);
        Organism cAnimal = this.searchClosestAnimal(w);

        double[] inputs = new double[]{
                1,
                this.energy,
                //Maturity,
                this.healthRatio(),
                this.speed(),
                cAnimal != null && this.getLoc().distSq(cAnimal.getLoc()) != 0 ? 1/this.getLoc().distSq(cAnimal.getLoc()) : 0,
                cAnimal != null ? Vector2D.angleBetween(this.getLoc(), cAnimal.getLoc()) : 0,
                cPlant != null && this.getLoc().distSq(cPlant.getLoc()) != 0 ? 1/this.getLoc().distSq(cPlant.getLoc()) : 0,
                cPlant != null ? Vector2D.angleBetween(this.getLoc(), cPlant.getLoc()) : 0,
                animals.size(),
                w.getPlantQuadTree().query(this).size(),
                cAnimal != null ? cAnimal.getColorRed() : 0,
                cAnimal != null ? cAnimal.getColorGreen() : 0,
                cAnimal != null ? cAnimal.getColorBlue() : 0,
                //clkTic: Internal timer (1s on, 1s off (actual period decided by genes))
                //clkMinut: kind of like a chronometer, counts time, gets reset by an output neuron
                this.getAge(),
        };

        double[] outputs = this.nn.predict(inputs);

        //Accelerate, Rotate
        this.transform.applyForce(Vector2D.fromAngle(outputs[0]-.5, this.transform.acceleration).setMag(outputs[1]-.5).limit(this.maxForce));

        //Herding Desire
        if(outputs[2] > Animal.herdingThreshold){
            this.transform.applyForce(separate(animals).setMag(this.separationWeight).limit(this.maxForce));
            this.transform.applyForce(cohesion(animals).setMag(this.cohesionWeight).limit(this.maxForce));
            this.transform.applyForce(align(animals).setMag(this.alignmentWeight).limit(this.maxForce));
        }

        //Mate Desire
        if(outputs[3] > Animal.matingThreshold){
            this.reproductiveUrge = outputs[3] * Animal.reproductiveUrgeFactor;
            Animal mate = this.searchClosestMate(w);
            if(this.collision(mate)){
                this.mate(mate, s);
            }
            /*
            else{
                this.seek(mate.getLoc(),1);
            }
             */
        }

        //Eat Desire
        if(outputs[4] > Animal.eatingThreshold){
            if(collision(cPlant)){
                double damage = this.strength * Animal.damageFactor;
                cPlant.takeDamage(damage);
                //TODO how much energy gets restored and based on what?
                this.restoreEnergy(damage);
                if(cPlant.getHealth() <= 0){
                    this.plantsKilled++;
                }
            }
        }

        //Growth
        if(outputs[5] > Animal.growthThreshold){
            this.grow(outputs[5]);
        }

        //Healing
        if(outputs[6] > Animal.healingThreshold){
            this.useEnergy(outputs[6] * Animal.healingFactor);//Animal.healingCostFactor);
            this.restoreHealth(outputs[6] * Animal.healingFactor);
        }

        //Attack
        if(outputs[7] > Animal.attackThreshold){
            if(collision(cAnimal)){
                //TODO consider strength of attacked animal
                cAnimal.takeDamage(this.strength * this.transform.velocity.magSq());
                if(cAnimal.getHealth() <= 0){
                    this.animalsKilled++;
                }
            }
        }
    }

    @Override
    public void grow(double factor) {
        double growth = this.growthRate()*factor;
        this.maturity += growth;
        double BPIncrease = 100 * growth * Math.pow(this.sizeRatio,2);
        this.useEnergy(BPIncrease * Animal.bodyEnergyRatio * (1+(1/Animal.healthBodyRatio)));
    }

    public Animal searchClosestMate(World w){
        //ArrayList<Animal> animals = w.getGrid().getGridFieldsA(this.getLoc(), this.viewDistance);
        ArrayList<Animal> animals = w.getAnimalQuadTree().query(this);


        Animal chosenMate = null;
        double mostAttractive = Double.NEGATIVE_INFINITY;

        for(Animal o : animals){
            double distance = this.getLoc().distSq(o.getLoc());
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

    public boolean wantsToMate(Animal a) {
        assert this != a : "wantsToMate on itself";

        if(this.reproductiveUrge <= 0){
            return false;
        }
        else{
            return this.attractiveness * (1 / this.reproductiveUrge) <= a.attractiveness;
        }
    }

    public boolean correctGenderComb(Animal mate){
        return this.gender.correctGender(mate.gender);
    }

    public boolean canMate(){
        return this.healthRatio() >= .5 && this.maturity >= 1;
    }

    //TODO Test
    //TODO write documentation
    public void mate(Animal mate, Simulation s){
        assert this.correctGenderComb(mate) : "Wrong gender combination";
        assert this.canMate();
        assert mate.canMate();

        Animal self = this;

        if (this.gender == Gender.FEMALE && mate.gender == Gender.MALE) {
            if (!this.gender.isPregnant()) { // check if not already pregnant

                new Timer().schedule(new TimerTask() {
                    @Override
                    public void run() {
                        self.reproduce(s);
                    }
                }, this.gestationDuration);

                this.gender.getPregnant(mate); // set pregnant flag
            }
        }
        else if (this.gender == Gender.MALE && mate.gender == Gender.FEMALE) {
            mate.mate(this, s);
        }
    }

    //TODO Test
    //TODO write documentation
    @Override
    public Organism reproduce(Simulation s) {
        assert this.gender.canBirth() : "this can't birth";

        Animal child = new Animal(this.gender.getMate(),this);
        s.addAnimal(child);

        Animal.aniBornCount++;
        this.offspringBirthed++;
        this.gender.giveBirth();

        return child;
    }

    //TODO Test
    //TODO write documentation
    //Collision registration
    public boolean collision(Organism o){
        //check if this collides with something
        if(o == null){
            return false;
        }
        else{
            return this.getLoc().distSq(o.getLoc()) <= Math.pow(this.getR() + o.getR(), 2);
        }
    }

    //TODO Test
    //TODO write documentation
    //Search for food
    public Plant searchClosestPlant(World w){
        assert !this.isDead() : "This is dead";

        //ArrayList<Organism> foods = w.getGrid().getGridFieldsP(this.getLoc(), this.viewDistance);     //get all food in view Distance
        ArrayList<Plant> plants = w.getPlantQuadTree().query(this);

        //calculate the closest organism
        assert !this.isDead() : "This is dead";

        Plant closestOrganism = null;
        double closestDistance = Double.POSITIVE_INFINITY;

        //calculate the closest organism
        for(Plant p : plants){
            double distance = this.getLoc().distSq(p.getLoc());
            //if the distance is smaller than the current closest distance and smaller than the viewDistance
            if((closestDistance >= distance) && (distance <= Math.pow(this.viewDistance,2)) && (p.getId() != this.id)){
                closestDistance = distance;
                closestOrganism = p;
            }
        }
        return closestOrganism;
    }

    public Organism searchClosestAnimal(World w){
        assert !this.isDead() : "This is dead";

        //ArrayList<Organism> animals = w.getGrid().getGridFieldsA(this.getLoc(), this.viewDistance);     //get all animals in view Distance
        ArrayList<Animal> animals = w.getAnimalQuadTree().query(this);

        //calculate the closest organism
        Animal closestAnimal = null;
        double closestDistance = Double.POSITIVE_INFINITY;

        //calculate the closest organism
        for(Animal a : animals){
            double distance = this.getLoc().distSq(a.getLoc());
            //if the distance is smaller than the current closest distance and smaller than the viewDistance
            if((closestDistance >= distance) && (distance <= Math.pow(this.viewDistance,2)) && (a.getId() != this.id)){
                closestDistance = distance;
                closestAnimal = a;
            }
        }
        return closestAnimal;
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
            if((closestDistance >= distance) && (distance <= Math.pow(this.viewDistance,2)) && (o.getId() != this.id)){
                closestDistance = distance;
                closestOrganism = o;
            }
        }
        return closestOrganism;
    }

    public double metabolismCost(){
        //TODO does this make sense? shouldn't more energy be used when bigger?
        return (this.speed()*Animal.metabolismFactor) / (2*this.size());
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

    //TODO maybe refactor into Transform class?
    public Ellipse2D getSensoryRadius(){
        return new Ellipse2D.Double(this.getLocX() - this.getR() - this.viewDistance/2, this.getLocY() - this.getR() - this.viewDistance/2, this.size() + this.viewDistance, this.size() + this.viewDistance);
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

    @Override
    public void paint(Graphics2D g) {
        super.paint(g);
        g.fill(this.transform.getRectangle());
        if(SimulationGUI.showHealth){
            g.setColor(this.color.darker());
            g.drawString(String.format("%.2f", this.health), (int)this.getLocX(), (int)this.getLocY());
        }
        if(SimulationGUI.showEnergy){
            g.setColor(this.color.brighter());
            g.drawString(String.format("%.2f", this.energy), (int)this.getLocX(), (int)this.getLocY()+10);
        }
        //g.drawString(String.format("%.2f", this.healthRatio()), (int)this.getLocX(), (int)this.getLocY());
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
