# NucBreak manual

<br><br>
## 1 Introduction
NucBreak detects structural errors in assemblies and structural variants between pairs of genomes when only a genome of one organism and Illumina paired-end reads from another organism are available. It is able to detect insertions, deletions, different inter- and intra-chromosomal translocations, and inversions. However, the types of detected breakpoints are not specified. It was written in Python and uses Bowtie2 for reads alignment. The tool is described in the manuscript mentioned in Section 5. 

<br><br>
## 2 Prerequisites
NucBreak can be run on Linux and Mac OS. It uses Python 2.7, Bowtie2 v2.2.9 and the SAMtools utilities v1.3.1. Bowtie2 and SAMtools should be installed and be in the PATH before running NucBreak.

Bowtie2 can be downloaded at https://sourceforge.net/projects/bowtie-bio/files/bowtie2/ . 
The SAMtools can be downloaded at https://github.com/samtools/samtools .

<br><br>
## 3 Running NucBreak
### 3.1 Command line syntax and input arguments
To run NucBreak, run the `nucbreak.py` script with valid input arguments:

```
python nucbreak.py [-h] [--min_frag_size [MIN_FRAG_SIZE]]
                        [--max_frag_size [MAX_FRAG_SIZE]
                        [--sam_1 [SAM_1]]
                        [--sam_2 [SAM_2]] 
                        [--bam_pos [{yes,no}]] 
                        [--version]
                        Genome.fasta PE_reads_1.fastq PE_reads_2.fastq Output_dir Prefix
```

Positional arguments:

* **Genome.fasta** - Fasta file with genome sequences
* **PE_reads_1.fastq** - Fastq file with the first part of paired-end reads. They supposed to be forward-oriented
* **PE_reads_2.fastq** - Fastq file with the second part of paired-end reads. They supposed to be reverse-oriented
* **Output_dir** - Path to the directory where all intermediate and final results will be stored
* **Prefix** - Name that will be added to all generated files including the ones created by Bowtie2

Optional arguments:

* **-h, --help** - show this help message and exit
* **--min_frag_size** - minimum fragment size used to choose perfectly mapped read pairs
* **--max_frag_size** - miximum fragment size used to choose perfectly mapped read pairs
* **--sam_1** - Path to the already existing Bowtie2 sam file containing alignment results for the first part of paired-end reads.
* **--sam_2** - Path to the already existing Bowtie2 sam file containing alignment results for the second part of paired-end reads.
* **--bam_pos** - Generate bam files with entries sorted out by location and index files (yes/no)
* **--version** - show program's version number and exit


### 3.2 Running examples
A running example with the NucBreak predefined parameters values:

```
python nucbreak.py my_genome.fasta my_pe_reads_1.fastq my_pe_reads_1.fastq my_output_dir my_prefix
```


A running example with the already existed Bowtie2 sam files. Each read file is supposed to be aligned independently of another read file. Bowtie2 should be run with the  "--sensitive_local --ma 1 -a" parameter settings. The output sam files should be sorted by read names.

```
python nucbreak.py --sam_1 my_sam_1 --sam_2 my_sam_2 my_genome.fasta my_pe_reads_1.fastq my_pe_reads_1.fastq my_output_dir my_prefix
```

A running example with the predefined minimum and maximum fragment sizes. It is better to use your own minimum and maximum fragment sizes only when you are not agree with automatically detected ones.

```
python nucbreak.py --min_frag_size 50 --max_frag_size 1150 my_sam_2 my_genome.fasta my_pe_reads_1.fastq my_pe_reads_1.fastq my_output_dir my_prefix
```

To visualize read alignments in genome browsers, use bam_pos option. The bam file with alignments sorted by positions together with indexed files will be generated automatically:
```
python nucbreak.py --bam_pos yes my_genome.fasta my_pe_reads_1.fastq my_pe_reads_1.fastq my_output_dir my_prefix
```

<br><br>
## 4 NucBreak output
NucBreak puts the Bowtie2 output in the `<output_dir>/bowtie2` directory. The file with the fragment size distribution and the file with detected breakpoints are located in `<output_dir>`. 


### 4.1 Fragment_size_distr.txt
The file contains information about the minimum and maximum fragments sizes and the read length used by NucBreak together with fragment size distribution. The first and second columns show found fragment sizes and the corresponding number of read pairs for each fragment size, respectively.

The Fragment_size_distr.txt file example:
```
min_frag_size=35
max_frag_size=1129
read_length=251

Fragment size distribution
250	200
251	287
252	357
253	344
254	317
255	351
256	369
257	397
258	426
...
```


### 4.2 prefix_breakpoints.bedgraph
The file contains information about all detected assembly errors or structural variations in a genome.  The first column corresponds to the genome sequence name. The second and third columns show the location of detected breakpoints. The fourth column is used for the result visualization in a genome browser and is always equal to 1. 


The prefix_breakpoints.bedgraph file example:
```
track type=bedGraph name=breakpoints description="BedGraph format" visibility=full color=0,0,0 graphType=bar autoScale=on
NODE_44	   9866	 9873	1
NODE_136   352	 369	1
NODE_136   537	 589	1
NODE_136   1047	 1064	1
NODE_150   2533	 2541	1
NODE_649   506	 526	1
...
```

<br><br>
## 5 Citing NucBreak
To cite your use of NucBreak in your publication :

Khelik K., et al. NucBreak: Location of structural errors in a genome assembly and structural variations between a pair of genomes using Illumina paired-end reads. (in preparation) 





