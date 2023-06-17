import os
import json
import openai
import re
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from random import randrange
import random

#random.seed(42)

"""
Old generator, for basic move,fill,fmove,tasks based on basic tasks (e.g. bfill_3), and the arcfill reduction series.
"""

# Quick generator functions for 1d tasks, and some 2d-from-1d tasks
class Generator:
    max_digits = 9
    back_ground = 0

    def __init__(self, max_len):
        self.max_seq_len = max_len
        self.gen_type_map = {'bfill': self.gen_fill_single_hole_pair,
                        'bmove': self.gen_move_single_bar_pair
                    }

    def helper_gen_arcfill_1d_row(self, obj_num, pat_len, pivot_color, filling_color, trim_flag=False):
        """
        Basic, reduced from ARC #a699fb00, a sequence of same size "holes" to fill
        This helper func generates a row of ARC-like 1d rows
        """
        # seqlen should be pattern objects with gaps
        # initial indent
        if trim_flag:
            indent_gap = 0
        else:
            indent_gap = randrange(2,4)
        input,output = [self.back_ground]*indent_gap,[self.back_ground]*indent_gap
        for pat_i in range(obj_num):
            # number of repeated fill patterns
            if obj_num>1:
                pat_num = randrange(1,3)
            else:
                pat_num = randrange(1,5)
            # pattern gap length
            pat_gap = randrange(pat_len+1,pat_len+4)
            if trim_flag and pat_i==obj_num-1:
                pat_gap=0
            # the whole sub-sequence
            sub_seq_len = pat_len*pat_num + 1 + pat_gap

            # build sub-seq
            sub_input,sub_output = [self.back_ground]*sub_seq_len,[self.back_ground]*sub_seq_len
            for i in range(pat_num+1):
                sub_input[pat_len*i]=pivot_color
                sub_output[pat_len*i]=pivot_color
                if(i<pat_num):
                    for j in range(1,pat_len):
                        sub_output[pat_len*i+j]=filling_color

            # pile them up
            input += sub_input
            output += sub_output

        return input, output

    def check_dup(self, train_set, t_input):
        """
        Helper function that checks duplicate of training, test sets
        """
        for tr_pair in train_set:
            print("Check dup:")
            print("t_input :",t_input)
            print("training:",tr_pair["input"])
            if t_input == tr_pair["input"]:
                return True

        return False

    def gen_arcfill_1d_pair(self, filepath, obj_num=1, trim_flag=False):
        """
        Basic, reduced from ARC #a699fb00, a sequence of same size "holes" to fill
        obj_num: number of patterns to include
        trim_flag: whether include margins
        """
        # determine colors
        pivot_color = randrange(1,self.max_digits-1)
        filling_color = randrange(1,self.max_digits)
        if filling_color == pivot_color:
            filling_color = pivot_color+1

        # fill pattern length
        pat_len = randrange(2,4)
        
        # make json
        json_str = {}
        # Generate 3 training set
        json_str["train"]=[]
        for i in range(3):
            input, output = self.helper_gen_arcfill_1d_row(obj_num, pat_len, pivot_color, filling_color, trim_flag)
            while( self.check_dup(json_str["train"], [input]) ):
                input, output = self.helper_gen_arcfill_1d_row(obj_num, pat_len, pivot_color, filling_color, trim_flag)
            print(input)
            print(output)
            json_str["train"].append({"input":[input],"output":[output]})

        t_input, t_output = self.helper_gen_arcfill_1d_row(obj_num, pat_len, pivot_color, filling_color, trim_flag)
        while( self.check_dup(json_str["train"], [t_input]) ):
            t_input, t_output = self.helper_gen_arcfill_1d_row(obj_num, pat_len, pivot_color, filling_color, trim_flag)
        print(t_input)
        print(t_output)
            
        json_str["test"]=[{"input":[t_input],"output":[t_output]}]

        print(json_str)
        with open(filepath, 'w') as f:
            json.dump(json_str, f)

    def helper_trim_1d(self, row):
        """
        Trim a 1d sequence, remove begin and trailing background pixels
        """
        start,end=-1,-1
        for idx,v in enumerate(row):
            if v!=self.back_ground and start==-1:
                start = idx

        for idx,v in enumerate(row[::-1]):
            if v!=self.back_ground and end==-1:
                end = idx

        if end==-1:
            end = len(row)
        else:
            end = len(row)-end

        if start==-1:
            start = 0

        return row[start:end]

    def helper_add_padding(self,demo):
        print(demo['input'])
        print(demo['output'])
        left_pad = [self.back_ground]*randrange(1,4)
        right_pad = [self.back_ground]*randrange(1,4)
        demo['input'][0] = left_pad+demo['input'][0]+right_pad
        demo['output'][0] = left_pad+demo['output'][0]+right_pad
        print(demo['input'])
        print(demo['output'])

        return demo


    # Construct 1d tasks from the arcfill 1d trimed tasks
    # By adding padding background pixels
    def gen_arcfill_1d_padding(self,type_1d="single"):
        if type_1d=="single":
            load_path="../dataset/1d_tasks/arcfill_1d_single_trim/"
        else:
            load_path="../dataset/1d_tasks/arcfill_1d_mult_trim/"

        for entry in os.scandir(load_path):
            task_1d = json.load(open(entry.path))
            # trim 1d sequences
            for demo in task_1d['train']:
                demo = self.helper_add_padding(demo)
            for demo_t in task_1d['test']:
                demo_t = self.helper_add_padding(demo_t)

            print(task_1d)
            if type_1d=="single":
                filepath = os.path.basename(entry.path).replace("arc1st_","arc1s_")
                filepath = "../dataset/1d_tasks/arcfill_1d_single/"+filepath
            else:
                filepath = os.path.basename(entry.path).replace("arc1mt_","arc1m_")
                filepath = "../dataset/1d_tasks/arcfill_1d_mult/"+filepath

            print(filepath)
            with open(filepath, 'w') as f:
                    json.dump(task_1d, f)

            #break


    # Construct 2d tasks from the arcfill 1d tasks
    # By adding two blank rows on top and bottom, so it's still 1 object
    def gen_arcfill_1d_to_2d_basic(self, type_1d="single"):
        if type_1d=="single":
            load_path="../dataset/1d_tasks/arcfill_1d_single/"
        else:
            load_path="../dataset/1d_tasks/arcfill_1d_mult/"

        for entry in os.scandir(load_path):
        #for entry in os.scandir("../dataset/1d_tasks/arcfill_1d_single/"):
            task_1d = json.load(open(entry.path))
            # trim 1d sequences
            for demo in task_1d['train']:
                print(demo['input'])
                print(demo['output'])

                blank_row = [self.back_ground]*len(demo['input'][0])
                demo['input'] = [blank_row]+demo['input']+[blank_row]
                demo['output'] = [blank_row]+demo['output']+[blank_row]

                print(demo['input'])
                print(demo['output'])
            for demo_t in task_1d['test']:
                blank_row = [self.back_ground]*len(demo_t['input'][0])
                demo_t['input'] = [blank_row]+demo_t['input']+[blank_row]
                demo_t['output'] = [blank_row]+demo_t['output']+[blank_row]

                print(demo_t['input'])

            print(task_1d)
            if type_1d=="single":
                filepath = os.path.basename(entry.path).replace("arc1s_","arc2s_")
                filepath = "../dataset/1d_tasks/arcfill_2d_single_basic/"+filepath
            else:
                filepath = os.path.basename(entry.path).replace("arc1m_","arc2m_")
                filepath = "../dataset/1d_tasks/arcfill_2d_mult_basic/"+filepath

            print(filepath)
            with open(filepath, 'w') as f:
                    json.dump(task_1d, f)

            #break

    def helper_arcfill_1d_to_2d_basic(self, demo, max_row_len, max_obj_num=1):
            print(demo['input'])
            print(demo['output'])

            # retrieve demo colors and fill pattern length
            pc_flag, fc_flag = True, True
            start,end,pat_len,filling_color,pivot_color=0,0,-1,0,0
            for idx, i in enumerate(demo['output'][0]):
                if i!=self.back_ground and pc_flag:
                    pivot_color = i
                    pc_flag=False
                    start=idx
                elif i!=self.back_ground and not pc_flag and fc_flag:
                    #print("here:",idx,i)
                    filling_color = i
                    fc_flag = False

                if not pc_flag and not fc_flag and i==pivot_color and pat_len==-1:
                    end=idx
                    pat_len = end-start

            print(pivot_color, filling_color, pat_len)
            if max_obj_num > 1:
                obj_num=randrange(1,max_obj_num)
                # Determine how many rows will contain objects
                # Smaller grids due to GPT 4097 tokens limit 
                obj_rows_cnt = randrange(2,3)
            else:
                obj_num=1
                obj_rows_cnt = randrange(2,4)

            # Generate rows with objects
            obj_rows=[]
            for obj_i in range(obj_rows_cnt):
                input, output = self.helper_gen_arcfill_1d_row(obj_num, pat_len, pivot_color, filling_color)
                obj_rows.append((input,output))
                if len(input)>max_row_len:
                    max_row_len=len(input)

            return obj_rows, max_row_len 


    def helper_assemble_2d_basic(self, demo, obj_rows, max_row_len, max_obj_num=1 ):
            blank_row = [self.back_ground]*max_row_len

            # Fill blanks to make the width matches the new 2d grid
            demo['input'][0] = [self.back_ground]*(max_row_len - len(demo['input'][0])) + demo['input'][0]
            demo['output'][0] = [self.back_ground]*(max_row_len - len(demo['output'][0])) + demo['output'][0]

            # Original in/out pair as our first object row
            demo['input'] = [blank_row]+demo['input']
            demo['output'] = [blank_row]+demo['output']

            for (input, output) in obj_rows:
                # Fill blanks to make the width matches the new 2d grid
                full_input = [self.back_ground]*(max_row_len - len(input)) + input
                full_output = [self.back_ground]*(max_row_len - len(output)) + output

                # 0,1 or 2 rows of blanks
                if max_obj_num>1:
                    num_blank_rows = randrange(2)
                else:
                    num_blank_rows = randrange(3)
                demo['input'] += [blank_row]*num_blank_rows + [full_input]
                demo['output'] += [blank_row]*num_blank_rows + [full_output]

            print(demo['input'])
            print(demo['output'])

            return demo

    def helper_1d_to_2d_mrows(self,max_obj_num,task_1d):
        max_row_len=0
        for demo in task_1d['train']:
            if len(demo['input'][0])>max_row_len:
                max_row_len=len(demo['input'][0])
        for demo_t in task_1d['test']:
            if len(demo_t['input'][0])>max_row_len:
                max_row_len=len(demo_t['input'][0])

        # trim 1d sequences
        for demo in task_1d['train']:
            obj_rows, max_row_len = self.helper_arcfill_1d_to_2d_basic(demo, max_row_len, max_obj_num)
        for demo_t in task_1d['test']:
            obj_rows_t, max_row_len = self.helper_arcfill_1d_to_2d_basic(demo_t, max_row_len, max_obj_num)

        # assemble
        for demo in task_1d['train']:
            demo = self.helper_assemble_2d_basic(demo, obj_rows, max_row_len, max_obj_num)
        for demo_t in task_1d['test']:
            demo_t = self.helper_assemble_2d_basic(demo_t, obj_rows_t, max_row_len, max_obj_num)

        return task_1d

    def check_dup_2d(self, task_1d):
        input_list = []
        for demo in task_1d['train']:
            if demo['input'] in input_list:
                return True
            input_list.append(demo['input'])

        for demo_t in task_1d['test']:
            if demo_t['input'] in input_list:
                return True
            input_list.append(demo_t['input'])

        return False
            

    # Construct 2d tasks from the arcfill 1d tasks
    # This time it's more like the ARC one, 1 single object per row, or multi objs per row, and random [3,5] rows will contain an object
    def gen_arcfill_1d_to_2d_mrows(self, max_obj_num=1):
        if max_obj_num>1:
            load_path = "../dataset/1d_tasks/arcfill_1d_mult/"
        else:
            load_path = "../dataset/1d_tasks/arcfill_1d_single/"

        for entry in os.scandir(load_path):
            task_1d = json.load(open(entry.path))

            task_1d = self.helper_1d_to_2d_mrows(max_obj_num,task_1d)
            while( self.check_dup_2d(task_1d) ):
                task_1d = self.helper_1d_to_2d_mrows(max_obj_num,task_1d)

            print(task_1d)

            if max_obj_num>1:
                filepath = os.path.basename(entry.path).replace("arc1m_","arc2mmr_")
                filepath = "../dataset/1d_tasks/arcfill_2d_mult_mrows/"+filepath
            else:
                filepath = os.path.basename(entry.path).replace("arc1s_","arc2smr_")
                filepath = "../dataset/1d_tasks/arcfill_2d_single_mrows/"+filepath

            print(filepath)
            with open(filepath, 'w') as f:
                    json.dump(task_1d, f)
            #break


    def helper_2d_cropper(self,demo):
        print(demo['input'])
        print(demo['output'])
        # crop based on output is the safest
        # measure the paddings
        crop_rows=[]
        left_crop, right_crop = 100,100
        top_crop_flag, bottom_crop_flag=True, True
        for r_idx, row in enumerate(demo['output']):
            if row.count(self.back_ground)==len(row) and len(row)>0 and top_crop_flag:
                # A blank row, and at top/bot padding
                crop_rows.append(r_idx)
            else:
                top_crop_flag=False

            r_start,r_end=100,100
            for c_idx, v in enumerate(row):
                if v!=self.back_ground and r_start==100:
                    r_start=c_idx

            for c_idx,v in enumerate(row[::-1]):
                if v!=self.back_ground and r_end==100:
                    r_end=c_idx

            left_crop=min(left_crop,r_start)
            right_crop=min(right_crop,r_end)

        row_len = len(demo['output'])
        for r_idx, row in enumerate(demo['output'][::-1]):
            if row.count(self.back_ground)==len(row) and len(row)>0 and bottom_crop_flag:
                # A blank row, and at top/bot padding
                crop_rows.append(row_len-r_idx-1)
            else:
                bottom_crop_flag=False

        # actual cropping
        for c_i in crop_rows:
            demo['input'].pop(c_i)
            demo['output'].pop(c_i)
        
        for r_i, row in enumerate(demo['input']):
            crop_end = len(row)-right_crop
            demo['input'][r_i]=row[left_crop:crop_end]

        for r_i, row in enumerate(demo['output']):
            crop_end = len(row)-right_crop
            demo['output'][r_i]=row[left_crop:crop_end]

        print(demo['input'])
        print(demo['output'])

        return demo


    # Construct 2d tasks from the arcfill 2d tasks
    # By cropping the surrounding backgound pixels
    def gen_arcfill_2d_mrows_crop(self, type_1d="single"):
        if type_1d=="single":
            load_path="../dataset/1d_tasks/arcfill_2d_single_mrows/"
        else:
            load_path="../dataset/1d_tasks/arcfill_2d_mult_mrows/"

        for entry in os.scandir(load_path):
            task_1d = json.load(open(entry.path))
            # crop 1d grids
            for demo in task_1d['train']:
                demo = self.helper_2d_cropper(demo)

            for demo_t in task_1d['test']:
                demo_t = self.helper_2d_cropper(demo_t)

            print(task_1d)
            if type_1d=="single":
                filepath = os.path.basename(entry.path).replace("arc2smr_","arc2smrc_")
                filepath = "../dataset/1d_tasks/arcfill_2d_single_mrows_crop/"+filepath
            else:
                filepath = os.path.basename(entry.path).replace("arc2mmr_","arc2mmrc_")
                filepath = "../dataset/1d_tasks/arcfill_2d_mult_mrows_crop/"+filepath

            print(filepath)
            with open(filepath, 'w') as f:
                    json.dump(task_1d, f)

            #break

    def helper_array_rotate(self,array_2d):
        list_of_tuples = zip(*array_2d[::-1])
        return [list(elem) for elem in list_of_tuples]

    def helper_to_vertical(self,demo):
        print(demo['input'])
        print(demo['output'])

        # Rotate
        demo['input'] = self.helper_array_rotate(demo['input'])
        demo['output'] = self.helper_array_rotate(demo['output'])

        print(demo['input'])
        print(demo['output'])

        return demo

    def gen_vertical_versions(self,load_path,new_path,file_prefix):
        for entry in os.scandir(load_path):
            task_1d = json.load(open(entry.path))
            # get 1d or 2d grids
            for demo in task_1d['train']:
                demo = self.helper_to_vertical(demo)

            for demo_t in task_1d['test']:
                demo_t = self.helper_to_vertical(demo_t)

            print(task_1d)
            filepath = os.path.basename(entry.path).replace(file_prefix,file_prefix+"_v")
            filepath = new_path+filepath

            print(filepath)
            with open(filepath, 'w') as f:
                    json.dump(task_1d, f)

    def gen_reverse_versions(self,load_path,new_path,file_prefix):
        for entry in os.scandir(load_path):
            task_1d = json.load(open(entry.path))
            # get 1d or 2d grids
            for demo in task_1d['train']:
                temp = demo['input']
                demo['input'] = demo['output']
                demo['output'] = temp

            for demo_t in task_1d['test']:
                temp = demo_t['input']
                demo_t['input'] = demo_t['output']
                demo_t['output'] = temp

            print(task_1d)
            filepath = os.path.basename(entry.path).replace(file_prefix,file_prefix+"_r")
            filepath = new_path+filepath

            print(filepath)
            with open(filepath, 'w') as f:
                    json.dump(task_1d, f)


    def gen_fill_single_hole_pair(self, seq_len, min_hole_len=1):
        """
        Basic, fill a single hole in 1D
        """
        # seqlen - 2 (pivots) - 3 (space for future move task)
        hole_len = randrange(min_hole_len, seq_len - 2 - 3) 
        hole_start = randrange(seq_len - hole_len - 2)
        hole_end = hole_start + hole_len + 1
        #print(seq_len, hole_len, hole_start, hole_end)

        pivot_pt = randrange(1,self.max_digits)
        filling_color = pivot_pt
        #filling_color = randrange(1,self.max_digits)
        #if filling_color == pivot_pt:
        #    filling_color = pivot_pt+1

        input,output = [self.back_ground]*seq_len,[self.back_ground]*seq_len
        input[hole_start]=pivot_pt
        input[hole_end]=pivot_pt

        output[hole_start]=pivot_pt
        for i in range(hole_start+1,hole_end):
            output[i]=filling_color
        output[hole_end]=pivot_pt

        return input, output

    def gen_move_single_bar_pair(self, seq_len, move_len=3, min_bar_len=3):
        """
        Basic, move all single objs (bar) for a fixed move_len in 1D
        """
        bar_len = randrange(min_bar_len, seq_len - move_len) 
        bar_start = randrange(seq_len - bar_len - move_len)
        #move_len = randrange(min_move,seq_len - bar_len - bar_start)
        print(seq_len, bar_len, bar_start, move_len)

        filling_color = randrange(1,self.max_digits)

        input,output = [self.back_ground]*seq_len,[self.back_ground]*seq_len
        for i in range(bar_start,bar_start+bar_len):
            input[i]=filling_color

        for j in range(bar_start+move_len,bar_start+bar_len+move_len):
            output[j]=filling_color

        return input, output

    def gen_json(self, filepath, gen_type="bfill"):
        seq_len = randrange(8,self.max_seq_len)
        json_str = {}
        # Generate 3 training set
        json_str["train"]=[]
        for i in range(3):
            input, output = self.gen_type_map[gen_type](seq_len)
            json_str["train"].append({"input":[input],"output":[output]})

        input, output = self.gen_type_map[gen_type](seq_len)
        json_str["test"]=[{"input":[input],"output":[output]}]

        print(input)
        print(output)
        print(json_str)
        with open(filepath, 'w') as f:
            json.dump(json_str, f)

    def helper_hole_cutter(self, input_l):
        start,end=-1,-1
        for idx,v in enumerate(input_l):
            if v!=0 and start==-1:
                start=idx
            if start!=-1 and v==0 and end==-1:
                end=idx-1
        print("\n",start,end)
        print(input_l)

        
        for i in range(start+1,end):
            input_l[i]=0


    # Construct 2-step 1d tasks from the bmove tasks
    # We cut holes in the bars just as bfill tasks, so the solver need to fill-in and move the bars
    def gen_fill_then_move(self):
        for entry in os.scandir("../dataset/1d_tasks/basic_move/"):
            task_1d = json.load(open(entry.path))
            # make holes in input
            for demo in task_1d['train']:
                self.helper_hole_cutter(demo['input'][0])
                print(demo['input'][0])
            for demo_t in task_1d['test']:
                self.helper_hole_cutter(demo_t['input'][0])
                print(demo_t['input'][0])

            print(task_1d)
            filepath = os.path.basename(entry.path).replace("bmove","fmove")
            print(filepath)
            with open("../dataset/1d_tasks/fill_n_move/"+filepath, 'w') as f:
                json.dump(task_1d, f)
            
            #break

    # Construct 2d tasks from the bfill tasks
    # Basically, we stack one more row on top of the original 1d task
    def gen_2dfill(self):
        for entry in os.scandir("../dataset/1d_tasks/basic_fill/"):
            task_1d = json.load(open(entry.path))
            # make holes in input
            for demo in task_1d['train']:
                demo['input'].append(demo['input'][0])
                demo['output'].append(demo['output'][0])
                print(demo['input'])
            for demo_t in task_1d['test']:
                demo_t['input'].append(demo_t['input'][0])
                demo_t['output'].append(demo_t['output'][0])
                print(demo_t['input'][0])

            print(task_1d)
            filepath = os.path.basename(entry.path).replace("bfill","2dfill")
            print(filepath)
            with open("../dataset/1d_tasks/2d_fill/"+filepath, 'w') as f:
                json.dump(task_1d, f)
            
            #break
        
    # Construct 1d tasks from the 2dfill tasks
    # 2dfill's two rows are now appended to be one row
    def gen_2d1dfill(self):
        for entry in os.scandir("../dataset/1d_tasks/basic_fill/"):
            task_1d = json.load(open(entry.path))
            # make holes in input
            for demo in task_1d['train']:
                demo['input'][0] = demo['input'][0] + demo['input'][0]
                demo['output'][0] = demo['output'][0] + demo['output'][0]
                print(demo['input'])
            for demo_t in task_1d['test']:
                demo_t['input'][0] = demo_t['input'][0] + demo_t['input'][0]
                demo_t['output'][0] = demo_t['output'][0] + demo_t['output'][0]
                print(demo_t['input'])

            print(task_1d)
            filepath = os.path.basename(entry.path).replace("bfill","2d1dfill")
            print(filepath)
            with open("../dataset/1d_tasks/2d1d_fill/"+filepath, 'w') as f:
                    json.dump(task_1d, f)
            
            #break

    # Construct 1d tasks from the bfill tasks
    # Bfill expand to x3
    def gen_bfill_three(self):
        for entry in os.scandir("../dataset/1d_tasks/basic_fill/"):
            task_1d = json.load(open(entry.path))
            # make holes in input
            for demo in task_1d['train']:
                demo['input'][0] = demo['input'][0] + demo['input'][0] + demo['input'][0]
                demo['output'][0] = demo['output'][0] + demo['output'][0] + demo['output'][0]
                print(demo['input'])
            for demo_t in task_1d['test']:
                demo_t['input'][0] = demo_t['input'][0] + demo_t['input'][0] + demo_t['input'][0]
                demo_t['output'][0] = demo_t['output'][0] + demo_t['output'][0] + demo_t['output'][0]
                print(demo_t['input'])

            print(task_1d)
            filepath = os.path.basename(entry.path).replace("bfill","bfill_3")
            print(filepath)
            with open("../dataset/1d_tasks/basic_fill_3/"+filepath, 'w') as f:
                    json.dump(task_1d, f)
            
            #break

    # Construct 1d tasks from the bfill tasks
    # Bfill expand to x3, but only keep the middle part
    def gen_bfill_three_mid(self):
        for entry in os.scandir("../dataset/1d_tasks/basic_fill/"):
            task_1d = json.load(open(entry.path))
            # make holes in input
            for demo in task_1d['train']:
                blank_block = [self.back_ground]*len(demo['input'][0])
                demo['input'][0] = blank_block + demo['input'][0] + blank_block
                demo['output'][0] = blank_block + demo['output'][0] + blank_block
                print(demo['input'])
            for demo_t in task_1d['test']:
                blank_block = [self.back_ground]*len(demo_t['input'][0])
                demo_t['input'][0] = blank_block + demo_t['input'][0] + blank_block
                demo_t['output'][0] = blank_block + demo_t['output'][0] + blank_block
                print(demo_t['input'])

            print(task_1d)
            filepath = os.path.basename(entry.path).replace("bfill","bfill_3m")
            print(filepath)
            with open("../dataset/1d_tasks/basic_fill_3_m/"+filepath, 'w') as f:
                    json.dump(task_1d, f)
            
            #break

    # Construct 1d tasks from the bfill tasks
    # Bfill expand to x3, but only keep the left part
    def gen_bfill_three_left(self):
        for entry in os.scandir("../dataset/1d_tasks/basic_fill/"):
            task_1d = json.load(open(entry.path))
            # make holes in input
            for demo in task_1d['train']:
                blank_block = [self.back_ground]*len(demo['input'][0])
                demo['input'][0] = demo['input'][0] + blank_block + blank_block
                demo['output'][0] = demo['output'][0] + blank_block + blank_block
                print(demo['input'])
            for demo_t in task_1d['test']:
                blank_block = [self.back_ground]*len(demo_t['input'][0])
                demo_t['input'][0] = demo_t['input'][0] + blank_block + blank_block
                demo_t['output'][0] = demo_t['output'][0] + blank_block + blank_block
                print(demo_t['input'])

            print(task_1d)
            filepath = os.path.basename(entry.path).replace("bfill","bfill_3l")
            print(filepath)
            with open("../dataset/1d_tasks/basic_fill_3_l/"+filepath, 'w') as f:
                    json.dump(task_1d, f)
            
            #break

    # Construct 1d tasks from the bfill tasks
    # Bfill expand to x3, but only keep the right part
    def gen_bfill_three_right(self):
        for entry in os.scandir("../dataset/1d_tasks/basic_fill/"):
            task_1d = json.load(open(entry.path))
            # make holes in input
            for demo in task_1d['train']:
                blank_block = [self.back_ground]*len(demo['input'][0])
                demo['input'][0] = blank_block + blank_block + demo['input'][0]
                demo['output'][0] = blank_block + blank_block + demo['output'][0]
                print(demo['input'])
            for demo_t in task_1d['test']:
                blank_block = [self.back_ground]*len(demo_t['input'][0])
                demo_t['input'][0] = blank_block + blank_block + demo_t['input'][0]
                demo_t['output'][0] = blank_block + blank_block + demo_t['output'][0]
                print(demo_t['input'])

            print(task_1d)
            filepath = os.path.basename(entry.path).replace("bfill","bfill_3r")
            print(filepath)
            with open("../dataset/1d_tasks/basic_fill_3_r/"+filepath, 'w') as f:
                    json.dump(task_1d, f)
            
            #break

    # Construct 1d tasks from the bfill tasks
    # Bfill expand to x3, but only keep the first start pixel and the last end pixel
    def gen_bfill_three_full(self):
        for entry in os.scandir("../dataset/1d_tasks/basic_fill/"):
            task_1d = json.load(open(entry.path))
            # make holes in input
            for demo in task_1d['train']:
                start,end,fill_color = self.helper_get_bar_info(demo['output'][0])
                print(start,end,fill_color)
                seq_len = len(demo['input'][0])
                demo['input'][0] = [self.back_ground]*(seq_len*3)
                demo['output'][0] = [self.back_ground]*(seq_len*3)

                demo['input'][0][start]=fill_color
                demo['input'][0][seq_len*2+end-1]=fill_color
                for i in range(start,seq_len*2+end ):
                    demo['output'][0][i]=fill_color

                print(demo['input'])

            for demo in task_1d['test']:
                start,end,fill_color = self.helper_get_bar_info(demo['output'][0])
                print(start,end,fill_color)
                seq_len = len(demo['input'][0])
                demo['input'][0] = [self.back_ground]*(seq_len*3)
                demo['output'][0] = [self.back_ground]*(seq_len*3)

                demo['input'][0][start]=fill_color
                demo['input'][0][seq_len*2+end-1]=fill_color
                for i in range(start,seq_len*2+end ):
                    demo['output'][0][i]=fill_color

                print(demo['input'])


            print(task_1d)
            filepath = os.path.basename(entry.path).replace("bfill","bfill_3f")
            print(filepath)
            with open("../dataset/1d_tasks/basic_fill_3_f/"+filepath, 'w') as f:
                    json.dump(task_1d, f)
            
            #break

    def helper_get_bar_info(self,grid):
        start,end,fill_color=-1,-1,0
        for idx, i in enumerate(grid):
            if i!=self.back_ground and start==-1:
                fill_color = i
                start=idx
            elif i==self.back_ground and start>-1 and end==-1:
                end=idx
        return start,end,fill_color


    # Construct 1d tasks from the bmove tasks
    # Now only moves 1 pixel to the right
    def gen_bmove_one(self):
        for entry in os.scandir("../dataset/1d_tasks/basic_move/"):
            task_1d = json.load(open(entry.path))
            # make holes in input
            for demo in task_1d['train']:
                print(demo['output'])
                start,end,fill_color = self.helper_get_bar_info(demo['output'][0])
                print(start,end,fill_color)
                for i in range(start-2,start):
                    demo['output'][0][i]=fill_color
                for i in range(end-2,end):
                    demo['output'][0][i]=self.back_ground

                print(demo['output'])

            for demo in task_1d['test']:
                print(demo['output'])
                start,end,fill_color = self.helper_get_bar_info(demo['output'][0])
                print(start,end,fill_color)
                for i in range(start-2,start):
                    demo['output'][0][i]=fill_color
                for i in range(end-2,end):
                    demo['output'][0][i]=self.back_ground

                print(demo['output'])

            print(task_1d)
            filepath = os.path.basename(entry.path).replace("bmove","bmove_1p")
            print(filepath)
            with open("../dataset/1d_tasks/basic_move_1/"+filepath, 'w') as f:
                    json.dump(task_1d, f)


    # Construct 1d tasks from the bmove tasks
    # Now only moves 2 pixel to the right
    def gen_bmove_two(self):
        for entry in os.scandir("../dataset/1d_tasks/basic_move/"):
            task_1d = json.load(open(entry.path))
            # make holes in input
            for demo in task_1d['train']:
                print(demo['output'])
                start,end,fill_color = self.helper_get_bar_info(demo['output'][0])
                print(start,end,fill_color)
                for i in range(start-1,start):
                    demo['output'][0][i]=fill_color
                for i in range(end-1,end):
                    demo['output'][0][i]=self.back_ground

                print(demo['output'])

            for demo in task_1d['test']:
                print(demo['output'])
                start,end,fill_color = self.helper_get_bar_info(demo['output'][0])
                print(start,end,fill_color)
                for i in range(start-1,start):
                    demo['output'][0][i]=fill_color
                for i in range(end-1,end):
                    demo['output'][0][i]=self.back_ground

                print(demo['output'])

            print(task_1d)
            filepath = os.path.basename(entry.path).replace("bmove","bmove_2p")
            print(filepath)
            with open("../dataset/1d_tasks/basic_move_2/"+filepath, 'w') as f:
                    json.dump(task_1d, f)

    # Construct 1d tasks from the bmove tasks
    # Now move to a pixel instead of fix length
    def gen_bmove_to_pixel(self, relist=[]):
        for entry in os.scandir("../dataset/1d_tasks/basic_move/"):
            task_1d = json.load(open(entry.path))
            
            task_id_num_f = os.path.basename(entry.path).split("_")[-1]
            task_id_num = int(task_id_num_f.split(".")[0])

            if relist and task_id_num not in relist:
                continue

            print(task_id_num)
            #break

            bar_colors = []
            for demo in task_1d['train']:
                start,end,fill_color = self.helper_get_bar_info(demo['output'][0])
                bar_colors.append(fill_color)
            for demo in task_1d['test']:
                start,end,fill_color = self.helper_get_bar_info(demo['output'][0])
                bar_colors.append(fill_color)

            pivot_colors = list( set(range(1,self.max_digits+1)) - set(bar_colors) )
            pivot_color = random.choice(pivot_colors)
            print(pivot_color)

            # check colors in input
            for demo in task_1d['train']:
                print(demo['output'])
                start,end,fill_color = self.helper_get_bar_info(demo['input'][0])
                print(start,end,fill_color)
                seq_len = len(demo['output'][0])
                pivot_pos = randrange(end+2,seq_len)

                for i in range(len(demo['output'][0])):
                    demo['output'][0][i]=self.back_ground

                demo['input'][0][pivot_pos]=pivot_color
                demo['output'][0][pivot_pos]=pivot_color
                for i in range(pivot_pos-(end-start),pivot_pos):
                    demo['output'][0][i]=fill_color

                print(demo['output'])

            for demo in task_1d['test']:
                print(demo['input'])
                print(demo['output'])
                start,end,fill_color = self.helper_get_bar_info(demo['input'][0])
                print(start,end,fill_color)
                seq_len = len(demo['output'][0])
                pivot_pos = randrange(end+2,seq_len)

                for i in range(len(demo['output'][0])):
                    demo['output'][0][i]=self.back_ground

                demo['input'][0][pivot_pos]=pivot_color
                demo['output'][0][pivot_pos]=pivot_color
                for i in range(pivot_pos-(end-start),pivot_pos):
                    demo['output'][0][i]=fill_color

                print(demo['input'])
                print(demo['output'])

            print(task_1d)
            filepath = os.path.basename(entry.path).replace("bmove","bmove_dp")
            print(filepath)

            with open("../dataset/1d_tasks/basic_move_dp/"+filepath, 'w') as f:
                    json.dump(task_1d, f)

            #break


    # Construct 1d tasks from the bmove tasks
    # Now move to 2 pixels right, but with a pixel indicating the move
    def gen_bmove_to_pixel_2(self, relist=[]):
        for entry in os.scandir("../dataset/1d_tasks/basic_move/"):
            task_1d = json.load(open(entry.path))

            task_id_num_f = os.path.basename(entry.path).split("_")[-1]
            task_id_num = int(task_id_num_f.split(".")[0])

            if relist and task_id_num not in relist:
                continue

            print(task_id_num)

            bar_colors = []
            for demo in task_1d['train']:
                start,end,fill_color = self.helper_get_bar_info(demo['output'][0])
                bar_colors.append(fill_color)
            for demo in task_1d['test']:
                start,end,fill_color = self.helper_get_bar_info(demo['output'][0])
                bar_colors.append(fill_color)

            pivot_colors = list( set(range(1,self.max_digits+1)) - set(bar_colors) )
            pivot_color = random.choice(pivot_colors)
            print(pivot_color)

            for demo in task_1d['train']:
                print(demo['output'])
                start,end,fill_color = self.helper_get_bar_info(demo['output'][0])
                print(start,end,fill_color)
                for i in range(start-1,start):
                    demo['output'][0][i]=fill_color

                demo['input'][0][end-1]=pivot_color
                demo['output'][0][end-1]=pivot_color

                print(demo['output'])

            for demo in task_1d['test']:
                print(demo['output'])
                start,end,fill_color = self.helper_get_bar_info(demo['output'][0])
                print(start,end,fill_color)
                for i in range(start-1,start):
                    demo['output'][0][i]=fill_color

                demo['input'][0][end-1]=pivot_color
                demo['output'][0][end-1]=pivot_color

                print(demo['output'])

            print(task_1d)
            filepath = os.path.basename(entry.path).replace("bmove","bmove_2p_p")
            print(filepath)

            with open("../dataset/1d_tasks/basic_move_2p_p/"+filepath, 'w') as f:
                    json.dump(task_1d, f)

            #break

    # Construct 1d tasks from the bmove dp tasks
    # Now extend to a pixel instead of move
    def gen_extend_to_pixel(self,relist=[]):
        for entry in os.scandir("../dataset/1d_tasks/basic_move/"):
            task_1d = json.load(open(entry.path))

            task_id_num_f = os.path.basename(entry.path).split("_")[-1]
            task_id_num = int(task_id_num_f.split(".")[0])

            if relist and task_id_num not in relist:
                continue

            print(task_id_num)

            bar_colors = []
            for demo in task_1d['train']:
                start,end,fill_color = self.helper_get_bar_info(demo['output'][0])
                bar_colors.append(fill_color)
            for demo in task_1d['test']:
                start,end,fill_color = self.helper_get_bar_info(demo['output'][0])
                bar_colors.append(fill_color)

            pivot_colors = list( set(range(1,self.max_digits+1)) - set(bar_colors) )
            pivot_color = random.choice(pivot_colors)
            print(pivot_color)

            # check colors in input
            for demo in task_1d['train']:
                print(demo['output'])
                start,end,fill_color = self.helper_get_bar_info(demo['input'][0])
                print(start,end,fill_color)
                seq_len = len(demo['output'][0])
                pivot_pos = randrange(end+2,seq_len)

                for i in range(len(demo['output'][0])):
                    demo['output'][0][i]=self.back_ground

                demo['input'][0][pivot_pos]=pivot_color
                demo['output'][0][pivot_pos]=pivot_color
                for i in range(start,pivot_pos):
                    demo['output'][0][i]=fill_color

                print(demo['output'])

            for demo in task_1d['test']:
                print(demo['input'])
                print(demo['output'])
                start,end,fill_color = self.helper_get_bar_info(demo['input'][0])
                print(start,end,fill_color)
                seq_len = len(demo['output'][0])
                pivot_pos = randrange(end+2,seq_len)

                for i in range(len(demo['output'][0])):
                    demo['output'][0][i]=self.back_ground

                demo['input'][0][pivot_pos]=pivot_color
                demo['output'][0][pivot_pos]=pivot_color
                for i in range(start,pivot_pos):
                    demo['output'][0][i]=fill_color

                print(demo['input'])
                print(demo['output'])

            print(task_1d)
            filepath = os.path.basename(entry.path).replace("bmove","1dscale_dp")
            print(filepath)

            with open("../dataset/1d_tasks/1d_scale_dp/"+filepath, 'w') as f:
                    json.dump(task_1d, f)

            #break

    # Construct 1d level-2 tasks from the bmove tasks
    # Now only moves 1 pixel to the right, and recolor
    # Need to check duplicates
    def gen_bmove_one_recolor(self):
        for entry in os.scandir("../dataset/1d_tasks/basic_move/"):
            task_1d = json.load(open(entry.path))
            ori_color = randrange(1,gen1.max_digits+1)
            other_colors = list(range(1,gen1.max_digits+1))
            other_colors.remove(ori_color)
            rep_color = random.choice(other_colors)

            # make holes in input
            for demo in task_1d['train'] + task_1d['test']:
                print(demo['output'])
                start,end,fill_color = self.helper_get_bar_info(demo['output'][0])
                print(start,end,fill_color)

                for i in range(len(demo['output'][0])):
                    demo['input'][0][i]=self.back_ground
                    demo['output'][0][i]=self.back_ground

                for i in range(start,end):
                    demo['input'][0][i]=ori_color
                for i in range(start+1,end+1):
                    demo['output'][0][i]=rep_color

                print(demo['output'])

            print(task_1d)
            filepath = os.path.basename(entry.path).replace("bmove","bmove_1p_rec")
            print(filepath)
            with open("../dataset/1d_tasks/basic_move_1_recolor/"+filepath, 'w') as f:
                    json.dump(task_1d, f)



