package Main.Organisms.Attributes.DNA;

import Main.Helper.mutable;

public class Gene implements mutable {
    private double value;
    private String name;

    public Gene(double value, String name) {
        this.value = value;
        this.name = name;
    }

    @Override
    public void rangedMutate(double mutationChance, double range) {
        if(Math.random() < mutationChance){
            this.value += (Math.random()* 2*range) - range;
        }
    }

    @Override
    public void rangedMutate() {
        this.rangedMutate(1,1);
    }

    @Override
    public void percentageMutate(double mutationChance, double range){
        this.rangedMutate(mutationChance, this.getValue() * range);
    }

    @Override
    public void percentageMutate(){
        this.percentageMutate(1,1);
    }

    //TODO think if this is better
    //@Override
    public void mutateFactor(double mutationChance, double factor) {
        double range = factor * this.value;
        if(Math.random() < mutationChance){
            this.value += (Math.random()* 2*range) - range;
        }
    }

    public void gene0to1Check(){
        this.geneBoundCheck(0,1);
    }

    public void genePositiveCheck(){
        if(this.value < 0){
            this.value = 0;
        }
    }

    public void geneBoundCheck(double lowerBound, double upperBound){
        if(this.value < lowerBound){
            this.value = lowerBound;
        }
        else if(this.value > upperBound){
            this.value = upperBound;
        }
    }

    //------------------------------------------------Getter and Setter------------------------------------------------
    public double getValue() {
        return value;
    }

    public void setValue(double value) {
        this.value = value;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
