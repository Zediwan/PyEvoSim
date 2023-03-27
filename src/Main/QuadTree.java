package Main;

import Main.Helper.Vector2D;
import Main.Organisms.Animal;
import Main.Organisms.Plant;

import java.awt.*;
import java.awt.geom.Ellipse2D;
import java.util.ArrayList;

public abstract class QuadTree {
    protected int capacity;
    protected Rectangle boundary;
    protected boolean isDivided  = false;
    protected World w;

    public static class Animals extends QuadTree {
        private ArrayList<Animal> animals;

        protected QuadTree.Animals northeast;
        protected QuadTree.Animals northwest;
        protected QuadTree.Animals southwest;
        protected QuadTree.Animals southeast;

        public Animals(Rectangle boundary, int capacity, World w) {
            assert capacity > 0 : "capacity is smaller than 1";
            this.boundary = boundary;
            this.capacity = capacity;
            this.animals = new ArrayList<>();
            this.w = w;
        }

        public void clear() {
            this.animals.clear();

            if(this.isDivided){
                this.northwest = null;
                this.northeast = null;
                this.southwest = null;
                this.southeast = null;
                this.isDivided = false;
            }
        }

        public boolean insert(Animal a){
            Point p = a.getLoc().toPoint();
            if(!this.boundary.contains(p)){
                return false;
            }
            if(this.animals.size() < this.capacity){
                this.animals.add(a);
                return true;
            }
            else{
                if(!this.isDivided){
                    this.subdivide();
                }

                if(this.northwest.insert(a)){
                    return true;
                }
                else if(this.northeast.insert(a)){
                    return true;
                }
                else if(this.southwest.insert(a)){
                    return true;
                }
                else if(this.southeast.insert(a)){
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

            this.northeast =  new QuadTree.Animals(new Rectangle(x , y , w / 2, h/2), this.capacity, this.w);
            this.northwest = new QuadTree.Animals(new Rectangle(x + w/2 , y , w / 2, h/2), this.capacity, this.w);
            this.southwest = new QuadTree.Animals(new Rectangle(x, y + h/2, w/2, h/2), this.capacity, this.w);
            this.southeast = new QuadTree.Animals(new Rectangle(x + w/2, y + h/2, w/2, h/2), this.capacity, this.w);

            this.isDivided = true;
        }

        public ArrayList<Animal> query(Animal a){
            ArrayList<Animal> animalsFound = new ArrayList<Animal>();
            Ellipse2D rangeArea = a.getSensoryRadius();

            //if they don't intersect return an empty array
            if(!rangeArea.intersects(this.boundary)){
                return animalsFound;
            }
            else{
                for(Animal ani : this.animals){
                    //check if the organism is in the area
                    if(rangeArea.contains(ani.getLoc().toPoint())){
                        animalsFound.add(ani);
                    }
                }

                //check for all subdivisions if divided
                if(this.isDivided){
                    this.northwest.query(a, animalsFound);
                    this.northeast.query(a, animalsFound);
                    this.southwest.query(a, animalsFound);
                    this.southeast.query(a, animalsFound);
                }

                return animalsFound;
            }
        }

        public ArrayList<Animal> query(Animal a, ArrayList<Animal> animalsFound){
            Ellipse2D rangeArea = a.getSensoryRadius();

            //if they don't intersect return an empty array
            if(!rangeArea.intersects(this.boundary)){
                return animalsFound;
            }
            else{
                for(Animal ani : this.animals){
                    //check if the organism is in the area
                    if(rangeArea.contains(ani.getLoc().toPoint())){
                        animalsFound.add(ani);
                    }
                }

                //check for all subdivisions if divided
                if(this.isDivided){
                    this.northwest.query(a, animalsFound);
                    this.northeast.query(a, animalsFound);
                    this.southwest.query(a, animalsFound);
                    this.southeast.query(a, animalsFound);
                }

                return animalsFound;
            }
        }

        public ArrayList<Animal> query(Vector2D v, int range){
            ArrayList<Animal> organismsFound = new ArrayList<Animal>();
            Rectangle rangeArea = new Rectangle((int)(v.x - range / 2), (int)(v.y - range / 2), range, range);

            //if they don't intersect return an empty array
            if(!this.boundary.intersects(rangeArea)){
                return organismsFound;
            }
            else{
                for(Animal a : this.animals){
                    //check if the organism is in the area
                    if(rangeArea.contains(a.getLoc().toPoint())){
                        organismsFound.add(a);
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

        public ArrayList<Animal> query(Vector2D v, int range, ArrayList<Animal> organismsFound){
            Rectangle rangeArea = new Rectangle((int)(v.x - range / 2), (int)(v.y - range / 2), range, range);

            //if they don't intersect return the array
            if(!this.boundary.intersects(rangeArea)){
                return organismsFound;
            }
            else{
                for(Animal a : this.animals){
                    //check if the organism is in the area
                    if(rangeArea.contains(a.getLoc().toPoint())){
                        organismsFound.add(a);
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
            if(SimulationGUI.showAnimalQT){
                if(this.isDivided){
                    this.northwest.paint(g);
                    this.northeast.paint(g);
                    this.southwest.paint(g);
                    this.southeast.paint(g);
                }
                else{
                    g.drawRect(this.boundary.x, this.boundary.y, this.boundary.width, this.boundary.height);
                }
            }
        }
    }

    public static class Plants extends QuadTree {
        private ArrayList<Plant> plants;

        protected QuadTree.Plants northeast;
        protected QuadTree.Plants northwest;
        protected QuadTree.Plants southwest;
        protected QuadTree.Plants southeast;

        public Plants(Rectangle boundary, int capacity, World w) {
            assert capacity > 0 : "capacity is smaller than 1";
            this.boundary = boundary;
            this.capacity = capacity;
            this.plants = new ArrayList<>();
            this.w = w;
        }

        public void clear() {
            this.plants.clear();

            if(this.isDivided){
                this.northwest = null;
                this.northeast = null;
                this.southwest = null;
                this.southeast = null;
                this.isDivided = false;
            }
        }

        public boolean insert(Plant p){
            Point point = p.getLoc().toPoint();
            if(!this.boundary.contains(point)){
                return false;
            }
            if(this.plants.size() < this.capacity){
                this.plants.add(p);
                return true;
            }
            else{
                if(!this.isDivided){
                    this.subdivide();
                }

                if(this.northwest.insert(p)){
                    return true;
                }
                else if(this.northeast.insert(p)){
                    return true;
                }
                else if(this.southwest.insert(p)){
                    return true;
                }
                else if(this.southeast.insert(p)){
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

            this.northeast =  new QuadTree.Plants(new Rectangle(x , y , w / 2, h/2), this.capacity, this.w);
            this.northwest = new QuadTree.Plants(new Rectangle(x + w/2 , y , w / 2, h/2), this.capacity, this.w);
            this.southwest = new QuadTree.Plants(new Rectangle(x, y + h/2, w/2, h/2), this.capacity, this.w);
            this.southeast = new QuadTree.Plants(new Rectangle(x + w/2, y + h/2, w/2, h/2), this.capacity, this.w);

            this.isDivided = true;
        }

        public ArrayList<Plant> query(Animal a){
            ArrayList<Plant> animalsFound = new ArrayList<Plant>();
            Ellipse2D rangeArea = a.getSensoryRadius();

            //if they don't intersect return an empty array
            if(!rangeArea.intersects(this.boundary)){
                return animalsFound;
            }
            else{
                for(Plant p : this.plants){
                    //check if the organism is in the area
                    if(rangeArea.contains(p.getLoc().toPoint())){
                        animalsFound.add(p);
                    }
                }

                //check for all subdivisions if divided
                if(this.isDivided){
                    this.northwest.query(a, animalsFound);
                    this.northeast.query(a, animalsFound);
                    this.southwest.query(a, animalsFound);
                    this.southeast.query(a, animalsFound);
                }

                return animalsFound;
            }
        }

        public ArrayList<Plant> query(Animal a, ArrayList<Plant> plantsFound){
            Ellipse2D rangeArea = a.getSensoryRadius();

            //if they don't intersect return an empty array
            if(!rangeArea.intersects(this.boundary)){
                return plantsFound;
            }
            else{
                for(Plant p : this.plants){
                    //check if the organism is in the area
                    if(rangeArea.contains(p.getLoc().toPoint())){
                        plantsFound.add(p);
                    }
                }

                //check for all subdivisions if divided
                if(this.isDivided){
                    this.northwest.query(a, plantsFound);
                    this.northeast.query(a, plantsFound);
                    this.southwest.query(a, plantsFound);
                    this.southeast.query(a, plantsFound);
                }

                return plantsFound;
            }
        }

        public ArrayList<Plant> query(Vector2D v, int range){
            ArrayList<Plant> organismsFound = new ArrayList<Plant>();
            Rectangle rangeArea = new Rectangle((int)(v.x - range / 2), (int)(v.y - range / 2), range, range);

            //if they don't intersect return an empty array
            if(!this.boundary.intersects(rangeArea)){
                return organismsFound;
            }
            else{
                for(Plant p : this.plants){
                    //check if the organism is in the area
                    if(rangeArea.contains(p.getLoc().toPoint())){
                        organismsFound.add(p);
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

        public ArrayList<Plant> query(Vector2D v, int range, ArrayList<Plant> plantsFound){
            Rectangle rangeArea = new Rectangle((int)(v.x - range / 2), (int)(v.y - range / 2), range, range);

            //if they don't intersect return the array
            if(!this.boundary.intersects(rangeArea)){
                return plantsFound;
            }
            else{
                for(Plant p : this.plants){
                    //check if the organism is in the area
                    if(rangeArea.contains(p.getLoc().toPoint())){
                        plantsFound.add(p);
                    }
                }

                //check for all subdivisions if divided
                if(this.isDivided){
                    this.northwest.query(v, range, plantsFound);
                    this.northeast.query(v, range, plantsFound);
                    this.southwest.query(v, range, plantsFound);
                    this.southeast.query(v, range, plantsFound);
                }

                return plantsFound;
            }
        }
        public void paint(Graphics2D g){
            if(SimulationGUI.showPlantQT){
                if(this.isDivided){
                    this.northwest.paint(g);
                    this.northeast.paint(g);
                    this.southwest.paint(g);
                    this.southeast.paint(g);
                }
                else{
                    g.drawRect(this.boundary.x, this.boundary.y, this.boundary.width, this.boundary.height);
                }
            }
        }
    }
}
