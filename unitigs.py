import sys
from operator import itemgetter

# input_file = sys.argv[1]
# output_file = sys.argv[2]

# input_file = "test.txt"
# output_file = "output3.txt"

class Tigs:
    def __init__(self, input_file, output_file) :
        self.input_file = input_file
        self.output_file = output_file
        self.bml = {}
        self.bmr = {}
        self.tigs = {}
        self.leftmost = []
        self.rightmost = []
        self.rights_done = set()
        self.create_bi_table()
        self.extend_tigs()
        self.print_tigs()

    def extend_tigs(self):
        '''
            unitigs by right extension
        '''
        for start in self.leftmost:
            extend_right = self.bmr[start][1]
            match_right = self.bmr[start][0]
            l_most = start
            self.tigs[l_most] = []
            # self.tigs[extend_right] = []
            if extend_right not in self.bml:
                self.tigs[extend_right] = []
            while start not in self.rightmost:
                if extend_right in self.bml:
                    if self.bml[extend_right][1] != start:
                        break
                    else:
                        self.tigs[l_most].append([match_right, extend_right])
                        start = extend_right
                        if start in self.bmr:
                            extend_right = self.bmr[start][1]
                            match_right = self.bmr[start][0]
                else:
                    break

    def create_bi_table(self):
        '''
            bmr has source ID -> [matchlen, target ID]
            bml has target ID -> [matchlen, source ID]
        '''
        with open(self.input_file, "r") as fp:
            while True:
                line = fp.readline().strip()
                if len(line) == 0:
                    break
                line = line.split(" ")
                self.bmr[line[0]] = [line[1], line[2]]

                if line[2] in self.bml:
                    self.bml[line[2]].append([line[1], line[0]])
                else:
                    self.bml[line[2]] = [[line[1], line[0]]]

        mark = []
        for k,v in self.bml.items():
            self.bml[k] = sorted(v, key = itemgetter(0), reverse=True)
            matches = self.bml[k]
            maxlen = matches[0][0]
            flag = False
            for i in range(1, len(matches)):
                if matches[i][0] == maxlen:
                    flag = True
                    break
            if flag == False:
                self.bml[k] = self.bml[k][0]
            else:
                mark.append(k)

        for m in mark:
            del self.bml[m]

        ### Find the left most start and right most stops of the unitigs
        for k,_ in sorted(self.bmr.items()):
            if k not in self.bml:
                self.leftmost.append(k)

        for k,_ in sorted(self.bml.items()):
            if k not in self.bmr:
                self.rightmost.append(k)
    
    def print_tigs(self):
        with open(self.output_file, "w") as fp:
            for k,v in sorted(self.tigs.items()):
                fp.write(k + "\n")
                for match in v:
                    fp.write(match[0] + " " + match[1] + "\n")
        fp.close()

# def main():
#     tigs = Tigs(input_file=input_file, output_file=output_file)   

    

# if __name__ == "__main__":
#     main()