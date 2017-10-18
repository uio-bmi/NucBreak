import general
# copyright (c) 2017 Ksenia Khelik
#
# This Source Code Form is subject to the 
# terms of the Mozilla Public License, v. 2.0. 
# If a copy of the MPL was not distributed 
# with this file, You can obtain one at 
# https://mozilla.org/MPL/2.0/.
#
#-------------------------------------------------------------------------------



def PARSE_SAM_FILES(pe_sam_1,pe_sam_2):
    insertion_size_dict={}
    asmb_seq_dict={}
    temp_list=[]

    #find full read_length
    read_length=-1
    f1=open(pe_sam_1,'r')
    line1=f1.readline()
    
    while line1:
        
        if not line1.startswith('@'): 
            temp1=line1.split('\t')
            read_name1=temp1[0].split('/')[0]
            read_length=max(len(temp1[9]),read_length)
        

        line1=f1.readline()
            
    f1.close()

    f1=open(pe_sam_2,'r')
    line1=f1.readline()
    
    while line1:
        
        if not line1.startswith('@'): 
            temp1=line1.split('\t')
            read_name1=temp1[0].split('/')[0]
            read_length=max(len(temp1[9]),read_length)
        

        line1=f1.readline()
            
    f1.close()
    



    
    # parse_file
    f1=open(pe_sam_1,'r')
    f2=open(pe_sam_2,'r')



    line1=f1.readline()
    line2=f2.readline()

    

    while line1:
        if line1.startswith('@'):
                if line1.startswith('@SQ'):
                    
                    temp=line1[:-1].split()
                    seq_name=temp[1][3:]
                    seq_len=int(temp[2][3:])

                    asmb_seq_dict[seq_name]=seq_len

                    
                line1=f1.readline()
        else:
            break
        

    while line2:
        if line2.startswith('@'):
                if line2.startswith('@SQ'):
                    
                    temp=line2[:-1].split()
                    seq_name=temp[1][3:]
                    seq_len=int(temp[2][3:])

                    if not asmb_seq_dict.has_key(seq_name):
                        asmb_seq_dict[seq_name]=seq_len

                line2=f2.readline()
                
        else:
            break
    
    read_groups_dict={}
    for entry in asmb_seq_dict.keys():
        
        read_groups_dict[entry]={'Single_forward':[], 'Single_reverse':[],
                                 'Multiple_Single_s':[],'Multiple_Single_m':[],
                                 'Single_Multiple_s':[],'Single_Multiple_m':[],
                                 'Multiple_forward':[],'Multiple_reverse':[],
                                 'single_forward:single_multiple_s':[],
                                 'single_reverse:single_multiple_m':[],
                                 'single_multiple_s:multiple_forward':[],
                                 'single_multiple_m:multiple_reverse':[],
                                 'multiple_forward:multiple_single_m':[],
                                 'multiple_reverse:multiple_single_s':[],
                                 'mutiple_single_m:single_forward':[],'multiple_single_s:single_reverse':[]
                                 }

   
    read_set=[[],[]]

    if line1!='':
        end1_flag=0
    else:
        end1_flag=1
        
    if line2!='':
        end2_flag=0
    else:
        end2_flag=1

    
    while end1_flag==0 and end2_flag==0:

                temp1=line1.split('\t')
                read_name1=temp1[0].split('/')[0]
                append_line=general.FIND_LINE(temp1)
                read_set[0].append(append_line)

               
                flag_1=0
                while flag_1==0:
                    line1=f1.readline()
                    
                    if line1!='':
                        temp_cur=line1.split('\t')
                        read_name_cur=temp_cur[0].split('/')[0]

                        if read_name_cur==read_name1:
                            append_line=general.FIND_LINE(temp_cur)
                            read_set[0].append(append_line)
                        else:
                            flag_1=1
                    else:
                        end1_flag=1
                        flag_1=1
               
                flag_2=0
                temp2=line2.split('\t')
                read_name2=temp2[0].split('/')[0]

                if read_name2==read_name1:
                        append_line=general.FIND_LINE(temp2)
                        read_set[1].append(append_line)

                        while flag_2==0:
                            line2=f2.readline()

                            if line2!='':
                                temp_cur=line2.split('\t')
                                read_name_cur=temp_cur[0].split('/')[0]

                                if read_name_cur==read_name2:
                                    append_line=general.FIND_LINE(temp_cur)
                                    read_set[1].append(append_line)
                                else:
                                    flag_2=1
                            else:
                                end2_flag=1
                                flag_2=1

                if len(read_set[0])==1 and len(read_set[1])==1:
                    entry1=read_set[0][0]
                    entry2=read_set[1][0]
                    

                    if (entry1[0]==1 and entry2[0]==-1 and entry1[2]<=entry2[2]) or (entry1[0]==-1 and entry2[0]==1 and entry2[2]<=entry1[2]):
                        if entry1[0]==-1:
                            entry1=read_set[1][0]
                            entry2=read_set[0][0]

                            
                        if entry1[1]==entry2[1]:
                            ins_size=FIND_INSERT_SIZE(entry1,entry2)

                            if entry2[5]-entry2[4]+1==len(entry2[8]) and entry1[5]-entry1[4]+1==len(entry1[8]) and entry1[3]<=entry2[3] :
                                if not insertion_size_dict.has_key(ins_size):
                                    insertion_size_dict[ins_size]=0
                                insertion_size_dict[ins_size]+=1

                            if (entry1[4]==1 and entry2[5]==len(entry2[8])) or\
                               (entry1[2]==1 and entry2[5]==len(entry2[8])) or\
                               (entry1[4]==1 and entry2[3]==asmb_seq_dict[entry2[1]]) or\
                               (entry1[2]==1 and entry2[3]==asmb_seq_dict[entry2[1]]):

                                if entry1[3]<=entry2[3]:
                                    read_groups_dict[entry1[1]]['Single_forward'].append([ins_size,entry1[2],entry1[3]])
                                    read_groups_dict[entry2[1]]['Single_reverse'].append([ins_size,entry2[2],entry2[3]])


                elif (len(read_set[0])==1 and len(read_set[1])>1) or (len(read_set[0])>1 and len(read_set[1])==1):

                    if len(read_set[0])==1:
                        entry1_list=read_set[0]
                        entry2_list=read_set[1]
                    else:
                        entry2_list=read_set[0]
                        entry1_list=read_set[1]

                    
                    for entry1_raw in entry1_list:
                        for entry2_raw in entry2_list:
                            
                            if (entry1_raw[0]==1 and entry2_raw[0]==-1 and entry1_raw[2]<=entry2_raw[2]) or (entry1_raw[0]==-1 and entry2_raw[0]==1 and entry2_raw[2]<=entry1_raw[2]):
                                if entry1_raw[0]==1:
                                    group_type='Single_Multiple'
                                    entry1=entry1_raw
                                    entry2=entry2_raw
                                else:
                                    group_type='Multiple_Single'
                                    entry1=entry2_raw
                                    entry2=entry1_raw
                                    
                                
                                if entry1[1]==entry2[1]: #same reference
                                    ins_size=FIND_INSERT_SIZE(entry1,entry2)

                                    
                                    entry1.append(group_type)
                                    entry2.append(group_type)
                                        
                                    if entry1[4]==1 and entry2[5]==len(entry2[8]) or\
                                       (entry1[2]==1 and entry2[5]==len(entry2[8])) or\
                                       (entry1[4]==1 and entry2[3]==asmb_seq_dict[entry2[1]]) or\
                                       (entry1[2]==1 and entry2[3]==asmb_seq_dict[entry2[1]]):

                                        if entry1[3]<=entry2[3]:

                                            if group_type=='Single_Multiple':
                                                temp_list.append([ins_size,entry1[1],entry1[2],entry1[3],group_type+'_s'])
                                                temp_list.append([ins_size, entry2[1],entry2[2],entry2[3],group_type+'_m'])
                                            else:
                                                temp_list.append([ins_size,entry1[1],entry1[2],entry1[3],group_type+'_m'])
                                                temp_list.append([ins_size, entry2[1],entry2[2],entry2[3],group_type+'_s'])

                                            
                          
                        for entry in temp_list: 
                                read_groups_dict[entry[1]][entry[4]].append([entry[0],entry[2],entry[3]])
                        for i in range(len(temp_list)):
                            temp_list.pop(0)

                                
                elif len(read_set[0])>1 and len(read_set[1])>1:
                    entry1_list=read_set[0]
                    entry2_list=read_set[1]

                    for entry1_raw in entry1_list:
                        flag=0
                        for entry2_raw in entry2_list:
                            
                            if (entry1_raw[0]==1 and entry2_raw[0]==-1 and entry1_raw[2]<=entry2_raw[2]) or (entry1_raw[0]==-1 and entry2_raw[0]==1 and entry2_raw[2]<=entry1_raw[2]):
                                if entry1_raw[0]==1:
                                    entry1=entry1_raw
                                    entry2=entry2_raw
                                else:
                                    entry1=entry2_raw
                                    entry2=entry1_raw
                                
                                    
                                if entry1[1]==entry2[1]: #same r
                                    ins_size=FIND_INSERT_SIZE(entry1,entry2)

                                    if entry1[4]==1 and entry2[5]==len(entry2[8]) or\
                                      (entry1[2]==1 and entry2[5]==len(entry2[8])) or\
                                      (entry1[4]==1 and entry2[3]==asmb_seq_dict[entry2[1]]) or\
                                      (entry1[2]==1 and entry2[3]==asmb_seq_dict[entry2[1]]):

                                      if entry1[3]<=entry2[3]:      
                                        read_groups_dict[entry1[1]]['Multiple_forward'].append([ins_size,entry1[2],entry1[3]])
                                        read_groups_dict[entry2[1]]['Multiple_reverse'].append([ins_size,entry2[2],entry2[3]])

                for i in range(len(read_set[0])):
                    read_set[0].pop(0)
                for i in range(len(read_set[1])):
                    read_set[1].pop(0)
                    
    f1.close()
    f2.close()


    return insertion_size_dict, read_length, read_groups_dict, asmb_seq_dict

