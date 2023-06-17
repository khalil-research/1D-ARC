from Generator import *

# 1D fills
class Gen_Fill(Generator):
    min_hole_len=1

    def __init__(self, save_folder, file_prefix, min_len=8, max_len=32, min_hole_len=1):
        super().__init__(save_folder, file_prefix, min_len, max_len)
        self.gen_func = self.gen_fill_single_hole_pair
        self.min_hole_len=min_hole_len

    def gen_fill_single_hole_pair(self, seq_len, io_idx):
        """
        Basic, fill a single hole in 1D
        """
        # seqlen - 2 (pivots) - 3 (space for future nested move task)
        hole_len = randrange(self.min_hole_len, seq_len - 2 - 3) 
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
    # Reverse bfill input/output, now we have a hollowing/hole cutting task
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


gen1=Gen_Fill(save_folder="../dataset/1d_tasks/basic_fill",file_prefix="bfill")
"""
# Basic fill (fill in backgrounds between two pixels)
for i in range(50):
    gen1.gen_json(dryrun=True)
"""

# Padded fill ( expand bfill tasks to 3x the same task in one row)
#gen1.gen_bfill_three()

# Hollow ( reverse input/output of the bfill tasks )
#gen1.gen_reverse_versions(load_path="../dataset/1d_tasks/basic_fill/",new_path="../dataset/1d_tasks/basic_fill_reverse/",file_prefix="bfill")
