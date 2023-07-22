# commands
# dataName = 'shapeNet'
# dataName = 'modelNet'
dataName = 'abc'

# scale
step1 = 'python 1_scale.py --in_dir=/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/1_{}_off --out_dir=/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/1_{}_obj_scaled/'.format(dataName, dataName)

# 2_fusion.py --mode=render --in_dir=examples/1_scaled/ --depth_dir=examples/2_depth/ --out_dir=examples/2_watertight/
step2 = 'python 2_fusion.py --mode=render --in_dir=/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/1_{}_obj_scaled/ --depth_dir=/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/2_{}_obj_depth/ --out_dir=/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/2_{}_obj_watertight/'.format(dataName, dataName, dataName)

# 2_fusion.py --mode=fuse --in_dir=examples/1_scaled/ --depth_dir=examples/2_depth/ --out_dir=examples/2_watertight/
step3 = 'python 2_fusion.py --mode=fuse --in_dir=/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/1_{}_obj_scaled/ --depth_dir=/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/2_{}_obj_depth/ --out_dir=/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/2_{}_obj_watertight/'.format(dataName, dataName, dataName)
# python 2_fusion.py --mode=fuse --in_dir=/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/1_ycb_obj_scaled/ --depth_dir=/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/2_ycb_obj_depth/ --out_dir=/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/2_ycb_obj_watertight/

# python 3_simplify.py --in_dir=examples/2_watertight/ --out_dir=examples/3_out/
step4 = 'python 3_simplify.py --in_dir=/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/2_{}_obj_watertight/ --out_dir=/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/3_{}_obj_out/'.format(dataName, dataName)
# python 3_simplify.py --in_dir=/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/2_ycb_obj_watertight/ --out_dir=/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/3_ycb_obj_out/

print(step1)
print(step2)
print(step3)
print(step4)