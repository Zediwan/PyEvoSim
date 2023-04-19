package Main.Organisms;

import Main.GUI.SimulationGUI;
import Main.Helper.Transform;
import Main.Helper.Vector2D;
import Main.Organisms.Attributes.DNA.DNA;
import Main.World.Simulation;
import Main.World.World;

import java.awt.*;

//TODO create tests for all the methods

/**
 *
 * The abstract class representing an organism in the simulation.
 * This class contains variables and methods that are common to all organisms in the simulation.
 * Organisms are represented by their DNA and a Transform object, which contains information about their location,
 * rotation, and scale in the simulation. Organisms can also move, grow, and reproduce.
 * The variables and methods in this class are not meant to be accessed directly by other classes, but rather
 * through the public methods in the subclasses.
 *
 * @author Jeremy Moser
 * @since 02.04.2023
 * @see Animal
 * @see Plant
 */
public abstract class Organism {
    /**
     * All time amount of organisms
     * */
    public static long orgCount = 0;
    /**
     * This is used to scale maxEnergy in relation to the BodyPoints
     */
    private static double maxEnergyToBodyRatio = 3;

    /**
     * Holds all physical information about an Organism
     * @see Transform
     */
    protected Transform transform;

    /**
     * This holds the genetic Information used to create an Organism
     */
    protected DNA dna;

    /**
     * Time of birth
     */
    protected long birt = 0;
    /**
     * identification number
     */
    protected double id;
    /**
     * amount of animals that this has killed
     */
    protected int animalsKilled = 0;
    /**
     * amount of plants this has killed
     */
    protected int plantsKilled = 0;
    /**
     * amount of offspring this has birthed
     */
    protected int offspringBirthed = 0;

    /**
     * current health of this
     */
    protected double health;
    /**
     * current energy of this
     */
    protected double energy;
    /**
     * color of this
     */
    protected Color color;
    /**
     * maturity of this
     */
    protected double maturity;

    //------------------------------------------------DNA Variables----------------------------------------------------

    /**
     * Gene number 0
     * <p> TODO add description </p>
     * <p> Positive value </p>
     */
    protected double sizeRatio;
    /**
     * Gene number 1
     * <p> Represents the red value of this color </p>
     * <p> Value between 0 and 255 </p>
     */
    protected int colorRed;
    /**
     * Gene number 2
     * <p> Represents the green value of this color </p>
     * <p> Value between 0 and 255 </p>
     */
    protected int colorGreen;
    /**
     * Gene number 3
     * <p> Represents the blue value of this color </p>
     * <p> Value between 0 and 255 </p>
     */
    protected int colorBlue;
    /**
     * Gene number 4
     * <p> How much DNA genes can mutate when they do </p>
     */
    protected double mutSizeDNA;
    /**
     * Gene number 5
     * <p> How likely it is for genes of the DNA to mutate </p>
     * <p> Value between 0 and 1 </p>
     */
    protected double mutProbDNA;
    /**
     * Gene number 6
     * <p> How much the biases and weights of the brain can mutate when they do </p>
     */
    protected double mutSizeNN;
    /**
     * Gene number 7
     * <p> How likely it is for brain wiring to mutate </p>
     * <p> Value between 0 and 1 </p>
     */
    protected double mutProbNN;
    /**
     * Gene number 8
     * <p> The objective attractiveness of this </p>
     * @see Animal#wantsToMate(Animal)
     * @see Animal#searchClosestMate(World) 
     */
    protected double attractiveness;
    /**
     * Gene number 9
     * <p> Used to calculate the growth rate </p>
     * @see #growthRate()
     * @see Animal#grow(double) 
     * @see Plant#grow(double) 
     */
    protected double growthScaleFactor;
    /**
     * Gene number 10
     * <p> Used to calculate the growth rate </p>
     * @see #growthRate()
     * @see Animal#grow(double)
     * @see Plant#grow(double)
     */
    protected double growthMaturityFactor;
    /**
     * Gene number 11
     * <p> Used to calculate the growth rate </p>
     * @see #growthRate()
     * @see Animal#grow(double)
     * @see Plant#grow(double)
     */
    protected double growthMaturityExponent;
    /**
     * used as a shift value when expressing genes of children classes
     * @see Animal#expressGenes()
     * @see Plant#expressGenes()
     */
    protected static int numberOrganismGenes = 12;

    //-----------------------------------------------------------------------------------------------------------------

