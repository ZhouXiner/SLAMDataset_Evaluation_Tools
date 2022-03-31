import subprocess
import numpy as np
import os
import pandas as pd

from numpy.lib.function_base import median

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
                #int(float(pose[0]) * 0.000001) for Ela
                f.write("{} {} {} {} {} {} {} {}\n".format(pose[0],pose[1],pose[2],pose[3],pose[4],pose[5],pose[6],pose[7]))


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
            gt_seq_path = gt_path + "/" + seq_list[j] + "/groundtruth.txt"
            #eva_seq_path =  evaluate_path + "/" + seq_list[j] + "_{}".format(i) + ".txt"
            eva_seq_path =  evaluate_path + "/" + seq_list[j] + "_{}".format(i) + ".txt"
            eva_part_path = evaluate_path + "/" + seq_list[j] + "_{}".format(i) + "part.txt"
            if(erase_num != 0):
                GetPartPose(eva_seq_path,erase_num,eva_part_path)
                cmd_eva = "evo_ape tum {} {} -a".format(gt_seq_path,eva_part_path)
                eva_count = len(open(eva_part_path,'r').readlines())

            else:
                cmd_eva = "evo_ape tum {} {} -a".format(gt_seq_path,eva_seq_path)
                eva_count = len(open(eva_seq_path,'r').readlines())

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


def SolveElaTimeStamp(evaluate_path):
    for j in range(len(seq_list)):
        eva_seq_path =  evaluate_path + "/" + seq_list[j] + ".klg.freiburg"
        eva_seq_new_path = evaluate_path + "/" + seq_list[j] + ".txt"
        poses = OpenTUMPose(eva_seq_path,False)
        SaveTUMPose(eva_seq_new_path,poses,False)

def EvaluateEla(gt_path,evaluate_path,seq_list,iter_num):
    results = list()
    for i in range(1,iter_num + 1):
        print("for {} time".format(i))
        one_result = list()
        for j in range(len(seq_list)):
            print_flag = False
            gt_seq_path = gt_path + "/" + seq_list[j] + "/groundtruth_plus.txt"
            eva_seq_path =  evaluate_path + "/" + seq_list[j] + ".klg.freiburg"

            cmd_eva = "evo_rpe tum {} {} -a".format(gt_seq_path,eva_seq_path)
            eva_count = len(open(eva_seq_path,'r').readlines())

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

        results.append(one_result)

    
def EvaluateKin(gt_path,evaluate_path,seq_list,iter_num):
    results = list()
    for i in range(1,iter_num + 1):
        print("for {} time".format(i))
        one_result = list()
        for j in range(len(seq_list)):
            print_flag = False
            gt_seq_path = gt_path + "/" + seq_list[j] + "/groundtruth.txt"
            eva_seq_path =  evaluate_path + "/" + seq_list[j] + ".klg.poses"

            cmd_eva = "evo_rpe tum {} {} -a".format(gt_seq_path,eva_seq_path)
            eva_count = len(open(eva_seq_path,'r').readlines())

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

        results.append(one_result)
    
def EvaluateDVO(gt_path,evaluate_path,seq_list,iter_num):
    results = list()
    for i in range(1,iter_num + 1):
        print("for {} time".format(i))
        one_result = list()
        for j in range(len(seq_list)):
            print_flag = False
            gt_seq_path = gt_path + "/" + seq_list[j] + "/groundtruth.txt"
            eva_seq_path =  evaluate_path + "/" + seq_list[j] + ".txt"

            cmd_eva = "evo_ape tum {} {} -a -p".format(gt_seq_path,eva_seq_path)
            eva_count = len(open(eva_seq_path,'r').readlines())

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

        results.append(one_result)

def EvaluationWithName(gt_path,evaluate_path,seq_list,iter_num):
    results = list()
    for j in range(len(seq_list)):
        one_result = list()
        for i in range(1,iter_num + 1):
            print_flag = False
            seq_iter_name = seq_list[j] + "_{}".format(i)
            gt_seq_path = gt_path + "/" + seq_list[j] + "/groundtruth.txt"
            eva_seq_path =  evaluate_path + "/" + seq_list[j] + "_{}".format(i) + ".txt"
            
            if not os.path.exists(eva_seq_path):
                continue
            cmd_eva = "evo_ape tum {} {} -a".format(gt_seq_path,eva_seq_path)
            eva_count = len(open(eva_seq_path,'r').readlines())

            res = subprocess.check_output(cmd_eva, shell=True)
            res = str(res)
            result = res.split("\\n")
            gt_count = len(open(gt_seq_path,'r').readlines())
            for info in result:
                detail = info.split("\\t")
                if(detail[0].strip() == "rmse"):
                    one_result.append([seq_iter_name,float(detail[1]),eva_count])
        one_result = sorted(one_result,key = lambda x:-x[1])   

    
        sum = 0
        for i in range(0,len(one_result)):
            print(one_result[i])
            if i >= 5:
                sum = sum + float(one_result[i][1])
        
        if len(one_result) < iter_num:
            continue

        sum = sum / 10.0 
           
        results.append(one_result)
        print("average: ",sum," median: ",(one_result[9][1] + one_result[10][1]) / 2.0,'\n')
    return results

