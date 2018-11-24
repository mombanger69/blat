#!/usr/bin/env python
# -*- coding: utf-8 -*-

# if k-mer appears more often then 60 times, skip it
CUTOFF = 60

# kannski sniðugt að nota classa, bara fyrir skipulag, kannski er það stupid
class Blat:

    # kannski best að láta genome vera path að fælnum, og svo self.genome vera strengur með erfðamenginu
    def __init__(self, genome, k):
        self.genome = open(genome).read().split('\n')[1]
        self.k = k
        # index of hit in the database
        file = open('./data/index.txt', "r").read().split("\n")
        #na i index save-ad i file
        self.index = {}
        file.pop()
        for f in file:
            line = f.split(" ")
            nums = line[1].split(",")
            self.index[line[0]] = [int(nums[0])]
            if(len(nums) < CUTOFF):
                for i in range(1,len(nums)):
                    self.index[line[0]].append(int(nums[i]))





#búum til refrence index fyrir erfðamengið
    def create_index(self):
        i = 0
        self.index = {}
        while i < (len(self.genome)-self.k+1):
            if self.genome[i:i+self.k] in self.index:
                self.index[self.genome[i:i+self.k]].append(i)
            else:
                self.index[self.genome[i:i+self.k]] = [i]
            i += self.k
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
        i = 0
        dict = {}
        # pos in query is key, pos in genome is value (list)
        while i < (len(query)-self.k+1):
            if(query[i:i+self.k] in self.index):
                dict[i] = self.index[query[i:i+self.k]]
            i += 1
        # print(dict)
        diag = {}
        # key is

        for ke, itm in dict.items():
            for j in range(len(itm)):
                if (itm[j] - ke) in diag:
                    # print("in")
                    # hits[ke] = diag[itm[j] -ke][0]
                    diag[itm[j]-ke].append(itm[j])
                else:
                    diag[itm[j] -ke] = [itm[j]]
        # print(diag)
        hits = []
        for ke, itm in diag.items():
            if len(itm) > 1 :
                hits.append(itm[0])
                # print("more")
                # print("many " + str(len(itm)))
                #
                # for i in range(len(itm)-1):
                #     print(itm[i])
                #     if itm[i+1] -itm[i] > self.k:
                #         print("stokk")
                # print(itm[-1])
        if(len(hits) > 0):
            self.nucleotide_alignment(hits,query)
        return hits




    #take two strings and compare every letter and return how many dont match
    def match_errors(self, t1, t2):
        err = 0
        for i in range(len(t1)):
            if t1[i] != t2[i]:
                err += 1
        return err

# returns if deletions is less then N
    def N_deletions(N, t1, t2):
        j=0
        i=0
        err = 0
        while i < len(t1):
            if(err > N):
                return False
            if(t1[i] != t2[j]):
                i+=1
                err+=1
            else:
                i+=1
                j+=1
        return True


    def nucleotide_alignment(self, hits, query):
        print()
        for j in range(len(hits)):
            firstHit = hits[j]
            for i in range(len(query)):
                if query[i:i+self.k] == self.genome[firstHit:firstHit+self.k]:
                    i1 = i
                    i2 = i + self.k
                    f1 = firstHit
                    f2 = firstHit+self.k
                    while True:
                        if i1>0 and f1>0 and query[i1-1] == self.genome[f1-1]:
                            i1-=1
                            f1-=1
                        if i2<len(query)-1 and f2<len(self.genome)-1 and query[i2+1] == self.genome[f2+1]:
                            i2+=1
                            f2+=1
                        else:
                            break
                    print("^^^^^^^^^^^^^")
                    print(query[i1:i2])
                    print(i1,i2)
                    print(f1, f2)
                    break









b = Blat('./data/subseq.fasta', 11)

# only run create index in first run
# b.create_index()
qu = open("./data/transcripts.fasta").read().split("\n")
b.search_with_multiple_perfect_matches(qu[5], 2, 200)

i = 1


while i < len(qu):
    print("############")
    print(i)
    b.search_with_multiple_perfect_matches(qu[i], 2, 200)
    i+=2
# b.get_dict()

print("buid")
