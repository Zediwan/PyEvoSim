using System.Collections;
using System.Collections.Generic;
using UnityEngine;

//https://www.youtube.com/playlist?list=PLC8R0n_dfXXr0fc4NdsInilobjVhpXZk4
public class AnimalController : MonoBehaviour
{
    public NeatNetwork myNetwork;

    private float[] sensors;

    private float hitDivider = 20f;
    private float rayDistance = 50f;

    [Header("Energy Options")]

    public float totalEnergy;
    public float rewardEnergy;
    public float currentEnergy;

    [Header("Fitness Options")]

    public float overallFitness = 0;
    public float plantsMultiplier;
    public float plantsSinceStart = 0f;

    [Header("Network Settings")]

    public int myBrainIndex;

    public int inputNodes, outputNodes, hiddenNodes; // Number of respective nodes for the initial network

    void Start()
    {
        currentEnergy = totalEnergy;
        sensors = new float[inputNodes];    //Initialize the sensors
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        InputSensors();
        float[] outputs = myNetwork.FeedForwardNetwork(sensors); // Pass in sensor information

        MoveAnimal(outputs[0], outputs[1]);
        CalculateFitness();
    }

    private void CalculateFitness()
    {
        UpdateEnergy();
        overallFitness = (plantsSinceStart * plantsMultiplier);

        if(currentEnergy <= 0)
        {
            Death();
        }
    }

    private void UpdateEnergy()
    {
        currentEnergy -=  Time.deltaTime;
    }

    private void Death()
    {
        GameObject.FindObjectOfType<NeatGManager>().Death(overallFitness, myBrainIndex);
        Destroy(gameObject);
    }

    private void OnCollisionEnter(Collision other) {
        if(other.transform.tag == "Wall")
        {
            overallFitness = 0;
            Death();
        }
        else if(other.transform.tag == "Plant")
        {
            other.gameObject.GetComponent<PlantController>().SpawnSinglePlant();
            Destroy(other.gameObject);
            currentEnergy += rewardEnergy;
            plantsSinceStart += 1;
        }
    }

    private void InputSensors()
    {
        Ray r = new Ray(transform.position, transform.up);
        RaycastHit hit;
        if(Physics.Raycast(r, out hit, rayDistance))
        {
            if(hit.transform.tag == "Wall")
            {
                sensors[0] = hit.distance / hitDivider;
                Debug.DrawLine(r.origin, hit.point, Color.white);
            }
        }
        r.direction = (transform.up + transform.right);
        if(Physics.Raycast(r, out hit, rayDistance))
        {
            if(hit.transform.tag == "Wall")
            {
                sensors[1] = hit.distance / hitDivider;
                Debug.DrawLine(r.origin, hit.point, Color.white);
            }
        }
        r.direction = (transform.up - transform.right);
        if(Physics.Raycast(r, out hit, rayDistance))
        {
            if(hit.transform.tag == "Wall")
            {
                sensors[2] = hit.distance / hitDivider;
                Debug.DrawLine(r.origin, hit.point, Color.white);
            }
        }
    }

    public void MoveAnimal(float v, float h)
    {
        // Getting Next Position.
        Vector3 input = Vector3.Lerp(Vector3.zero, new Vector3(0, v * 2f, 0), 0.1f);
        input = transform.TransformDirection(input);

        // Actual Movement of Agent.
        transform.position += input;

        // Rotation of Agent.
        transform.eulerAngles += new Vector3(0, 0, (h*90)*0.1f);
    }
}
