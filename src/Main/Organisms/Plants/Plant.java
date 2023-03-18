package Main.Organisms.Plants;

import Main.Helper.Vector2D;
import Main.Organisms.Attributes.DNA.DNA;
import Main.Helper.Transform;
import Main.Organisms.Organism;
import java.awt.*;

public class Plant extends Organism {
    public static long plaCount = 0;

    public static double nutritionFactor;
    public static double growthFactor;
    protected double growthTimer = 0;

    //------------------------------------------------DNA Variables----------------------------------------------------

    protected double spreadingRange;
    protected double growthInterval;

    //-----------------------------------------------------------------------------------------------------------------

    //Constructors
    public Plant(Transform transform, DNA dna){
        super(transform,dna);
        this.plaCount++;
        this.id = Plant.plaCount;
    }

    public Plant(){
        super();
        this.plaCount++;
        this.id = Plant.plaCount;
    }

    @Override
    public void expressGenes() {
        super.expressGenes();
        int shift = Organism.numberOrganismGenes;
        this.spreadingRange = (int)Math.round(this.dna.getGene(shift+0).getValue());
        this.growthInterval = (int)Math.round(this.dna.getGene(shift+1).getValue());
    }

    @Override
    public void update() {
        if(this.growthTimer <= 0){
            this.grow();
            this.growthTimer = this.growthInterval;
        }else{
            this.growthTimer--;
        }
    }

    @Override
    public void grow() {
        this.transform.size *= Plant.growthFactor;
    }

    public Organism reproduce(DNA mateDNA){
        return this.reproduce();
    }

    public Organism reproduce(){
        Transform transform = this.transform.clone();

        //displace around the seed by the spreading range
        Vector2D displacement = Vector2D.randLimVec(this.spreadingRange,this.spreadingRange);
        displacement.sub(Vector2D.randLimVec(-this.spreadingRange,-this.spreadingRange).div(2));
        transform.getLocation().add(displacement);

        DNA newDNA = this.dna.copy();
        newDNA.mutate(this.mutProbDNA,this.mutSizeDNA);

        return new Plant(transform, newDNA);
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

    public void setGrowthInterval(double growthInterval) {
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

    }
}
