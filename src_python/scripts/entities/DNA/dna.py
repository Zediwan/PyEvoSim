from scripts.entities.DNA.gene import ColorGene, SizeGene

class DNA:
    def __init__(self, sizeGene: SizeGene, colorGene: ColorGene | None = None):        
        if sizeGene == None:
            self.sizeGene = SizeGene()
        else:
            self.sizeGene = sizeGene
        
        if colorGene == None:
            self.colorGene = ColorGene()
        else:
            self.colorGene = colorGene
        
    def copy(self):
        copy_dna = DNA(self.sizeGene.copy(), self.colorGene.copy())
        return copy_dna
    
    def mutate(self):
        self.sizeGene.mutate()
        self.colorGene.mutate()