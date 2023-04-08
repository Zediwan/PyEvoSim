package Main.Organisms.Attributes.DNA;

public enum GeneType {
    /**
     * note if another gene type is added update {@link Gene#percentageMutate(double, double)}
     */
    COLOR, TIME, PROBABILITY, DISTANCE, BIGGER, SMALLER, OTHER, ANGLE
}