gen1 = Generator(32) 
#for i in range(1,51):
#for i in range(50):
    # Basic tasks
    #gen1.gen_json(filepath="../dataset/1d_tasks/basic_move/bmove_"+str(i)+".json", gen_type="bmove")
    #gen1.gen_json(filepath="../dataset/1d_tasks/basic_fill/bfill_"+str(i)+".json", gen_type="bfill")
    #gen1.gen_arcfill_1d_pair(filepath="../dataset/1d_tasks/arcfill_1d_single/arc1s_"+str(i)+".json")
    #obj_num=randrange(2,4)
    #gen1.gen_arcfill_1d_pair(filepath="../dataset/1d_tasks/arcfill_1d_mult/arc1m_"+str(i)+".json", obj_num=obj_num)

    # Trimmed series
    #obj_num=1
    #obj_num=randrange(2,4)
    #gen1.gen_arcfill_1d_pair(filepath="../dataset/1d_tasks/arcfill_1d_single_trim/arc1st_"+str(i)+".json", obj_num=obj_num, trim_flag=True)
    #gen1.gen_arcfill_1d_pair(filepath="../dataset/1d_tasks/arcfill_1d_mult_trim/arc1mt_"+str(i)+".json", obj_num=obj_num, trim_flag=True)
    #break