def EvaluateDROID(gt_path,evaluate_path,seq_list,iter_num):
    results = list()
    for i in range(1,iter_num + 1):
        print("for {} time".format(i))
        one_result = list()
        for j in range(len(seq_list)):
            print_flag = False
            gt_seq_path = gt_path + "/" + seq_list[j] + "/groundtruth.txt"
            #eva_seq_path =  evaluate_path + "/" + seq_list[j] + "_{}".format(i) + ".txt"
            eva_seq_path =  evaluate_path + "/" + seq_list[j] + "_full/traj.tum"
            if not os.path.exists(eva_seq_path):
                continue
            cmd_eva = "evo_ape tum {} {} -a".format(gt_seq_path,eva_seq_path)
            eva_count = len(open(eva_seq_path,'r').readlines())

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
        results.append(one_result)
    return results

def EvaluationNoRemove(gt_path,evaluate_path,seq_list,iter_num):
    results = list()
    for j in range(len(seq_list)):
        one_result = list()
        for i in range(1,iter_num + 1):
            print_flag = False
            seq_iter_name = seq_list[j] + "_{}".format(i)
            gt_seq_path = gt_path + "/" + seq_list[j] + "/groundtruth.txt"
            eva_seq_path =  evaluate_path + "/" + seq_list[j] + "_{}".format(i) + ".txt"
            
            if not os.path.exists(eva_seq_path):
                continue
            cmd_eva = "evo_rpe tum {} {} -a".format(gt_seq_path,eva_seq_path)
            eva_count = len(open(eva_seq_path,'r').readlines())

            res = subprocess.check_output(cmd_eva, shell=True)
            res = str(res)
            result = res.split("\\n")
            gt_count = len(open(gt_seq_path,'r').readlines())
            for info in result:
                detail = info.split("\\t")
                if(detail[0].strip() == "rmse"):
                    one_result.append([seq_iter_name,float(detail[1]),eva_count])
            one_result = sorted(one_result,key = lambda x:-x[1])   

    
        sum = 0
        min_seq_iter_name = 1
        max_seq_iter_name = 1
        min_ape = 999
        max_ape = -1
        for i in range(0,len(one_result)):
            print(one_result[i])
            if(one_result[i][1] > max_ape):
                max_seq_iter_name = one_result[i][0]
                max_ape = one_result[i][1]
            if(one_result[i][1] < min_ape):
                min_seq_iter_name = one_result[i][0]
                min_ape = one_result[i][1]
            sum = sum + float(one_result[i][1])

        # if len(one_result) < iter_num:
        #     continue

        sum = sum / len(one_result) * 1.0 
           
        results.append(one_result)
        print("average: ",sum,'\n')
        for i in range(0,len(one_result)):
            print(one_result[i][1],end = ',')
        print("end")
        
        #visualization
        # eva_seq_path =  evaluate_path + "/" + min_seq_iter_name + ".txt"
        # print(max_seq_iter_name)
        # cmd_eva = "evo_ape tum {} {} -a -p".format(gt_seq_path,eva_seq_path)
        # res = subprocess.check_output(cmd_eva, shell=True)
    return results

def GetAverageResult(results):
    results_array = np.array(results)
    average_ape = np.mean(results_array,axis=0)
    median_ape = np.median(results_array,axis=0)
    print(median_ape)

def SaveResult(results,save_path):
    results_array = np.array(results)
    results_array = results_array.transpose()
    np.savetxt(save_path,results_array,delimiter = ",")

def GetPartPose(old_path,erase_num,new_path):
    poses = OpenTUMPose(old_path,False)
    save_num = int(len(poses)) - int(erase_num)
    new_poses = poses[-save_num:]
    SaveTUMPose(new_path,new_poses,False)


gt_path = "/media/zhouxin/66D231E0D231B4E15/Dataset/ICL-NUIM/depth_noise"
#eva_path = "/home/zhouxin/GitHub/Uncertain_SLAM/resultICL/加上外点" #Uncertain_SLAM ORB_SLAM2
seq_list_path = "/home/zhouxin/evaluation/ICL/seq_list.txt"
seq_list = ReadSequence(seq_list_path)

#orbslam3
#eva_path = "/home/zhouxin/project/ORB_SLAM3/resultICL" #Uncertain_SLAM ORB_SLAM2
#EvaluationNoRemove(gt_path,eva_path,seq_list,7)

#orbslam2
#eva_path = "/home/zhouxin/GitHub/ORB_SLAM2/resultICL" #Uncertain_SLAM ORB_SLAM2
#EvaluationNoRemove(gt_path,eva_path,seq_list,10)
#EvaluationWithName(gt_path,eva_path,seq_list,15)
#EvaluatePlus(gt_path,eva_path,seq_list,9)

#Ela
#eva_path = "/home/zhouxin/graduation/补充实验/补充实验轨迹/Ela/ICL_weak_ICP" 
#SolveElaTimeStamp(eva_path)
#EvaluateEla(gt_path,eva_path,seq_list,1)

#kin
#eva_path = "/home/zhouxin/graduation/补充实验/补充实验轨迹/kin/ICL" 
#EvaluateKin(gt_path,eva_path,seq_list,1)

#DVO
# eva_path = "/home/zhouxin/graduation/补充实验/补充实验轨迹/DVO/ICL_minus_y" 
# EvaluateDVO(gt_path,eva_path,seq_list,1)

eva_path = "/home/zhouxin/graduation/补充实验/补充实验轨迹/DROID/results" 
EvaluateDROID(gt_path,eva_path,seq_list,1)
