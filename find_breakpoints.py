# copyright (c) 2017 Ksenia Khelik
#
# This Source Code Form is subject to the 
# terms of the Mozilla Public License, v. 2.0. 
# If a copy of the MPL was not distributed 
# with this file, You can obtain one at 
# https://mozilla.org/MPL/2.0/.
#
#-------------------------------------------------------------------------------


def MERGE_BREAKPOINTS(breakpoints_forward,breakpoints_reverse):

    res_list=[]
    temp_dict={}

    for forw in breakpoints_forward:
        for i in range(forw[0], forw[1]+1):
            temp_dict[i]=0

    for rev in breakpoints_reverse:
        for i in range(rev[0], rev[1]+1):
            if temp_dict.has_key(i):
                temp_dict[i]+=1

    temp_list=[]
    for i in temp_dict.keys():
        if temp_dict[i]>0:
            temp_list.append(i)

    
    temp_list=sorted(temp_list)

    if temp_list!=[]:
        st_int=temp_list[0]
        end_int=temp_list[0]
        for num in temp_list[1:]:
            if num==end_int+1:
                end_int=num
            else:
                res_list.append([st_int,end_int,1])
                st_int=num
                end_int=num
        res_list.append([st_int,end_int,1])


    temp_2_dict={}
    for forw in breakpoints_forward:
        for i in range(forw[0], forw[1]+6):
            temp_2_dict[i]=0
        
    for rev in breakpoints_reverse:
        for i in range(rev[0]-5, rev[1]+1):
            if temp_2_dict.has_key(i):
                temp_2_dict[i]+=1

    temp_2_list=[]
    for i in temp_2_dict.keys():
        if temp_2_dict[i]>0 :
            temp_2_list.append(i)


    temp_2_list=sorted(temp_2_list)
    
    if temp_2_list!=[]:
        st_int=temp_2_list[0]
        end_int=temp_2_list[0]
        for num in temp_2_list[1:]:
            if num==end_int+1:
                end_int=num
            else:
                flag=0
                for entry in res_list:
                    en_st=entry[0]
                    en_end=entry[1]

                    if st_int<=en_st and end_int>=en_st:
                        flag=1
                        break
                    elif st_int>en_st and st_int<=en_end:
                        flag=1
                        break
                
                if flag==0:
                    res_list.append([st_int,end_int,1])
                st_int=num
                end_int=num
        flag=0
        for entry in res_list:
            en_st=entry[0]
            en_end=entry[1]

            if st_int<=en_st and end_int>=en_st:
                flag=1
                break
            elif st_int>en_st and st_int<=en_end:
                flag=1
                break
        if flag==0:
            res_list.append([st_int,end_int,1])
                                
    res_list=sorted(res_list, key=lambda inter:inter[0], reverse=False)    
    return res_list

def IS_COVERED_POINT_second(point, SM_list):

    flag=0
    for entry1 in SM_list:
        if entry1[0]<=point and entry1[1]>=point:
            flag=1
            break

    return flag



def IS_INSIDE_INTERV(interv, inside_list):

    flag=0
    for entry in inside_list:
        
        if entry[0]<interv[0] and interv[1]<entry[1]:
            flag=1
            break

    return flag

def IS_COVERED_POINT(point, SM_list):

    flag=0
    overlap_breakpoint_len=4
    for entry1 in SM_list:
        if entry1[0]+overlap_breakpoint_len<point and entry1[1]-overlap_breakpoint_len>point:
            flag=1
            break
       

    return flag

def CHECK_POINT_SECOND(point,SM_list,  Mult_list):

    
    int_coord=[0,0]
    flag=0

    for i in range(len(SM_list)-1):
        int_coord[0]=SM_list[i][1]+1
        int_coord[1]=SM_list[i+1][0]-1

        if SM_list[i][1]==point:
            for entry in Mult_list:
                if entry[0]<point and entry[1]>point:
                    flag=1
                    
                    break
  
        elif point>int_coord[0] and point <int_coord[1]:
            for entry in Mult_list:
                if entry[0]<int_coord[0] and entry[1]>point:
                    flag=1
                    
                    break
        
    return flag

