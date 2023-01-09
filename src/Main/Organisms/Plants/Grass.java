package Main.Organisms.Plants;

import Main.Helper.Vector2D;

import java.awt.*;

public class Grass extends Plant {
    public static final double ENERGY_FACTOR = 100;              //the factor that the eating of a Grass gives
    public static final double BASE_ENERGY_PROVIDED = 50;        //base energy that eating a Grass gives
    public static final double GROWTH_INTERVAL = 50;            //Interval at which Growth happens
    public static final double GROWTH = .1;                     //Rate at which a Grass grows
    public static final double BASE_SIZE = 3;                   //Base size of a Grass
    public static final double HEALTH_REGENERATION = .1;        //Amount that is regenerated at once
    public static final double MAX_HEALTH = 100;                //Maximum health of a plant
    public Color col = new Color(150, 200, 20 ,125);


    //Constructor
    public Grass(){
        super();
        this.growthInterval = GROWTH_INTERVAL;
        this.decodeDNA();

        this.health = MAX_HEALTH;
    }

    /**
     * genes[0] = size
     */
    @Override
    public void decodeDNA() {
        this.transform.size = this.dna.genes[0]+BASE_SIZE;
    }

    //Behavior
    public void update(){
        //if the plant is damaged use energy to regenerate, else to grow
        if(this.health < MAX_HEALTH){
            this.health += HEALTH_REGENERATION;
        }else{
            this.growthTimer--;
            if(this.growthTimer <= 0){
                this.grow();
                this.growthTimer = this.growthInterval;
            }
        }
        //this.transform.size = Vector2D.map(this.health, 0, MAX_HEALTH, 0, this.transform.size);
    }

    @Override
    public Plant reproduce() {
        return null;
    }

    @Override
    public void grow() {
        this.transform.size += GROWTH;
    }

    @Override
    public void paint(Graphics2D g) {
        assert !this.dead() : "This is dead";

        this.col = new Color(150, 200, 20 ,55+(int)Vector2D.map(this.health,0,MAX_HEALTH,0,200));
        g.setColor(this.col);
        g.fillOval((int)(this.transform.location.x-this.transform.size/2),(int)(this.transform.location.y-this.transform.size/2),(int)this.transform.size,(int)this.transform.size);
    }
}
