/*
import java.awt.*;

public class Vehicle {
    Main.Main.NeuralNetwork.NeuralNetwork.Vector2D location;
    Main.Main.NeuralNetwork.NeuralNetwork.Vector2D velocity;
    Main.Main.NeuralNetwork.NeuralNetwork.Vector2D acceleration;

    float r = 1;        //radius
    float maxForce = 1; //maximum steering force
    float maxSpeed = 10; //maximum speed

    public Vehicle(float x, float y){
        acceleration = new Main.Main.NeuralNetwork.NeuralNetwork.Vector2D();
        velocity = new Main.Main.NeuralNetwork.NeuralNetwork.Vector2D();
        location = new Main.Main.NeuralNetwork.NeuralNetwork.Vector2D(x,y);
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
        if(this.location.x < -this.r)this.location.x = Main.Main.NeuralNetwork.NeuralNetwork.CFrame.WIDTH+this.r;
        if(this.location.y < -this.r)this.location.y = Main.Main.NeuralNetwork.NeuralNetwork.CFrame.HEIGHT+this.r;
        if(this.location.x > Main.Main.NeuralNetwork.NeuralNetwork.CFrame.WIDTH+this.r)this.location.x = -this.r;
        if(this.location.y > Main.Main.NeuralNetwork.NeuralNetwork.CFrame.HEIGHT+this.r)this.location.y = -this.r;
    }

    public void seek(Main.Main.NeuralNetwork.NeuralNetwork.Vector2D target){
        Main.Main.NeuralNetwork.NeuralNetwork.Vector2D desired = Main.Main.NeuralNetwork.NeuralNetwork.Vector2D.sub(target,this.location);

        desired.setMag(this.maxSpeed);

        Main.Main.NeuralNetwork.NeuralNetwork.Vector2D steer = Main.Main.NeuralNetwork.NeuralNetwork.Vector2D.sub(desired,this.velocity);
        steer.limit(this.maxForce);
        applyForce(steer);
    }

    public void arrive(Main.Main.NeuralNetwork.NeuralNetwork.Vector2D target){
        Main.Main.NeuralNetwork.NeuralNetwork.Vector2D desired = Main.Main.NeuralNetwork.NeuralNetwork.Vector2D.sub(target,this.location);  //Vector from target to this
        float distance = desired.mag();                         //calculate the distance

        if(distance <= this.r){
            float m = Main.Main.NeuralNetwork.NeuralNetwork.Vector2D.map(distance,0,this.r,0,this.maxSpeed);
            desired.setMag(m);
        }else desired.setMag(this.maxSpeed);

        //Steering = Desired minus Velocity
        Main.Main.NeuralNetwork.NeuralNetwork.Vector2D steer = Main.Main.NeuralNetwork.NeuralNetwork.Vector2D.sub(desired,this.velocity);
        steer.limit(this.maxForce);                                  //Limit to maximum steering
        applyForce(steer);
    }

    public void follow(FlowField flow){
        Main.Main.NeuralNetwork.NeuralNetwork.Vector2D desired = flow.lookup(this.location);
        desired.setMag(this.maxSpeed);

        Main.Main.NeuralNetwork.NeuralNetwork.Vector2D steer = Main.Main.NeuralNetwork.NeuralNetwork.Vector2D.sub(desired,this.velocity);
        steer.limit(this.maxForce);
        applyForce(steer);
    }

    private void applyForce(Main.Main.NeuralNetwork.NeuralNetwork.Vector2D force) {
        this.acceleration.add(force);
    }

    public void paint(Graphics g){
        g.setColor(Color.BLACK);
        g.drawLine((int)this.location.x,(int)this.location.y, (int)(this.location.x +this.velocity.x), (int)(this.location.y + this.velocity.y));
    }
}

 */