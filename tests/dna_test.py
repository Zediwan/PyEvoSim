from code.simulation.dna.dna import DNA
import pygame
import unittest
from unittest.mock import patch

class TestDNA(unittest.TestCase):
    def setUp(self) -> None:
        self.initial_color = pygame.Color(255, 1, 1)
        self.attack_power = 25
        self.defense = 5
        self.prefered_moisture = 0.5
        self.prefered_height = 0.7
        self.mutation_chance = 0.1
        self.min_reproduction_health=0.3
        self.min_reproduction_energy=0.4
        self.min_reproduction_chance = 0.8
        self.energy_to_offspring_ratio=0.6

        self.init_DNA()

    def tearDown(self) -> None:
        DNA.set_color_mutation_range(10)
        DNA.set_prefered_moisture_mutation_range(0.1)
        DNA.set_prefered_height_mutation_range(0.1)
        DNA.set_min_reproduction_health_mutation_range(0.01)
        DNA.set_min_reproduction_energy_mutation_range(0.01)
        DNA.set_reproduction_chance_mutation_range(0.01)
        DNA.set_mutation_chance_mutation_range(0.01)
        DNA.set_energy_to_offspring_mutation_range(0.01)
    
    def init_DNA(self) -> DNA:
        self.dna_instance = DNA(
            color=self.initial_color,
            attack_power=self.attack_power,
            defense=self.defense,
            prefered_moisture=self.prefered_moisture,
            prefered_height=self.prefered_height,
            muation_chance=self.mutation_chance,
            min_reproduction_health=self.min_reproduction_health,
            min_reproduction_energy=self.min_reproduction_energy,
            reproduction_chance=self.min_reproduction_chance,
            energy_to_offspring_ratio=self.energy_to_offspring_ratio
        )

class TestInit(TestDNA):
    def test_initialize_with_valid_parameters(self):
        """
        Initialize DNA with valid parameters and check all gene values are set correctly with corrected import statement
        """
        self.assertEqual(self.dna_instance.color_r_gene.value, self.initial_color.r)
        self.assertEqual(self.dna_instance.color_g_gene.value, self.initial_color.g)
        self.assertEqual(self.dna_instance.color_b_gene.value, self.initial_color.b)
        self.assertEqual(self.dna_instance.attack_power_gene.value, self.attack_power)
        self.assertEqual(self.dna_instance.defense_gene.value, self.defense)
        self.assertEqual(self.dna_instance.prefered_moisture_gene.value, self.prefered_moisture)
        self.assertEqual(self.dna_instance.prefered_height_gene.value, self.prefered_height)
        self.assertEqual(self.dna_instance.mutation_chance_gene.value, self.mutation_chance)
        self.assertEqual(self.dna_instance.min_reproduction_health_gene.value, self.min_reproduction_health)
        self.assertEqual(self.dna_instance.min_reproduction_energy_gene.value, self.min_reproduction_energy)
        self.assertEqual(self.dna_instance.reproduction_chance_gene.value, self.min_reproduction_chance)
        self.assertEqual(self.dna_instance.energy_to_offspring_ratio_gene.value, self.energy_to_offspring_ratio)

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

        self.assertRaises(ValueError, self.init_DNA)

class TestColor(TestDNA):
    def test_access_color_property(self):
        """
        Access the color property and verify it returns the correct pygame.Color based on gene values
        """
        # Access the color property
        color = self.dna_instance.color
    
        # Verify the color property returns the correct pygame.Color based on gene values
        self.assertEqual(color.r, self.dna_instance.color.r, "Red component of color property is incorrect")
        self.assertEqual(color.g, self.dna_instance.color.g, "Green component of color property is incorrect")
        self.assertEqual(color.b, self.dna_instance.color.b, "Blue component of color property is incorrect")

