from code.simulation.dna.dna import DNA
import pygame
import unittest
from unittest.mock import patch

class TestDNA(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        DNA.set_color_mutation_range(10)
        DNA.set_prefered_moisture_mutation_range(0.1)
        DNA.set_prefered_height_mutation_range(0.1)
        DNA.set_min_reproduction_health_mutation_range(0.01)
        DNA.set_min_reproduction_energy_mutation_range(0.01)
        DNA.set_reproduction_chance_mutation_range(0.01)
        DNA.set_mutation_chance_mutation_range(0.01)
        DNA.set_energy_to_offspring_mutation_range(0.01)

class TestInit(TestDNA):
    def test_initialize_with_valid_parameters(self):
        """
        Initialize DNA with valid parameters and check all gene values are set correctly with corrected import statement
        """
        initial_color = pygame.Color(255, 1, 1)
        dna_instance = DNA(
            color=initial_color,
            attack_power=25,
            prefered_moisture=0.5,
            prefered_height=0.7,
            muation_chance=0.1,
            min_reproduction_health=0.3,
            min_reproduction_energy=0.4,
            reproduction_chance=0.8,
            energy_to_offspring_ratio=0.6
        )
        self.assertEqual(dna_instance.color_r_gene.value, 255)
        self.assertEqual(dna_instance.color_g_gene.value, 1)
        self.assertEqual(dna_instance.color_b_gene.value, 1)
        self.assertEqual(dna_instance.attack_power_gene.value, 25)
        self.assertEqual(dna_instance.prefered_moisture_gene.value, 0.5)
        self.assertEqual(dna_instance.prefered_height_gene.value, 0.7)
        self.assertEqual(dna_instance.mutation_chance_gene.value, 0.1)
        self.assertEqual(dna_instance.min_reproduction_health_gene.value, 0.3)
        self.assertEqual(dna_instance.min_reproduction_energy_gene.value, 0.4)
        self.assertEqual(dna_instance.reproduction_chance_gene.value, 0.8)
        self.assertEqual(dna_instance.energy_to_offspring_ratio_gene.value, 0.6)

    def test_initialize_dna_with_negative_mutation_ranges_expect_value_error(self):
        """
        Initialize DNA with negative mutation ranges and expect a ValueError
        """
        DNA.set_color_mutation_range(-10)
        DNA.set_prefered_moisture_mutation_range(-0.3)
        DNA.set_prefered_height_mutation_range(-0.3)
        DNA.set_min_reproduction_health_mutation_range(-0.01)
        DNA.set_min_reproduction_energy_mutation_range(-0.01)
        DNA.set_reproduction_chance_mutation_range(-0.01)
        DNA.set_mutation_chance_mutation_range(-0.01)
        DNA.set_energy_to_offspring_mutation_range(-0.01)

        self.assertRaises(ValueError, DNA, color=pygame.Color(255, 0, 0), attack_power=5, prefered_moisture=0.5, prefered_height=0.3, muation_chance=0.1, min_reproduction_health=0.2, min_reproduction_energy=0.1, reproduction_chance=0.5, energy_to_offspring_ratio=0.7)

class TestColor(TestDNA):
    def test_access_color_property(self):
        """
        Access the color property and verify it returns the correct pygame.Color based on gene values
        """
        # Create a DNA instance with specific gene values
        dna = DNA(color=pygame.Color(100, 150, 200), attack_power=20, prefered_moisture=0.5, prefered_height=0.7, muation_chance=0.3, min_reproduction_health=0.4, min_reproduction_energy=0.6, reproduction_chance=0.8, energy_to_offspring_ratio=0.9)
    
        # Access the color property
        color = dna.color
    
        # Verify the color property returns the correct pygame.Color based on gene values
        self.assertEqual(color.r, 100, "Red component of color property is incorrect")
        self.assertEqual(color.g, 150, "Green component of color property is incorrect")
        self.assertEqual(color.b, 200, "Blue component of color property is incorrect")

class TestMutate(TestDNA):
    def test_mutate_dna_no_mutation(self):
        """
        Mutate DNA where mutation chance is high and ensure no genes are mutated
        """
        # Set up DNA instance with high mutation chance
        dna_original = DNA(color=pygame.Color(255, 0, 0), attack_power=20, prefered_moisture=0.5, prefered_height=0.7, muation_chance=0.9, min_reproduction_health=0.3, min_reproduction_energy=0.4, reproduction_chance=0.6, energy_to_offspring_ratio=0.8)
        dna_copy = dna_original.copy()
        
        # Mock the random.random() function to always return a value greater than mutation chance
        with patch('random.random', return_value=1):
            dna_copy.mutate()
    
        # Check that most genes have mutated
        num_dif_genes = 0
        for i, gene in enumerate(dna_copy.genes):
            if dna_copy.genes[i].value != dna_original.genes[i].value:
                num_dif_genes += 1

        self.assertEqual(num_dif_genes, 0, f"{num_dif_genes} genes have mutated despite expecting 0 to mutate.")

    def test_mutate_dna_zero_mutation_ranges_fixed(self):
        """
        Mutate DNA with zero mutation ranges set for all genes and verify that gene values remain the same after mutation
        """
        # Set all mutation ranges to zero
        DNA.set_attack_power_mutation_range(0)
        DNA.set_color_mutation_range(0)
        DNA.set_prefered_moisture_mutation_range(0)
        DNA.set_prefered_height_mutation_range(0)
        DNA.set_min_reproduction_health_mutation_range(0)
        DNA.set_min_reproduction_energy_mutation_range(0)
        DNA.set_reproduction_chance_mutation_range(0)
        DNA.set_mutation_chance_mutation_range(0)
        DNA.set_energy_to_offspring_mutation_range(0)
    
        # Create a DNA instance
        dna = DNA(color=pygame.Color(255, 0, 0), attack_power=10, prefered_moisture=0.5, prefered_height=0.7, muation_chance=0.3, min_reproduction_health=0.4, min_reproduction_energy=0.6, reproduction_chance=0.8, energy_to_offspring_ratio=0.2)
    
        # Store the initial gene values
        initial_gene_values = [gene.value for gene in dna.genes]
    
        # Mutate the DNA
        dna.mutate()
    
        # Check if gene values remain the same after mutation
        for i, gene in enumerate(dna.genes):
            self.assertEqual(gene.value, initial_gene_values[i], f"Gene value {gene.value} changed after mutation with zero mutation range.")

class TestSetters(TestDNA):
    def test_mutation_range_update(self):
        """
        Verify that setting class-level mutation ranges updates the mutation behavior of genes
        """
        # Set class-level mutation ranges
        DNA.set_attack_power_mutation_range(3)
        DNA.set_color_mutation_range(15)
        DNA.set_prefered_moisture_mutation_range(0.3)
        DNA.set_prefered_height_mutation_range(0.4)
        DNA.set_min_reproduction_health_mutation_range(0.02)
        DNA.set_min_reproduction_energy_mutation_range(0.03)
        DNA.set_reproduction_chance_mutation_range(0.04)
        DNA.set_mutation_chance_mutation_range(0.05)
        DNA.set_energy_to_offspring_mutation_range(0.06)

        # Create a DNA instance
        dna = DNA(color=pygame.Color(100, 150, 200), attack_power=20, prefered_moisture=0.5, prefered_height=0.6, muation_chance=0.1, min_reproduction_health=0.7, min_reproduction_energy=0.8, reproduction_chance=0.9, energy_to_offspring_ratio=0.2)

        # Mutate the DNA instance
        dna.mutate()

        # Check if the mutation ranges have been updated for each gene
        self.assertEqual(dna.attack_power_gene._mutation_range, 3)
        self.assertEqual(dna.color_r_gene._mutation_range, 15)
        self.assertEqual(dna.prefered_moisture_gene._mutation_range, 0.3)
        self.assertEqual(dna.prefered_height_gene._mutation_range, 0.4)
        self.assertEqual(dna.min_reproduction_health_gene._mutation_range, 0.02)
        self.assertEqual(dna.min_reproduction_energy_gene._mutation_range, 0.03)
        self.assertEqual(dna.reproduction_chance_gene._mutation_range, 0.04)
        self.assertEqual(dna.mutation_chance_gene._mutation_range, 0.05)
        self.assertEqual(dna.energy_to_offspring_ratio_gene._mutation_range, 0.06)

class TestCopy(TestDNA):
    def test_copy_dna_instance_and_verify_gene_values(self):
        """
        Copy a DNA instance and ensure all gene values are identical to the original
        """
        # Create a DNA instance with specific gene values
        original_dna = DNA(color=pygame.Color(100, 150, 200), attack_power=20, prefered_moisture=0.5, prefered_height=0.7, muation_chance=0.1, min_reproduction_health=0.3, min_reproduction_energy=0.4, reproduction_chance=0.6, energy_to_offspring_ratio=0.8)
    
        # Copy the DNA instance
        copied_dna = original_dna.copy()
    
        # Verify that all gene values in the copied DNA instance are identical to the original
        # Verify that the genes are deep copies and don't point to the same gene to avoid bugs
        for i, gene in enumerate(copied_dna.genes):
            self.assertEqual(original_dna.genes[i].value, copied_dna.genes[i].value, "Copied values are not equal.")
            self.assertNotEqual(original_dna.genes[i], copied_dna.genes[i], "Copied genes are identical references.")