def FILTER_GROUP(group_list,min_ins_size,max_ins_size):
    new_group=[]

    flag=0
    
    for entry in group_list:
        if entry[0]>=min_ins_size and entry[0]<=max_ins_size:
            new_group.append([entry[1],entry[2],flag])
            
    return new_group

def  FILTER_READ_GROUPS(read_groups_dict,min_ins_size,max_ins_size):

    for seq_name in read_groups_dict.keys():
        for gr_name in ['Single_forward', 'Single_reverse',
                    'Multiple_Single_s','Multiple_Single_m',
                    'Single_Multiple_s','Single_Multiple_m',
                    'Multiple_forward','Multiple_reverse']:
         
            read_groups_dict[seq_name][gr_name]=FILTER_GROUP(read_groups_dict[seq_name][gr_name],min_ins_size,max_ins_size)

    

def FIND_INSERT_SIZE(read_1, read_2):

    if read_1[0]==1 and read_2[0]==-1:
            ins_size=read_2[3]+len(read_2[8])-read_2[5]-read_1[2]+read_1[4]-1+1


    elif read_1[0]==-1 and read_2[0]==1:
            ins_size=read_1[3]+len(read_1[8])-read_1[5]-read_2[2]+read_2[4]-1+1
            
    else:
        insert_size='unknown'
            


    return ins_size

            

