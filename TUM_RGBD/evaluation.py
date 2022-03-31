import subprocess
import numpy as np
import os

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

def EvaluationNoRemove(gt_path,evaluate_path,seq_list,iter_num):
    results = list()
    for j in range(len(seq_list)):
        one_result = list()
        for i in range(1,iter_num + 1):
            print_flag = False
            seq_iter_name = seq_list[j] + "_{}".format(i)
            gt_seq_path = gt_path + "/" + seq_list[j] + "/groundtruth.txt"
            eva_seq_path =  evaluate_path + "/" + seq_iter_name + ".txt"
            
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
        
        if len(one_result) < iter_num:
            continue

        sum = sum / iter_num
           
        results.append(one_result)
        print("average: ",sum,'\n')

        for i in range(0,len(one_result)):
            print(one_result[i][1],end = ',')
        print("end")

        #visualization
        # eva_seq_path =  evaluate_path + "/" + min_seq_iter_name + ".txt"
        # cmd_eva = "evo_ape tum {} {} -a -p".format(gt_seq_path,eva_seq_path)
        # res = subprocess.check_output(cmd_eva, shell=True)
    return results

def EvaluateEla(gt_path,evaluate_path,seq_list,iter_num):
    results = list()
    for i in range(1,iter_num + 1):
        print("for {} time".format(i))
        one_result = list()
        for j in range(len(seq_list)):
            print_flag = False
            gt_seq_path = gt_path + "/" + seq_list[j] + "/groundtruth.txt"
            #eva_seq_path =  evaluate_path + "/" + seq_list[j] + "_{}".format(i) + ".txt"
            eva_seq_path =  evaluate_path + "/" + seq_list[j] + ".klg.freiburg"
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
                    print(seq_list[j],detail[1],gt_count,eva_count)
                    one_result.append(float(detail[1]))
                    print_flag = True
            if not print_flag:
                print(seq_list[j],"wrong")
                one_result.append(float(1e3))
        results.append(one_result)
    return results

def EvaluateKin(gt_path,evaluate_path,seq_list,iter_num):
    results = list()
    for i in range(1,iter_num + 1):
        print("for {} time".format(i))
        one_result = list()
        for j in range(len(seq_list)):
            print_flag = False
            gt_seq_path = gt_path + "/" + seq_list[j] + "/groundtruth.txt"
            #eva_seq_path =  evaluate_path + "/" + seq_list[j] + "_{}".format(i) + ".txt"
            eva_seq_path =  evaluate_path + "/" + seq_list[j] + ".klg.poses"
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
                    print(seq_list[j],detail[1],gt_count,eva_count)
                    one_result.append(float(detail[1]))
                    print_flag = True
            if not print_flag:
                print(seq_list[j],"wrong")
                one_result.append(float(1e3))
        results.append(one_result)
    return results

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
                cmd_eva = "evo_ape tum {} {} -a -p".format(gt_seq_path,eva_part_path)
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

def EvaluatePlus(gt_path,evaluate_path,seq_list,iter_num):
    results = list()
    for j in range(len(seq_list)):
        for w in range(5,100,5):
            one_result = []
            for i in range(1,iter_num + 1):
                print_flag = False
                gt_seq_path = gt_path + "/" + seq_list[j] + "/groundtruth.txt"
                #eva_seq_path =  evaluate_path + "/" + seq_list[j] + "_{}".format(i) + ".txt"
                eva_seq_path =  evaluate_path + "/" + seq_list[j] + "_{}_{}".format(i,w) + ".klg.freiburg"
                
                cmd_eva = "evo_ape tum {} {} -a".format(gt_seq_path,eva_seq_path)
                eva_count = len(open(eva_seq_path,'r').readlines())

                res = subprocess.check_output(cmd_eva, shell=True)
                res = str(res)
                result = res.split("\\n")
                gt_count = len(open(gt_seq_path,'r').readlines())
                for info in result:
                    detail = info.split("\\t")
                    if(detail[0].strip() == "rmse"):
                        one_result.append(float(detail[1]))
                        print_flag = True
                if not print_flag:
                    print(seq_list[j],"wrong")
                    one_result.append(float(1e3))
            print(seq_list[j])
            GetAverageResult(one_result)
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


gt_path = "/media/zhouxin/66D231E0D231B4E15/Dataset/TUM_RGBD/TUM"
seq_list_path = "/home/zhouxin/evaluation/TUM_RGBD/seq_list.txt"
seq_list = ReadSequence(seq_list_path)

#ORBSLAM3
# eva_path = "/home/zhouxin/project/ORB_SLAM3/resultTUM1"
# EvaluationNoRemove(gt_path,eva_path,seq_list,10)

# eva_path =  "/home/zhouxin/graduation/补充实验/补充实验一致性轨迹/BADSLAM"
# EvaluationNoRemove(gt_path,eva_path,seq_list,10)

#ELAFUSION
# eva_path = "/home/zhouxin/graduation/补充实验/补充实验轨迹/Ela/TUM"
# EvaluateEla(gt_path,eva_path,seq_list,1)

#kin
eva_path = "/home/zhouxin/graduation/补充实验/补充实验轨迹/kin/TUM"
EvaluateKin(gt_path,eva_path,seq_list,1)
