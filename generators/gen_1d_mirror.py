from Generator import *

# 1D fills
class Gen_Mirror(Generator):

    def __init__(self, save_folder, file_prefix, min_len=12, max_len=32):
        super().__init__(save_folder, file_prefix, min_len, max_len)
        self.gen_func = self.gen_single_mirror

    def gen_single_mirror(self, seq_len, io_idx, pivot_pt=9):
        """
        1D flip, single object
        """
        obj_len = randrange(seq_len//4, seq_len//3) 
        obj_to_pivot = randrange(1,max(2,( (seq_len - obj_len*2 - 3)//2 ) ))

        obj1_start = randrange(seq_len - obj_len*2 - obj_to_pivot*2 - 1)
        obj1_end = obj1_start + obj_len

        obj2_start = obj1_end + obj_to_pivot*2 + 1
        obj2_end = obj2_start + obj_len

        filling_color = randrange(1,self.max_digits)

        input,output = [self.back_ground]*seq_len,[self.back_ground]*seq_len

        for i in range(obj1_start,obj1_end):
            input[i]=filling_color

        for i in range(obj2_start,obj2_end):
            output[i]=filling_color

        input[obj1_end+obj_to_pivot]=pivot_pt
        output[obj1_end+obj_to_pivot]=pivot_pt

        return input, output

gen1=Gen_Mirror(save_folder="../dataset/1d_tasks/1d_mirror_single",file_prefix="1dmirror_s")
for i in range(50):
    gen1.gen_json(dryrun=True)
