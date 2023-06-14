using System.Collections;
using System.Collections.Generic;
using UnityEngine;

//https://www.youtube.com/watch?v=o9gI5679M_8&list=PLC8R0n_dfXXr0fc4NdsInilobjVhpXZk4&index=5
public class NeatNetwork
{
    public NeatGenome myGenome;
    public List<Node> nodes;
    public List<Node> inputNodes;
    public List<Node> outputNodes;
    public List<Node> hiddenNodes;
    public List<Connection> connections;

    public float fitness;

    public NeatNetwork(int inp, int outp, int hid)
    {
        this.myGenome = CreateInitialGenome(inp, outp, hid);
        this.nodes = new List<Node>();
        this.inputNodes = new List<Node>();
        this.outputNodes = new List<Node>();
        this.hiddenNodes = new List<Node>();
        this.connections = new List<Connection>();
        CreateNetwork();
    }

    private NeatGenome CreateInitialGenome(int inp, int outp, int hid)
    {
        List<NodeGene> newNodeGenes = new List<NodeGene>();
        List<ConGene> newConGenes = new List<ConGene>();
        int nodeId = 0;

        for(int i = 0; i < inp; i++)
        {
            NodeGene newNodeGene = new NodeGene(nodeId, NodeGene.TYPE.Input);
            newNodeGenes.Add(newNodeGene);
            nodeId += 1;
        }

        for(int i = 0; i < outp; i++)
        {
            NodeGene newNodeGene = new NodeGene(nodeId, NodeGene.TYPE.Output);
            newNodeGenes.Add(newNodeGene);
            nodeId += 1;
        }

        //hidden are added last so we can easily add new hidden nodes
        for(int i = 0; i < hid; i++)
        {
            NodeGene newNodeGene = new NodeGene(nodeId, NodeGene.TYPE.Hidden);
            newNodeGenes.Add(newNodeGene);
            nodeId += 1;
        }

        ConGene newConGene1 = new ConGene(Random.Range(0,3), Random.Range(3,5), Random.Range(0f,1f), true, 0);
        newConGenes.Add(newConGene1);
        ConGene newConGene2 = new ConGene(Random.Range(0,3), Random.Range(3,5), Random.Range(0f,1f), true, 1);
        newConGenes.Add(newConGene2);
        ConGene newConGene3 = new ConGene(Random.Range(0,3), Random.Range(3,5), Random.Range(0f,1f), true, 2);
        newConGenes.Add(newConGene3);

        NeatGenome newGenome = new NeatGenome(newNodeGenes, newConGenes);
        return newGenome;
    }

    private void CreateNetwork()
    {
        // Creation of Network Structure: Nodes
        foreach(NodeGene nodeGene in this.myGenome.nodeGenes)
        {
            Node newNode = new Node(nodeGene.id);
            this.nodes.Add(newNode);
            if(nodeGene.type == NodeGene.TYPE.Input)
            {
                this.inputNodes.Add(newNode);
            }
            else if(nodeGene.type == NodeGene.TYPE.Hidden)
            {
                this.hiddenNodes.Add(newNode);
            }
            else if(nodeGene.type == NodeGene.TYPE.Output)
            {
                this.outputNodes.Add(newNode);
            }
        }

        // Creation of Network Structure: Edges
        foreach(ConGene conGene in this.myGenome.conGenes)
        {
            Connection newCon = new Connection(conGene.inputNode, conGene.outputNode, conGene.weight, conGene.isActive);
            this.connections.Add(newCon);
        }

        // Creation of Network Structure: Node Neighbors
        foreach(Node node in this.nodes)
        {
            foreach(Connection con in this.connections)
            {
                if(con.inputNode == node.id)
                {
                    node.outputConnections.Add(con);
                }
                else if(con.outputNode == node.id)
                {
                    node.inputConnections.Add(con);
                }
            }
        }
    }