    /**
     * Creates a new Organism instance with genetic material from the given father and mother organisms.
     *
     * @param father The father organism to inherit genetic material from.
     * @param mother The mother organism to inherit genetic material from.
     * @throws AssertionError if the father or mother organisms are null.
     */
    public Organism(Organism father, Organism mother){
        assert father != null : "first organism is null";
        assert mother != null : "second organism is null";

        this.transform = new Transform(
                mother.getLocation().copy().
                        add(Vector2D.randSurroundingVec(mother.transform.getSize()*2))
        );

        this.birt = System.currentTimeMillis();

        Organism.orgCount++;
    }

    /**
     * Creates a new Organism instance with genetic material from a single ancestor.
     *
     * @param ancestor of this organism
     * @see #Organism(Organism, Organism)
     */
    public Organism(Organism ancestor){
        this(ancestor,ancestor);
    }

    /**
     * Constructs a new Organism with the given Transform and DNA.
     *
     * @param transform the initial transform of the organism
     * @param dna of the Organism
     */
    public Organism(Transform transform, DNA dna){
        this.transform = transform.clone();
        this.dna = dna.copy();
        this.birt = System.currentTimeMillis();

        Organism.orgCount++;
    }

    /**
     * Expresses the genes of the organism, retrieving and setting values for the different DNA genes.
     * The genes are stored in the DNA object, which is an attribute of the organism.
     * Each gene is accessed and its value is checked and set within specific bounds, and then used to set the values of
     * the corresponding attributes of the organism.
     * <p>
     *     Genes:
     *     <ul>
     *         <li>[0] sizeRatio: size ratio of the organism</li>
     *         <li>[1] colorRed: red component of the color of the organism (0-255)</li>
     *         <li>[2] colorGreen: green component of the color of the organism (0-255)</li>
     *         <li>[3] colorBlue: blue component of the color of the organism (0-255)</li>
     *         <li>[4] mutSizeDNA: mutation size for DNA genes</li>
     *         <li>[5] mutProbDNA: mutation probability for DNA genes</li>
     *         <li>[6] mutSizeNN: mutation size for neural network genes</li>
     *         <li>[7] mutProbNN: mutation probability for neural network genes</li>
     *         <li>[8] attractiveness: attractiveness of the organism</li>
     *         <li>[9] growthScaleFactor: growth scale factor for the organism</li>
     *         <li>[10] growthMaturityFactor: growth maturity factor for the organism</li>
     *         <li>[11] growthMaturityExponent: growth maturity exponent for the organism</li>
     *     </ul>
     * </p>
     * The values of health and energy are set to their maximum value, and the color of the organism is set using the
     * red, green, and blue components retrieved from the DNA genes.
     * @see DNA
     */
    public void expressGenes(){
        this.dna.getGene(0).genePositiveCheck();
        this.sizeRatio = this.dna.getGene(0).getValue();

        this.dna.getGene(1).geneBoundCheck(0,255);
        this.colorRed = (int)Math.round(this.dna.getGene(1).getValue());
        this.dna.getGene(2).geneBoundCheck(0,255);
        this.colorGreen = (int)Math.round(this.dna.getGene(2).getValue());
        this.dna.getGene(3).geneBoundCheck(0,255);
        this.colorBlue = (int)Math.round(this.dna.getGene(3).getValue());

        this.dna.getGene(4).gene0to1Check();
        this.mutSizeDNA = this.dna.getGene(4).getValue();

        this.dna.getGene(5).gene0to1Check();
        this.mutProbDNA = this.dna.getGene(5).getValue();

        this.mutSizeNN = this.dna.getGene(6).getValue();

        this.dna.getGene(6).gene0to1Check();
        this.mutProbNN = this.dna.getGene(7).getValue();

        this.attractiveness = this.dna.getGene(8).getValue();

        this.dna.getGene(9).genePositiveCheck();
        this.growthScaleFactor = this.dna.getGene(9).getValue();
        this.dna.getGene(10).genePositiveCheck();
        this.growthMaturityFactor = this.dna.getGene(10).getValue();
        this.growthMaturityExponent = this.dna.getGene(11).getValue();

        //each animal starts with health and energy at max value
        //TODO think of a better way to do this
        this.health = this.maxHealth();
        this.energy = this.maxEnergy();

        assert this.colorRed <= 255 && this.colorRed >= 0 : "R Value is not in range " + this.colorRed;
        assert this.colorGreen <= 255 && this.colorGreen >= 0 : "G Value is not in range " + this.colorGreen;
        assert this.colorBlue <= 255 && this.colorBlue >= 0 : "B Value is not in range " + this.colorBlue;
        this.color = new Color(this.colorRed,this.colorGreen,this.colorBlue);
    }

    public abstract void update(Simulation s);

    public abstract void grow(double factor);

    public abstract Organism reproduce(Simulation s);

