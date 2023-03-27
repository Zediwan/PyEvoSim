import Main.Helper.Vector2D;
import Main.Organisms.Organism;

import java.awt.*;
import java.util.ArrayList;

public class QuadTree {
    private ArrayList<Organism> organisms;
    private int capacity;
    private Rectangle boundary;
    private QuadTree northeast;
    private QuadTree northwest;
    private QuadTree southwest;
    private QuadTree southeast;
    private boolean isDivided  = false;

    public QuadTree(Rectangle boundary, int capacity) {
        assert capacity > 0 : "capacity is smaller than 1";
        this.boundary = boundary;
        this.capacity = capacity;
        this.organisms = new ArrayList<>();
    }

    public boolean insert(Organism o){
        Point p = o.getLoc().toPoint();
        if(!this.boundary.contains(p)){
            return false;
        }
        if(this.organisms.size() < this.capacity){
            this.organisms.add(o);
            return true;
        }
        else{
            if(!this.isDivided){
                this.subdivide();
            }

            if(this.northwest.insert(o)){
                return true;
            }
            else if(this.northeast.insert(o)){
                return true;
            }
            else if(this.southwest.insert(o)){
                return true;
            }
            else if(this.southeast.insert(o)){
                return true;
            }
        }
        return false;
    }

    private void subdivide() {
        int x = this.boundary.x;
        int y = this.boundary.y;
        int w = this.boundary.width;
        int h = this.boundary.height;

        this.northeast =  new QuadTree(new Rectangle(x , y , w / 2, h/2), this.capacity);
        this.northwest = new QuadTree(new Rectangle(x + w/2 , y , w / 2, h/2), this.capacity);
        this.southwest = new QuadTree(new Rectangle(x, y + h/2, w/2, h/2), this.capacity);
        this.southeast = new QuadTree(new Rectangle(x + w/2, y + h/2, w/2, h/2), this.capacity);

        this.isDivided = true;
    }

    public ArrayList<Organism> query(Vector2D v, int range){
        ArrayList<Organism> organismsFound = new ArrayList<Organism>();
        Rectangle rangeArea = new Rectangle((int)(v.x - range / 2), (int)(v.y - range / 2), range, range);

        //if they don't intersect return an empty array
        if(!this.boundary.intersects(rangeArea)){
            return organismsFound;
        }
        else{
            for(Organism o : this.organisms){
                //check if the organism is in the area
                if(rangeArea.contains(o.getLoc().toPoint())){
                    organismsFound.add(o);
                }
            }

            //check for all subdivisions if divided
            if(this.isDivided){
                this.northwest.query(v, range, organismsFound);
                this.northeast.query(v, range, organismsFound);
                this.southwest.query(v, range, organismsFound);
                this.southeast.query(v, range, organismsFound);
            }

            return organismsFound;
        }
    }

    public ArrayList<Organism> query(Vector2D v, int range, ArrayList<Organism> organismsFound){
        Rectangle rangeArea = new Rectangle((int)(v.x - range / 2), (int)(v.y - range / 2), range, range);

        //if they don't intersect return the array
        if(!this.boundary.intersects(rangeArea)){
            return organismsFound;
        }
        else{
            for(Organism o : this.organisms){
                //check if the organism is in the area
                if(rangeArea.contains(o.getLoc().toPoint())){
                    organismsFound.add(o);
                }
            }

            //check for all subdivisions if divided
            if(this.isDivided){
                this.northwest.query(v, range, organismsFound);
                this.northeast.query(v, range, organismsFound);
                this.southwest.query(v, range, organismsFound);
                this.southeast.query(v, range, organismsFound);
            }

            return organismsFound;
        }
    }

    public void paint(Graphics2D g){
        g.drawRect(this.boundary.x, this.boundary.y, this.boundary.width, this.boundary.height);
        if(this.isDivided){
            this.northwest.paint(g);
            this.northeast.paint(g);
            this.southwest.paint(g);
            this.southeast.paint(g);
        }
    }
}
