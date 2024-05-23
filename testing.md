# Unit Testing for NoiseFunction Class
This function may produce unexpected output if the noise function logic is changed in the future. This may not seem like a big thing at first however these bugs may be very subtle and not get noticed right away and thus lead to strange results in the world creation and customisation. Due to this I wrote the unit test for this method so in the future we can quickly asses if new bugs arise.

## Test Case 1: test_weigh_without_weights

### Description:
This test case checks if the `NoiseFunction.weigh` method works correctly when no weights are given.

### Steps:
1. Create two NoiseFunction instances with specific parameters.
2. Calculate the expected result based on the noise values from the two functions.
3. Call the `NoiseFunction.weigh` method with the functions and no weights.
4. Assert that the calculated result matches the expected result.

## Test Case 2: test_weigh_with_custom_weights

### Description:
This test case verifies the functionality of `NoiseFunction.weigh` with custom weights for each function.

### Steps:
1. Create two NoiseFunction instances with specific parameters.
2. Define custom weights for each function.
3. Calculate the expected result based on the noise values and custom weights.
4. Call the `NoiseFunction.weigh` method with the functions and custom weights.
5. Assert that the calculated result matches the expected result.

## Test Case 3: test_weigh_with_insufficient_weights

### Description:
This test case tests the behavior of `NoiseFunction.weigh` when fewer weights than functions are provided.

### Steps:
1. Create two NoiseFunction instances with specific parameters.
2. Define weights for one function and an expected weight for the other.
3. Calculate the expected result based on the noise values and weights.
4. Call the `NoiseFunction.weigh` method with the functions and insufficient weights.
5. Assert that the calculated result matches the expected result.

## Test Case 4: test_weigh_with_single_function

### Description:
This test case validates the functionality of `NoiseFunction.weigh` with only one function.

### Steps:
1. Create a NoiseFunction instance with specific parameters.
2. Calculate the expected result based on the noise value from the function.
3. Call the `NoiseFunction.weigh` method with the single function.
4. Assert that the calculated result matches the expected result.

## Test Case 5: test_weigh_without_functions

### Description:
This test case ensures that `NoiseFunction.weigh` raises an error when an empty list of functions is provided.

### Steps:
1. Define x and y values.
2. Try to call the `NoiseFunction.weigh` method with an empty list of functions.
3. Expect a ValueError to be raised.