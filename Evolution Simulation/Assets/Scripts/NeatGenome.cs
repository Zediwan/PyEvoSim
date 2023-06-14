using System.Collections;
using System.Collections.Generic;
using UnityEngine;

//https://www.cse.unr.edu/~sushil/class/gas/papers/NEAT.pdf
public class NeatGenome
{
    public List<NodeGene> nodeGenes;
    public List<ConGene> conGenes;

    public NeatGenome()
    {
        this.nodeGenes = new List<NodeGene>();
        this.conGenes = new List<ConGene>();
    }

    public NeatGenome(List<NodeGene> nodeGens, List<ConGene> conGens)
    {
        this.nodeGenes = nodeGens;
        this.conGenes = conGens;
    }
}

//https://www.youtube.com/watch?v=jeSehoB1uog&list=PLC8R0n_dfXXr0fc4NdsInilobjVhpXZk4&index=4
public class NodeGene
{
    public int id;
    public enum TYPE
    {
        Input,Output,Hidden
    };
    public TYPE type;

    public NodeGene(int givenID, TYPE givenType)
    {
        this.id = givenID;
        this.type = givenType;
    }
}

public class ConGene
{
    public int inputNode;
    public int outputNode;
    public float weight;
    public bool isActive;
    // Innovation number.
    public int innovNum; 

    public ConGene(int inNode, int outNode, float wei, bool active, int innov)
    {
        this.inputNode = inNode;
        this.outputNode = outNode;
        this.weight = wei;
        this.isActive = active;
        this.innovNum = innov;
    }
}