def FIND_INTERV_LENGTH(st,all_list,seq_len):

    points=[]
    for entry in all_list:
        points.append([entry[0]+5,'st'])
        points.append([entry[1],'end'])

    points=sorted(points,key=lambda inter:inter[0], reverse=False)
        
    end=-1
    for entry in points:
        if st<entry[0]:
            if entry[1]=='end':
               end=entry[0]+5
            else:
               end=entry[0] 
            break
    
    if end==-1:
        end=seq_len

    

    return end

def MERGE_FALSE_GAPS_SECOND(input_list_init,sup_list):

    new_list=[]
    input_list=[]

    for i in range(len(input_list_init)):
       input_list.append([input_list_init[i][0],input_list_init[i][1]]) 
        
    overlap_gap_len=10
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
                if entry[0]<=check_int[0] and entry[1]>=check_int[1]:
                    flag=1
                    break
                
                
            if flag==1:
                first[1]=second[1]
            else:
                new_list.append([first[0],first[1]])
                first=second
                
        new_list.append([first[0],first[1]])

    i=1
    for entry in new_list:
        entry.append(i)

        if i==1:
           i=2
        else:
            i=1

    return new_list



def FIND_BREAKPOINTS(Single_list_init, Single_Multiple_list_init, Multiple_Single_list_init, Multiple_list_init,seq_len):

    Single_list=sorted(Single_list_init,key=lambda inter:inter[0], reverse=False )
    Single_Multiple_list=sorted(Single_Multiple_list_init,key=lambda inter:inter[0], reverse=False )
    Multiple_Single_list=sorted(Multiple_Single_list_init,key=lambda inter:inter[0], reverse=False )
    Multiple_list=sorted(Multiple_list_init,key=lambda inter:inter[0], reverse=False )

    all_list=[]

    for entr_list in [Single_list,Single_Multiple_list,Multiple_Single_list,Multiple_list]:
        for entry in entr_list:
            all_list.append(entry)

    all_list=sorted(all_list,key=lambda inter:inter[0], reverse=False)

    raw_intervals={'single:single_mult':[],'single_mult:mult':[],'mult:mult_single':[],
                   'mult_single:single':[],'breakpoints':[]}


    
    Multiple_Single_list_merged=MERGE_FALSE_GAPS_SECOND(Multiple_Single_list,Single_Multiple_list)
    Single_Multiple_list_merged=MERGE_FALSE_GAPS_SECOND(Single_Multiple_list,Multiple_Single_list)

    
    
    for entry in Single_list:
        if IS_COVERED_POINT(entry[1], Single_Multiple_list_merged)==0:
            if CHECK_POINT_SECOND(entry[1],Single_Multiple_list_merged,  Multiple_list)==0:
                if IS_INSIDE_INTERV(entry, Multiple_list)==0:
                    end_int=FIND_INTERV_LENGTH(entry[1],all_list,seq_len)
                    raw_intervals['single:single_mult'].append([entry[1], end_int,1])

    for entry in Single_Multiple_list:
         if IS_COVERED_POINT(entry[1], Multiple_list)==0:
                 if IS_COVERED_POINT_second(entry[1], Multiple_Single_list)==0:
                     if IS_INSIDE_INTERV(entry, Single_list)==0:
                         end_int=FIND_INTERV_LENGTH(entry[1],all_list,seq_len)
                         raw_intervals['single_mult:mult'].append([entry[1], end_int,1])

    for entry in Multiple_list:
        if IS_COVERED_POINT(entry[1],Multiple_Single_list_merged)==0:
            if CHECK_POINT_SECOND(entry[1],Multiple_Single_list_merged,  Single_list)==0: 
                if IS_INSIDE_INTERV(entry, Single_list)==0:
                    end_int=FIND_INTERV_LENGTH(entry[1],all_list,seq_len)
                    raw_intervals['mult:mult_single'].append([entry[1], end_int,1])
    
    
    for entry in Multiple_Single_list:
        if IS_COVERED_POINT(entry[1],Single_list)==0:
                if IS_COVERED_POINT_second(entry[1],Single_Multiple_list)==0:
                    if IS_INSIDE_INTERV(entry, Multiple_list)==0:
                        end_int=FIND_INTERV_LENGTH(entry[1],all_list,seq_len)
                        raw_intervals['mult_single:single'].append([entry[1], end_int,1])


    
    for entr_list in [raw_intervals['single:single_mult'],raw_intervals['single_mult:mult'],
                      raw_intervals['mult:mult_single'],raw_intervals['mult_single:single']]:
        for entry in entr_list:
            raw_intervals['breakpoints'].append([entry[0],entry[1],1])


    raw_intervals['breakpoints']=MERGE_ERRORS(raw_intervals['breakpoints'])

    for entry in raw_intervals['breakpoints']:
        entry.append(1)
        
    return raw_intervals
    