    // Main Driver Function for the NeuralNetwork
    public float[] FeedForwardNetwork(float[] inputs)
    {
        float[] outputs = new float[outputNodes.Count];
        for (int i = 0; i < inputNodes.Count; i++)
        {
            inputNodes[i].SetInputNodeValue(inputs[i]);
            inputNodes[i].FeedForwardValue();
            inputNodes[i].value = 0;    // Reset value
        }
        for (int i = 0; i < hiddenNodes.Count; i++)
        {
            hiddenNodes[i].SetHiddenNodeValue();
            hiddenNodes[i].FeedForwardValue();
            hiddenNodes[i].value = 0;   // Reset value
        }
        for (int i = 0; i < outputNodes.Count; i++)
        {
            outputNodes[i].SetOutputNodeValue();
            outputs[i] = outputNodes[i].value;
            outputNodes[i].value = 0;   // Reset value
        }
        //Debug.Log(outputNodes.Count);
        return outputs;
    }
}

//https://www.youtube.com/watch?v=o9gI5679M_8&list=PLC8R0n_dfXXr0fc4NdsInilobjVhpXZk4&index=5
public class Node
{
    public int id;
    // Stored value in the node that gets fed forward.
    public float value; 
    public List<Connection> inputConnections;
    public List<Connection> outputConnections;

    public Node(int ident)
    {
        this.id = ident;
        inputConnections = new List<Connection>();
        outputConnections = new List<Connection>();
    }

    //https://www.youtube.com/watch?v=toTwSTUdL5Y&list=PLC8R0n_dfXXr0fc4NdsInilobjVhpXZk4&index=6
    public void SetInputNodeValue(float val)
    {
        // Uses sigmoid as an activation function because the input values are never negative
        // and sigmoid goes from 0 to 1.
        this.value = Sigmoid(val);
    }

    //https://www.youtube.com/watch?v=toTwSTUdL5Y&list=PLC8R0n_dfXXr0fc4NdsInilobjVhpXZk4&index=6
    public void SetHiddenNodeValue()
    {
        float val = 0;
        foreach (Connection con in inputConnections)
        {
            val += (con.weight * con.inputNodeValue);
        }
        // Uses tanh as an activation function.
        value = TanH(val);
    }

    //https://www.youtube.com/watch?v=toTwSTUdL5Y&list=PLC8R0n_dfXXr0fc4NdsInilobjVhpXZk4&index=6
    public void SetOutputNodeValue()
    {
        float val = 0;
        foreach (Connection con in inputConnections)
        {
            val += (con.weight * con.inputNodeValue);
        }
        value = TanH(val);
    }

    // Pushes forward the values into the edges for all the connections.
    //https://www.youtube.com/watch?v=toTwSTUdL5Y&list=PLC8R0n_dfXXr0fc4NdsInilobjVhpXZk4&index=6
    public void FeedForwardValue()
    {
        // Goes through each connection and stores the output of the input node
        // as the input of the output node.
        foreach(Connection con in this.outputConnections)
        {
            con.inputNodeValue = this.value;
        }
    }

    // Activation Functions.
    // Search for faster calculation of Sigmoid.
    //https://en.wikipedia.org/wiki/Sigmoid_function
    private float Sigmoid(float x) 
    {  
        return (1 / (1 + Mathf.Exp(-x)));  
    }

    // Search for a faster cacluation of TanH.
    //https://de.wikipedia.org/wiki/Tangens_hyperbolicus_und_Kotangens_hyperbolicus
    private float TanH(float x)
    {
        return ((2 / (1 + Mathf.Exp(-2 * x))) - 1);
    }

    private float TanHMod1(float x)
    {
        return ((2 / (1 + Mathf.Exp(-4 * x))) - 1);
    }
}

//https://www.youtube.com/watch?v=o9gI5679M_8&list=PLC8R0n_dfXXr0fc4NdsInilobjVhpXZk4&index=5
public class Connection
{
    public int inputNode;
    public int outputNode;
    public float weight;
    public bool isActive;
    public float inputNodeValue;

    public Connection(int inNode, int outNode, float wei, bool active)
    {
        this.inputNode = inNode;
        this.outputNode = outNode;
        this.weight = wei;
        this.isActive = active;
    }

}