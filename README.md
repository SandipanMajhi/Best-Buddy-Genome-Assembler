# Best-Buddy-Genome-Assembler

Here I have coded a best buddy genome assembler which creates unambiguous genome assemblies from the fastq sequences. 

The program `rights.py` finds the longest unambiguous matches for its suffixes with the prefixes of the other reads in the fastq.
The program `unitigs.py` then finds the leftmost reads and its unambiguous extensions towards the right. It finds the longest unambiguous extension for the reads.
Finally `combine.py` combines these extensions into sequences.

The file `input.fastq` contains sequence reads of some genome. 

## Instructions for running the code

The main driver code is `main.py`.

Example of running the code - 
```
> python3 main.py input_file output_file -k 85
```
For help run 
```
> python3 main.py -h
> python3 main.py --help
```
The code produces some intermediate files like, `bmr.txt`, `unitigs.txt`.

The file `bmr.txt` contains the read sequence names having the longest suffix match with the prefix of a read sequence.
Hence, the file contains information like the following,
```
READ_NAME1 MATCH_LENGTH READ_NAME2
```
The file `unitigs.txt` contains the extensions of assembly. Start with the leftmost possible read that does not have any unambiguous prefix match with any other read. Now, we extend it by fetching the suffix-prefix matches towards the right.
Hence, `unitigs.txt` conatins information like this,
```
LEFTMOST READ1
MATCH_LENGTH READ2
MATCH_LENGTH READ3
MATCH_LENGTH READ4
```
