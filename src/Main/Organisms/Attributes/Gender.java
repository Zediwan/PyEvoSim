package Main.Organisms.Attributes;

import Main.Organisms.Animal;

public enum Gender {
    MALE {
        @Override
        public void getPregnant(Animal mate) {
            throw new UnsupportedOperationException("Male animals cannot get pregnant.");
        }

        @Override
        public void giveBirth() {
            throw new UnsupportedOperationException("Male animals cannot give birth.");
        }

        @Override
        public boolean isPregnant() {
            throw new UnsupportedOperationException("Male animals cannot be pregnant.");
        }
    },
    FEMALE {
        private boolean pregnant = false;

        @Override
        public void getPregnant(Animal mate) {
            if (!this.pregnant) {
                this.setMate(mate);
                this.pregnant = true;
                // Start the timer here
            }
        }

        @Override
        public void giveBirth() {
            this.setMate(null);
            this.pregnant = false;
        }

        @Override
        public boolean isPregnant() {
            return this.pregnant;
        }
    };

    private Animal mate;

    public abstract void getPregnant(Animal mate);

    public abstract void giveBirth();

    public abstract boolean isPregnant();

    public boolean canBirth() {
        return this == FEMALE;
    }

    public boolean correctGender(Gender mate) {
        return (this == Gender.FEMALE && mate == Gender.MALE) ||
                (this == Gender.MALE && mate == Gender.FEMALE);
    }

    public Animal getMate() {
        return mate;
    }

    public void setMate(Animal mate) {
        assert mate != null ? this.correctGender(mate.getGender()) : true : "wrong mate gender";
        this.mate = mate;
    }

    /**
     * @return a random Gender
     */
    public static Gender getRandomGender() {
        if (Math.random() < .5) return Gender.MALE;
        else return Gender.FEMALE;
    }
}


