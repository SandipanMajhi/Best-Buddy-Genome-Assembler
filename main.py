import sys
import argparse
from operator import itemgetter

from rights import RightSearch
from unitigs import Tigs
from combine import Assembly

parser = argparse.ArgumentParser(description="Best Buddy Assembler")
parser.add_argument("input_file", help="Fastq File", type=str)
parser.add_argument("output_file", help="Genome Assembly", type=str)
parser.add_argument("-k", metavar="--min_overlap" ,help="Minimum Overlaps for assembly", type=int, default=85)
args = parser.parse_args()


if __name__ == "__main__": 
    '''
        input_file  ->  fastq file
        output_file ->  provides the assemblies
    '''
    ### main arguments to the file
    input_file = args.input_file
    output_file = args.output_file
    min_overlap = args.k

    ### intermediate output files
    bmr_file = "bmr.txt"
    unitigs_file = "unitigs.txt"
    assembly_file = "assembly.txt"

    ### main program
    _ = RightSearch(input_file=input_file, min_overlap=min_overlap, output_file=bmr_file)
    _ = Tigs(input_file=bmr_file, output_file=unitigs_file)
    _ = Assembly(fastq_file=input_file, input_file=unitigs_file, output_file=output_file)

 