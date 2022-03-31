import subprocess
import numpy as np

def ReadSequence(list_path):
    seq = list()
    with open(list_path) as f:
        for line in f.readlines():
            line=line.strip('\n')
            if(line[0] == "#"):
                continue
            seq.append(line)
    print("all_seq",seq)
    return seq

def Evaluate(gt_path,evaluate_path,seq_list,num):
    results = list()
    for i in range(1,num + 1):
        print("for {} time".format(i))
        one_result = list()
        for j in range(len(seq_list)):
            print_flag = False
            gt_seq_path = gt_path + "/" + seq_list[j] + "_tum.txt"
            eva_seq_path =  evaluate_path + "/" + seq_list[j] + ".txt"
            cmd = "evo_ape tum {} {} -as".format(gt_seq_path,eva_seq_path)
            res = subprocess.check_output(cmd, shell=True)
            res = str(res)
            result = res.split("\\n")
            for info in result:
                detail = info.split("\\t")
                if(detail[0].strip() == "rmse"):
                    print(seq_list[j],detail[1])
                    one_result.append(detail[1])
                    print_flag = True
            if not print_flag:
                print(seq_list[j],"wrong")
                one_result.append(1e3)
        results.append(one_result)
    return results

seq_list_path = "/home/zhouxin/evaluation/Kitti/seq_list.txt"
gt_path = "/home/zhouxin/evaluation/Kitti/gt"
eva_path = "/home/zhouxin/GitHub/ORB_SLAM3_loop/resultkitti"
seq_list = ReadSequence(seq_list_path)
results = Evaluate(gt_path,eva_path,seq_list,1)