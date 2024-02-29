package Main.Organisms.Attributes;

public enum Diet {
    OMNIVORE{

    },
    CARNIVORE{

    },
    HERBIVORE{

    };

    /**
     * @return a random Diet
     */
    public static Diet getRandomDiet(){
        double number = Math.random();
        if(number < (1/3)){
            return Diet.OMNIVORE;
        }
        else if (number < (2/3)) {
            return Diet.CARNIVORE;
        }
        else{
            return Diet.HERBIVORE;
        }
    }
}
