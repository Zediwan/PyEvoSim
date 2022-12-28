import java.awt.*;

public class Grass extends Plant{
    //Constructor
    public Grass(){
        super();
        this.growthInterval = 50;
        this.decodeDNA();
    }

    /**
     * genes[0] = size
     */
    @Override
    public void decodeDNA() {
        this.transform.size = this.dna.genes[0]+3;
    }

    //Behavior
    public void update(){
        this.growthTimer--;
        if(this.growthTimer <= 0){
            this.grow();
            this.growthTimer = this.growthInterval;
        }
    }

    @Override
    public Plant reproduce() {
        return null;
    }

    @Override
    public void grow() {
        this.transform.size += .1;
    }

    @Override
    public void paint(Graphics2D g) {
        Color c = new Color(150, 200, 20 ,125);
        g.setColor(Color.GREEN.darker());
        g.fillOval((int)(this.transform.location.x-this.transform.size/2),(int)(this.transform.location.y-this.transform.size/2),(int)this.transform.size,(int)this.transform.size);
    }
}
