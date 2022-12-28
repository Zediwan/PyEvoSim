package Main.Organisms.Attributes;

import java.util.Random;

public class DNA {
    Random rand = new Random();
    public double[] genes;

    public DNA(int num){
        this.genes = new double[num];
        for(int i = 0; i < this.genes.length; i++) this.genes[i] = this.rand.nextDouble(3);
    }
    public DNA(){
        this(1);
    }
    public DNA(double[] genes){
        this.genes = genes;
    }


    public DNA copy(){
        double[] newGenes = new double[this.genes.length];
        for(int i = 0; i < this.genes.length; i++) newGenes[i] = this.genes[i];
        return new DNA(newGenes);
    }

    public void mutate(double mutationChance) {
        for(int i = 0; i < this.genes.length; i++){
            if(Math.random() < mutationChance) this.genes[i] += this.rand.nextDouble(4)-2;
        }
    }

    public static DNA initiateSumDNA(int num){
        DNA dna = new DNA();
        dna.genes = new double[num];
        for(int i = 0; i < dna.genes.length; i++) dna.genes[i] = 0;
        return dna;
    }

    public void add(DNA dna){
        assert dna.genes.length >= this.genes.length;

        for(int i = 0; i < this.genes.length; i++) this.genes[i] += dna.genes[i] ;
    }
    public static DNA div(int num, DNA dna){
        assert num != 0;

        DNA resultDNA = new DNA(dna.genes.length);
        for(int i = 0; i < dna.genes.length; i++) resultDNA.genes[i] = dna.genes[i] / num ;
        return resultDNA;
    }

    public String toString(){
        String s = "[ ";
        for(int i = 0; i< this.genes.length; i++){
            if(genes[i] >= 0) s += "+";
            s += String.format("%.2f",genes[i]) + ", ";
        }
        s += "]";
        return s;
    }
}
