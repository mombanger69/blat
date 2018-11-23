# kannski sniðugt að nota classa, bara fyrir skipulag, kannski er það stupid
class Blat:

    # kannski best að láta genome vera path að fælnum, og svo self.genome vera strengur með erfðamenginu
    def __init__(self, genome):
        self.genome = open(genome).read().split('/n')[0]
        # index of hit in the database
        print(len(self.genome))

    # K:The K-mer size. Typically this is 8–16 for nucleotide comparisons and 3–7 for amino acid comparisons
    def search_with_single_perfect_match(self, k, query):
        hits = []
        for i in range(len(self.genome)-k+1):
            # á kannski fyrst að skoða hvort eitt passi og svo rest, er það betra fyrir hraða?
            if(self.genome[i:i+k] == query[:k]):
                # þarf að passa non overlapping k-mers
                hits.append(i)
                i+=k
        print(hits)
        return hits


#las a wikipedia ad blat notar thetta, held lika ad thetta se seed and extend
# N er number of perfect matches
    def searching_with_multiple_perfect_matches(self,k, query, N, W):
        print()
        hits = []
        for i in range(len(self.genome)-k+1):
            num_of_hits = 0
            last_hit_index = 0
            j = 0
            if(i%100==0):
                print(i)
            while j < len(query):
                if(self.genome[i:i+k] == query[j:j+k]):
                    num_of_hits += 1
                if(num_of_hits == N):
                    hits.append(i)
                    print("hit")
                    break
                j += 1
                # j += W
        print(hits)


    def nucleotide_alignment(self):
        print()




# ég skil þetta þannig að við eigum a nota hlutina í transcipt filnum til að leita í reads filnum, er það rétt???
qu = open("./data/transcripts.fasta").read().split("\n")

b = Blat('./data/subseq.fasta')
i=1

b.searching_with_multiple_perfect_matches(11,qu[1], 2, 20)

# while i < len(qu):
#     b.searching_with_multiple_perfect_matches(11, qu[i], 2, 20)
#     i+=2
