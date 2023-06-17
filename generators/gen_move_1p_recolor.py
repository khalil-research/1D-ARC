from Generator import *

# Example of a level 2 1D-ARC task generator
# 1. Move 1 pixel to the right
# 2. Recolor
class Gen_move_1p_recolor(Generator):

    def __init__(self, save_folder, file_prefix, min_len=12, max_len=33):
        super().__init__(save_folder, file_prefix, min_len, max_len)
        self.gen_func = self.gen_move_1p_recolor

    def gen_move_1p_recolor(self, seq_len, io_idx, ori_color, new_color):
        """
        Level-2 1D task, move to right 1 pixel, then recolor, ARC#a79310a0
        """
        input,output = [self.back_ground]*seq_len,[self.back_ground]*seq_len

        min_bar_len=5
        move_len=1
        # Basic, move all single objs (bar) for a fixed move_len in 1D
        bar_len = randrange(min_bar_len, seq_len - move_len - 3)
        bar_start = randrange(seq_len - bar_len - move_len - 2 )
        print(seq_len, bar_len, bar_start, move_len)

        for i in range(bar_start,bar_start+bar_len):
            input[i]=ori_color

        for j in range(bar_start+move_len,bar_start+bar_len+move_len):
            output[j]=new_color

        return input, output


gen1=Gen_move_1p_recolor(save_folder="../dataset/1d_tasks/1d_move_1p_recolor",file_prefix="1dm1p_rec")
for i in range(50):
    # Gen color
    # TODO, for tasks without randomness inside io pair generation, this needs to be nested into the while-check loop
    ori_color = randrange(1,gen1.max_digits+1)
    other_colors = list(range(1,gen1.max_digits+1))
    other_colors.remove(ori_color)
    new_color = random.choice(other_colors)

    gen1.gen_json(dryrun=False, ori_color=ori_color, new_color=new_color)
