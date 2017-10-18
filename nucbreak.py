# copyright (c) 2017 Ksenia Khelik
#
# This Source Code Form is subject to the 
# terms of the Mozilla Public License, v. 2.0. 
# If a copy of the MPL was not distributed 
# with this file, You can obtain one at 
# https://mozilla.org/MPL/2.0/.
#
#-------------------------------------------------------------------------------


import init
import run_Bowtie2
import insert_size
import find_paths
import find_breakpoints
import generate_output

import sys
import argparse



def START(args):
    asmb_file=args['asmb_file']
    pe_1_file=args['pe_1_file']
    pe_2_file=args['pe_2_file']
    working_dir=args['working_dir']
    prefix=args['prefix']

    bowtie2_1sam=args['sam_1']
    bowtie2_2sam=args['sam_2']

    bam_opt=args['bam_pos']

    min_frag_size=args['min_frag_size']
    max_frag_size=args['max_frag_size']
    
    
   
    #1. check input data correctness

    working_dir,pe_1_file,pe_2_file,asmb_file,bowtie2_1sam,bowtie2_2sam=init.INIT_FUNC(working_dir,pe_1_file,pe_2_file,asmb_file,bowtie2_1sam,bowtie2_2sam)

    working_dir+='Results/'

    
    if bowtie2_1sam=='' and bowtie2_2sam=='':
        pe_sam_1, pe_sam_2=run_Bowtie2.RUN_BOWTIE(working_dir+'bowtie2/', prefix, asmb_file, pe_1_file, pe_2_file, bam_opt)
    else:
        pe_sam_1=bowtie2_1sam
        pe_sam_2=bowtie2_2sam

    
    min_ins_size, max_ins_size, read_length,read_groups_dict, asmb_seq_dict=insert_size.FIND_INSERT_SIZE_VALUES(pe_sam_1,pe_sam_2,working_dir+'Fragment_size_distr.txt',min_frag_size, max_frag_size)

    print 'min_frag_size', min_ins_size
    print 'max_frag_size', max_ins_size
    print 'read_length', read_length

    

    
    read_groups_dict, asmb_seq_dict=find_paths.FIND_READS_GROUPS(read_groups_dict, asmb_seq_dict)

    read_groups_dict=find_breakpoints.FIND_ERRORS(read_groups_dict, asmb_seq_dict,read_length)

    generate_output.GENERATE_OUTPUT(read_groups_dict, working_dir, prefix)


def main():
    
    argv=sys.argv
    parser = argparse.ArgumentParser()

    parser.add_argument('asmb_file',metavar='Genome.fasta', type=str, help='- Fasta file with genome sequences')
    parser.add_argument('pe_1_file',metavar='PE_reads_1.fastq', type=str, help='- Fastq file with the first part of paired-end reads. They supposed to be forward-oriented')
    parser.add_argument('pe_2_file',metavar='PE_reads_2.fastq', type=str, help='- Fastq file with the second part of paired-end reads. They supposed to be reverse-oriented')
    parser.add_argument('working_dir',metavar='Output_dir', type=str, help='- Path to the directory where all intermediate and final results will be stored')
    parser.add_argument('prefix',metavar='Prefix', type=str, help='- Name that will be added to all generated files including the ones created by Bowtie2')
    parser.add_argument('--min_frag_size',  type=str, nargs='?',default="", help='- minimum fragment size used to choose perfectly mapped read pairs ')
    parser.add_argument('--max_frag_size',  type=str, nargs='?',default="", help='- miximum fragment size used to choose perfectly mapped read pairs ')
    parser.add_argument('--sam_1',  type=str, nargs='?',default="", help='- Path to the already existing Bowtie2 sam file containing alignment results for the first part of paired-end reads. ')
    parser.add_argument('--sam_2',  type=str, nargs='?',default="", help='- Path to the already existing Bowtie2 sam file containing alignment results for the second part of paired-end reads. ')
    parser.add_argument('--bam_pos',  type=str, nargs='?',default='no',choices=['yes','no'], help="- Generate bam files with entries sorted out by location and index files (yes/no)")
    parser.add_argument('--version', action='version', version='NucBreak version 1.0')
   
    args=vars(parser.parse_args())

    START(args)
    
main()
