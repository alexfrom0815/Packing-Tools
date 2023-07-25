from shutil import copyfile
import os


# source = '../final_data/IR_concaveArea3_nomin/vhacd_with_pose/board'
source = '../final_data/IR_concaveArea3_nomin/pointCloud_with_pose/board'

allF = os.listdir(source)
for f in allF:
    name = f.replace('_0.npz', '.npz')
    print(f)
    print(name)
    copyfile(os.path.join(source, f), os.path.join(source, name))