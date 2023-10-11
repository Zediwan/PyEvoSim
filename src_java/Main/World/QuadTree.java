package Main.World;

import Main.GUI.SimulationGUI;
import Main.Organisms.Animal;
import Main.Organisms.Plant;

import java.awt.*;
import java.awt.geom.Ellipse2D;
import java.awt.geom.Rectangle2D;
import java.util.ArrayList;

public abstract class QuadTree {
    protected int depth;
    protected int maxDepth = 10;

    protected int capacity;
    protected Rectangle2D.Double boundary;
    protected boolean isDivided  = false;
    protected World w;

    public int getCapacity() {
        return capacity;
    }

    public void setCapacity(int capacity) {
        this.capacity = capacity;
    }

    public int getDepth() {
        return depth;
    }

    public void setDepth(int depth) {
        this.depth = depth;
    }

    public int getMaxDepth() {
        return maxDepth;
    }

    public void setMaxDepth(int maxDepth) {
        this.maxDepth = maxDepth;
    }

    public static class Animals extends QuadTree {
        private ArrayList<Animal> animals;

        protected QuadTree.Animals northeast;
        protected QuadTree.Animals northwest;
        protected QuadTree.Animals southwest;
        protected QuadTree.Animals southeast;

        public Animals(Rectangle2D.Double boundary, int capacity, int depth, World w) {
            assert capacity > 0 : "capacity is smaller than 1";
            this.boundary = boundary;
            this.capacity = capacity;
            this.depth = depth;
            this.animals = new ArrayList<>();
            this.w = w;
        }

        public Animals(Rectangle2D.Double boundary, int capacity, World w) {
            assert capacity > 0 : "capacity is smaller than 1";
            this.boundary = boundary;
            this.capacity = capacity;
            this.depth = 0;
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
            Point center = a.getTransform().getLocation().toPoint();
            if(!this.boundary.contains(center)){
                return false;
            }

            assert (this.boundary.x <= center.x && center.x <= this.boundary.x + this.boundary.width &&
                    this.boundary.y <= center.y && center.y <= this.boundary.y + this.boundary.height);

            if(!this.isDivided){
                if(this.animals.size() < this.capacity || this.depth == this.maxDepth){
                    this.animals.add(a);
                    return true;
                }

                this.subdivide();
            }
            return (
                    this.northeast.insert(a) ||
                            this.northwest.insert(a) ||
                            this.southeast.insert(a) ||
                            this.southwest.insert(a)
            );
        }

        private void subdivide() {
            double x = this.boundary.x;
            double y = this.boundary.y;
            double w = this.boundary.width;
            double h = this.boundary.height;

            this.northeast =  new QuadTree.Animals(new Rectangle2D.Double(x , y , w / 2, h/2), this.capacity, this.depth+1, this.w);
            this.northwest = new QuadTree.Animals(new Rectangle2D.Double(x + w/2 , y , w / 2, h/2), this.capacity, this.depth+1, this.w);
            this.southwest = new QuadTree.Animals(new Rectangle2D.Double(x, y + h/2, w/2, h/2), this.capacity, this.depth+1, this.w);
            this.southeast = new QuadTree.Animals(new Rectangle2D.Double(x + w/2, y + h/2, w/2, h/2), this.capacity, this.depth+1, this.w);

            this.isDivided = true;

            // Move points to children.
            // This improves performance by placing points
            // in the smallest available rectangle.
            for (Animal a : this.animals) {
                boolean inserted =
                        this.northeast.insert(a) ||
                                this.northwest.insert(a) ||
                                this.southeast.insert(a) ||
                                this.southwest.insert(a);

                assert inserted;
            }

            this.animals.clear();
        }

        /**
         * @deprecated since 11.04.2023 use {@link QuadTree.Animals#query(Shape)} instead
         * @param a
         * @return
         */
        public ArrayList<Animal> query(Animal a){
            ArrayList<Animal> found = new ArrayList<>();
            Ellipse2D rangeArea = a.getSensoryRadius();

            //if they don't intersect return an empty array
            if(!rangeArea.intersects(this.boundary)){
                return found;
            }

            //check for all subdivisions if divided
            if(this.isDivided){
                this.northwest.query(a, found);
                this.northeast.query(a, found);
                this.southwest.query(a, found);
                this.southeast.query(a, found);
            }

            for(Animal ani : this.animals){
                //check if the organism is in the area
                if(rangeArea.contains(ani.getLocation().toPoint())){
                    found.add(ani);
                }
            }

            return found;
        }