    /**
     * Calculates the maximum health of this organism based on its current maturity and size ratio.
     * <p>The formula used is: {@code 100 * maturity * Math.pow(sizeRatio,2)}.</p>
     *
     * @return The maximum health of this organism.
     */
    public double maxHealth() {
        return 100 * this.maturity * Math.pow(this.sizeRatio,2);
    }

    /**
     * Calculates the health ratio
     *
     * @return health ratio
     */
    public double healthRatio(){
        assert this.maxHealth() >= this.health;
        return this.health/this.maxHealth();
    }


    /**
     * Calculates the maximum amount of energy an organism can have
     * based on its maximum health and a fixed energy-to-body ratio.
     *
     * @return The maximum energy of the organism.
     */
    public double maxEnergy(){
        return this.maxHealth() * Organism.maxEnergyToBodyRatio;
    }

    /**
     * Calculates the energy ratio
     *
     * @return energy ratio
     */
    public double energyRatio() {
        assert this.maxEnergy() >= this.energy;
        return this.energy/this.maxEnergy();
    }

    /**
     * Calculates the growth rate of this organism based on its maturity level and growth parameters.
     *
     * @return the growth rate of this organism
     */
    public double growthRate(){
        return this.growthScaleFactor/(1+this.growthMaturityFactor*Math.pow(this.maturity,this.growthMaturityExponent));
    }

    /**
     * Translates the graphics context to the location of this object.
     *
     * @param g the graphics context to be translated
     */
    protected void translateGraphics(Graphics2D g) {
        g.translate(this.getLocX(), this.getLocY());
    }

    //------------------------------------------------Getter and Setter------------------------------------------------

    public boolean isDead(){
        return health <= 0;
    }

    /**
     * Updates the color of the organism
     */
    public void refreshColor() {
        this.color = new Color(this.colorRed,this.colorGreen,this.colorBlue);
    }

    /**
     * @return age in seconds
     */
    public double getAge(){
        return (double)(System.currentTimeMillis()-this.birt)/1000.0;
    }

    public Transform getTransform() {
        return this.transform;
    }

    public void setTransform(Transform transform) {
        this.transform = transform;
    }

    public double getR() {
        return this.transform.getR();
    }

    public Vector2D getLocation() {
        return this.transform.getLocation();
    }

    public void setLocation(Vector2D location) {
        this.transform.setLocation(location);
    }

    public double getLocX() {
        return this.transform.getLocX();
    }

    public void setLocX(float x) {
        this.transform.setLocX(x);
    }

    public double getLocY() {
        return this.transform.getLocY();
    }

    public void setLocY(float y) {
        this.transform.setLocY(y);
    }

    public DNA getDna() {
        return dna;
    }

    public void setDna(DNA dna) {
        this.dna = dna;
    }

    public long getBirt() {
        return birt;
    }

    public double getId() {
        return id;
    }

    public void setId(double id) {
        this.id = id;
    }

    public double getSizeRatio() {
        return sizeRatio;
    }

    public void setSizeRatio(double sizeRatio) {
        this.sizeRatio = sizeRatio;
    }

    public int getColorRed() {
        return colorRed;
    }

    public void setColorRed(int colorRed) {
        this.colorRed = colorRed;
    }

    public int getColorGreen() {
        return colorGreen;
    }

    public void setColorGreen(int colorGreen) {
        this.colorGreen = colorGreen;
    }

    public int getColorBlue() {
        return colorBlue;
    }

    public void setColorBlue(int colorBlue) {
        this.colorBlue = colorBlue;
    }

    public Color getColor() {
        return color;
    }

    public void setColor(Color color) {
        this.color = color;
    }

    public double getMutSizeDNA() {
        return mutSizeDNA;
    }

    public void setMutSizeDNA(double mutSizeDNA) {
        this.mutSizeDNA = mutSizeDNA;
    }

    public double getMutProbDNA() {
        return mutProbDNA;
    }

    public void setMutProbDNA(double mutProbDNA) {
        this.mutProbDNA = mutProbDNA;
    }

    public double getMutSizeNN() {
        return mutSizeNN;
    }

    public void setMutSizeNN(double mutSizeNN) {
        this.mutSizeNN = mutSizeNN;
    }

    public double getMutProbNN() {
        return mutProbNN;
    }

    public void setMutProbNN(double mutProbNN) {
        this.mutProbNN = mutProbNN;
    }

    public double getAttractiveness() {
        return attractiveness;
    }

    public void setAttractiveness(double attractiveness) {
        this.attractiveness = attractiveness;
    }

    public double getHealth() {
        return this.health;
    }

