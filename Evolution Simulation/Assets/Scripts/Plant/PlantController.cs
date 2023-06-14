using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlantController : MonoBehaviour
{
    public PlantManager plantManager;

    public void SpawnSinglePlant()
    {
        plantManager.SpawnSinglePlant();
    }
}
