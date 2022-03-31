import argparse
import sys
import os
import numpy


def read_file_list(filename):
    """
    Reads a trajectory from a text file. 
    
    File format:
    The file format is "stamp d1 d2 d3 ...", where stamp denotes the time stamp (to be matched)
    and "d1 d2 d3.." is arbitary data (e.g., a 3D position and 3D orientation) associated to this timestamp. 
    
    Input:
    filename -- File name
    
    Output:
    dict -- dictionary of (stamp,data) tuples
    
    """
    file = open(filename)
    data = file.read()
    lines = data.replace(","," ").replace("\t"," ").split("\n") 
    list = [[v.strip() for v in line.split(" ") if v.strip()!=""] for line in lines if len(line)>0 and line[0]!="#"]
    list = [(float(l[0]),l[1:]) for l in list if len(l)>1]
    return dict(list)

def associate(first_list, second_list,offset,max_difference):
    """
    Associate two dictionaries of (stamp,data). As the time stamps never match exactly, we aim 
    to find the closest match for every input tuple.
    
    Input:
    first_list -- first dictionary of (stamp,data) tuples
    second_list -- second dictionary of (stamp,data) tuples
    offset -- time offset between both dictionaries (e.g., to model the delay between the sensors)
    max_difference -- search radius for candidate generation

    Output:
    matches -- list of matched tuples ((stamp1,data1),(stamp2,data2))
    
    """
    first_keys = first_list.keys()
    second_keys = second_list.keys()
    potential_matches = [(abs(a - (b + offset)), a, b) 
                         for a in first_keys 
                         for b in second_keys 
                         if abs(a - (b + offset)) < max_difference]
    potential_matches.sort()
    matches = []
    for diff, a, b in potential_matches:
        if a in first_keys and b in second_keys:
            first_keys.remove(a)
            second_keys.remove(b)
            matches.append((a, b))
    
    matches.sort()
    return matches

if __name__ == '__main__':
    data_path = "/media/zhouxin/66D231E0D231B4E12/Dataset/TUM_RGBD/TUM"
    dirs = os.listdir(data_path)
    for sequence_dir in dirs:
        sequence_path = os.path.join(data_path, sequence_dir)
        rgb_path = sequence_path + "/rgb.txt"
        depth_path = sequence_path + "/depth.txt"
        accosiate_path = sequence_path + "/" + sequence_dir + ".txt"
        remove_cmd = "rm {}".format(accosiate_path)
        os.system(remove_cmd)
        print(rgb_path,depth_path,accosiate_path)
        first_list = read_file_list(rgb_path)
        second_list = read_file_list(depth_path)
        matches = associate(first_list, second_list,0,0.02) 
        with open(accosiate_path,"w") as file:
            for a,b in matches:
                file.write("%f %s %f %s\n"%(a," ".join(first_list[a]),b," ".join(second_list[b])))