        /**
         * @deprecated since 11.04.2023 use {@link QuadTree.Animals#query(Shape, ArrayList)} instead
         * @param a
         * @param found
         * @return
         */
        public ArrayList<Animal> query(Animal a, ArrayList<Animal> found){
            Ellipse2D rangeArea = a.getSensoryRadius();

            //if they don't intersect return an empty array
            if(!rangeArea.intersects(this.boundary)){
                return found;
            }

            //check for all subdivisions if divided
            if(this.isDivided){
                this.northwest.query(a, found);
                this.northeast.query(a, found);
                this.southwest.query(a, found);
                this.southeast.query(a, found);
            }

            for(Animal ani : this.animals){
                //check if the organism is in the area
                if(rangeArea.contains(ani.getLocation().toPoint())){
                    found.add(ani);
                }
            }

            return found;
        }

        /**
         * @param s
         * @return
         * @since 11.04.2023
         */
        public ArrayList<Animal> query(Shape s){
            ArrayList<Animal> found = new ArrayList<>();

            //if they don't intersect return an empty array
            if(!s.intersects(this.boundary)){
                return found;
            }

            //check for all subdivisions if divided
            if(this.isDivided){
                this.northwest.query(s, found);
                this.northeast.query(s, found);
                this.southwest.query(s, found);
                this.southeast.query(s, found);
            }

            for(Animal ani : this.animals){
                //check if the organism is in the area
                if(s.contains(ani.getLocation().toPoint())){
                    found.add(ani);
                }
            }

            return found;
        }

