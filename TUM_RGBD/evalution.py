import os
import subprocess

def GetSeq(path):
    seq_list = list()
    for file in os.listdir(path):
        seq_list.append(file.split('.')[0])
    return seq_list

def Evaluation(seq_list,eva_path,gt_path):
    for seq in seq_list:
        gt_seq_path = gt_path + "/" + seq + "/groundtruth.txt"
        eva_seq_path = eva_path + "/" + seq + ".txt"
        cmd_eva = "evo_ape tum {} {} -a -p".format(gt_seq_path,eva_seq_path)
        res = subprocess.check_output(cmd_eva, shell=True)
        res = str(res)
        result = res.split("\\n")
        gt_count = len(open(gt_seq_path,'r').readlines())
        eva_count = len(open(eva_seq_path,'r').readlines())
        for info in result:
            detail = info.split("\\t")
            if(detail[0].strip() == "rmse"):
                print(seq,detail[1],gt_count,eva_count)
                break

gt_path = "/media/zhouxin/66D231E0D231B4E12/Dataset/TUM_RGBD/TUM"
eva_path = "/home/zhouxin/GitHub/ORB_SLAM2_Normal/resultTUM1"
seq_list = GetSeq(eva_path)
Evaluation(seq_list,eva_path,gt_path)
