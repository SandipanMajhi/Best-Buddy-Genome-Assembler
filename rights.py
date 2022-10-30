import sys
from operator import itemgetter

# input_file = sys.argv[1]
# min_overlap = sys.argv[2]
# output_file = sys.argv[3]

class RightSearch:
    def __init__(self, input_file, min_overlap, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.overlap = min_overlap
        self.reads = []
        self.readsdict = {}
        self.table = {}
        self.max_tabs = {}
        self.read_genome()
        self.make_reads_dict()
        self.find_matches()
    
    def read_genome(self):
        with open(self.input_file, "r") as fp:
            while True:
                first_line = fp.readline()
                if(len(first_line) == 0):
                    break
                name = first_line[1:].rstrip()
                seq = fp.readline().rstrip()
                fp.readline()
                fp.readline()
                self.reads.append((str(name), str(seq)))

    def make_reads_dict(self):
        for name, seq in self.reads:
            self.readsdict[name] = seq

    def make_kmer_table(self, k):
        table = {}
        for name, seq in self.reads:
            for i in range(0, len(seq) - k + 1):
                kmer = seq[i:i+k]
                if kmer not in table:
                    table[kmer] = set()
                table[kmer].add(name)
        return table

    def find_matches(self):
        self.table = self.make_kmer_table(self.overlap)
        for k,v in self.table.items():
            for n1 in v:
                for n2 in v:
                    if n1 != n2:
                        match_len = self.suffix_prefix(self.readsdict[n1], self.readsdict[n2], self.overlap)
                        if match_len > 0:
                            if n1 in self.max_tabs:
                                if [match_len, n2] not in self.max_tabs[n1]:
                                    self.max_tabs[n1].append([match_len, n2])
                            else:
                                self.max_tabs[n1] = []
                                self.max_tabs[n1].append([match_len, n2])
        mark = []
        for k,v in self.max_tabs.items():
            v = sorted(v, key=itemgetter(0), reverse = True)
            self.max_tabs[k] = v
            maxlen = v[0][0]
            for i in range(1,len(v)):
                if v[i][0] == maxlen:
                    mark.append(k)
                    break
            self.max_tabs[k] = v[0]

        for key in mark:
            del self.max_tabs[key]
        
        with open(self.output_file, "w") as fp:
            for k,v in sorted(self.max_tabs.items()):
                fp.write(str(k) + " " + str(v[0]) + " " + str(v[1]) + "\n")
        
    
    def suffix_prefix(self, str1, str2, min_overlap):
        if len(str2) < min_overlap:
            return 0
        str2_prefix = str2[:min_overlap]
        str1_pos = -1
        while True:
            str1_pos = str1.find(str2_prefix, str1_pos + 1)
            if str1_pos == -1:
                return 0
            str1_suffix = str1[str1_pos:]
            if str2.startswith(str1_suffix):
                return len(str1_suffix)


# if __name__ == "__main__":
#     rhs = RightSearch(input_file=input_file, min_overlap= int(min_overlap), output_file=output_file)