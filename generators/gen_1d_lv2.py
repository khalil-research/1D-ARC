from Generator import *

# Sample script, generating Lv2 1D-ARC tasks
# Lv2 task is a nesting of two lv1 1D-ARC tasks, e.g. Lv2 Move and fill is a direct combination of "Move 3 pixels" and "Fill".
# This is designed to build from exact original lv1 ( e.g. lv1-move-3-pixels) tasks so we can make a comparison, you may also start completely newly generate lv2 tasks.
# Keep in mind some nesting combos might cause duplications.
# From here, you can produce lv3 and so on, e.g. add a recolor step to this lv2.
# So we have a difficulty hierarchy in those tasks. 
# We see slightly evidences that solve rate of GPT might follows Bayesian rules: solve_rate(Lv2_t1_t2) = solve_rate(Lv1_t1)*solve_rate(lv1_t2). But we did not have the time/cost resource to dig this further. Feel free to shoot me emails discuss about your findings and ideas about this dataset.

class Gen_Lv2(Generator):
    def __init__(self, save_folder="", file_prefix="", min_len=8, max_len=32):
        super().__init__(save_folder, file_prefix, min_len, max_len)

    # Construct 2-step 1d tasks from the move 3 pixels tasks
    # We cut holes in the bars just as fill tasks, so the solver need to move the object 3 pixels to the right, then fill the holes
    def gen_move_then_fill(self, source_path, source_prefix, target_path, target_prefix, dryrun=True):
        for entry in os.scandir(source_path):
            task_1d = json.load(open(entry.path))
            # make holes in input
            for demo in task_1d['train']:
                self.helper_hole_cutter(demo['input'][0])
                print(demo['input'][0])
            for demo_t in task_1d['test']:
                self.helper_hole_cutter(demo_t['input'][0])
                print(demo_t['input'][0])

            print(task_1d)
            filepath = os.path.basename(entry.path).replace(source_prefix,target_prefix)
            print(filepath)
            if not dryrun:
                with open(target_path+filepath, 'w') as f:
                    json.dump(task_1d, f)

gen1=Gen_Lv2()

# Lv2 Move and fill
gen1.gen_move_then_fill(source_path="../dataset/1d_move_3p/", source_prefix="1d_move_3p", target_path="../dataset/1d_lv2_move_n_fill/", target_prefix="1d_lv2_move_n_fill", dryrun=True)
