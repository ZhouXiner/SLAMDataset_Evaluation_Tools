import sys
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
                f.write("{} {} {} {} {} {} {} {}\n".format(pose[0],pose[1],pose[2],pose[3],pose[4],pose[5],pose[6],pose[7]))



def ChangePose(poses):
    for pose in poses:
        pose[0] = float(pose[0])*1e-9
    return poses

def s2ns(path,new_path):
    for seq in os.listdir(path):
        old_seq_path = path + "/" + seq
        new_seq_path = new_path + "/" + seq
        old_poses = OpenTUMPose(old_seq_path,False)
        new_poses = ChangePose(old_poses)
        SaveTUMPose(new_seq_path,new_poses,False)

old_path = "/home/zhouxin/evaluation/TUM_VI/gt_ns"
new_path = "/home/zhouxin/evaluation/TUM_VI/gt_s"

s2ns(old_path,new_path)
# pose_path = "/home/zhouxin/evaluation/TUM_VI/gt/Room3.csv"
# save_path = "/home/zhouxin/evaluation/TUM_VI/gt/Room3.txt"
# pose = OpenTUMPose(pose_path,True)
# SaveTUMPose(save_path,pose,False)