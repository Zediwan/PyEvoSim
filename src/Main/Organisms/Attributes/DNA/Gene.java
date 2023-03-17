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
    public void mutate() {
        this.mutate(1,1);
    }

    @Override
    public void mutate(double mutationChance, double range) {
        if(Math.random() < mutationChance){
            this.value += Math.random()*range - (range/2);
        }
    }

    public void gene1to0Check(){
        this.geneBoundCheck(0,1);
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
