using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Animal : MonoBehaviour
{
    Vector3 location;       //current location
    Vector3 velocity;       //current traveling direction
    Vector3 acceleration;   //current desired change of direction

    public float health;
    public float energy;
    public float maxForce;
    public float maxSpeed;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {

        //this.addAcceleration();
    }

    public void move(){
        if(this.maxSpeed <= 0){
            return;
        }else{
            this.addVelocity(this.acceleration);

            this.location += this.velocity;
            this.acceleration *= 0;  //TODO think more about this, if it is needed everytime...
        }
    }

    public void addVelocity(Vector3 v){
        this.velocity += v;
        this.velocity = Vector3.ClampMagnitude(this.velocity, this.maxSpeed);
    }

    public void addAcceleration(Vector3 v){
        this.acceleration += v;
        this.acceleration = Vector3.ClampMagnitude(this.velocity, this.maxForce);
    }
}
