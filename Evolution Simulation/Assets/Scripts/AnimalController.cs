using System.Collections;
using System.Collections.Generic;
using UnityEngine;

//https://www.youtube.com/playlist?list=PLC8R0n_dfXXr0fc4NdsInilobjVhpXZk4
public class AnimalController : MonoBehaviour
{
    [Range(-1f,1f)]
    public float a,t;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        MoveAnimal(a,t);
    }

    public void MoveAnimal(float v, float h)
    {
        // Getting Next Position
        Vector3 input = Vector3.Lerp(Vector3.zero, new Vector3(0, v * 2f, 0), 0.1f);
        input = transform.TransformDirection(input);

        // Actual Movement of Agent
        transform.position += input;

        // Rotation of Agent
        transform.eulerAngles += new Vector3(0, 0, (h*90)*0.1f);
    }
}
