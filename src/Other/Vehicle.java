/*
import java.awt.*;

public class Vehicle {
    Vector2D location;
    Vector2D velocity;
    Vector2D acceleration;

    float r = 1;        //radius
    float maxForce = 1; //maximum steering force
    float maxSpeed = 10; //maximum speed

    public Vehicle(float x, float y){
        acceleration = new Vector2D();
        velocity = new Vector2D();
        location = new Vector2D(x,y);
    }

    public Vehicle(float x, float y, float r, float maxForce, float maxSpeed){
        this(x,y);
        this.r = r;
        this.maxForce = maxForce;
        this.maxSpeed = maxSpeed;
    }

    public void run(Graphics g){
        this.update();
        this.borders();
        this.paint(g);
    }

    public void update(){
        this.velocity.add(this.acceleration);
        this.velocity.limit(this.maxSpeed);
        this.location.add(this.velocity);
        this.acceleration.mult(0);
    }

    public void borders(){
        if(this.location.x < -this.r)this.location.x = CFrame.WIDTH+this.r;
        if(this.location.y < -this.r)this.location.y = CFrame.HEIGHT+this.r;
        if(this.location.x > CFrame.WIDTH+this.r)this.location.x = -this.r;
        if(this.location.y > CFrame.HEIGHT+this.r)this.location.y = -this.r;
    }

    public void seek(Vector2D target){
        Vector2D desired = Vector2D.sub(target,this.location);

        desired.setMag(this.maxSpeed);

        Vector2D steer = Vector2D.sub(desired,this.velocity);
        steer.limit(this.maxForce);
        applyForce(steer);
    }

    public void arrive(Vector2D target){
        Vector2D desired = Vector2D.sub(target,this.location);  //Vector from target to this
        float distance = desired.mag();                         //calculate the distance

        if(distance <= this.r){
            float m = Vector2D.map(distance,0,this.r,0,this.maxSpeed);
            desired.setMag(m);
        }else desired.setMag(this.maxSpeed);

        //Steering = Desired minus Velocity
        Vector2D steer = Vector2D.sub(desired,this.velocity);
        steer.limit(this.maxForce);                                  //Limit to maximum steering
        applyForce(steer);
    }

    public void follow(FlowField flow){
        Vector2D desired = flow.lookup(this.location);
        desired.setMag(this.maxSpeed);

        Vector2D steer = Vector2D.sub(desired,this.velocity);
        steer.limit(this.maxForce);
        applyForce(steer);
    }

    private void applyForce(Vector2D force) {
        this.acceleration.add(force);
    }

    public void paint(Graphics g){
        g.setColor(Color.BLACK);
        g.drawLine((int)this.location.x,(int)this.location.y, (int)(this.location.x +this.velocity.x), (int)(this.location.y + this.velocity.y));
    }
}

 */