# copyright (c) 2017 Ksenia Khelik
#
# This Source Code Form is subject to the 
# terms of the Mozilla Public License, v. 2.0. 
# If a copy of the MPL was not distributed 
# with this file, You can obtain one at 
# https://mozilla.org/MPL/2.0/.
#
#-------------------------------------------------------------------------------


def PARSE_CIGAR_CLIP_LEN(cigar):

    
    if 'S' in cigar or 'H' in cigar:
        len_clip_st=0
        num_simb=''

        for i in range(len( cigar)):
            if cigar[i] in '0123456789':
                num_simb+=cigar[i]
            elif cigar[i] in 'SH':
              len_clip_st+=int(num_simb)
              num_simb=''
            else:
                clip_part=i
                break

        len_clip_end=0
        num_simb=''
        for i in range(i,len(cigar)):
            if cigar[i] in '0123456789':
                num_simb+=cigar[i]
            elif cigar[i] in 'SH':
              len_clip_end+=int(num_simb)
              num_simb=''
            else:
                num_simb=''
         
            
    else:
        len_clip_st=0
        len_clip_end=0

    
    return len_clip_st, len_clip_end



def FIND_END_POSITION(ref_st, cigar):

    ref_end=ref_st
    numb=''
    for i in range(len(cigar)):
        if cigar[i] in '0123456789':
            numb+=cigar[i]

        else:
            if cigar[i] in 'MS':
                j=i+1
                break
            else:
                print cigar[i]
                print 'ERROR: unknown simbol in the beginning of the sigar string'

    if cigar[i]!='S':
        ref_end+=int(numb)

    if j!=len(cigar):
        numb=''

        for i in range(j, len(cigar)):
            if cigar[i] in '0123456789':
                numb+=cigar[i]

            else:
                if cigar[i] in 'MD':
                    ref_end+=int(numb)
                
                numb=''

        

    return ref_end-1


def FIND_LINE(temp):

    read_name=temp[0].split('/')[0]
    map_flag=int(temp[1])
    ref_name=temp[2]
    ref_st=int(temp[3])
    cigar=temp[5]
    qual_ascii_33=temp[10]

    map_flag_dict={0:1, 256:1, 16:-1, 272:-1, 4:0}

                
    if map_flag!=4:

                    for i in range(11,len(temp)):
                        if temp[i].startswith('NM'):
                            nm=int(temp[i][5:])
                    
                    
                    ref_end=FIND_END_POSITION(ref_st, cigar)
                    len_clip_st,len_clip_end=PARSE_CIGAR_CLIP_LEN(cigar)
                    read_st=len_clip_st+1
                    read_end=len(qual_ascii_33)-len_clip_end
                    
    else:
                    nm=-1
                    ref_end='*'
                    read_st='*'
                    read_end='*'


    return [map_flag_dict[map_flag],ref_name,ref_st,ref_end,read_st, read_end, cigar,nm,qual_ascii_33]
