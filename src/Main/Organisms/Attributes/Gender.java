package Main.Organisms.Attributes;

public enum Gender {
    //TODO: implement methods that come with being female f.e. getPregnant and giveBirth
    MALE,
    FEMALE;

    /**
     * @return a random Gender
     */
    public static Gender getRandomGender(){
        if(Math.random() < .5)return Gender.MALE;
        else return Gender.FEMALE;
    }
}
