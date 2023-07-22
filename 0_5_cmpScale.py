import trimesh


my = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/5_ycb_scale/014_lemon.off'
liu = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/Grasp Dataset/good_shapes/ycb_014_lemon_scaled.obj.smoothed.off'

my = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/5_ycb_scale/011_banana.off'
liu = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/Grasp Dataset/good_shapes/ycb_011_banana_scaled.obj.smoothed.off'

my = trimesh.load(my)
liu = trimesh.load(liu)
print(my.scale)
print(liu.scale / my.scale)