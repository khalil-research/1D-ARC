from Generator import *

# 1D fills
class Gen_Move(Generator):
    move_len=1
    min_bar_len=3

    def __init__(self, save_folder, file_prefix, min_len=8, max_len=32, move_len=3, min_bar_len=3):
        super().__init__(save_folder, file_prefix, min_len, max_len)
        self.gen_func = self.gen_move_single_bar_pair
        self.move_len = move_len
        self.min_bar_len = min_bar_len

    # Construct a basic 1D move task, move a single bar 3 pixels to the right 
    def gen_move_single_bar_pair(self, seq_len, io_idx):
        """
        Basic, move all single objs (bar) for a fixed move_len in 1D
        """
        bar_len = randrange(self.min_bar_len, seq_len - self.move_len) 
        bar_start = randrange(seq_len - bar_len - self.move_len)
        print(seq_len, bar_len, bar_start, self.move_len)

        # Bar color = any non background color
        filling_color = randrange(1,self.max_digits+1)

        input,output = [self.back_ground]*seq_len,[self.back_ground]*seq_len
        for i in range(bar_start,bar_start+bar_len):
            input[i]=filling_color

        for j in range(bar_start+self.move_len,bar_start+bar_len+self.move_len):
            output[j]=filling_color

        return input, output

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
            #with open("../dataset/1d_tasks/basic_move_1/"+filepath, 'w') as f:
            #        json.dump(task_1d, f)


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
    # Now move to 2 pixels right, but with a pixel indicating the end of movement
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

gen1=Gen_Move(save_folder="../dataset/1d_tasks/basic_move",file_prefix="bmove")
"""
# Basic move ( Move 3 pixels)
for i in range(50):
    gen1.gen_json(dryrun=False)
"""

# More tasks based on basic tasks
# Rememeber to check duplicates with check_dup.py

# Basic move ( Move 1 pixel)
#gen1.gen_bmove_one()

# Basic move ( Move 2 pixels)
#gen1.gen_bmove_two()

# Basic move ( Move to dynamic located pixel)
#gen1.gen_bmove_to_pixel()

# Basic move ( Move to fixed position[+2 right] pixel)
#gen1.gen_bmove_to_pixel_2()

# Basic move ( Scaling )
#gen1.gen_extend_to_pixel()

# You may also build completely new generators for those new task types
