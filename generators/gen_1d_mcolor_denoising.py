from Generator import *

# 1D fills
class Gen_mc_denoising(Generator):

    def __init__(self, save_folder, file_prefix, min_len=32, max_len=33):
        super().__init__(save_folder, file_prefix, min_len, max_len)
        self.gen_func = self.gen_single_mc_denoising

    def gen_single_mc_denoising(self, seq_len, io_idx):
        """
        1D same color denoising, single object
        """
        obj_len = randrange(seq_len-12, seq_len - 6) 
        obj_start = randrange(seq_len - obj_len - 2)
        obj_end = obj_start + obj_len

        filling_color = randrange(1,self.max_digits+1)
        noise_colors = list(range(1,self.max_digits+1))
        noise_colors.remove(filling_color)

        input,output = [self.back_ground]*seq_len,[self.back_ground]*seq_len

        for i in range(obj_start,obj_end):
            input[i]=filling_color
            output[i]=filling_color

        # Noise pixels = 1~4
        for i in range( randrange(1,5) ):
            noise_color = random.choice(noise_colors)
            input[randrange(obj_start+2,obj_end-2)] = noise_color

        return input, output

gen1=Gen_mc_denoising(save_folder="../dataset/1d_tasks/1d_mc_denoising_single",file_prefix="1dmcdenoi_s")
for i in range(50):
    gen1.gen_json(dryrun=True)
