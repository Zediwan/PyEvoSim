package Main.Organisms.Attributes;

import Main.Organisms.Animals.Animal;

public enum Gender {
    //TODO: implement methods that come with being female f.e. getPregnant and giveBirth
    MALE{

    },
    FEMALE{

    };

    private Animal mate;

    public boolean canBirth(){
        return this == FEMALE;
    }

    public Animal getMate(){
        return mate;
    }

    public void setMate(Animal mate){
        this.mate = mate;
    }

    /**
     * @return a random Gender
     */
    public static Gender getRandomGender(){
        if(Math.random() < .5)return Gender.MALE;
        else return Gender.FEMALE;
    }
}
