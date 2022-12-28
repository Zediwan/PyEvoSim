package Main.Organisms.Animals;

import Main.CFrame;
import Main.Organisms.Attributes.DNA;
import Main.Organisms.Attributes.Gender;
import Main.Helper.Transform;
import Main.Helper.Vector2D;
import Main.Organisms.Organism;

import java.awt.*;
import java.util.ArrayList;

public class Fox extends Animal {
    public static DNA sumDNA = DNA.initiateSumDNA(11);
    public static int totalAmountOfFoxes = 0;

    //Constructors
    public Fox(Transform transform, float health, DNA dna){
        super(transform, health, dna);
        this.decodeDNA();
        sumDNA.add(this.dna);
        totalAmountOfFoxes++;
        //System.out.println("F: " + this.dna);
    }
    public Fox(){
        super();
        this.dna = new DNA(11);
        this.decodeDNA();
        this.health = 600;
        //System.out.println(this.dna);
    }

    @Override
    public boolean collision(Organism Rabbit) {
        assert Rabbit.getClass() == Main.Organisms.Animals.Rabbit.class;
        if(this.transform.location.dist(Rabbit.transform.location) <= this.transform.getR()){
            if(this.health >= 400) this.health = 400;
            Rabbit.health -= 500;                                     //reduce plants health to 0
            if(Rabbit.health <= 0) this.health += Rabbit.transform.size * 100;
            //System.out.println(this.health);
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
        for(Organism o : CFrame.Rabbits){
            assert o.getClass() == Rabbit.class;
            double distance = Vector2D.sub(o.transform.location, this.transform.location).mag();
            if((closestDistance >= distance) && (distance <= this.viewDistance)){
                closestDistance = distance;
                closestFood = o;
            }
        }
        if(closestFood != null) assert closestFood.getClass() == Rabbit.class;
        return closestFood;
    }

    @Override
    public void reproduce(){
        double birthChance = 0;
        if(this.health >= 300){
            birthChance = .005;
        }else if(this.health >= 200){
            birthChance = .0025;
        }else if(this.health >= 100){
            birthChance = .001;
        }
        if(Math.random() <= birthChance){
            DNA childDNA = dna.copy();
            childDNA.mutate(.5);
            Transform t = this.transform.clone();
            CFrame.Foxes.add(new Fox(t,300, childDNA));
        }
    }

    @Override
    public void flee(ArrayList<Animal> animals) {
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
     */
    @Override
    public void decodeDNA() {
        //Define Main.NeuralNetwork.NeuralNetwork.Gender
        /*
        if(this.dna.genes[0]) this.gender = Main.NeuralNetwork.NeuralNetwork.Gender.MALE;
        else this.gender = Main.NeuralNetwork.NeuralNetwork.Gender.FEMALE;
         */
        if(Math.random() <= .5) this.gender = Gender.MALE;
        else this.gender = Gender.FEMALE;
        //Define size
        this.transform.size = this.dna.genes[1]+7;
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
        //System.out.println(this.dna);
    }

    //Behavior
    public void update(){
        //TODO: rework
        target = searchFood();
        if(target != null  && this.health <= 300) {
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
        if(this.transform.velocity.mag() <= this.maxSpeed){
            this.health -= Vector2D.map(this.transform.velocity.mag(),0,this.maxSpeed,5, 8);
        }else this.health -= 5;

        //System.out.println(this.health);
    }

    @Override
    public void grow() {

    }

    //Visualization
    @Override
    public void paint(Graphics2D g) {
        Color c = new Color(237, 150, 11, 200);
        g.setColor(c);
        //g.draw(this.transform.getRectangle());
        g.fill(this.transform.getRectangle());
    }
}
