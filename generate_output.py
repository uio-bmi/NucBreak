# copyright (c) 2017 Ksenia Khelik
#
# This Source Code Form is subject to the 
# terms of the Mozilla Public License, v. 2.0. 
# If a copy of the MPL was not distributed 
# with this file, You can obtain one at 
# https://mozilla.org/MPL/2.0/.
#
#-------------------------------------------------------------------------------

import re

def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def CREATE_BedGraph_FILE(result_dict,error_name, output_file):

    
    
    f=open(output_file,'w')

    f.write('track type=bedGraph name='+error_name+' description="BedGraph format" visibility=full color=0,0,0 graphType=bar autoScale=on\n')

    for ref_seq_name in sorted(result_dict.keys(), key=natural_key):
        for entry in result_dict[ref_seq_name][error_name]:
            if entry[2]>=0:
                f.write(ref_seq_name+'\t'+str(entry[0]-1)+'\t'+str(entry[1])+'\t'+str(entry[2])+'\n')

    f.close() 


def GENERATE_OUTPUT(read_groups_dict, working_dir, prefix):

    CREATE_BedGraph_FILE(read_groups_dict, 'breakpoints', working_dir+prefix+'_'+'breakpoints'+'.bedgraph')

    '''
    for gr in ['single_forward:single_multiple_s', 'single_multiple_s:multiple_forward',
               'single_reverse:single_multiple_m', 'single_multiple_m:multiple_reverse',
               'multiple_forward:multiple_single_m', 'multiple_reverse:multiple_single_s',
               'multiple_single_m:single_forward', 'multiple_single_s:single_reverse',
               'breakpoints_forward','breakpoints_reverse', 'breakpoints'
               ]:
            CREATE_BedGraph_FILE(read_groups_dict, gr, working_dir+'evaluation/'+prefix+'_'+gr+'.bedgraph')

    for gr in ['Single_forward','Single_reverse','Multiple_forward','Multiple_reverse','Single_Multiple_s', 'Multiple_Single_m','Single_Multiple_m', 'Multiple_Single_s']:
            CREATE_BedGraph_FILE(read_groups_dict, gr, working_dir+'evaluation/'+prefix+'_'+gr+'.bedgraph')
    
    '''