def FIND_INSERT_SIZE_VALUES(pe_sam_1,pe_sam_2,out_file,min_frag_size, max_frag_size):
 
    insertion_size_dict, read_length, read_groups_dict, asmb_seq_dict=PARSE_SAM_FILES(pe_sam_1,pe_sam_2)


    min_ins_size='none'
    max_ins_size='none'

    sorted_keys=sorted(insertion_size_dict.keys())
                                                        
    for i in range(len(insertion_size_dict.keys())):
        ins_size=sorted_keys[i]
        if insertion_size_dict[ins_size]>=10:
            flag_ins=0

            if i+10<len(insertion_size_dict.keys()):
                for j in range(1,11):
                    k_size=sorted_keys[i+j]
                    if insertion_size_dict[k_size]>=10:
                        flag_ins+=1
            else:
                flag_ins=10

            if flag_ins>2:
                min_ins_size=ins_size
                break

    for i in range(len(insertion_size_dict.keys())-1,-1,-1):
        ins_size=sorted_keys[i]

        if insertion_size_dict[ins_size]>=10:
            flag_ins=0

            if i>10:
                for j in range(1,11):
                    k_size=sorted_keys[i-j]
                    if insertion_size_dict[k_size]>=10:
                        flag_ins+=1
            else:
                flag_ins=10

            if flag_ins>2:
                max_ins_size=ins_size
                break

        
    if  min_ins_size=='none' or max_ins_size=='none':
        max_val=-1
        max_ind=-1
        for i in range(len(insertion_size_dict.keys())):
            ins_size=insertion_size_dict.keys()[i]
            if insertion_size_dict[ins_size]>max_val:
                max_val=insertion_size_dict[ins_size]
                max_ind=ins_size
        min_ins_size=max_ind-50
        max_ins_size=max_ind+50
        
        min_ins_size=max(0, min_ins_size)

    f=open(out_file,'w')
    f.write('min_frag_size='+str(min_ins_size)+'\n')
    f.write('max_frag_size='+str(max_ins_size)+'\n')
    f.write('read_length='+str(read_length)+'\n')
    f.write('\nFragment size distribution\n')
    for ins_size in sorted(insertion_size_dict.keys()):
        f.write(str(ins_size)+'\t'+str(insertion_size_dict[ins_size])+'\n')
    f.close()


    if min_frag_size!='':
        min_ins_size=int(min_frag_size)

    if max_frag_size!='':
        max_ins_size=int(max_frag_size)
            

    
    FILTER_READ_GROUPS(read_groups_dict,min_ins_size,max_ins_size)

    return min_ins_size, max_ins_size, read_length,read_groups_dict, asmb_seq_dict                     
                        
