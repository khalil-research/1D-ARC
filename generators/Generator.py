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


# For re-produce
random.seed(42)
os.environ['PYTHONHASHSEED'] = '42'

# Generator base class
class Generator:
    max_digits = 9
    back_ground = 0
    generator_type = "base"

    # Since grid size is a rather important variable for solvability, fix max to 32 for now.
    min_seq_len = 8
    max_seq_len = 32

    train_set = []
    test_set = []
    save_folder = ""
    file_prefix = ""
    uuid = ""
    task_num = 0

    # This should be the actual generator function, which should return input, output
    gen_func = None
    """
    gen_type_map = {'bfill': self.gen_fill_single_hole_pair,
                    'bmove': self.gen_move_single_bar_pair
                    }
    """

    dup_io_cnt=0
    dup_io_maxtry=500
    dup_file_cnt=0
    dup_file_maxtry=500

    def __init__(self, save_folder, file_prefix, min_len=8, max_len=32):
        self.min_seq_len = min_len
        self.max_seq_len = max_len
        self.save_folder = save_folder
        self.file_prefix = file_prefix

    def check_dup(self, new_input, new_output):
        """
        Helper function that checks duplicates among training, test sets
        """
        if self.gen_type=="2d":
            new_input = new_input[0]
            new_output = new_output[0]

        for io_pair in self.train_set+self.test_set:
            #print("Check dup:")
            #print("new_input :",new_input)
            #print("check_input :",io_pair["input"])
            if new_input == io_pair["input"] and new_output==io_pair["output"]:
                return True

        return False
            
    def helper_gen_uuid(self):
        """
        Generate a hashed UUID for the given train/test set
        """
        in_hash, out_hash = [],[]
        for io_pair in self.train_set:
            train_hash=[]
            for i_row in io_pair["input"]:
                train_hash.append(tuple(i_row))
            for o_row in io_pair["output"]:
                train_hash.append(tuple(o_row))

            in_hash.append(tuple(train_hash))

        for io_pair in self.test_set:
            test_hash=[]
            for i_row in io_pair["input"]:
                test_hash.append(tuple(i_row))
            for o_row in io_pair["output"]:
                test_hash.append(tuple(o_row))

            out_hash.append(tuple(test_hash))
        
        final_hash = str(hash(tuple(sorted(in_hash))))+str(hash(tuple(sorted(out_hash))))
        self.uuid = final_hash

        return final_hash

    def helper_cal_uuid(self, task_json):
        """
        Generate a hashed UUID for the given train/test set
        """
        in_hash, out_hash = [],[]
        for io_pair in task_json['train']:
            train_hash=[]
            for i_row in io_pair["input"]:
                train_hash.append(tuple(i_row))
            for o_row in io_pair["output"]:
                train_hash.append(tuple(o_row))

            in_hash.append(tuple(train_hash))

        for io_pair in task_json['test']:
            test_hash=[]
            for i_row in io_pair["input"]:
                test_hash.append(tuple(i_row))
            for o_row in io_pair["output"]:
                test_hash.append(tuple(o_row))

            out_hash.append(tuple(test_hash))
        
        final_hash = str(hash(tuple(sorted(in_hash))))+str(hash(tuple(sorted(out_hash))))

        return final_hash

    def check_dup_file(self, new_json):
        """
        Helper function, checks if the full train/test set is already generated
        """
        if new_json:
            for entry in os.scandir(self.save_folder):
                task_1d = json.load(open(entry.path))
            
                if 'uuid' not in task_1d:
                    task_uuid = self.helper_cal_uuid(task_1d) 
                else:
                    task_uuid = task_1d['uuid'] 

                if task_uuid == self.uuid and self.uuid!="":
                    return True

            return False
        else:
            return True


    def gen_json(self, dryrun=True, gen_type="1d", **kwargs):
        """
        Generate the json file
        """
        self.gen_type = gen_type

        json_str = {}
        while( self.check_dup_file(json_str)):
            # randomize sequence length
            seq_len = randrange(self.min_seq_len,self.max_seq_len+1)

            # init
            json_str = {}
            self.train_set = []
            self.test_set = []

            # Generate 3 training set
            for i in range(3):
                input, output = self.gen_func(seq_len,io_idx=i,**kwargs)
                while( self.check_dup([input],[output]) ):
                    input, output = self.gen_func(seq_len,io_idx=i, **kwargs)
                    self.dup_io_cnt+=1
                    if self.dup_io_cnt > self.dup_io_maxtry:
                        print("Randomness exhausted for IO pairs...")
                        sys.exit(-2)
                self.dup_io_cnt=0

                if self.gen_type=="1d":
                    self.train_set.append({"input":[input],"output":[output]})
                else:
                    self.train_set.append({"input":input,"output":output})

            input, output = self.gen_func(seq_len, io_idx=3, **kwargs)
            while( self.check_dup([input],[output]) ):
                input, output = self.gen_func(seq_len, io_idx=3, **kwargs)
                self.dup_io_cnt+=1
                if self.dup_io_cnt > self.dup_io_maxtry:
                    print("Randomness exhausted for IO pairs...")
                    sys.exit(-2)
            self.dup_io_cnt=0

            if self.gen_type=="1d":
                self.test_set.append({"input":[input],"output":[output]})
            else:
                self.test_set.append({"input":input,"output":output})

            uuid = self.helper_gen_uuid()
            json_str = {"train":self.train_set, "test":self.test_set, "uuid":self.uuid}

            self.dup_file_cnt+=1
            if self.dup_file_cnt > self.dup_file_maxtry:
                print("Randomness exhausted...")
                sys.exit(-2)

        self.dup_file_cnt=0
        print(json_str)

        if json_str:
            filepath = self.save_folder + '/' + self.file_prefix + '_' + str(self.task_num) + '.json'
            print(filepath)

            if not dryrun:
                with open(filepath, 'w') as f:
                    json.dump(json_str, f)

            self.task_num+=1

    def helper_get_bar_info(self,grid):
        start,end,fill_color=-1,-1,0
        for idx, i in enumerate(grid):
            if i!=self.back_ground and start==-1:
                fill_color = i
                start=idx
            elif i==self.back_ground and start>-1 and end==-1:
                end=idx
        return start,end,fill_color

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

