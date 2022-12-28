package Main.Organisms.Plants;

import Main.Organisms.Attributes.DNA;
import Main.Helper.Transform;
import Main.Organisms.Organism;

public abstract class Plant extends Organism {
    float growthInterval, growthTimer = 0;

    //Constructors
    public Plant(Transform transform, float health, DNA dna){
        super(transform,health,dna);
    }
    public Plant(){
        super();
    }

    public abstract Plant reproduce();
}
