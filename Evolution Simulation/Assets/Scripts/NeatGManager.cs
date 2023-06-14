using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NeatGManager : MonoBehaviour
{
    public GameObject NeatAnimalPrefab;
    public GameObject[] allNeatAnimals;
    public NeatNetwork[] allNeatNetworks;

    public int inputNodes, outputNodes, hiddenNodes;

    [SerializeField] private int currentGeneration = 0;
    
    public int startingPopulation;

    // How many should be kept each generation? How many should be left?
    public int keepBest, leaveWorst;

    public int currentAlive;
    private bool repoping = false;

    // Start is called before the first frame update
    void Start()
    {
        // Initialize population
        allNeatAnimals = new GameObject[startingPopulation];
        allNeatNetworks = new NeatNetwork[startingPopulation];

        StartingNetworks();
        SpawnBody();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    // Initializes the starting Networks
    private void StartingNetworks()
    {
        for(int i = 0; i < startingPopulation; i++)
        {
            allNeatNetworks[i] = new NeatNetwork(inputNodes, outputNodes, hiddenNodes);
        }
    }

    // Instantiate each Animal Object and matches bodies with their networks
    private void SpawnBody()
    {
        for(int i = 0; i < startingPopulation; i++)
        {
            // Spwan the Animals inside the Camera View
            Vector3 pos = new Vector3(Random.value, Random.value, 89);
            pos = Camera.main.ViewportToWorldPoint(pos);

            allNeatAnimals[i] = Instantiate(NeatAnimalPrefab, pos, transform.rotation);
            allNeatAnimals[i].gameObject.GetComponent<AnimalController>().myBrainIndex  = i;
            allNeatAnimals[i].gameObject.GetComponent<AnimalController>().myNetwork = allNeatNetworks[i];
            allNeatAnimals[i].gameObject.GetComponent<AnimalController>().inputNodes = inputNodes;
            allNeatAnimals[i].gameObject.GetComponent<AnimalController>().outputNodes = outputNodes;
            allNeatAnimals[i].gameObject.GetComponent<AnimalController>().hiddenNodes = hiddenNodes;
        }
    }

}
