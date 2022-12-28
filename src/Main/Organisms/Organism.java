package Main.Organisms;

import Main.CFrame;
import Main.Organisms.Attributes.DNA;
import Main.Helper.Transform;
import Main.Helper.Vector2D;

import java.awt.*;

public abstract class Organism {
    public double health;
    public DNA dna;
    public Transform transform;
    //TODO: change variables to private
    //TODO: implement age via sys-time
    //TODO: set a timescale for the age according to sys-time
    //float age = 0;

    public Organism(Transform transform, float health, DNA dna){
        this.transform = transform;
        this.health = health;
        this.dna = dna;
    }
    public Organism(){
        this(new Transform(Vector2D.randLimVec(CFrame.WIDTH,CFrame.HEIGHT)), 100, new DNA());
    }

    public abstract void decodeDNA();

    public abstract void update();

    public abstract void grow();

    public abstract void paint(Graphics2D g);

    public boolean dead(){
        return health <= 0 || this.transform.size <= 0;
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

    public double getHealth() {
        return this.health;
    }
    public void setHealth(float health) {
        this.health = health;
    }
}
