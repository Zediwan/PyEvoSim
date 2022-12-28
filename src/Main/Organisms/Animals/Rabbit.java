package Main.Organisms.Animals;

import Main.CFrame;
import Main.Organisms.Attributes.DNA;
import Main.Organisms.Attributes.Gender;
import Main.Helper.Transform;
import Main.Helper.Vector2D;
import Main.Organisms.Organism;
import Main.Organisms.Plants.Grass;

import java.awt.*;
import java.util.ArrayList;

public class Rabbit extends Animal {
    public static DNA sumDNA = DNA.initiateSumDNA(12);
    public static int totalAmountOfRabbits = 0;

    //Constructors
    public Rabbit(Transform transform, float health, DNA dna){
        super(transform, health, dna);
        this.decodeDNA();
        sumDNA.add(this.dna);
        totalAmountOfRabbits++;
        //System.out.println("R: " + this.dna);
    }
    public Rabbit(){
        super();
        this.dna = new DNA(12);
        this.decodeDNA();
        this.health = 200;
        //System.out.println(this.dna);
    }

    /**
     * genes[0] =
     * genes[1] = size
     * genes[2] = maxSpeed
     * genes[3] = maxForce
     * genes[4] = viewDistance
     * genes[5] = desiredSeparationDist
     * genes[6] = desiredAlignmentDist
     * genes[7] = desiredCohesionDist
     * genes[8] = separationWeight
     * genes[9] = alignmentWeight
     * genes[10] = cohesionWeight
     * genes[11] = fleeWeight
     */
    @Override
    public void decodeDNA() {
        //Define Main.Main.NeuralNetwork.NeuralNetwork.Gender
        /*
        if(this.dna.genes[0]) this.gender = Main.Main.NeuralNetwork.NeuralNetwork.Gender.MALE;
        else this.gender = Main.Main.NeuralNetwork.NeuralNetwork.Gender.FEMALE;
         */
        if(Math.random() <= .5) this.gender = Gender.MALE;
        else this.gender = Gender.FEMALE;
        //Define size
        this.transform.size = this.dna.genes[1]+4;
        //Define maxSpeed
        this.maxSpeed = this.dna.genes[2];
        //Define maxForce
        this.maxForce = this.dna.genes[3];
        //Define viewDistance
        this.viewDistance = (this.dna.genes[4])*this.transform.size;
        //Define separation, alignment, cohesion distances
        this.desiredSepDist = this.dna.genes[5] * this.transform.size;
        this.desiredAliDist = this.dna.genes[6] * this.transform.size;
        this.desiredCohDist = this.dna.genes[7] * this.transform.size;
        //Define separation, alignment, cohesion weights
        this.sepWeight = this.dna.genes[8];
        this.aliWeight = this.dna.genes[9];
        this.cohWeight = this.dna.genes[10];
        //Define flee weight
        this.fleeWeight = this.dna.genes[11];
        //System.out.println(this.dna);
    }


    //Behavior
    public void update(){
        //TODO: rework
        target = searchFood();
        if(target != null && this.health <= 300) {
            this.transform.applyForce(seek(target.getLocation()));
            if (collision(target)) target = searchFood();
        }

        this.transform.velocity.add(this.transform.acceleration);
        this.transform.velocity.limit(maxSpeed);
        this.transform.location.add(this.transform.velocity);
        this.transform.acceleration.mult(0);

        //this.transform.move(this.maxSpeed);
        this.borders1();
        //this.grow();
        this.health -= 5;
        //System.out.println(this.health);
    }
    @Override
    public boolean collision(Organism Grass) {
        assert Grass.getClass() == Main.Organisms.Plants.Grass.class;
        if(this.transform.location.dist(Grass.transform.location) <= this.transform.getR()){
            this.health += (Grass.transform.size*20)+1;     //gain health
            if(this.health >= 400) this.health = 400;
            Grass.health--;                                 //reduce plants health to 0
            Grass.transform.size--;
            target = null;                                  //remove target
            //System.out.println("eating");
            return true;
        } return false;
    }

    //TODO: rework for better performance
    @Override
    public Organism searchFood() {
        Organism closestFood = null;
        double closestDistance = Double.POSITIVE_INFINITY;
        for(Organism o : CFrame.Plants){
            double distance = Vector2D.sub(o.transform.location, this.transform.location).mag();
            if((closestDistance >= distance) && (distance <= this.viewDistance)){
                closestDistance = distance;
                closestFood = o;
            }
        }
        if(closestFood != null) assert closestFood.getClass() == Grass.class;
        return closestFood;
    }

    //Reproduction
    @Override
    public void grow() {
        if(this.health >= 100) this.transform.size += .25;
    }
    @Override
    public void reproduce(){
        double birthChance = 0;
        if(this.health >= 300){
            birthChance = .0075;
        }else if(this.health >= 200){
            birthChance = .0025;
        }else if(this.health >= 100){
            birthChance = .001;
        }
        if(Math.random() <= birthChance){
            DNA childDNA = dna.copy();
            childDNA.mutate(.1);
            Transform t = this.transform.clone();
            CFrame.Rabbits.add(new Rabbit(t,300, childDNA));
        }
    }

    public void flee(ArrayList<Animal> animals) {
        Vector2D sum = new Vector2D();
        Vector2D steer = new Vector2D();
        int count = 0; //of animals being too close

        for (Animal a : animals) {
            assert a.getClass() == Fox.class;
            //calculate distance of the two animals
            double distance = Vector2D.dist(this.getLocation(), a.getLocation());
            //here check distance > 0 to avoid an animal fleeing from itself
            if ((distance > 0) && (distance < this.viewDistance)) {
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
        if (count > 0) {
            sum.div(count);
            sum.setMag(this.maxSpeed);
            steer = Vector2D.sub(sum, this.transform.getVelocity());
            steer.limit(this.maxForce);
            //this.transform.applyForce(steer);
        }
        steer.mult(this.fleeWeight);
        this.transform.applyForce(steer);
    }

            //Visualization
    @Override
    public void paint(Graphics2D g) {
        Color c = new Color(121, 83, 71, 200);
        g.setColor(c);
        //g.draw(this.transform.getRectangle());
        g.fill(this.transform.getRectangle());
    }
}
