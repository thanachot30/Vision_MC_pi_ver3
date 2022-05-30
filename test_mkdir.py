import os
import shutil
from os import listdir


# directory = "dataset_testnew"

# # Parent Directory path
# parent_dir = "D:/p_ARM/ANTROBOTICS_VISION_MC_SMALL_3/Vision_mc_ver3/"

# # Path
# path = os.path.join(parent_dir, directory)


# os.makedirs(path)
# print("Directory '% s' created" % directory)

# location = "D:/p_ARM/ANTROBOTICS_VISION_MC_SMALL_3/Vision_mc_ver3/data_new_model/"

# # directory
# dir = "pos_1"

# # path
# path = os.path.join(location, dir)

# # removing directory
# shutil.rmtree(path, ignore_errors=False)

path_to_pos = "D:/p_ARM/ANTROBOTICS_VISION_MC_SMALL_3/Vision_mc_ver3/data_new_model/pos_1/ok/"

len_actual_image = len(listdir(path_to_pos))
print(len_actual_image)
