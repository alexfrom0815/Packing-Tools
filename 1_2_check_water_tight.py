import os
import trimesh


# 基本上都不是watertight的
# 另外一个事情是, 加载的材质贴图写在原来的obj文件里面
# 下一步, 补全成waterTight的
alllength = []
# source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/apc_obj'
# source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/YCB_obj'
# source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/Grasp Dataset/good_shapes'
# source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/3_apc_obj_out'
# source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/3_YCB_obj_out'
# source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/4_apc_good'
# source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/4_YCB_good'
# source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/YCB_dataset/YCB_obj'
# source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing/0_rss_scale'

# source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing/0_apc_scale'
# source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing/0_rss_scale'
# source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/3_packing/0_ycb_scale'
# source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/1_modelNet_off'
# source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/1_sort/1_shapeNet_off'
source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/process/2_reconstruct/3_abc_obj_out'


for f in os.listdir(source):
    print(f)
    mesh = trimesh.load_mesh(os.path.join(source,f))
    print(mesh.is_watertight)
    # print(mesh.bounds[0])
    print(mesh.scale)
    print(len(mesh.faces))
    # alllength.append(len(mesh.faces))
# print(min(alllength))

# # modelNet 40
# # 这里面的face是真不少
# source = '/media/hang/f9f4716a-9f6f-4c7a-b604-6f088954bdef/dataset/ModelNet40'
# for cate in os.listdir(source):
#     for t_v in os.listdir(os.path.join(source, cate)):
#         for f in os.listdir(os.path.join(source, cate, t_v)):
#             file = os.path.join(source,cate,t_v,f)
#             mesh = trimesh.load_mesh(file)
#             # print(mesh.is_watertight)
#             print(len(mesh.faces))
