package Main.Organisms.Attributes;

public enum Gender {
    MALE {

    },
    FEMALE {

    };

    public boolean canBirth() {
        return this == FEMALE;
    }

    public boolean correctGenderForReproduction(Gender mate) {
        return (this == Gender.FEMALE && mate == Gender.MALE) ||
                (this == Gender.MALE && mate == Gender.FEMALE);
    }

    /**
     * @return a random Gender
     */
    public static Gender getRandomGender() {
        if (Math.random() < .5) return Gender.MALE;
        else return Gender.FEMALE;
    }
}


