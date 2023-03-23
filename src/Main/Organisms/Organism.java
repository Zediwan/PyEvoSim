package Main.Organisms;

import Main.Organisms.Attributes.DNA.DNA;
import Main.Helper.Transform;
import Main.Helper.Vector2D;
import Main.World;

import java.awt.*;

public abstract class Organism {
    public static long orgCount = 0;

    protected Transform transform;
    protected DNA dna;
    protected long birt = 0;
    protected double id;
    protected double maxHealth = 100;
    protected double health = maxHealth;
    protected double energy = 100;
    protected Color color;                  //color of the organism

    //------------------------------------------------DNA Variables----------------------------------------------------

    protected double sizeRatio;             //[0]
    protected int colorRed;                 //[1]   0.0-1.0
    protected int colorGreen;               //[2]   0.0-1.0
    protected int colorBlue;                //[3]   0.0-1.0
    protected double mutSizeDNA;            //[4]   how much
    protected double mutProbDNA;            //[5]   how likely
    protected double mutSizeNN;             //[6]   how much
    protected double mutProbNN;             //[7]   how likely
    protected double attractiveness;        //[8]
    protected static int numberOrganismGenes = 9;

    //-----------------------------------------------------------------------------------------------------------------

    public Organism(){
        this(new Transform(), new DNA());
        Organism.orgCount++;
    }

    public Organism(Organism father, Organism mother){
        this.transform = new Transform(mother.getLoc());

        this.birt = System.currentTimeMillis();

        Organism.orgCount++;
    }

    public Organism(Organism ancestor){
        this(ancestor,ancestor);
    }

    public Organism(double width, double height){
        this(new Transform(Vector2D.randLimVec(width,height)), new DNA());
        Organism.orgCount++;
    }

    public Organism(Transform transform, DNA dna){
        this.transform = transform.clone();
        this.dna = dna.copy();
        this.birt = System.currentTimeMillis();

        Organism.orgCount++;
    }

    public void expressGenes(){
        this.dna.getGene(0).gene0to1Check();
        this.sizeRatio = this.dna.getGene(0).getValue();

        this.dna.getGene(1).geneBoundCheck(0,255);
        this.colorRed = (int)Math.round(this.dna.getGene(1).getValue());
        this.dna.getGene(2).geneBoundCheck(0,255);
        this.colorGreen = (int)Math.round(this.dna.getGene(2).getValue());
        this.dna.getGene(3).geneBoundCheck(0,255);
        this.colorBlue = (int)Math.round(this.dna.getGene(3).getValue());

        this.mutSizeDNA = this.dna.getGene(4).getValue();
        this.dna.getGene(5).gene0to1Check();
        this.mutProbDNA = this.dna.getGene(5).getValue();
        this.mutSizeNN = this.dna.getGene(6).getValue();
        this.dna.getGene(6).gene0to1Check();
        this.mutProbNN = this.dna.getGene(7).getValue();
        this.attractiveness = this.dna.getGene(8).getValue();

        assert this.colorRed < 255 && this.colorRed > 0 : "R Value is not in range " + this.colorRed;
        assert this.colorGreen < 255 && this.colorGreen > 0 : "G Value is not in range " + this.colorGreen;
        assert this.colorBlue < 255 && this.colorBlue > 0 : "B Value is not in range " + this.colorBlue;
        this.color = new Color(this.colorRed,this.colorGreen,this.colorBlue);
    }

    public abstract void update(World w);

    public abstract void grow(double factor);

    public abstract Organism reproduce();

    //------------------------------------------------Getter and Setter------------------------------------------------

    public boolean isDead(){
        return health <= 0;
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

    public Vector2D getLoc(){return this.transform.getLocation();}

    public void setLocation(Vector2D location) {this.transform.location = location;}

    public double getLocX(){return this.transform.getLocX();}

    public void setLocX(float x) {this.transform.setLocX(x);}

    public double getLocY(){return this.transform.getLocY();}

    public void setLocY(float y){this.transform.setLocY(y);}

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
    public void setHealth(double health){this.health = health;}
    public void takeDamage(double damage) {
        //if the damage is negative it should be added to remove the right amount and not add to the health
        if(damage <= 0){
            this.health += damage;
        }
        //if the damage is positive the amount should be subtracted
        else{
            this.health -= damage;
        }
    }
    public void restoreHealth(double restoredHealth) {
        assert restoredHealth >= 0 : "restored amount is negative";

        this.health += restoredHealth;
        if(this.health > maxHealth){
            this.health = maxHealth;
        }
    }

    public double getEnergy(){return this.energy;}
    public void setEnergy(double energy){this.energy = energy;}
    public void useEnergy(double energyUsed){
        if(this.energy >= energyUsed){
            this.energy -= energyUsed;
        }
        else{
            this.takeDamage(energyUsed);
        }
    }


    //------------------------------------------------toString and paint-----------------------------------------------

    public abstract void paint(Graphics2D g);
}
