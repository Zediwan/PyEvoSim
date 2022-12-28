public abstract class Plant extends Organism{
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