# From basic tasks
#gen1.gen_fill_then_move()
#gen1.gen_2dfill()
#gen1.gen_2dfill()

# ARC fills
#gen1.gen_arcfill_1d_padding(type_1d="single")
#gen1.gen_arcfill_1d_padding(type_1d="mult")

#gen1.gen_arcfill_1d_to_2d_basic(type_1d="single")
#gen1.gen_arcfill_1d_to_2d_basic(type_1d="mult")

#gen1.gen_arcfill_1d_to_2d_mrows(max_obj_num=1)
#gen1.gen_arcfill_1d_to_2d_mrows(max_obj_num=3)

#gen1.gen_arcfill_2d_mrows_crop(type_1d="single")
#gen1.gen_arcfill_2d_mrows_crop(type_1d="mult")


# Vertical grids
#gen1.gen_vertical_versions(load_path="../dataset/1d_tasks/arcfill_1d_single_trim/",new_path="../dataset/1d_tasks/arcfill_1d_single_trim_v/",file_prefix="arc1st")
#gen1.gen_vertical_versions(load_path="../dataset/1d_tasks/arcfill_1d_mult_trim/",new_path="../dataset/1d_tasks/arcfill_1d_mult_trim_v/",file_prefix="arc1mt")

# Vertical 1d padding
#gen1.gen_vertical_versions(load_path="../dataset/1d_tasks/arcfill_1d_single/",new_path="../dataset/1d_tasks/arcfill_1d_single_v/",file_prefix="arc1s")
#gen1.gen_vertical_versions(load_path="../dataset/1d_tasks/arcfill_1d_mult/",new_path="../dataset/1d_tasks/arcfill_1d_mult_v/",file_prefix="arc1m")

