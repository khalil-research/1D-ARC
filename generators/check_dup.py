from Generator import *

# 1D duplicate checkers
class Gen_chk(Generator):

    def __init__(self, save_folder, file_prefix, min_len=8, max_len=32):
        super().__init__(save_folder, file_prefix, min_len, max_len)

    def check_all_dup(self, main_folder):
        """
        Check files before having uuid, see if there's any duplicate full sets
        """
        for folder in os.scandir(main_folder):
            if folder.is_dir():
                print(folder.path)
                folder_uuids={}
                for entry in os.scandir(folder):
                    #print(entry.path)
                    task_1d = json.load(open(entry.path))
                    self.train_set = task_1d["train"]
                    self.test_set = task_1d["test"]

                    full_set = self.train_set + self.test_set

                    for demo in full_set:
                       tmp_set = full_set.copy()
                       tmp_set.remove(demo)

                       for chk in tmp_set:
                           if chk == demo: 
                            print("Found in set duplicate: ", entry.path)
                            #print(demo)
                            #print(chk)
                            #print(tmp_set)

                    uuid = self.helper_gen_uuid()
                    for i,v in folder_uuids.items():
                        if uuid==v:
                            print("Found duplicate: ",i, entry.path)

                    folder_uuids[entry.path]=uuid

    def check_io_dup(self, main_folder, io_file):
        """
        Check a specific IO pair, see if there's any duplicates
        """
        chk_iopair = json.load(open(io_file))

        for folder in os.scandir(main_folder):
            if folder.is_dir():
                print(folder.path)
                folder_uuids={}
                for entry in os.scandir(folder):
                    #print(entry.path)
                    task_1d = json.load(open(entry.path))
                    self.train_set = task_1d["train"]
                    self.test_set = task_1d["test"]

                    full_set = self.train_set + self.test_set

                    for demo in full_set:
                        if chk_iopair == demo: 
                            print("Found in set duplicate: ", entry.path)
                            #print(demo)
                            #print(chk)
                            #print(tmp_set)




gen1=Gen_chk(save_folder="../dataset/1d_tasks/1d_move_test",file_prefix="1dmove_test")

#gen1.check_all_dup(main_folder="../dataset/1d_tasks")
gen1.check_all_dup(main_folder="../dataset/arc_hv_tasks")
#gen1.check_io_dup(main_folder="../dataset/1d_tasks", io_file="../dataset/io_pair/few_shot_4.json")
