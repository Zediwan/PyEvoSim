import Main.Helper.Vector2D;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

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

    @Test
    void copy() {
        Vector2D v1 = new Vector2D(1,0);
        Vector2D copy = v1.copy();

        assertNotEquals(v1, copy);
        assertEquals(v1.getX(), copy.getX());
        assertEquals(v1.getY(), copy.getY());
    }

    @Test
    void randSurroundingVec(){
        int amountOfTests = 100;

        for(int i = 0; i < amountOfTests; i++){
            Vector2D v1 = Vector2D.randSurroundingVec(i);

            assertEquals(true, v1.mag() <= i);
        }
    }

    //TODO write a test case to check if the assertion is thrown
    @Test
    void randSurroundingVecAssertion(){
        //assertThrows(   , Vector2D.randSurroundingVec(-1));
    }

    @Test
    void randLimVec(){
        int amountOfTests = 100;

        for(int x = -amountOfTests; x < amountOfTests; x++){
            for(int y = -amountOfTests; y < amountOfTests; y++){
                Vector2D v1 = Vector2D.randLimVec(x, y);

                assert Math.abs(v1.getX()) <= Math.abs(x);
                assert Math.abs(v1.getY()) <= Math.abs(y);
            }
        }
    }

    //TODO add an assertion test to check if the assertion is thrown in the correct moments
    @Test
    void addRandom(){
        int amountOfTests = 100;

        for(int x = -amountOfTests; x < amountOfTests; x++){
            for(int y = -amountOfTests; y < amountOfTests; y++){
                Vector2D v1 = Vector2D.randSurroundingVec(100);
                Vector2D v2 = Vector2D.randSurroundingVec(100);

                assertEquals(v1.getX() + v2.getX(), v1.add(v2).getX());
                assertEquals(v1.getY() + v2.getY(), v1.add(v2).getY());
            }
        }
    }

    @Test
    void addPositiveVectors(){
        Vector2D v1 = new Vector2D(1,0);
        Vector2D v2 = new Vector2D(1,1);

        Vector2D sum = v1.add(v2);

        assertEquals(2, sum.getX());
        assertEquals(1, sum.getY());
    }

    @Test
    void addNegativeVectors(){
        Vector2D v1 = new Vector2D(1,0);
        Vector2D v2 = new Vector2D(1,1);

        Vector2D sum = v1.add(v2);

        assertEquals(2, sum.getX());
        assertEquals(1, sum.getY());
    }

    @Test
    void testFromAngleNullTarget() {
        Vector2D expected = new Vector2D(Math.sqrt(2) / 2, Math.sqrt(2) / 2);
        Vector2D actual = Vector2D.fromAngle(Math.PI / 4, null);
        assertEquals(expected.getX(), actual.getX(), .0001);
        assertEquals(expected.getY(), actual.getY(), .0001);
    }

    @Test
    void testFromAngleNonNullTarget() {
        Vector2D target = new Vector2D(1, 0);
        Vector2D expected = new Vector2D(Math.sqrt(3) / 2, 0.5);
        Vector2D actual = Vector2D.fromAngle(Math.PI / 3, target);
        assertEquals(expected.getX(), actual.getX(), .0001);
        assertEquals(expected.getY(), actual.getY(), .0001);
    }

    @Test
    void testFromAngleZeroAngle() {
        Vector2D expected = new Vector2D(1, 0);
        Vector2D actual = Vector2D.fromAngle(0, null);
        assertEquals(expected.getX(), actual.getX(), .0001);
        assertEquals(expected.getY(), actual.getY(), .0001);
    }

    @Test
    void testFromAngleNegativeAngle() {
        Vector2D expected = new Vector2D(-Math.sqrt(3) / 2, 0.5);
        Vector2D actual = Vector2D.fromAngle(-2 * Math.PI / 3, null);
        assertEquals(expected.getX(), actual.getX(), .0001);
        assertEquals(expected.getY(), actual.getY(), .0001);
    }
}