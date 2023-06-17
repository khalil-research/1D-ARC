from Generator import *

# 1D fills
class Gen_pcopy(Generator):

    def __init__(self, save_folder, file_prefix, min_len=32, max_len=33,gentype="1c"):
        super().__init__(save_folder, file_prefix, min_len, max_len)
        gentype_map = {
            "1c":self.gen_pcopy_pair_1c,
            "mc":self.gen_pcopy_pair_mc,
        }

        self.gen_func = gentype_map[gentype]

    def gen_pcopy_pair_1c(self, seq_len, io_idx):
        """
        Pattern copy, replace each 1 pixel to match the leftmost 3-pixel-bar
        """
        input,output = [self.back_ground]*seq_len,[self.back_ground]*seq_len

        filling_color = randrange(1,self.max_digits+1)

        init_space = randrange(1,3)
        for j in range(3):
            input[init_space+j]=filling_color
            output[init_space+j]=filling_color

        start = init_space+3
        for i in range(1,randrange(2,5)):
            bwt_space = randrange(1,4)
            start += bwt_space
            input[start+1]=filling_color
            for j in range(3):
                output[start+j]=filling_color
            start += 3

        return input, output

    def gen_pcopy_pair_mc(self, seq_len, io_idx):
        """
        Pattern copy, replace each 1 pixel to match the leftmost 3-pixel-bar, each io pair contains multiple colors
        """
        input,output = [self.back_ground]*seq_len,[self.back_ground]*seq_len

        filling_color = randrange(1,self.max_digits+1)

        init_space = randrange(1,3)
        for j in range(3):
            input[init_space+j]=filling_color
            output[init_space+j]=filling_color

        start = init_space+3
        for i in range(1,randrange(2,5)):
            filling_color = randrange(1,self.max_digits+1)
            bwt_space = randrange(1,4)
            start += bwt_space
            input[start+1]=filling_color
            for j in range(3):
                output[start+j]=filling_color
            start += 3

        return input, output

"""
gen1=Gen_pcopy(save_folder="../dataset/1d_tasks/1d_pcopy_1c",file_prefix="1dpcopy_1c")
#gen1.gen_json(dryrun=False)
for i in range(50):
    gen1.gen_json(dryrun=False)
"""

gen1=Gen_pcopy(save_folder="../dataset/1d_tasks/1d_pcopy_mc",file_prefix="1dpcopy_mc",gentype="mc")
for i in range(50):
    gen1.gen_json(dryrun=True)
