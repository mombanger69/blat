# kannski sniðugt að nota classa, bara fyrir skipulag, kannski er það stupid
class Blat:

    # kannski best að láta genome vera path að fælnum, og svo self.genome vera strengur með erfðamenginu
    def __init__(self, genome, query):
        self.genome = open(genome).read().split('/n')[0]
        self.query = query
        # index of hit in the database
        self.hits = []
        print(len(self.genome))

    # K:The K-mer size. Typically this is 8–16 for nucleotide comparisons and 3–7 for amino acid comparisons
    def search_with_single_perfect_match(self, k):
        for i in range(len(self.genome)-k+1):
            # á kannski fyrst að skoða hvort eitt passi og svo rest, er það betra fyrir hraða?
            if(self.genome[i:i+k] == self.query[:k]):
                # þarf að passa non overlapping k-mers
                self.hits.append(i)
        print(self.hits)

    def nucleotide_alignment(self):
        print()



qu = 'AAAGACTTTTTTTTAATTAGCTGGTCCTGGAGGCACTCGCCTGT'
b = Blat('./data/subseq.fasta', qu)

b.search_with_single_perfect_match(8)
