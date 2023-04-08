package Main.Organisms.Attributes.DNA;

import Main.Helper.Vector2D;
import Main.Helper.mutable;

import java.awt.*;

//TODO: Test
public class DNA implements mutable {
    private Gene[] genes;

    public DNA(Gene[] genes){
        this.genes = genes;
    }

    public DNA(double[] values, String[] names, GeneType[] geneTypes){
        assert names.length == values.length: "more names given than genes";

        this.genes = new Gene[values.length];
        for(int i = 0; i < this.genes.length; i++){
            this.genes[i] = new Gene(values[i], names[i], geneTypes[i]);
        }
    }

    public DNA copy(){
        Gene[] newGenes = new Gene[this.genes.length];
        System.arraycopy(this.genes, 0, newGenes, 0, this.genes.length);    //copy all elements
        return new DNA(newGenes);
    }

    @Override
    public void rangedMutate(double mutationChance, double range) {
        for(Gene gene : this.genes){
            gene.rangedMutate(mutationChance, range);
        }
    }

    @Override
    public void rangedMutate() {
        this.rangedMutate(1,1);
    }

    @Override
    public void percentageMutate(double mutationChance, double range){
        for(Gene gene : this.genes){
            gene.percentageMutate(mutationChance, range);
        }
    }

    @Override
    public void percentageMutate(){
        this.rangedMutate(1,1);
    }

    public static DNA crossover(DNA father, DNA mother){
        Gene[] genes = new Gene[father.genes.length];
        for(int i = 0; i < father.genes.length; i++){
            //select randomly genes from the father or the mother
            if(Math.random() < .5){
                genes[i] = father.getGene(i);
            }else{
                genes[i] = mother.getGene(i);;
            }
        }
        return new DNA(genes);
    }

    //------------------------------------------------Getter and Setter------------------------------------------------

    public Gene[] getGenes() {
        return genes;
    }

    public void setGenes(Gene[] genes) {
        this.genes = genes;
    }

    public Gene getGene(int i){
        return this.genes[i];
    }

    public void setGene(int i, double value){
        this.genes[i].setValue(value);
    }

    //------------------------------------------------toString and paint-----------------------------------------------

    public void paint(Graphics2D g, int x, int y) {
        //TODO: figure out how long the longest string is and auto-scale the positions according to it
        for(int i = 0; i < this.genes.length; i++){
            Gene gene = this.genes[i];

            g.setColor(Color.BLACK);

            g.drawString(gene.getName(), x, y + i * 15);

            if(gene.getValue() < 0) g.setColor(Color.RED);

            //TODO: for some weird reason the last number isn't painted
            g.drawString(": "+String.format("%.3f",Math.abs(gene.getValue())), x+100, i * 15);
        }
    }

    public void paint(Graphics2D g, Vector2D loc) {
        this.paint(g, (int)loc.getX(),(int)loc.getY());
    }

    public String toString(){
        String s = "[ ";
        for (Gene gene : this.genes) {
            if (gene.getValue() >= 0) s += "+";
            s += String.format("%.2f", gene.getName()) + ", ";
        }
        s += "]";
        return s;
    }
}
