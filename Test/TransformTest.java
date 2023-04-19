import Main.Helper.Transform;
import Main.Helper.Vector2D;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class TransformTest {

    @BeforeEach
    void setUp() {
    }

    @AfterEach
    void tearDown() {
    }

    @Test
    void testGetRotationPositiveY() {
        Vector2D velocity = new Vector2D(1, 2);
        Transform transform = new Transform(new Vector2D(0, 0), velocity, new Vector2D(0, 0), 1, null);
        double expected = Vector2D.angleBetween(velocity, new Vector2D(1, 0));
        if (velocity.getY() > 0) {
            expected = Math.PI - expected;
        }
        double actual = transform.getRotation();
        assertEquals(expected, actual, 0.001);
    }


    @Test
    void testGetRotationNegativeY() {
        Vector2D velocity = new Vector2D(-1, -2);
        Transform transform = new Transform(new Vector2D(0, 0), velocity, new Vector2D(0, 0), 1, null);
        double expected = Vector2D.angleBetween(velocity, new Vector2D(1, 0));
        double actual = transform.getRotation();
        assertEquals(expected, actual, 0.001);
    }

    @Test
    void testGetRotationZeroVelocity() {
        Vector2D velocity = new Vector2D(0, 0);
        Transform transform = new Transform(new Vector2D(0, 0), velocity, new Vector2D(0, 0), 1, null);
        double expected = 0;
        double actual = transform.getRotation();
        assertEquals(expected, actual, 0.001);
    }

    @Test
    void testGetRotationHorizontalVelocity() {
        Vector2D velocity = new Vector2D(3, 0);
        Transform transform = new Transform(new Vector2D(0, 0), velocity, new Vector2D(0, 0), 1, null);
        double expected = 0;
        double actual = transform.getRotation();
        assertEquals(expected, actual, 0.001);
    }

    @Test
    void testGetRotationVerticalVelocity() {
        Vector2D velocity = new Vector2D(0, 5);
        Transform transform = new Transform(new Vector2D(0, 0), velocity, new Vector2D(0, 0), 1, null);
        double expected = Math.toRadians(90);
        double actual = transform.getRotation();
        assertEquals(expected, actual, 0.001);
    }

}