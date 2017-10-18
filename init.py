# copyright (c) 2017 Ksenia Khelik
#
# This Source Code Form is subject to the 
# terms of the Mozilla Public License, v. 2.0. 
# If a copy of the MPL was not distributed 
# with this file, You can obtain one at 
# https://mozilla.org/MPL/2.0/.
#
#-------------------------------------------------------------------------------


import os
import sys

def INIT_FUNC(working_dir,pe_1_file,pe_2_file,file_ref,bowtie2_1sam,bowtie2_2sam):

    cur_dir=os.getcwd()

    working_dir=os.path.abspath(working_dir)
    pe_1_file=os.path.abspath(pe_1_file)
    pe_2_file=os.path.abspath(pe_2_file)
    file_ref=os.path.abspath(file_ref)

    if bowtie2_1sam!='' and bowtie2_2sam!='':
        bowtie2_1sam=os.path.abspath(bowtie2_1sam)
        bowtie2_2sam=os.path.abspath(bowtie2_2sam)
    


    if not os.path.exists(file_ref):
        print
        print 'ERROR: the provided fasta file with genome sequences does not exist'
        print
        sys.exit(0)

    if not os.path.exists(pe_1_file):
        print
        print 'ERROR: the provided fastq file with the first part of the reads does not exist'
        print
        sys.exit(0)

    if not os.path.exists(pe_2_file):
        print
        print 'ERROR: the provided fastq file with the second part of the reads does not exist'
        print
        sys.exit(0) 


    if not os.path.exists(working_dir):
            cur_dir=os.getcwd()
            
            try:
                os.makedirs(working_dir)
            except OSError:
                print
                print 'ERROR: it is not possible to create working directory'
                print
                sys.exit(0)

    if not working_dir.endswith('/'):
        working_dir+='/'

    
        
    if not os.path.exists(working_dir+'Results'):
        os.makedirs(working_dir+'Results')

    if not os.path.exists(working_dir+'Results/bowtie2'):
        os.makedirs(working_dir+'Results/bowtie2')


    if bowtie2_1sam!='' and bowtie2_2sam!='':
        if not os.path.exists(bowtie2_1sam):
            print
            print 'ERROR: the provided sam file with the alignment results of the first part of the reads does not exist'
            print
            sys.exit(0)

        if not os.path.exists(bowtie2_2sam):
            print
            print 'ERROR: the provided sam file with the alignment results of the second part of the reads does not exist'
            print
            sys.exit(0) 
    elif bowtie2_1sam!='' and bowtie2_2sam=='':
        print
        print 'ERROR: the sam file with the alignment results of the second part of the reads was not provided'
        print
        sys.exit(0)

    elif bowtie2_1sam=='' and bowtie2_2sam!='':
        print
        print 'ERROR: the sam file with the alignment results of the first part of the reads was not provided'
        print
        sys.exit(0)
   
   
    return working_dir,pe_1_file,pe_2_file,file_ref,bowtie2_1sam,bowtie2_2sam 

