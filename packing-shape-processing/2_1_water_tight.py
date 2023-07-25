# commands
dataName = 'ycb'

# Download the watertight reconstruction code from: https://github.com/autonomousvision/occupancy_networks/tree/master/external/mesh-fusion
# Execute the following commands in the terminal to get the watertight meshes.

# scale
step1 = 'python 1_scale.py --in_dir=/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/1_{}_off --out_dir=/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/1_{}_obj_scaled/'.format(dataName, dataName)
step2 = 'python 2_fusion.py --mode=render --in_dir=/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/1_{}_obj_scaled/ --depth_dir=/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/2_{}_obj_depth/ --out_dir=/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/2_{}_obj_watertight/'.format(dataName, dataName, dataName)
step3 = 'python 2_fusion.py --mode=fuse --in_dir=/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/1_{}_obj_scaled/ --depth_dir=/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/2_{}_obj_depth/ --out_dir=/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/2_{}_obj_watertight/'.format(dataName, dataName, dataName)
step4 = 'python 3_simplify.py --in_dir=/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/2_{}_obj_watertight/ --out_dir=/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/3_{}_obj_out/'.format(dataName, dataName)

print(step1)
print(step2)
print(step3)
print(step4)