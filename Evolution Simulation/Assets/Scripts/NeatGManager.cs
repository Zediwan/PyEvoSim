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
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
