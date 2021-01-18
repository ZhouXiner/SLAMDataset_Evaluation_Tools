import numpy as np 
import os

def GetPose(path,new_path):
    for name in os.listdir(path):
        if(path == "__MACOSX"):
            continue
        else:
            common_path = path + "/" + name + "/mav0/state_groundtruth_estimate0"
            full_path = common_path +  "/data.tum"
            euroc_full_path = common_path + "/data.csv"
            new_full_path = new_path + "/" + name + ".tum"
            if not os.path.exists(full_path):
                os.system("cd {} ".format(common_path) + "&&" +  " evo_traj euroc {} --save_as_tum".format(euroc_full_path))
            else:
                print(name)
            os.popen("cp {} {}".format(full_path,new_full_path))
    
path = "/media/zhouxin/66D231E0D231B4E1/Dataset/EuRoC/EuRoc"
new_path = "/home/zhouxin/evaluation/EUROC/gt_s"
GetPose(path,new_path)