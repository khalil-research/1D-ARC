from Generator import *

# 1D flips
class Gen_Filp(Generator):

    def __init__(self, save_folder, file_prefix, min_len=8, max_len=32):
        super().__init__(save_folder, file_prefix, min_len, max_len)
        self.gen_func = self.gen_single_flip

    def gen_single_flip(self, seq_len, io_idx):
        """
        1D flip, single object
        """
        obj_len = randrange(seq_len//4, seq_len//2) 
        obj_start = randrange(seq_len - obj_len - 1)
        obj_end = obj_start + obj_len + 1

        pivot_pt = randrange(1,self.max_digits)
        filling_color = randrange(1,self.max_digits)
        if filling_color == pivot_pt:
            filling_color = pivot_pt+1

        input,output = [self.back_ground]*seq_len,[self.back_ground]*seq_len

        for i in range(obj_start,obj_end):
            if i==obj_start:
                input[i]=pivot_pt
            else:
                input[i]=filling_color

            if i==obj_end-1:
                output[i]=pivot_pt
            else:
                output[i]=filling_color

        return input, output

gen1=Gen_Filp(save_folder="../dataset/1d_tasks/1d_flip_single",file_prefix="1dflip_s")
for i in range(50):
    gen1.gen_json(dryrun=True)