    public void setHealth(double health) {
        this.health = health;
        assert this.health <= this.maxHealth();
    }

    /**
     * Updates the organism's health by subtracting the given damage.
     * If the damage is negative, it will be added to the organism's health.
     * If the damage is positive, it will be subtracted from the organism's health.
     *
     * @param damage the amount of damage to subtract or add to the organism's health
     * @throws AssertionError if health is higher than maxHealth
     */
    public void takeDamage(double damage) {
        //if the damage is negative it should be added to remove the right amount and not add to the health
        if(damage <= 0){
            this.health += damage;
        }
        //if the damage is positive the amount should be subtracted
        else{
            this.health -= damage;
        }
        assert this.health <= this.maxHealth();
    }

    /**
     * Restores the organism's health by a specified amount.
     *
     * @param restoredHealth the amount of health to be restored
     * @throws AssertionError if the restored amount is negative
     */
    public void restoreHealth(double restoredHealth) {
        assert restoredHealth >= 0 : "restored amount is negative";

        this.health += restoredHealth;
        if(this.health > maxHealth()){
            this.health = maxHealth();
        }
    }

    public double getEnergy(){
        return this.energy;
    }

    public void setEnergy(double energy){
        this.energy = energy;
        if(this.energy > this.maxEnergy()){
            this.energy = this.maxEnergy();
        }
    }

    /**
     * Reduces the energy of the organism by the given amount. If the organism has enough energy,
     * the energy is simply reduced by the given amount. If not, the organism takes damage equal to
     * the difference between the energy used and the current energy.
     *
     * @param energyUsed the amount of energy to be used
     * @throws AssertionError if the energy used is negative
     */
    public void useEnergy(double energyUsed){
        assert energyUsed >= 0 : "energy used is negative";

        if(this.energy >= energyUsed){
            this.energy -= energyUsed;
        }
        else{
            double rest = energyUsed-this.energy;
            this.energy = 0;
            this.takeDamage(rest);
        }
    }

    public void restoreEnergy(double restoreEnergy) {
        assert restoreEnergy >= 0 : "restored amount is negative";

        this.energy += restoreEnergy;
        if(this.energy > this.maxEnergy()){
            this.energy = this.maxEnergy();
        }
    }

    public int getAnimalsKilled() {
        return animalsKilled;
    }

    public void setAnimalsKilled(int animalsKilled) {
        this.animalsKilled = animalsKilled;
    }

    public void incrementAnimalsKilled() {
        this.animalsKilled++;
    }

    public int getPlantsKilled() {
        return plantsKilled;
    }

    public void setPlantsKilled(int plantsKilled) {
        this.plantsKilled = plantsKilled;
    }

    public void incrementPlantsKilled() {
        this.plantsKilled++;
    }

    public int getOffspringBirthed() {
        return offspringBirthed;
    }

    public void setOffspringBirthed(int offspringBirthed) {
        this.offspringBirthed = offspringBirthed;
    }

    public void incrementOffspringBirthed() {
        this.offspringBirthed++;
    }

    public void setBirt(long birt) {
        this.birt = birt;
    }

    public double getMaturity() {
        return maturity;
    }

    public void setMaturity(double maturity) {
        this.maturity = maturity;
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

    public static int getNumberOrganismGenes() {
        return numberOrganismGenes;
    }

    public static void setNumberOrganismGenes(int numberOrganismGenes) {
        Organism.numberOrganismGenes = numberOrganismGenes;
    }

    //------------------------------------------------toString and paint-----------------------------------------------

    public String toString(){
        return this.id + "";
    }

    public void paint(Graphics2D g){
        g.setColor(this.color);
    }

    /**
     * Paints the health and energy statistics of the animal, if enabled by the {@link SimulationGUI} settings.
     *
     * @param g the graphics context to use for painting
     * @since 12.04.2023
     * TODO progress bars
     * TODO box that forms next to the organism
     */
    protected void paintStats(Graphics2D g) {
        // Paint the health statistic
        if (SimulationGUI.showHealth) {
            // Set the color to a darker version of the animal's color
            g.setColor(this.color.darker());

            // Draw the health value as a string at the animal's location
            g.drawString(String.format("%1$,.1f", this.health), this.getLocation().getRoundedX(), this.getLocation().getRoundedY());
        }

        // Paint the energy statistic
        if (SimulationGUI.showEnergy) {
            // Set the color to a brighter version of the animal's color
            g.setColor(this.color.brighter());

            // Draw the energy value as a string above the animal's location
            g.drawString(String.format("%1$,.1f", this.energy), this.getLocation().getRoundedX(), this.getLocation().getRoundedY() - 10);
        }
    }

}
