# copyright (c) 2017 Ksenia Khelik
#
# This Source Code Form is subject to the 
# terms of the Mozilla Public License, v. 2.0. 
# If a copy of the MPL was not distributed 
# with this file, You can obtain one at 
# https://mozilla.org/MPL/2.0/.
#
#-------------------------------------------------------------------------------


import subprocess
import os

def RUN_BOWTIE(work_dir, prefix, assembly, PE_reads_1, PE_reads_2, bam_opt):

    
    subprocess.call(['bowtie2-build', '-f', assembly, work_dir+prefix+'_tree'])
    current_dir=os.getcwd()    
    os.chdir(work_dir)
    
    subprocess.call(['bowtie2','--sensitive-local','--ma','1','-a','-p','5', '-x', prefix+'_tree', '-U',  PE_reads_1, '-S', work_dir+prefix+'_1.sam'])
    subprocess.call(['bowtie2','--sensitive-local','--ma','1' ,'-a','-p','5', '-x', prefix+'_tree', '-U',  PE_reads_2, '-S', work_dir+prefix+'_2.sam'])
        
    f=open(work_dir+prefix+'_1.bam','w')
    subprocess.call(['samtools', 'view', '-Sb',  work_dir+prefix+'_1.sam'],stdout=f )
    f.close()
    subprocess.call(['samtools', 'sort','-n', work_dir+prefix+'_1.bam', '-o', work_dir+prefix+'_1_sorted_name.bam']) 
    subprocess.call(['samtools', 'view', '-h','-o', work_dir+prefix+'_1_sorted_name.sam', work_dir+prefix+'_1_sorted_name.bam'])
    os.remove(work_dir+prefix+'_1_sorted_name.bam')


    f=open(work_dir+prefix+'_2.bam','w')
    subprocess.call(['samtools', 'view', '-Sb',  work_dir+prefix+'_2.sam'],stdout=f )
    f.close()
    subprocess.call(['samtools', 'sort','-n', work_dir+prefix+'_2.bam', '-o', work_dir+prefix+'_2_sorted_name.bam']) 
    subprocess.call(['samtools', 'view', '-h','-o', work_dir+prefix+'_2_sorted_name.sam', work_dir+prefix+'_2_sorted_name.bam'])
    os.remove(work_dir+prefix+'_2_sorted_name.bam')


    if bam_opt=='yes':
        subprocess.call(['samtools', 'sort', work_dir+prefix+'_1.bam', '-o', work_dir+prefix+'_1_sorted.bam']) 
        subprocess.call(['samtools', 'index', work_dir+prefix+'_1_sorted.bam', work_dir+prefix+'_1_sorted.bai'])
        
        subprocess.call(['samtools', 'sort', work_dir+prefix+'_2.bam', '-o', work_dir+prefix+'_2_sorted.bam']) 
        subprocess.call(['samtools', 'index', work_dir+prefix+'_2_sorted.bam', work_dir+prefix+'_2_sorted.bai'])
        
    os.remove(work_dir+prefix+'_1.sam')
    os.remove(work_dir+prefix+'_1.bam')
    os.remove(work_dir+prefix+'_2.sam')
    os.remove(work_dir+prefix+'_2.bam')
        

    
    os.chdir(current_dir)

    
    return work_dir+prefix+'_1_sorted_name.sam',work_dir+prefix+'_2_sorted_name.sam'