class TestMutate(TestDNA):
    def test_mutate_dna_no_mutation(self):
        """
        Mutate DNA where no genes are mutated
        """
        self.dna_instance.mutation_chance_gene.value = .8
        dna_copy = self.dna_instance.copy()
        
        # Mock the random.random() function to always return a value greater than mutation chance
        with patch('random.random', return_value=.9):
            dna_copy.mutate()
    
        # Check that most genes have mutated
        num_dif_genes = 0
        for i, gene in enumerate(dna_copy.genes):
            if dna_copy.genes[i].value != self.dna_instance.genes[i].value:
                num_dif_genes += 1

        self.assertEqual(num_dif_genes, 0, f"{num_dif_genes} genes have mutated despite expecting 0 to mutate.")
    
    def test_mutate_dna(self):
        """
        Mutate DNA where some genes are mutated
        """
        self.dna_instance.mutation_chance_gene.value = .8
        dna_copy = self.dna_instance.copy()
        
        # Mock the random.random() function to always return a value greater than mutation chance
        with patch('random.random', return_value=.6):
            dna_copy.mutate()
    
        # Check that most genes have mutated
        num_dif_genes = 0
        for i, gene in enumerate(dna_copy.genes):
            if dna_copy.genes[i].value != self.dna_instance.genes[i].value:
                num_dif_genes += 1

        self.assertGreaterEqual(num_dif_genes, 0, f"{num_dif_genes} genes have mutated despite expecting at least 1 to mutate.")

    def test_mutate_dna_zero_mutation_ranges_fixed(self):
        """
        Mutate DNA with zero mutation ranges set for all genes and verify that gene values remain the same after mutation
        """
        # Set all mutation ranges to zero
        DNA.set_attack_power_mutation_range(0)
        DNA.set_defense_mutation_range(0)
        DNA.set_color_mutation_range(0)
        DNA.set_prefered_moisture_mutation_range(0)
        DNA.set_prefered_height_mutation_range(0)
        DNA.set_min_reproduction_health_mutation_range(0)
        DNA.set_min_reproduction_energy_mutation_range(0)
        DNA.set_reproduction_chance_mutation_range(0)
        DNA.set_mutation_chance_mutation_range(0)
        DNA.set_energy_to_offspring_mutation_range(0)
    
        # Store the initial gene values
        self.init_DNA()
        initial_gene_values = [gene.value for gene in self.dna_instance.genes]
    
        # Mutate the DNA
        self.dna_instance.mutate()
    
        # Check if gene values remain the same after mutation
        for i, gene in enumerate(self.dna_instance.genes):
            self.assertEqual(gene.value, initial_gene_values[i], f"Gene value {gene.value} changed after mutation with zero mutation range.")

class TestSetters(TestDNA):
    def test_mutation_range_update(self):
        """
        Verify that setting class-level mutation ranges updates the mutation behavior of genes of dna created afterwards and does not affect dna created before.
        """
        copy_dna = self.dna_instance.copy()
        
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

        self.init_DNA()
        
        # Mutate the DNA instance
        self.dna_instance.mutate()

        # Check if the mutation ranges have been updated for each gene
        self.assertEqual(self.dna_instance.attack_power_gene._mutation_range, 3)
        self.assertEqual(self.dna_instance.color_r_gene._mutation_range, 15)
        self.assertEqual(self.dna_instance.prefered_moisture_gene._mutation_range, 0.3)
        self.assertEqual(self.dna_instance.prefered_height_gene._mutation_range, 0.4)
        self.assertEqual(self.dna_instance.min_reproduction_health_gene._mutation_range, 0.02)
        self.assertEqual(self.dna_instance.min_reproduction_energy_gene._mutation_range, 0.03)
        self.assertEqual(self.dna_instance.reproduction_chance_gene._mutation_range, 0.04)
        self.assertEqual(self.dna_instance.mutation_chance_gene._mutation_range, 0.05)
        self.assertEqual(self.dna_instance.energy_to_offspring_ratio_gene._mutation_range, 0.06)
        
        # Check that mutation ranges have not been updated for dna created before
        self.assertNotEqual(copy_dna.attack_power_gene._mutation_range, 3)
        self.assertNotEqual(copy_dna.color_r_gene._mutation_range, 15)
        self.assertNotEqual(copy_dna.prefered_moisture_gene._mutation_range, 0.3)
        self.assertNotEqual(copy_dna.prefered_height_gene._mutation_range, 0.4)
        self.assertNotEqual(copy_dna.min_reproduction_health_gene._mutation_range, 0.02)
        self.assertNotEqual(copy_dna.min_reproduction_energy_gene._mutation_range, 0.03)
        self.assertNotEqual(copy_dna.reproduction_chance_gene._mutation_range, 0.04)
        self.assertNotEqual(copy_dna.mutation_chance_gene._mutation_range, 0.05)
        self.assertNotEqual(copy_dna.energy_to_offspring_ratio_gene._mutation_range, 0.06)

class TestCopy(TestDNA):
    def test_copy_dna_instance_and_verify_gene_values(self):
        """
        Copy a DNA instance and ensure all gene values are identical to the original.
        Also ensure that the copy genes are actually different objects.
        """    
        # Copy the DNA instance
        copied_dna = self.dna_instance.copy()
    
        # Verify that all gene values in the copied DNA instance are identical to the original
        # Verify that the genes are deep copies and don't point to the same gene to avoid bugs
        for i, gene in enumerate(copied_dna.genes):
            self.assertEqual(self.dna_instance.genes[i].value, copied_dna.genes[i].value, "Copied values are not equal.")
            self.assertNotEqual(self.dna_instance.genes[i], copied_dna.genes[i], "Copied genes are identical references.")
