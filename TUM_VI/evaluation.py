import subprocess
import numpy as np
import os

def SplitType(csv_flag):
    if(csv_flag):
        return ","
    else:
        return " "

def OpenTUMPose(pose_path,csv_flag):
    Pose = list()
    with open(pose_path,encoding="utf-8") as f:
        for line in f.readlines():
            line=line.strip('\n')
            data = line.split(SplitType(csv_flag))
            if(data[0][0] == "#"):
                continue
            Pose.append(data)
        return Pose

def SaveTUMPose(save_path,Poses,csv_flags):
    if(csv_flags):
        data = np.array(Poses)
        data_float = data.astype(float)
        pd.DataFrame(data_float).to_csv(save_path,index=None,header=None)
    else:
        with open(save_path,'w',encoding = 'utf-8') as f:
            for pose in Poses:
                f.write("{} {} {} {} {} {} {} {}\n".format(float(pose[0])*1e-9,pose[1],pose[2],pose[3],pose[4],pose[5],pose[6],pose[7]))


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

def Evaluate(gt_path,evaluate_path,seq_list,iter_num,erase_num):
    results = list()
    for i in range(1,iter_num + 1):
        print("for {} time".format(i))
        one_result = list()
        for j in range(len(seq_list)):
            print_flag = False
            gt_seq_path = gt_path + "/" + seq_list[j] + ".txt"
            #eva_seq_path =  evaluate_path + "/" + seq_list[j] + "_{}".format(i) + ".txt"
            eva_seq_path =  evaluate_path + "/" + seq_list[j] + "_{}".format(i) + ".txt"
            eva_part_path = evaluate_path + "/" + seq_list[j] + "_{}".format(i) + "part.txt"
            if(erase_num != 0):
                GetPartPose(eva_seq_path,erase_num,eva_part_path)
                cmd_eva = "evo_ape tum {} {} -a -p".format(gt_seq_path,eva_part_path)
                eva_count = len(open(eva_part_path,'r').readlines())

            else:
                cmd_eva = "evo_ape tum {} {} -a".format(gt_seq_path,eva_seq_path)
                eva_count = len(open(eva_seq_path,'r').readlines())
                print(cmd_eva)

            res = subprocess.check_output(cmd_eva, shell=True)
            res = str(res)
            result = res.split("\\n")
            gt_count = len(open(gt_seq_path,'r').readlines())
            for info in result:
                detail = info.split("\\t")
                if(detail[0].strip() == "rmse"):
                    print(seq_list[j],detail[1],gt_count,eva_count)
                    one_result.append(float(detail[1]))
                    print_flag = True
            if not print_flag:
                print(seq_list[j],"wrong")
                one_result.append(float(1e3))
            if(erase_num != 0):
                cmd_erase = "rm {}".format(eva_part_path)
                os.system(cmd_erase)
        results.append(one_result)
    return results

def GetAverageResult(results):
    results_array = np.array(results)
    average_ape = np.mean(results_array,axis=0)
    print(average_ape)

def SaveResult(results,save_path):
    results_array = np.array(results)
    results_array = results_array.transpose()
    np.savetxt(save_path,results_array,delimiter = ",")

def GetPartPose(old_path,erase_num,new_path):
    poses = OpenTUMPose(old_path,False)
    save_num = int(len(poses)) - int(erase_num)
    new_poses = poses[-save_num:]
    SaveTUMPose(new_path,new_poses,False)


gt_path = "/home/zhouxin/evaluation/TUM_VI/gt_s"
eva_path = "/home/zhouxin/papers/pvio_expriments/pvio/tumvi/plane"
seq_list_path = "/home/zhouxin/evaluation/TUM_VI/seq_list_all.txt"
seq_list = ReadSequence(seq_list_path)

result_save_path = "/home/zhouxin/evaluation/TUM_VI/result.csv"
results = Evaluate(gt_path,eva_path,seq_list,1,0)
GetAverageResult(results)
# SaveResult(results,result_save_path)
# path = "/home/zhouxin/GitHub/ORB_SLAM3/result_TUM_VI/Corridor1_1s.txt"
# save_path = "/home/zhouxin/GitHub/ORB_SLAM3/result_TUM_VI/Corridor1_1.txt"
# pose =  OpenTUMPose(path,False)
# SaveTUMPose(save_path,pose,False)
