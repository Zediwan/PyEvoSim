package Main.Helper;

public interface mutable {
    //TODO: check if this interface is applied to all necessary classes
    void mutate();

    void mutate(double mutationChance, double range);
}