# Vertical 2d basic
#gen1.gen_vertical_versions(load_path="../dataset/1d_tasks/arcfill_2d_single_basic/",new_path="../dataset/1d_tasks/arcfill_2d_single_basic_v/",file_prefix="arc2s")
#gen1.gen_vertical_versions(load_path="../dataset/1d_tasks/arcfill_2d_mult_basic/",new_path="../dataset/1d_tasks/arcfill_2d_mult_basic_v/",file_prefix="arc2m")

# Vertical mrows
#gen1.gen_vertical_versions(load_path="../dataset/1d_tasks/arcfill_2d_single_mrows/",new_path="../dataset/1d_tasks/arcfill_2d_single_mrows_v/",file_prefix="arc2smr")
#gen1.gen_vertical_versions(load_path="../dataset/1d_tasks/arcfill_2d_mult_mrows/",new_path="../dataset/1d_tasks/arcfill_2d_mult_mrows_v/",file_prefix="arc2mmr")

# Vertical mrows, cropped
#gen1.gen_vertical_versions(load_path="../dataset/1d_tasks/arcfill_2d_single_mrows_crop/",new_path="../dataset/1d_tasks/arcfill_2d_single_mrows_crop_v/",file_prefix="arc2smrc")
#gen1.gen_vertical_versions(load_path="../dataset/1d_tasks/arcfill_2d_mult_mrows_crop/",new_path="../dataset/1d_tasks/arcfill_2d_mult_mrows_crop_v/",file_prefix="arc2mmrc")


# More tasks based on basic tasks
#gen1.gen_reverse_versions(load_path="../dataset/1d_tasks/basic_fill/",new_path="../dataset/1d_tasks/basic_fill_reverse/",file_prefix="bfill")
#gen1.gen_bfill_three()
#gen1.gen_bfill_three_mid()
#gen1.gen_bmove_one()
#gen1.gen_bmove_two()
#gen1.gen_bmove_to_pixel()
#gen1.gen_bmove_to_pixel_2()
#gen1.gen_extend_to_pixel()

# This one do not work, it makes too many duplicates, go generate completely new ones
#gen1.gen_bmove_one_recolor()

# Redo duplicates or previous tasks with issues
#gen1.gen_bmove_to_pixel(relist=[10,13,14,31,33,35,36,49])
#gen1.gen_bmove_to_pixel_2(relist=[5,12,22,24,43,45,47,49])
#gen1.gen_extend_to_pixel(relist=[1,2,4,21,23,28,33,41,42,46])

# More tasks based on basic tasks
#gen1.gen_bfill_three_left()
#gen1.gen_bfill_three_right()
gen1.gen_bfill_three_full()
