from Generator import *

# 1D fills
class Gen_1c_denoising(Generator):

    def __init__(self, save_folder, file_prefix, min_len=32, max_len=33):
        super().__init__(save_folder, file_prefix, min_len, max_len)
        self.gen_func = self.gen_single_1c_denoising

    def gen_single_1c_denoising(self, seq_len, io_idx):
        """
        1D same color denoising, single object
        """
        obj_len = randrange(seq_len//3, seq_len//2) 
        obj_start = randrange(seq_len - obj_len - 2)
        obj_end = obj_start + obj_len

        filling_color = randrange(1,self.max_digits)

        input,output = [self.back_ground]*seq_len,[self.back_ground]*seq_len

        for i in range(obj_start,obj_end):
            input[i]=filling_color
            output[i]=filling_color

        pixel_suffix = 1

        # prepending noises
        pixel_end = 0
        # Noise pixels = size 1 or 2
        for i in range( randrange(1,6) ):
            #pixel_len = randrange(1,3)
            pixel_len = 1
            pixel_prefix = randrange(2,5)

            pixel_start = pixel_end+pixel_prefix
            pixel_end = pixel_start+pixel_len

            if pixel_end+pixel_suffix > obj_start:
                break

            for i in range(pixel_start, pixel_end):
                input[i] = filling_color


        # appending noises
        pixel_end = obj_end
        # Noise pixels = size 1 or 2
        for i in range( randrange(1,6) ):
            #pixel_len = randrange(1,3)
            pixel_len = 1
            pixel_prefix = randrange(2,5)

            pixel_start = pixel_end+pixel_prefix
            pixel_end = pixel_start+pixel_len

            if pixel_end+pixel_suffix > seq_len:
                break

            for i in range(pixel_start, pixel_end):
                input[i] = filling_color

        return input, output

gen1=Gen_1c_denoising(save_folder="../dataset/1d_tasks/1d_1c_denoising_single",file_prefix="1d1cdenoi_s")
for i in range(50):
    gen1.gen_json(dryrun=True)
