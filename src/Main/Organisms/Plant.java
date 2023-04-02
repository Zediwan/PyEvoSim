package Main.Organisms;

import Main.Helper.Transform;
import Main.Helper.Vector2D;
import Main.Organisms.Attributes.DNA.DNA;
import Main.Organisms.Attributes.DNA.Gene;
import Main.Simulation;

import java.awt.*;

public class Plant extends Organism {
    public static long plaCount = 0;

    public static double nutritionFactor;

    public static double growthFactor;
    public static double allMaxSize;
    public static double avgAge;
    public static double avgMaxHealth;
    public static double avgHealth;
    public static double avgHealthRatio;
    public static double avgMaxEnergy;
    public static double avgEnergy;
    public static double avgEnergyRatio;

    private static Plant blueprint;
    public static double bodyEnergyRatio = 1;
    public static int healthBodyRatio = 1;
    private double generation = 0;
    protected double growthTimer = 0;

    //------------------------------------------------DNA Variables----------------------------------------------------

    protected double spreadingRange;
    protected long growthInterval;

    //-----------------------------------------------------------------------------------------------------------------

    //Constructors
    public Plant(Transform transform, DNA dna){
        super(transform,dna);
        this.plaCount++;
        this.id = Plant.plaCount;
    }

    public Plant(Plant ancestor){
        super(ancestor);

        this.dna = ancestor.dna;
        this.dna.mutate(ancestor.getDna().getGene(5).getValue(), ancestor.getDna().getGene(4).getValue());

        Plant.plaCount++;
        this.id = Plant.plaCount;
        this.generation += ancestor.generation + 1;
        this.maturity = 1;

        this.expressGenes();
    }

    public Plant(){
        this(Plant.blueprint());
    }

    /*
    public Plant(){
        super();
        this.plaCount++;
        this.id = Plant.plaCount;
    }
     */

    //TODO Test
    //TODO write documentation
    //this is a singleton pattern
    public static Plant blueprint(){
        if(Plant.blueprint == null) {
            Transform t = new Transform();  //location is at (0,0)

            Gene[] genes = {
                    //TODO: set default parameters
                    new Gene(1, "sizeRatio"),
                    new Gene(128, "colorRed"),
                    new Gene(180, "colorGreen"),
                    new Gene(128, "colorBlue"),
                    new Gene(.1, "mutSizeDNA"),
                    new Gene(.01, "mutProbDNA"),
                    new Gene(.1, "mutSizeNN"),
                    new Gene(.01, "mutProbNN"),
                    new Gene(1, "attractiveness"),
                    new Gene(.5, "growthScaleFactor"),
                    new Gene(.5, "growthMaturityFactor"),
                    new Gene(.5, "growthMaturityExponent"),
                    new Gene(10, "spreadingRange"),
                    new Gene(10*1000, "growthInterval")
            };
            DNA dna = new DNA(genes);

            Plant blueprint = new Plant(t,dna);
            Plant.plaCount--;  //to not increase the counter when not needed
            blueprint.id = 0;

            Plant.blueprint = blueprint;
        }
        return Plant.blueprint;
    }

    @Override
    public void expressGenes() {
        super.expressGenes();
        int shift = Organism.numberOrganismGenes;
        this.spreadingRange = (int)Math.round(this.dna.getGene(shift+0).getValue());
        this.growthInterval = (int)Math.round(this.dna.getGene(shift+1).getValue());

        this.transform.setSize(Plant.allMaxSize * this.sizeRatio * this.maturity +3);
        this.transform.setShape(this.transform.getRectangle());
    }

    @Override
    public void update(Simulation s) {
        if(this.growthTimer <= 0){
            //this.grow(1);
            //this.growthTimer = this.growthInterval;
        }else{
            //this.growthTimer--;
        }
    }

    @Override
    public void grow(double factor) {
        double growth = this.growthRate()*factor;
        this.maturity += growth;
        double BPIncrease = 100 * growth * Math.pow(this.sizeRatio,2);
        this.useEnergy(BPIncrease * Plant.bodyEnergyRatio * (1+(1/Plant.healthBodyRatio)));
    }

    public Organism reproduce(Simulation s){
        Transform transform = this.transform.clone();

        //displace around the seed by the spreading range
        transform.getLocation().add(Vector2D.randSurroundingVec(this.spreadingRange));

        DNA newDNA = this.dna.copy();
        newDNA.mutate(this.mutProbDNA,this.mutSizeDNA);

        Plant p = new Plant(transform, newDNA);
        s.addPlant(p);

        return p;
    }

    //------------------------------------------------Getter and Setter------------------------------------------------

    public static double getGrowthFactor() {
        return growthFactor;
    }

    public static void setGrowthFactor(double growthFactor) {
        Plant.growthFactor = growthFactor;
    }

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
