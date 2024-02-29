package Main.Organisms;

import Main.Helper.Transform;
import Main.Helper.Vector2D;
import Main.Organisms.Attributes.DNA.DNA;
import Main.Organisms.Attributes.DNA.Gene;
import Main.Organisms.Attributes.DNA.GeneType;
import Main.World.Simulation;

import java.awt.*;

public class Plant extends Organism {
    /**
     * is a static variable that keeps track of the total number of instances of the Plant class that have been created.
     */
    public static long plaCount = 0;

    /**
     * is a static variable that determines the amount of energy that the plant can provide to herbivorous organisms.
     */
    public static double nutritionFactor;

    /**
     * is a static variable that determines the rate at which the plant grows.
     */
    //public static double growthFactor;

    /**
     * is a static variable that keeps track of the maximum size of all the plants in the simulation.
     */
    public static double allMaxSize = 2;
    /**
     * is a static variable that keeps track of the average age of all the plants in the simulation.
     */
    public static double avgAge;
    /**
     *  is a static variable that keeps track of the average maximum health of all the plants in the simulation.
     */
    public static double avgMaxHealth;
    /**
     * is a static variable that keeps track of the average health of all the plants in the simulation.
     */
    public static double avgHealth;
    /**
     *  is a static variable that keeps track of the average health ratio (current health / max health) of all the plants in the simulation.
     */
    public static double avgHealthRatio;
    /**
     * is a static variable that keeps track of the average maximum energy of all the plants in the simulation.
     */
    public static double avgMaxEnergy;
    /**
     * is a static variable that keeps track of the average energy of all the plants in the simulation.
     */
    public static double avgEnergy;
    /**
     * is a static variable that keeps track of the average energy ratio (current energy / max energy) of all the plants in the simulation.
     */
    public static double avgEnergyRatio;
    /**
     * is a static variable that contains a blueprint of the Plant class, which can be used to create new instances of the class.
     */
    private static Plant blueprint;
    /**
     * is a static variable that determines the ratio of the plant's energy that is allocated to its body.
     */
    public static double bodyEnergyRatio = 1;
    /**
     * is a static variable that determines the ratio of the plant's health that is allocated to its body.
     */
    public static int healthBodyRatio = 1;
    /**
     * The minimum growth interval for a plant to grow.
     */
    private static long minGrowthInterval;
    /**
     * is a variable that keeps track of the generation of the plant.
     */
    private double generation = 0;
    /**
     * is a variable that keeps track of the time since the plant last grew.
     */
    protected double growthTimer = 0;

    //------------------------------------------------DNA Variables----------------------------------------------------

    /**
     * is a variable that determines the range of the plant's seeds when it spreads.
     */
    protected double spreadingRange;
    /**
     * is a variable that determines the time interval between two consecutive growth stages of the plant (in seconds).
     */
    protected long growthInterval;

    //-----------------------------------------------------------------------------------------------------------------

    //Constructors
    /**
     * Constructs a new Plant object with the given Transform and DNA.
     *
     * @param transform the Transform object that defines the position, size, and velocity of the Plant.
     * @param dna the DNA object that stores genetic information for the Plant.
     */
    public Plant(Transform transform, DNA dna){
        super(transform,dna);
        this.plaCount++;
        this.id = Plant.plaCount;
    }

    /**
     * Constructs a new Plant object with the genetic information of an ancestor Plant object.
     * The new Plant will have the same DNA, with a small chance of mutation.
     *
     * @param ancestor the ancestor Plant object to inherit genetic information from.
     */
    public Plant(Plant ancestor){
        super(ancestor);

        this.dna = ancestor.dna;
        this.dna.percentageMutate(ancestor.getMutProbDNA(), ancestor.getMutSizeDNA());

        Plant.plaCount++;
        this.id = Plant.plaCount;
        this.generation += ancestor.generation + 1;
        this.maturity = 1;

        this.expressGenes();
    }

    /**
     * Constructs a new Plant object using the default blueprint.
     */
    public Plant(){
        this(Plant.blueprint());
    }

