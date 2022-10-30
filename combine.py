import sys

# fastq_file = sys.argv[1]
# input_file = sys.argv[2]
# output_file = sys.argv[3]

class Assembly:
    def __init__(self, fastq_file, input_file, output_file):
        self.fastq = fastq_file
        self.input_file = input_file
        self.output_file = output_file
        self.reads = {}
        self.tigs = {}
        self.assembly = {}
        self.read_genome()
        self.read_unitigs()
        self.assemble()
        self.write_to_file()

    def read_genome(self):
        with open(self.fastq, "r") as fp:
            while True:
                first_line = fp.readline()
                if(len(first_line) == 0):
                    break
                name = first_line[1:].rstrip()
                seq = fp.readline().rstrip()
                fp.readline()
                fp.readline()
                self.reads[str(name)] = str(seq)

    def read_unitigs(self):
        with open(self.input_file,"r") as fp:
            while True:
                line = fp.readline().strip()
                if len(line) == 0:
                    break
                elif len(line.split(" ")) == 1:
                    self.tigs[line] = []
                    key = line
                else:
                    self.tigs[key].append(line.split(" "))

    def assemble(self):
        for k,v in sorted(self.tigs.items()):
            seq = self.reads[k]
            for slices in v:
                matched = int(slices[0])
                seq += self.reads[slices[1]][matched:]
            self.assembly["{} {}".format(k,len(v) + 1)] = seq

    def write_to_file(self):
        with open(self.output_file, "w") as fp:
            for k,v in sorted(self.assembly.items()):
                self.write_solution(k.split(" ")[0], v, k.split(" ")[1], fp)
            

    
    def write_solution(self, unitigID, unitigSequence, n, out_fh, per_line=60):
        offset = 0
        out_fh.write(f">{unitigID} {n}\n")
        while offset < len(unitigSequence):
            line = unitigSequence[offset:offset + per_line]
            offset += per_line
            out_fh.write(line + "\n")


# if __name__ == "__main__":
#     asm = Assembly(fastq_file=fastq_file, input_file=input_file, output_file=output_file)






    