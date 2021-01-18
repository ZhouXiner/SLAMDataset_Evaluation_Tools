for i in 00 01 02 03 04 05 06 07 08 09 10
do
python3 /home/zhouxin/GitHub/evo/contrib/kitti_poses_and_timestamps_to_trajectory.py "/home/zhouxin/data1/data-1/Dataset/KITTI/gt/"$i".txt" "/home/zhouxin/data1/data-1/Dataset/KITTI/"$i"/times.txt" "/home/zhouxin/data1/data-1/Dataset/KITTI/gt/"$i"_tum.txt"
done