package Main.Organisms;

import Main.CFrame;
import Main.Organisms.Attributes.DNA.DNA;
import Main.Helper.Transform;
import Main.Helper.Vector2D;
import Main.Organisms.Attributes.DNA.Gene;
import Main.Organisms.Attributes.Gender;

import java.awt.*;

public abstract class Organism {
    public static long orgCount = 0;
    /*
    public static DNA generalDNA = new DNA(
            new double[]{

            },
            new String[]{

            }
    );
     */

    protected Transform transform;
    protected DNA dna;
    protected long birt = 0;
    protected double id;
    protected double health = 100;

    //------------------------------------------------DNA Variables----------------------------------------------------

    protected double sizeRatio;             //[0]
    protected int colorRed;                 //[1]   0.0-1.0
    protected int colorGreen;               //[2]   0.0-1.0
    protected int colorBlue;                //[3]   0.0-1.0
    protected Color color;                  //      color of the organism
    protected double mutationSizeDNA;       //[4]   how much
    protected double mutationChancesDNA;    //[5]   how likely
    protected double mutationSizeNN;        //[6]   how much
    protected double mutationChancesNN;     //[7]   how likely
    protected double attractiveness;        //[8]
    protected static int numberOrganismGenes = 9;

    //-----------------------------------------------------------------------------------------------------------------

    public Organism(Transform transform, DNA dna){
        this.transform = transform.clone();
        this.dna = dna.copy();
        this.birt = System.currentTimeMillis();

        Organism.orgCount++;
    }

    public Organism(){
        //TODO: change this so it doesn't need the CFrame class
        this(new Transform(Vector2D.randLimVec(CFrame.WIDTH,CFrame.HEIGHT)), new DNA());
        Organism.orgCount++;
    }

    public void expressGenes(){
        this.sizeRatio = this.dna.getGene(0).getValue();
        this.colorRed = (int)Math.round(this.dna.getGene(1).getValue());
        this.colorGreen = (int)Math.round(this.dna.getGene(2).getValue());
        this.colorBlue = (int)Math.round(this.dna.getGene(3).getValue());
        this.color = new Color(this.colorRed,this.colorGreen,this.colorBlue);
        this.mutationSizeDNA = this.dna.getGene(4).getValue();
        this.mutationChancesDNA = this.dna.getGene(5).getValue();
        this.mutationSizeNN = this.dna.getGene(6).getValue();
        this.mutationChancesNN = this.dna.getGene(7).getValue();
        this.attractiveness = this.dna.getGene(8).getValue();
    }

    public abstract void update();

    public abstract void grow();

    public abstract Organism reproduce(DNA mateDNA);

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

    public Vector2D getLocation(){return this.transform.getLocation();}

    public double getLocX(){return this.transform.getLocX();}

    public void setLocX(float x) {this.transform.setLocX(x);}

    public double getLocY(){return this.transform.getLocY();}

    public void setLockY(float y){this.transform.setLocY(y);}

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

    public double getMutationSizeDNA() {
        return mutationSizeDNA;
    }

    public void setMutationSizeDNA(double mutationSizeDNA) {
        this.mutationSizeDNA = mutationSizeDNA;
    }

    public double getMutationChancesDNA() {
        return mutationChancesDNA;
    }

    public void setMutationChancesDNA(double mutationChancesDNA) {
        this.mutationChancesDNA = mutationChancesDNA;
    }

    public double getMutationSizeNN() {
        return mutationSizeNN;
    }

    public void setMutationSizeNN(double mutationSizeNN) {
        this.mutationSizeNN = mutationSizeNN;
    }

    public double getMutationChancesNN() {
        return mutationChancesNN;
    }

    public void setMutationChancesNN(double mutationChancesNN) {
        this.mutationChancesNN = mutationChancesNN;
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
        this.health -= damage;
    }

    //------------------------------------------------toString and paint-----------------------------------------------

    public abstract void paint(Graphics2D g);


}
