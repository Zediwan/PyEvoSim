package Main.Helper;

public interface mutable {
    //TODO: check if this interface is applied to all necessary classes
    void rangedMutate();

    void rangedMutate(double mutationChance, double range);

    void percentageMutate();

    void percentageMutate(double mutationChance, double percent);
}
