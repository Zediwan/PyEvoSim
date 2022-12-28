package Main.Organisms.Animals;

import Main.CFrame;
import Main.Organisms.Attributes.DNA;
import Main.Organisms.Attributes.Gender;
import Main.Helper.Transform;
import Main.Helper.Vector2D;
import Main.Organisms.Organism;

import java.util.ArrayList;

public abstract class Animal extends Organism {
    public Gender gender;
    public double maxSpeed, maxForce, viewDistance;
    public double desiredSepDist, desiredAliDist, desiredCohDist;
    public double sepWeight, aliWeight, cohWeight, fleeWeight;
    public Organism target = null;
    //float reproductiveUrge = 0;
    //float hunger = 0;
    //float viewDistance;


    //Constructors
    public Animal(Transform transform, float health, DNA dna){
        super(transform,health,dna);
        //this.gender = gender;
        //this.maxSpeed = maxSpeed;
        //this.maxForce = maxForce;
    }
    public Animal(){
        super();
    }

    //Collision registration
    public abstract boolean collision(Organism o);
    //Search for food
    public abstract Organism searchFood();
    public abstract void reproduce();
    //Border handling
    public void borders1(){
        if(this.transform.location.x < -this.transform.getR())this.transform.location.x = CFrame.WIDTH+this.transform.getR();
        if(this.transform.location.y < -this.transform.getR())this.transform.location.y = CFrame.HEIGHT+this.transform.getR();
        if(this.transform.location.x > CFrame.WIDTH+this.transform.getR())this.transform.location.x = -this.transform.getR();
        if(this.transform.location.y > CFrame.HEIGHT+this.transform.getR())this.transform.location.y = -this.transform.getR();
    }
    public void borders2(){
        if(this.getLocX() < 0){
            Vector2D desired = new Vector2D(this.maxSpeed, this.transform.velocity.getY());
            Vector2D steer = Vector2D.sub(desired,this.transform.getVelocity());
            steer.limit(this.maxForce);
            this.transform.applyForce(steer.mult(-this.transform.location.x));
        }else if (this.getLocX() > CFrame.WIDTH){
            Vector2D desired = new Vector2D(-this.maxSpeed, this.transform.velocity.getY());
            Vector2D steer = Vector2D.sub(desired,this.transform.getVelocity());
            steer.limit(this.maxForce);
            this.transform.applyForce(steer.mult(this.transform.location.x-CFrame.HEIGHT));
        }
        if(this.getLocY() < 0){
            Vector2D desired = new Vector2D(this.transform.velocity.getX(), this.maxSpeed);
            Vector2D steer = Vector2D.sub(desired,this.transform.getVelocity());
            steer.limit(this.maxForce);
            this.transform.applyForce(steer.mult(-this.transform.location.y));
        }else if (this.getLocY() > CFrame.HEIGHT){
            Vector2D desired = new Vector2D(this.transform.velocity.getX(), -this.maxSpeed);
            Vector2D steer = Vector2D.sub(desired,this.transform.getVelocity());
            steer.limit(this.maxForce);
            this.transform.applyForce(steer.mult(this.transform.location.y-CFrame.HEIGHT));
        }
    }


    //movement types
    /**
     * A method that calculates a steering force towards a target and slows down when being close
     * @param target that should be moved towards
     */
    public Vector2D arrive(Vector2D target){
        Vector2D desired = Vector2D.sub(target,this.transform.location);        //Vector from target to this
        double distance = desired.magSq();                                       //calculate the distance

        //if this is close to the target slow down
        if(distance <= Math.pow(this.transform.getR(),2)){
            double m = Vector2D.map(distance,0,Math.pow(this.transform.getR(),2),0,this.maxSpeed);
            desired.setMag(m);
        }else desired.setMag(this.maxSpeed);

        //Steering = Desired minus Velocity
        Vector2D steer = Vector2D.sub(desired,this.transform.velocity);
        steer.limit(this.maxForce);                                         //Limit to maximum steering
        //this.transform.applyForce(steer);
        return steer;
    }
    /**
     * A method that calculates a steering force towards a target
     * @param target that should be moved towards
     */
    public Vector2D seek(Vector2D target){
        Vector2D desired = Vector2D.sub(target,this.transform.location);

        desired.setMag(this.maxSpeed);

        Vector2D steer = Vector2D.sub(desired,this.transform.velocity);
        steer.limit(this.maxForce);
        //this.transform.applyForce(steer);
        return steer;
    }
    public Vector2D flee(Vector2D target){
        Vector2D desired = Vector2D.sub(target,this.transform.location);
        desired = desired.mult(-1);

        desired.setMag(this.maxSpeed);

        Vector2D steer = Vector2D.sub(desired,this.transform.velocity);
        steer.limit(this.maxForce);
        //this.transform.applyForce(steer);
        return steer;
    }
    public void flock(ArrayList<Animal> animals){
        this.transform.acceleration.mult(0);
        //flocking rules
        Vector2D sep = separate(animals);
        Vector2D ali = align(animals);
        Vector2D coh = cohesion(animals);


        //weights for the forces
        sep.mult(this.sepWeight);
        ali.mult(this.aliWeight);
        coh.mult(this.cohWeight);


        //apply forces
        this.transform.applyForce(sep);
        this.transform.applyForce(ali);
        this.transform.applyForce(coh);

    }

    //environmental effects
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
            double distance = Vector2D.dist(this.getLocation(),a.getLocation());

            //here check distance > 0 to avoid an animal separation from itself
            if((distance>0) && (distance<this.desiredSepDist)){
                Vector2D difference = Vector2D.sub(this.getLocation(), a.getLocation());
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

            //this.transform.applyForce(steer);
        }
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

        for(Animal a : animals){
            double distance = Vector2D.dist(this.getLocation(),a.getLocation());
            if((distance > 0) && (distance < this.desiredCohDist)){
                sum.add(a.getLocation());
                count++;
            }
        }
        if(count > 0){
            sum.div(count);
            return seek(sum);
        }else return new Vector2D();
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
            double distance = Vector2D.dist(this.getLocation(),a.getLocation());
            if((distance > 0) && (distance < this.desiredAliDist)){
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
        return steer;
    }

    public abstract void flee(ArrayList<Animal> animals);
}
