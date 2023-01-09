package Main.Organisms.Attributes;

import Main.Helper.Vector2D;

import java.awt.*;
import java.util.Arrays;
import java.util.Random;

public class DNA {
    Random rand = new Random();
    public double[] genes;
    public String[] names;

    public DNA(int num){
        this.genes = new double[num];
        for(int i = 0; i < this.genes.length; i++) this.genes[i] = this.rand.nextDouble(2)-.9;
    }
    public DNA(){
        this(1);
    }
    public DNA(double[] genes){
        this.genes = genes;
    }
    public DNA(double[] genes, String[] names){
        assert names.length <= genes.length: "more names given than genes";
        this.genes = genes;
        this.names = names;
    }


    public DNA copy(){
        double[] newGenes = new double[this.genes.length];
        System.arraycopy(this.genes, 0, newGenes, 0, this.genes.length);    //copy all elements
        return new DNA(newGenes);
    }

    public void mutate(double mutationChance) {
        for(int i = 0; i < this.genes.length; i++){
            if(Math.random() < mutationChance) this.genes[i] += this.rand.nextDouble(1)-.49;
        }
    }

    public static DNA initiateSumDNA(int num, String[] names){
        //assert names.length <= num: "more names given than genes";
        DNA dna = new DNA();
        dna.genes = new double[num];
        Arrays.fill(dna.genes, 0);      //fill the Array with 0
        dna.names = names;
        return dna;
    }

    //Adds a new element to an existing average
    public void addToAVG(DNA avg, int size, DNA newDNA){
        for(int i = 0; i < avg.genes.length; i++) {
            avg.genes[i] = (size * avg.genes[i] + newDNA.genes[i])/(size+1);
        }
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
        for (double gene : this.genes) {
            if (gene >= 0) s += "+";
            s += String.format("%.2f", gene) + ", ";
        }
        s += "]";
        return s;
    }

    public void paint(Graphics2D g, int x, int y) {
        //TODO: figure out how long the longest string is and auto-scale the positions according to it
        for(int i = 0; i < this.genes.length; i++){
            if(names.length >= i){
                g.setColor(Color.BLACK);
                g.drawString(names[i], x, y + i * 15);
                if(genes[i] < 0) g.setColor(Color.RED);
                //TODO: for some weird reason the last number isn't painted
                g.drawString(": "+String.format("%.2f",Math.abs(genes[i])), x+100, i * 15);
            }
            else {
                g.setColor(Color.BLACK);
                g.drawString(String.format("%.2f",genes[i]), x+100, i * 15);
            }
        }
    }

    public void paint(Graphics2D g, Vector2D loc) {
        this.paint(g, (int)loc.x,(int)loc.y);
    }
}
