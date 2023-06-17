from Generator import *

# 1D fills
class Gen_recolor(Generator):

    def __init__(self, save_folder, file_prefix, min_len=12, max_len=33, gentype="oe"):
        super().__init__(save_folder, file_prefix, min_len, max_len)
        gentype_map = {
            "oe":self.gen_recolor_odd_even,
            "cnt":self.gen_recolor_size_cnt,
            "cmp":self.gen_recolor_size_cmp,
        }

        self.gen_func = gentype_map[gentype]

    def helper_get_oe_color(self, len, odd_color, even_color):
        if len % 2 == 0:
            return even_color
        else:
            return odd_color

    def helper_get_cnt_color(self, len, one_color, two_color, three_color):
        if len == 1:
            return one_color
        elif len == 2:
            return two_color
        else:
            return three_color

    def gen_recolor_odd_even(self, seq_len, io_idx, ori_color, odd_color, even_color):
        """
        Recolor based on size(obj) = odd or even number
        """
        input,output = [self.back_ground]*seq_len,[self.back_ground]*seq_len

        start = 0
        # Make sure each io pair has at least 1 odd and 1 even
        has_odd, has_even = 0,0
        for i in range(1,6):
            bwt_space = randrange(1,4)
            start += bwt_space
            bar_len = randrange(1,6)

            if has_odd==0 and bar_len%2 == 0:
                bar_len+=1
                has_odd+=1
            elif has_even==0 and bar_len%2 == 1:
                bar_len+=1
                has_even+=1

            if start+bar_len > seq_len:
                break

            for j in range(bar_len):
                input[start+j]=ori_color
                output[start+j]=self.helper_get_oe_color(bar_len,odd_color,even_color)

            start += bar_len

        return input, output

    def gen_recolor_size_cnt(self, seq_len, io_idx, ori_color, one_color, two_color, three_color):
        """
        Recolor based on size(obj) = 1, 2, or 3
        """
        input,output = [self.back_ground]*seq_len,[self.back_ground]*seq_len

        start = 0
        # Make sure each io pair has at least 1 sample for each size
        bar_lens=[1,2,3]
        for i in range(1,6):
            bwt_space = randrange(1,4)
            start += bwt_space
            if i <= 3:
                bar_len = random.choice(bar_lens)
                bar_lens.remove(bar_len)
            else:
                bar_len = randrange(1,4)

            if start+bar_len > seq_len:
                break

            for j in range(bar_len):
                input[start+j]=ori_color
                output[start+j]=self.helper_get_cnt_color(bar_len,one_color, two_color, three_color)

            start += bar_len

        return input, output

    def gen_recolor_size_cmp(self, seq_len, io_idx, ori_color, max_color, max_lens):
        """
        Recolor based on size(obj), only the max size obj gets recolored
        """
        input,output = [self.back_ground]*seq_len,[self.back_ground]*seq_len

        # Make sure each io pair has at least two samples, so there's comparison
        # Also make sure max_len is not all the same across all train samples
        space_l=[]
        bar_l=[]

        # Insert the max bar
        bwt_space = randrange(1,4)
        space_l.append(bwt_space)
        if io_idx<3:
            max_bar_len = max_lens[io_idx]
        else:
            max_bar_len = random.choice([4,5,6,7])
        bar_l.append(max_bar_len)

        start = bwt_space+max_bar_len
        for i in range(6):
            bwt_space = randrange(1,4)
            if i == 0:
                bar_len = randrange(1,max_bar_len)
            else:
                bar_len = randrange(1,max_bar_len+1)
            start += bwt_space+bar_len

            if start > seq_len:
                break

            space_l.append(bwt_space)
            bar_l.append(bar_len)

        print("space_l",space_l)
        print("bar_l",bar_l)
        order_l = list(range(len(bar_l)))
        random.shuffle(order_l)

        print("order_l",order_l)
        # re-start
        start=0
        for i in order_l:
            bwt_space = space_l[i]
            bar_len = bar_l[i]
            start += bwt_space

            if start+bar_len > seq_len:
                break

            for j in range(bar_len):
                input[start+j]=ori_color
                if bar_len == max_bar_len:
                    output[start+j]=max_color
                else:
                    output[start+j]=ori_color

            start += bar_len

        print(input, output)
        return input, output

"""
gen1=Gen_recolor(save_folder="../dataset/1d_tasks/1d_recolor_oe",file_prefix="1drec_oe")
for i in range(50):
    # Gen color
    # TODO, for tasks without randomness inside io pair generation, this needs to be nested into the while-check loop
    ori_color = randrange(1,gen1.max_digits+1)
    other_colors = list(range(1,gen1.max_digits+1))
    other_colors.remove(ori_color)
    odd_color = random.choice(other_colors)
    other_colors.remove(odd_color)
    even_color = random.choice(other_colors)

    gen1.gen_json(dryrun=False, ori_color=ori_color, odd_color=odd_color, even_color=even_color)

"""

gen1=Gen_recolor(save_folder="../dataset/1d_tasks/1d_recolor_cnt",file_prefix="1drec_cnt", gentype="cnt")
for i in range(50):
    # Gen color
    # TODO, for tasks without randomness inside io pair generation, this needs to be nested into the while-check loop
    ori_color = randrange(1,gen1.max_digits+1)
    other_colors = list(range(1,gen1.max_digits+1))
    other_colors.remove(ori_color)
    one_color = random.choice(other_colors)
    other_colors.remove(one_color)
    two_color = random.choice(other_colors)
    other_colors.remove(two_color)
    three_color = random.choice(other_colors)

    gen1.gen_json(dryrun=True, ori_color=ori_color, one_color=one_color, two_color=two_color, three_color=three_color)

"""
gen1=Gen_recolor(save_folder="../dataset/1d_tasks/1d_recolor_cmp",file_prefix="1drec_cmp", min_len=17, gentype="cmp")
for i in range(50):
    # Gen color
    ori_color = randrange(1,gen1.max_digits+1)
    other_colors = list(range(1,gen1.max_digits+1))
    other_colors.remove(ori_color)
    max_color = random.choice(other_colors)

    max_lens = [4,5,7]
    random.shuffle(max_lens)
    print(max_lens)
    gen1.gen_json(dryrun=False, ori_color=ori_color, max_color=max_color, max_lens=max_lens)
"""