        /**
         * @param s
         * @param found
         * @return
         * @since 11.04.2023
         */
        public ArrayList<Animal> query(Shape s, ArrayList<Animal> found){
            //if they don't intersect return an empty array
            if(!s.intersects(this.boundary)){
                return found;
            }

            //check for all subdivisions if divided
            if(this.isDivided){
                this.northwest.query(s, found);
                this.northeast.query(s, found);
                this.southwest.query(s, found);
                this.southeast.query(s, found);
            }

            for(Animal ani : this.animals){
                //check if the organism is in the area
                if(s.contains(ani.getLocation().toPoint())){
                    found.add(ani);
                }
            }

            return found;
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
                    g.drawRect((int)Math.round(this.boundary.x), (int)Math.round(this.boundary.y),
                            (int)Math.round(this.boundary.width), (int)Math.round(this.boundary.height));
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

        public Plants(Rectangle2D.Double boundary, int capacity, int depth, World w) {
            assert capacity > 0 : "capacity is smaller than 1";
            this.boundary = boundary;
            this.capacity = capacity;
            this.depth = depth;
            this.plants = new ArrayList<>();
            this.w = w;
        }

        public Plants(Rectangle2D.Double boundary, int capacity, World w) {
            assert capacity > 0 : "capacity is smaller than 1";
            this.boundary = boundary;
            this.capacity = capacity;
            this.depth = 0;
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
            Point center = p.getTransform().getLocation().toPoint();
            if(!this.boundary.contains(center)){
                return false;
            }

            assert (this.boundary.x <= center.x && center.x <= this.boundary.x + this.boundary.width &&
                    this.boundary.y <= center.y && center.y <= this.boundary.y + this.boundary.height);

            if(!this.isDivided){
                if(this.plants.size() < this.capacity || this.depth == this.maxDepth){
                    this.plants.add(p);
                    return true;
                }

                this.subdivide();
            }
            return (this.northeast.insert(p) || this.northwest.insert(p) ||
                    this.southeast.insert(p) || this.southwest.insert(p));

            /*
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
             */
        }

        private void subdivide() {
            double x = this.boundary.x;
            double y = this.boundary.y;
            double w = this.boundary.width;
            double h = this.boundary.height;

            this.northeast =  new QuadTree.Plants(new Rectangle2D.Double(x + w/2, y , w / 2, h/2), this.capacity, this.depth+1, this.w);
            this.northwest = new QuadTree.Plants(new Rectangle2D.Double(x , y , w / 2, h/2), this.capacity, this.depth+1, this.w);
            this.southwest = new QuadTree.Plants(new Rectangle2D.Double(x, y + h/2, w/2, h/2), this.capacity, this.depth+1, this.w);
            this.southeast = new QuadTree.Plants(new Rectangle2D.Double(x + w/2, y + h/2, w/2, h/2), this.capacity, this.depth+1, this.w);

            this.isDivided = true;

            // Move points to children.
            // This improves performance by placing points
            // in the smallest available rectangle.
            for (Plant p : this.plants) {
                boolean inserted =
                                this.northeast.insert(p) ||
                                this.northwest.insert(p) ||
                                this.southeast.insert(p) ||
                                this.southwest.insert(p);

                assert inserted;
            }

            this.plants.clear();
        }

        /**
         * @deprecated since 11.04.2023 use {@link QuadTree.Plants#query(Shape)} instead
         * @param a
         * @return
         */
        public ArrayList<Plant> query(Animal a){
            ArrayList<Plant> found = new ArrayList<>();
            Ellipse2D rangeArea = a.getSensoryRadius();

            //if they don't intersect return an empty array
            if(!rangeArea.intersects(this.boundary)){
                return found;
            }

            //check for all subdivisions if divided
            if(this.isDivided){
                this.northwest.query(a, found);
                this.northeast.query(a, found);
                this.southwest.query(a, found);
                this.southeast.query(a, found);
            }

            for(Plant p : this.plants){
                //check if the organism is in the area
                if(rangeArea.contains(p.getLocation().toPoint())){
                    found.add(p);
                }
            }

            return found;
        }

        /**
         * @deprecated since 11.04.2023 use {@link QuadTree.Plants#query(Shape, ArrayList)} instead
         * @param a
         * @param found
         * @return
         */
        public ArrayList<Plant> query(Animal a, ArrayList<Plant> found){
            Ellipse2D rangeArea = a.getSensoryRadius();

            //if they don't intersect return an empty array
            if(!rangeArea.intersects(this.boundary)){
                return found;
            }

            //check for all subdivisions if divided
            if(this.isDivided){
                this.northwest.query(a, found);
                this.northeast.query(a, found);
                this.southwest.query(a, found);
                this.southeast.query(a, found);
            }

            for(Plant p : this.plants){
                //check if the organism is in the area
                if(rangeArea.contains(p.getLocation().toPoint())){
                    found.add(p);
                }
            }

            return found;
        }

        /**
         * @param s
         * @return
         * @since 11.04.2023
         */
        public ArrayList<Plant> query(Shape s){
            ArrayList<Plant> found = new ArrayList<>();

            //if they don't intersect return an empty array
            if(!s.intersects(this.boundary)){
                return found;
            }

            //check for all subdivisions if divided
            if(this.isDivided){
                this.northwest.query(s, found);
                this.northeast.query(s, found);
                this.southwest.query(s, found);
                this.southeast.query(s, found);
            }

            for(Plant pla : this.plants){
                //check if the organism is in the area
                if(s.contains(pla.getLocation().toPoint())){
                    found.add(pla);
                }
            }

            return found;
        }

        /**
         * @param s
         * @param found
         * @return
         * @since 11.04.2023
         */
        public ArrayList<Plant> query(Shape s, ArrayList<Plant> found){
            //if they don't intersect return an empty array
            if(!s.intersects(this.boundary)){
                return found;
            }

            //check for all subdivisions if divided
            if(this.isDivided){
                this.northwest.query(s, found);
                this.northeast.query(s, found);
                this.southwest.query(s, found);
                this.southeast.query(s, found);
            }

            for(Plant plant : this.plants){
                //check if the organism is in the area
                if(s.contains(plant.getLocation().toPoint())){
                    found.add(plant);
                }
            }

            return found;
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
                    g.drawRect((int)Math.round(this.boundary.x), (int)Math.round(this.boundary.y),
                            (int)Math.round(this.boundary.width), (int)Math.round(this.boundary.height));
                }
            }
        }
    }
}
