package Main.Organisms.Attributes.DNA;

import Main.Helper.mutable;

public class Gene implements mutable {
    private double value;
    private String name;
    private GeneType geneType;

    public Gene(double value, String name, GeneType geneType) {
        this.value = value;
        this.name = name;
        this.geneType = geneType;
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

    /*
    If a new Gene type is added in the future, the developer will need to remember to update this switch statement.
    If the developer forgets, the default case will be called, which throws an assertion error.
    It would be more robust to use an enum with a method to calculate the range based on the percentage,
    and then call that method in the percentageMutate method.
    This way, if a new Gene type is added, the enum can be updated and the percentage calculation method can be updated,
    and there will be no need to modify the percentageMutate method.
     */
    @Override
    public void percentageMutate(double mutationChance, double percentage){
        assert this.geneType != null : "Gene type not defined";
        assert percentage >= 0 && percentage <= 1;

        //TODO add this to the gene type enum
        double range = 0;
        //TODO rethink this
        switch(geneType){
            case COLOR:
                range = percentage * 6;
                break;
            case TIME:
                range = percentage * 500;
                break;
            case PROBABILITY:
                range = percentage * .05;
                break;
            case DISTANCE:
                range = percentage * 10;
                break;
            case BIGGER:
                range = percentage * 1;
                break;
            case SMALLER:
                range = percentage * .04;
                break;
            case OTHER:
                range = percentage * .5;
                break;
            case ANGLE:
                range = percentage * 5;
                break;
            default:
                assert false : "Type of Gene not supported";
        }
        //assert range != 0;
        this.rangedMutate(mutationChance, range);
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
