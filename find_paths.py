# copyright (c) 2017 Ksenia Khelik
#
# This Source Code Form is subject to the 
# terms of the Mozilla Public License, v. 2.0. 
# If a copy of the MPL was not distributed 
# with this file, You can obtain one at 
# https://mozilla.org/MPL/2.0/.
#
#-------------------------------------------------------------------------------


import general
import insert_size


def MERGE_FALSE_GAPS(input_list_init,sup_list):

    new_list=[]
    input_list=[]

    for i in range(len(input_list_init)):
       input_list.append([input_list_init[i][0],input_list_init[i][1]]) 
        
    overlap_gap_len=5
    check_int=[0,0]
    if len(input_list)==1:
        new_list.append(input_list[0])

    
    elif input_list!=[]:

        first=input_list[0]
        for i in range(1,len(input_list)):
            second=input_list[i]

            check_int[0]=first[1]
            check_int[1]=second[0]

            flag=0
            for entry in sup_list:
                if entry[0]+overlap_gap_len<=check_int[0] and entry[1]-overlap_gap_len>=check_int[1]:
                    flag=1
                    break
                elif entry[0]+overlap_gap_len<=check_int[0] and entry[1]>=check_int[1] and entry[1]-overlap_gap_len<check_int[1]:
                    flag=2
                    break
                elif entry[0]<=check_int[0] and entry[0]+overlap_gap_len>check_int[0] and entry[1]-overlap_gap_len>=check_int[1]:
                    flag=3
                    break
                elif entry[0]<=check_int[0] and entry[0]+overlap_gap_len>check_int[0] and entry[1]>=check_int[1] and entry[1]-overlap_gap_len<check_int[1]:
                    flag=4
                    break

            if flag==1:
                first[1]=second[1]
            elif flag==0:
                new_list.append([first[0],first[1]])
                first=second
            elif flag==2:
                new_list.append([first[0],first[1]])
                first=second
                first[0]=entry[1]+1
            elif flag==3:
                first[1]=entry[0]-1
                new_list.append([first[0],first[1]])
                first=second
            elif flag==4:
                first[1]=entry[0]-1
                new_list.append([first[0],first[1]])
                first=second
                first[0]=entry[1]+1
                
        new_list.append([first[0],first[1]])

    i=1
    for entry in new_list:
        entry.append(i)

        if i==1:
           i=2
        else:
            i=1

    return new_list
                    


def FIND_PATHS(elem_list):
   
    reads_full_list=[]
    reads_clipped_list=[]

    overlap_len=5

    result_list=[]
    
    for entry in elem_list:
        if entry[2]==0:
            reads_full_list.append(entry)
        else:
            reads_clipped_list.append(entry)


    if reads_full_list!=[]:
        if len(reads_full_list)==1:
            result_list.append([reads_full_list[0][0],reads_full_list[0][1],1])
        else:
            cur_interv=[reads_full_list[0][0],reads_full_list[0][1],1]
            val=2
            for i in range(1,len(reads_full_list)):
                next_elem=[reads_full_list[i][0],reads_full_list[i][1]]
                if next_elem[0]+overlap_len<cur_interv[1]:
                    cur_interv[1]=max(next_elem[1], cur_interv[1])

                elif next_elem[0]<=cur_interv[1] and next_elem[0]+overlap_len>=cur_interv[1]:
                    result_list.append([cur_interv[0],next_elem[0]-1,val])
                    if val==2:
                        val=1
                    else:
                        val=2
                    cur_interv[0]=cur_interv[1]+1
                    cur_interv[1]=next_elem[1]
                    
                else:
                    result_list.append([cur_interv[0],cur_interv[1],val])
                    if val==2:
                        val=1
                    else:
                        val=2
                    cur_interv[0]=next_elem[0]
                    cur_interv[1]=next_elem[1]
                    
            result_list.append([cur_interv[0],cur_interv[1],val])

    return result_list




def FIND_READS_GROUPS(read_groups_dict, asmb_seq_dict):

    for ref_name in read_groups_dict.keys():
            for gr in ['Single_forward','Single_reverse','Multiple_forward','Multiple_reverse','Single_Multiple_s', 'Multiple_Single_m','Single_Multiple_m', 'Multiple_Single_s']:
                read_groups_dict[ref_name][gr]=sorted(read_groups_dict[ref_name][gr],key=lambda inter:inter[0], reverse=False)
                read_groups_dict[ref_name][gr]=FIND_PATHS(read_groups_dict[ref_name][gr])
                
            read_groups_dict[ref_name]['Single_forward']=MERGE_FALSE_GAPS(read_groups_dict[ref_name]['Single_forward'],read_groups_dict[ref_name]['Single_reverse'])
            read_groups_dict[ref_name]['Single_reverse']=MERGE_FALSE_GAPS(read_groups_dict[ref_name]['Single_reverse'],read_groups_dict[ref_name]['Single_forward'])
            read_groups_dict[ref_name]['Multiple_forward']=MERGE_FALSE_GAPS(read_groups_dict[ref_name]['Multiple_forward'],read_groups_dict[ref_name]['Multiple_reverse'])
            read_groups_dict[ref_name]['Multiple_reverse']=MERGE_FALSE_GAPS(read_groups_dict[ref_name]['Multiple_reverse'],read_groups_dict[ref_name]['Multiple_forward'])
    
   
    return read_groups_dict, asmb_seq_dict