    /**
     * This class method returns a blueprint plant with default parameters
     * to be used as a template for the creation of new plants.
     * This is a singleton pattern method that creates the blueprint only once.
     *
     * @return The blueprint plant with default parameters.
     */
    public static Plant blueprint(){
        if(Plant.blueprint == null) {
            Transform t = new Transform();  //location is at (0,0)

            Gene[] genes = {
                    //TODO: set default parameters
                    new Gene(1, "sizeRatio", GeneType.SMALLER),
                    new Gene(128, "colorRed", GeneType.COLOR),
                    new Gene(180, "colorGreen", GeneType.COLOR),
                    new Gene(128, "colorBlue", GeneType.COLOR),
                    new Gene(.1, "mutSizeDNA", GeneType.SMALLER),
                    new Gene(.01, "mutProbDNA", GeneType.PROBABILITY),
                    new Gene(.1, "mutSizeNN", GeneType.PROBABILITY),
                    new Gene(.01, "mutProbNN", GeneType.PROBABILITY),
                    new Gene(1, "attractiveness", GeneType.SMALLER),
                    new Gene(1, "growthScaleFactor", GeneType.SMALLER),
                    new Gene(20, "growthMaturityFactor", GeneType.BIGGER),
                    new Gene(1, "growthMaturityExponent", GeneType.SMALLER),
                    new Gene(10, "spreadingRange", GeneType.SMALLER),
                    new Gene(10*1000, "growthInterval", GeneType.TIME)
            };
            DNA dna = new DNA(genes);

            Plant blueprint = new Plant(t,dna);
            Plant.plaCount--;  //to not increase the counter when not needed
            blueprint.id = 0;

            Plant.blueprint = blueprint;
        }
        return Plant.blueprint;
    }

    /**
     * Overrides the expressGenes method in the Organism class to express the genes specific to plants.
     * The method updates the values of the spreadingRange, growthInterval, and the size of the plant according to the
     * values of the genes in the plant's DNA.
     */
    @Override
    public void expressGenes() {
        super.expressGenes(); // Expresses the genes common to all organisms

        // Express the genes specific to plants
        int shift = Organism.numberOrganismGenes;

        //Update spreading range
        this.dna.getGene(shift+0).genePositiveCheck();
        this.spreadingRange = (int)Math.round(this.dna.getGene(shift+0).getValue());

        //Update growth interval
        this.dna.getGene(shift+1).geneBoundCheck(Plant.minGrowthInterval, Long.MAX_VALUE);
        this.growthInterval = (int)Math.round(this.dna.getGene(shift+1).getValue());

        // Update plant size
        this.transform.setSize(Plant.allMaxSize * this.sizeRatio * this.maturity +1);
    }

    /**
     * This method updates the plant's state in the simulation.
     * If the growth timer is less than or equal to zero, it calls the grow method with a factor of 1,
     * which will grow the plant by the growth rate for one growth interval.
     * If the growth timer is greater than zero, it decreases the growth timer.
     *
     * @param s the simulation object
     */
    @Override
    public void update(Simulation s) {
        if(this.growthTimer <= 0){
            //this.grow(1);
            //this.growthTimer = this.growthInterval;
        }
        else{
            //this.growthTimer--;
        }
    }

    /**
     * This method grows the plant by a specified factor, increasing its maturity and using energy.
     * It asserts that the old maturity is less than or equal to the new maturity.
     *
     * @param factor the factor by which to grow the plant
     */
    @Override
    public void grow(double factor) {
        assert factor > 0 : "factor is 0 or less";
        double oldMaturity = this.maturity;

        double growth = this.growthRate()*factor;
        this.setMaturity(this.maturity+growth);
        double BPIncrease = 100 * growth * Math.pow(this.sizeRatio,2);
        this.useEnergy(BPIncrease * Plant.bodyEnergyRatio * (1+(1/Plant.healthBodyRatio)));

        assert oldMaturity <= this.maturity;
    }

    /**
     * Reproduces the plant by creating a new plant with a mutated copy of its DNA, and adds the new plant to the simulation.
     *
     * @param s the simulation in which the plant will be added
     * @return the new plant
     */
    public Plant reproduce(Simulation s){
        Transform transform = this.transform.clone();

        // displace around the seed by the spreading range
        transform.getLocation().add(Vector2D.randSurroundingVec(this.spreadingRange));

        DNA newDNA = this.dna.copy();
        newDNA.rangedMutate(this.mutProbDNA,this.mutSizeDNA);

        Plant p = new Plant(transform, newDNA);
        s.addPlant(p);

        return p;
    }


    //------------------------------------------------Getter and Setter------------------------------------------------

    public double getSpreadingRange() {
        return spreadingRange;
    }

    public void setSpreadingRange(double spreadingRange) {
        this.spreadingRange = spreadingRange;
    }

    public double getGrowthInterval() {
        return growthInterval;
    }

    public void setGrowthInterval(long growthInterval) {
        this.growthInterval = growthInterval;
    }

    public double getGrowthTimer() {
        return growthTimer;
    }

    public void setGrowthTimer(double growthTimer) {
        this.growthTimer = growthTimer;
    }

    //------------------------------------------------toString and paint-----------------------------------------------

    @Override
    public void paint(Graphics2D g) {
        g.setColor(this.color);
        g.fillOval((int)(this.getLocX()-(this.getR())),
                (int)(this.getLocY()-(this.getR())),
                (int)this.transform.getSize(), (int)this.transform.getSize());
    }
}
