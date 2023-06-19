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
        currentGeneration++;
        SpawnBody();
    }

    void FixedUpdate()
    {
        currentAlive = CurrentAlive();
        if (!repoping && currentAlive <= 0)
        {
            repoping = true;
            Repopulate();
            repoping = false;
        }
    }

    public int CurrentAlive()
    {
        int alive = 0;
        for(int i = 0; i < allNeatAnimals.Length; i++){
            if(allNeatAnimals[i].gameObject)
            {
                alive++;
            }
        }
        return alive;
    }

    private void Repopulate()
    {
        currentGeneration++;
    }

    // TODO: Use a faster sorting algorithm.
    private void SortPopulation()
    {
        for(int i = 0; i < allNeatNetworks.Length; i++)
        {
            for(int j = i; j < allNeatNetworks.Length; j++)
            {
                if(allNeatNetworks[i].fitness < allNeatNetworks[j].fitness)
                {
                    NeatNetwork temp = allNeatNetworks[i];
                    allNeatNetworks[i] = allNeatNetworks[j];
                    allNeatNetworks[j] = temp;
                }
            }
        }
    }
    
    private void SetNewPopulationNetworks()
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

    public void Death(float fitness, int index)
    {
        allNeatNetworks[index].fitness = fitness;
    }

}
