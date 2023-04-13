package Test;

import Main.Helper.Vector2D;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

class Vector2DTest {

    @BeforeEach
    void setUp() {
    }

    @AfterEach
    void tearDown() {
    }


    @Test
    void angleBetweenFirstIf() {
        Vector2D v1 = new Vector2D(0,0);
        Vector2D v2 = new Vector2D(1,1);

        assertEquals(0.0, Vector2D.angleBetween(v1,v2));
    }

    @Test
    void angleBetweenSecondIf() {
        Vector2D v1 = new Vector2D(1,1);
        Vector2D v2 = new Vector2D(0,0);

        assertEquals(0.0, Vector2D.angleBetween(v1,v2));
    }

    @Test
    void angleBetweenParallel() {
        Vector2D v1 = new Vector2D(1, 2);
        Vector2D v2 = new Vector2D(2, 4);

        assertEquals(0.0, Vector2D.angleBetween(v1, v2), 0.001);
    }

    @Test
    void angleBetweenOrthogonal() {
        Vector2D v1 = new Vector2D(1, 0);
        Vector2D v2 = new Vector2D(0, 1);

        assertEquals(Math.PI / 2, Vector2D.angleBetween(v1, v2), 0.001);
    }

    @Test
    void angleBetweenOpposite() {
        Vector2D v1 = new Vector2D(1, 0);
        Vector2D v2 = new Vector2D(-1, 0);

        assertEquals(Math.PI, Vector2D.angleBetween(v1, v2), 0.001);
    }

    @Test
    void angleBetweenZeroVectors() {
        Vector2D v1 = new Vector2D(0, 0);
        Vector2D v2 = new Vector2D(0, 0);

        assertEquals(0.0, Vector2D.angleBetween(v1, v2), 0.001);
    }

    @Test
    void angleBetweenPerpendicular() {
        Vector2D v1 = new Vector2D(3, 4);
        Vector2D v2 = new Vector2D(-4, 3);

        assertEquals(Math.PI / 2, Vector2D.angleBetween(v1, v2), 0.001);
    }

    @Test
    void angleBetweenRandomVectors() {
        Vector2D v1 = new Vector2D(3, 4);
        Vector2D v2 = new Vector2D(1, -2);

        assertEquals(2.034, Vector2D.angleBetween(v1, v2), 0.01);
    }
}