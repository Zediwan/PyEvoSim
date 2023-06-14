using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlantManager : MonoBehaviour
{
    public GameObject plantPrefab;
    public int plantCount;
    public int curAlive;
    private GameObject[] plants;
    private bool repoping = false;    

    // Start is called before the first frame update
    void Awake()
    {
        curAlive = plantCount;
        plants = new GameObject[plantCount];
        SpawnPlants();
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        curAlive = CurrentAlive();
        if (!repoping && curAlive <= 0)
        {
            repoping = true;
            SpawnPlants();
            repoping = false;
        }
    }

    public int CurrentAlive()
    {
        PlantController[] localPlant = FindObjectsOfType<PlantController>();
        return localPlant.Length;
    }

    public void DestroyPlants()
    {
        PlantController[] localPlant = FindObjectsOfType<PlantController>();
        foreach(PlantController plant in localPlant)
        {
            Destroy(plant.gameObject);
        }
    }

    public void SpawnPlants()
    {
        for (int i = 0; i < plantCount; i++)
        {
            Vector3 pos = new Vector3(Random.value, Random.value, 89);
            pos = Camera.main.ViewportToWorldPoint(pos);

            plants[i] = Instantiate(plantPrefab, pos, transform.rotation);
            plants[i].gameObject.GetComponent<PlantController>().plantManager = this;
        }
    }

    public void SpawnSinglePlant()
    {
        Vector3 pos = new Vector3(Random.value, Random.value, 89);
        pos = Camera.main.ViewportToWorldPoint(pos);

        GameObject localPlant = Instantiate(plantPrefab, pos, transform.rotation);
        localPlant.gameObject.GetComponent<PlantController>().plantManager = this;
    }
}