def MERGE_ERRORS(input_list):
    err_list=[]

    if input_list!=[]:
        input_list=sorted(input_list,key=lambda inter:inter[0], reverse=False)

        err_st=input_list[0][0]
        err_end=input_list[0][1]

        for entry in input_list[1:]:
            en_st=entry[0]
            en_end=entry[1]

            if en_st >=err_st and en_st<=err_end:
                if en_end>err_end:
                    err_end=en_end
            else:
               err_list.append([err_st,err_end])

               err_st=en_st
               err_end=en_end
        err_list.append([err_st,err_end])
               
  
    return err_list

        
def FIND_ERRORS(read_groups_dict, asmb_seq_dict,read_length):

    for ref_name in read_groups_dict.keys(): 
        
        raw_intervals=FIND_BREAKPOINTS(read_groups_dict[ref_name]['Single_forward'],
                                                                read_groups_dict[ref_name]['Single_Multiple_s'],
                                                                read_groups_dict[ref_name]['Multiple_Single_m'],
                                                                read_groups_dict[ref_name]['Multiple_forward'],
                                                                asmb_seq_dict[ref_name])

        read_groups_dict[ref_name]['single_forward:single_multiple_s']=raw_intervals['single:single_mult']
        read_groups_dict[ref_name]['single_multiple_s:multiple_forward']=raw_intervals['single_mult:mult']
        read_groups_dict[ref_name]['multiple_forward:multiple_single_m']=raw_intervals['mult:mult_single']
        read_groups_dict[ref_name]['multiple_single_m:single_forward']=raw_intervals['mult_single:single']
        read_groups_dict[ref_name]['breakpoints_forward']=raw_intervals['breakpoints']


        
        
        raw_intervals=FIND_BREAKPOINTS(read_groups_dict[ref_name]['Single_reverse'],
                                                                read_groups_dict[ref_name]['Single_Multiple_m'],
                                                                read_groups_dict[ref_name]['Multiple_Single_s'],
                                                                read_groups_dict[ref_name]['Multiple_reverse'],
                                                                asmb_seq_dict[ref_name])

        read_groups_dict[ref_name]['single_reverse:single_multiple_m']=raw_intervals['single:single_mult']
        read_groups_dict[ref_name]['single_multiple_m:multiple_reverse']=raw_intervals['single_mult:mult']
        read_groups_dict[ref_name]['multiple_reverse:multiple_single_s']=raw_intervals['mult:mult_single']
        read_groups_dict[ref_name]['multiple_single_s:single_reverse']=raw_intervals['mult_single:single']
        read_groups_dict[ref_name]['breakpoints_reverse']=raw_intervals['breakpoints']

        read_groups_dict[ref_name]['breakpoints']=MERGE_BREAKPOINTS(read_groups_dict[ref_name]['breakpoints_forward'],read_groups_dict[ref_name]['breakpoints_reverse'])

        
        if read_groups_dict[ref_name]['breakpoints']!=[]:
            if read_groups_dict[ref_name]['breakpoints'][-1][1]<=asmb_seq_dict[ref_name] and read_groups_dict[ref_name]['breakpoints'][-1][1]>=asmb_seq_dict[ref_name]-read_length:
                read_groups_dict[ref_name]['breakpoints'].pop(-1)

        if read_groups_dict[ref_name]['breakpoints']!=[]:
            if read_groups_dict[ref_name]['breakpoints'][0][0]>=1 and read_groups_dict[ref_name]['breakpoints'][0][0]<=read_length:
                read_groups_dict[ref_name]['breakpoints'].pop(0)
        

    return read_groups_dict
   

