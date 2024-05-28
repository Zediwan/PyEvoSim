from code.simulation.dna.gene import Gene
import random
import threading
import unittest

class TestGene(unittest.TestCase):
    def setUp(self) -> None:
        pass
    
    def tearDown(self) -> None:
        pass

class TestInit(TestGene):
    def test_initialize_with_valid_parameters(self):
        """
        Initialize Gene with valid parameters and check attributes are set correctly
        """
        gene = Gene(max_value=10, min_value=5, value=7, mutation_range=0.5)
        self.assertEqual(gene._max_value, 10)
        self.assertEqual(gene._min_value, 5)
        self.assertEqual(gene.value, 7)
        self.assertEqual(gene._mutation_range, 0.5)

    def test_initialize_with_invalid_value_ranges(self):
        """
        Initialize Gene with max_value less than min_value and expect ValueError
        """
        self.assertRaises(ValueError, Gene, value=6, min_value=5, max_value=4, mutation_range=0.1)
    
    def test_initialize_gene_with_negative_mutation_range_expect_value_error(self):
        """
        Initialize Gene with a negative mutation range and expect ValueError
        """
        self.assertRaises(ValueError, Gene, max_value=1, min_value=0, value=0, mutation_range=-0.01)
    
    def test_gene_value_exceeds_max_value(self):
        """
        Set the value of a Gene to exceed the max_value and verify it is capped
        """
        gene = Gene(max_value=100, min_value=0, value=110, mutation_range=0.1)
        self.assertEqual(gene.value, 100, "Gene value should be capped at max_value")

class TestSetGet(TestGene):
    def test_set_and_get_value_within_range(self):
        """
        Set and get the value of a Gene within the allowed range
        """
        gene = Gene(max_value=10, min_value=0, value=5, mutation_range=2)
        self.assertEqual(gene.value, 5, "Initial value not set correctly")
        gene.value = 7
        self.assertEqual(gene.value, 7, "Value not set correctly")
        gene.value = 12
        self.assertEqual(gene.value, 10, "Value exceeds max value")
        gene.value = -1
        self.assertEqual(gene.value, 0, "Value below min value")

class TestMutate(TestGene):
    def test_mutate_uniform_mutation(self):
        """
        Mutate a Gene with 'uniform' mutation type and verify the value changes within expected range
        """
        gene = Gene(max_value=10, min_value=0, value=5, mutation_range=2)
        initial_value = gene.value
        gene.set_mutation_type(None, 'uniform')
        gene.mutate()
        mutated_value = gene.value
        assert initial_value - 2 <= mutated_value <= initial_value + 2, "Mutated value not within expected range"

    def test_mutate_gene_with_gauss_mutation(self):
        """
        Mutate a Gene with 'gauss' mutation type and verify the value changes within expected range
        """
        gene = Gene(max_value=10, min_value=0, value=5, mutation_range=2)
        initial_value = gene.value
        gene.mutate()
        mutated_value = gene.value
        assert initial_value - 2 <= mutated_value <= initial_value + 2, "Gene value did not change within expected range after mutation."
    
    def test_mutate_gene_zero_mutation_range(self):
        """
        Mutate a Gene where the mutation range is zero and verify the value does not change
        """
        gene = Gene(max_value=1, min_value=0, value=0.5, mutation_range=0)
        original_value = gene.value
        gene.mutate()
        self.assertEqual(gene.value, original_value, "Value should not change when mutation range is zero.")
    
    def test_mutation_range_extremely_small(self):
        """
        Check the behavior when mutation range is extremely small
        """
        gene = Gene(max_value=1, min_value=0, value=0.5, mutation_range=0.0001)
        initial_value = gene.value
        gene.mutate()
        mutated_value = gene.value
        self.assertNotEqual(initial_value, mutated_value, "Gene value did not mutate with extremely small mutation range.")

    # TODO this test is not working so far find out why
    def test_mutation_consistency(self):
        """
        Verify mutation consistency by repeating mutation under controlled random seed
        """
        # Set random seed for controlled randomness
        random.seed(1234)
    
        # Create a Gene instance with specific parameters
        gene = Gene(max_value=10, min_value=0, value=5, mutation_range=2)
    
        # Perform mutation multiple times and store the results
        results = []
        for _ in range(5):
            gene.mutate()
            results.append(gene.value)
    
        # Reset random seed for consistent results
        random.seed(1234)
    
        # Perform mutation again and compare the results with the stored values
        for i in range(5):
            gene.mutate()
            assert gene.value == results[i], f"Mutation result {gene.value} does not match expected {results[i]}."

    def test_validate_thread_safety_concurrent_mutations(self):
        """
        Validate thread safety during concurrent mutations
        """
        gene = Gene(max_value=1, min_value=0, value=0.5, mutation_range=0.1)
        initial_value = gene.value

        def mutate_gene(gene):
            for _ in range(1000):
                gene.mutate()

        threads = []
        for _ in range(5):
            thread = threading.Thread(target=mutate_gene, args=(gene,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        final_value = gene.value

        self.assertNotEqual(initial_value, final_value, "Gene value did not change after concurrent mutations.")
    
    def test_performance_impact_mutations(self):
        """
        Assess performance impact of frequent mutations on Gene object
        """
        gene = Gene(max_value=10, min_value=0, value=5, mutation_range=1)
        initial_value = gene.value

        for _ in range(1000):
            gene.mutate()

        mutated_value = gene.value

        self.assertNotEqual(initial_value, mutated_value, "Gene value did not change after mutations.")

class TestSetMutateType(TestGene):
    def test_attempt_set_unrecognized_mutation_type(self):
        """
        Attempt to set an unrecognized mutation type and expect ValueError
        """
        self.assertRaises(ValueError, Gene.set_mutation_type, "selected_item", "invalid_mutation_type")

class TestCopy(TestGene):
    def test_copy_gene_properties(self):
        """
        Copy a Gene and verify that the new Gene has the same properties as the original
        """
        gene = Gene(max_value=10, min_value=0, value=5, mutation_range=1)
        copied_gene = gene.copy()
    
        # Verify that the copied Gene has the same properties as the original
        self.assertEqual(copied_gene._max_value, gene._max_value)
        self.assertEqual(copied_gene._min_value, gene._min_value)
        self.assertEqual(copied_gene.value, gene.value)
        self.assertEqual(copied_gene._mutation_range, gene._mutation_range)
