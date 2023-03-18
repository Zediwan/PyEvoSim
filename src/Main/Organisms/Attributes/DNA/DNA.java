package Main.Organisms.Attributes.DNA;

import Main.Helper.Vector2D;
import Main.Helper.mutable;
import java.awt.*;
import java.awt.geom.AffineTransform;
import java.util.HashMap;
import java.util.Map;

//TODO: Test
public class DNA implements mutable {
    private Gene[] genes;

    public DNA(Gene[] genes){
        this.genes = genes;
    }

    public DNA(double[] values, String[] names){
        assert names.length == values.length: "more names given than genes";

        this.genes = new Gene[values.length];
        for(int i = 0; i < this.genes.length; i++){
            this.genes[i] = new Gene(values[i], names[i]);
        }
    }

    public DNA(int num){
        this.genes = new Gene[num];
    }

    public DNA(){
        this(1);
    }

    public DNA copy(){
        Gene[] newGenes = new Gene[this.genes.length];
        System.arraycopy(this.genes, 0, newGenes, 0, this.genes.length);    //copy all elements
        return new DNA(newGenes);
    }

    @Override
    public void mutate() {
        this.mutate(1,1);
    }

    public void mutate(double mutationChance, double range) {
        for(Gene gene : this.genes){
            gene.mutate(mutationChance, range);
        }
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
        this.paint(g, (int)loc.x,(int)loc.y);
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

    //LEGACY CODE
    /*
    public double[] genes;
    public String[] names;
    public DNA(int num, double range){
        this.genes = new double[num];
        for(int i = 0; i < this.genes.length; i++) this.genes[i] = this.rand.nextDouble(range)-(range/2);
    }
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

    public void mutate(double mutationChance, double range) {
        for(int i = 0; i < this.genes.length; i++){
            if(Math.random() < mutationChance) this.genes[i] += this.rand.nextDouble(range)-range/2;
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
    public void paint(Graphics2D g, int x, int y) {
        //TODO: figure out how long the longest string is and auto-scale the positions according to it
        for(int i = 0; i < this.genes.length; i++){
            if(names.length >= i){
                g.setColor(Color.BLACK);
                g.drawString(names[i], x, y + i * 15);
                if(genes[i] < 0) g.setColor(Color.RED);
                //TODO: for some weird reason the last number isn't painted
                g.drawString(": "+String.format("%.3f",Math.abs(genes[i])), x+100, i * 15);
            }
            else {
                g.setColor(Color.BLACK);
                g.drawString(String.format("%.3f",genes[i]), x+100, i * 15);
            }
        }
    }

    public void paint(Graphics2D g, Vector2D loc) {
        this.paint(g, (int)loc.x,(int)loc.y);
    }
    public String toString(){
        String s = "[ ";
        for (String name : phenotypeDict.keySet()) {
            if (phenotypeDict.get(name) >= 0) s += "+";
            s += String.format("%.2f", name) + ", ";
        }
        s += "]";
        return s;
    }
     */
    /*
    private Map<String, Double> phenotypeDict;

    public DNA() {
        this.phenotypeDict = new HashMap<>();
    }

    public void addPhenotypeFactor(String name, double value) {
        phenotypeDict.put(name, value);
    }

    public double getPhenotypeFactor(String name) {
        return phenotypeDict.get(name);
    }

    public void setPhenotypeFactor(String name, double value) {
        phenotypeDict.put(name, value);
    }

    public void mutate(double mutChance, double mutRange) {
        for (String name : phenotypeDict.keySet()) {
            double newValue = phenotypeDict.get(name);
            if(Math.random() < mutChance){
                newValue += Math.random()*mutRange - (mutRange/2.0);
            }
            phenotypeDict.put(name, newValue);
        }
    }

    public DNA copy() {
        DNA newDNA = new DNA();
        for (String name : phenotypeDict.keySet()) {
            double copyValue = phenotypeDict.get(name);
            newDNA.setPhenotypeFactor(name, copyValue);
        }
        return newDNA;
    }

    public void paint(Graphics2D g, int x, int y) {
        int rowHeight = 20;
        int cellWidth = 100;
        int tableWidth = 2 * cellWidth;
        int tableHeight = (phenotypeDict.size() + 1) * rowHeight;
        g.setColor(Color.WHITE);
        g.fillRect(x, y, tableWidth, tableHeight);
        g.setColor(Color.BLACK);
        g.drawRect(x, y, tableWidth, tableHeight);

        int row = 1;
        for (String name : phenotypeDict.keySet()) {
            Object value = phenotypeDict.get(name);
            String valueString = value.toString();
            g.drawString(name, x + 10, y + rowHeight * row);
            g.drawString(valueString, x + cellWidth + 10, y + rowHeight * row);
            row++;
        }
    }

    public String toString(){
        String s = "[ ";
        for (String name : phenotypeDict.keySet()) {
            if (phenotypeDict.get(name) >= 0) s += "+";
            s += String.format("%.2f", name) + ", ";
        }
        s += "]";
        return s;
    }
    private Object mutateValue(Object value) {
        if (value instanceof Integer) {
            int intValue = (int)value;
            int bitIndex = (int)(Math.random() * 32);
            intValue ^= 1 << bitIndex;
            return intValue;
        } else if (value instanceof Double) {
            double doubleValue = (double)value;
            doubleValue += Math.random() * 0.1 - 0.05;
            return doubleValue;
        } else if (value instanceof Boolean) {
            boolean booleanValue = (boolean)value;
            return !booleanValue;
        }
        // Add more mutation logic for other types as needed
        return value;
    }
    public Map<String, Double> getPhenotypeDict() {
        return phenotypeDict;
    }

    public void setPhenotypeDict(Map<String, Double> phenotypeDict) {
        this.phenotypeDict = phenotypeDict;
    }
     */
}
