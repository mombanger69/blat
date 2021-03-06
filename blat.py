

# kannski sniðugt að nota classa, bara fyrir skipulag, kannski er það stupid
class Blat:

    # kannski best að láta genome vera path að fælnum, og svo self.genome vera strengur með erfðamenginu
    def __init__(self, genome, k, cutoff, genomeoffset):
        self.genomeoffset = genomeoffset
        self.k = k
        self.cutoff = cutoff

        self.genome = open(genome).read().split('\n')[1]
        self.index = {}
        #na i index save-ad i file
        self.load_index()


    def load_index(self):
        # index of hit in the database

        file = open('./data/index.txt', "r").read().split("\n")
        file.pop()
        for f in file:
            line = f.split(" ")
            nums = line[1].split(",")
            self.index[line[0]] = [int(nums[0])]

            for i in range(1,len(nums)):
                self.index[line[0]].append(int(nums[i]))



# búum til refrence index fyrir erfðamengið
    def create_index(self):
        i = 0
        self.index = {}
        while i < (len(self.genome)-self.k+1):
            if self.genome[i:i+self.k] in self.index:
                self.index[self.genome[i:i+self.k]].append(i)
            else:
                self.index[self.genome[i:i+self.k]] = [i]
            i += self.k
        # eyða algengnum k-mers
        toDelete = []
        for ke, it in self.index.items():
            if len(it) >= self.cutoff:
                toDelete.append(ke)
        for t in toDelete:
            del self.index[t]

        self.save_index()


#save-um reference indexið í fæl, svo við þurfum ekki að búa það til í hvert sinn
    def save_index(self):
        s = ""
        for ke, it in self.index.items():
            s += str(ke) + " "
            for i in range(len(it)-1):
                s += str(it[i]) +","
            s += str(it[len(it)-1])
            s += "\n"
        f = open('./data/index.txt', 'w')
        f.write(s)
        f.close()




#las a wikipedia ad blat notar thetta, held lika ad thetta se seed and extend
# N er number of perfect matches
    def search_with_multiple_perfect_matches(self, query, N, W):
        if N<1:
            print("can't compare 0 items")
            return
        i = 0
        dict = {}
        # pos in query is key, pos in genome is value (list)
        while i < (len(query)-self.k+1):
            if query[i:i+self.k] in self.index:
                dict[i] = self.index[query[i:i+self.k]]
            i += 1
        diag = {}

        for ke, itm in dict.items():
            for j in range(len(itm)):
                if (itm[j] - ke) in diag:
                    diag[itm[j]-ke].append(itm[j])
                else:
                    diag[itm[j]-ke] = [itm[j]]
        hits = []
        for ke, itm in diag.items():
            if len(itm) > 1:
                for i in range(N-1, len(itm)):
                    # won't add to hits unless less then W away from other
                    if itm[i] - itm[i-N+1] < W:
                        hits.append(itm[i])
                        break
        return hits


    def nucleotide_alignment(self, hits, query):
        # byrja með score 1, því hann fær strax minus
        score = 1
        # athuga hvar lasthit var og ekki skoða lengra til baka í querinu en það
        lastHit = 0
        if len(hits) > 0:
            print("has alignments.")
        else:
            print("has no alignments.")
        for j in range(len(hits)):
            # minus einn ef hann hoppar milli blokka
            score -= 1
            firstHit = hits[j]
            for i in range(len(query)):
                if query[i:i+self.k] == self.genome[firstHit:firstHit+self.k]:
                    # kmer að lengd k er fra 0,k og fær því score er k+1
                    score += self.k +1
                    i1 = i
                    i2 = i + self.k
                    f1 = firstHit
                    f2 = firstHit+self.k
                    while True:
                        if i1>lastHit and f1>0 and query[i1-1] == self.genome[f1-1]:
                            score += 1
                            i1-=1
                            f1-=1

                        if i2<len(query)-1 and f2<len(self.genome)-1 and query[i2+1] == self.genome[f2+1]:
                            score += 1
                            i2+=1
                            f2+=1
                        else:
                            lastHit = i2 + 1
                            break
                    print("In Query.")
                    print("begin pos " + str(i1+1))
                    print("end pos " + str(i2+1))
                    print("In Genome.")
                    # with or without offset
                    print("begin pos " + str(self.genomeoffset + f1))
                    print("end pos "+ str(self.genomeoffset+ f2))
                    # without offsett
                    # print(f1,f2)
                    print()
                    break
                # i+=1
        if(len(hits) > 1):
            print("score " + str(score))





# cutoff is how many kmer is too many
b = Blat('./data/subseq.fasta', k=11, cutoff=20, genomeoffset=53000000)

# only run create index in first run
b.create_index()

qu = open("./data/transcripts.fasta").read().split("\n")


ind = 1
while ind < len(qu):
    print()
    print("###################")
    print("Nucleotide sequence")
    print(qu[ind-1])
    hits = b.search_with_multiple_perfect_matches(qu[ind], 2, 100000)
    b.nucleotide_alignment(hits, qu[ind])
    ind+=2
