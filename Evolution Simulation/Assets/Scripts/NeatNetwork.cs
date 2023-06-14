using System.Collections;
using System.Collections.Generic;

//https://www.youtube.com/watch?v=o9gI5679M_8&list=PLC8R0n_dfXXr0fc4NdsInilobjVhpXZk4&index=5
public class NeatNetwork
{
    public NeatGenome myGenome;
    public List<Node> nodes;
    public List<Node> inputNodes;
    public List<Node> outputNodes;
    public List<Node> hiddenNodes;
    public List<Connection> connections;

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

        NeatGenome newGenome = new NeatGenome(newNodeGenes, newConGenes);
        return newGenome;
    }

    private void CreateNetwork()
    {
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

        foreach(ConGene conGene in this.myGenome.conGenes)
        {
            Connection newCon = new Connection(conGene.inputNode, conGene.outputNode, conGene.weight, conGene.isActive);
            this.connections.Add(newCon);
        }

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
}

//https://www.youtube.com/watch?v=o9gI5679M_8&list=PLC8R0n_dfXXr0fc4NdsInilobjVhpXZk4&index=5
public class Node
{
    public int id;
    public float value; //stored value in the node that gets fed forward
    public List<Connection> inputConnections;
    public List<Connection> outputConnections;

    public Node(int ident)
    {
        this.id = ident;
    }
}

//https://www.youtube.com/watch?v=o9gI5679M_8&list=PLC8R0n_dfXXr0fc4NdsInilobjVhpXZk4&index=5
public class Connection
{
    public int inputNode;
    public int outputNode;
    public float weights;
    public bool isActive;

    public Connection(int inNode, int outNode, float wei, bool active)
    {
        this.inputNode = inNode;
        this.outputNode = outNode;
        this.weights = wei;
        this.isActive = active;
    }
}