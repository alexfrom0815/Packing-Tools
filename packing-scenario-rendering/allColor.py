import sys
import os
# if os.path.exists('/home/hang/Documents/GitHub/IRBPP/picture/BlenderToolbox'):
#     sys.path.append('/home/hang/Documents/GitHub/IRBPP/picture/BlenderToolbox') # change this to your path to “path/to/BlenderToolbox/
# elif os.path.exists('/home/dell/zhaohang/IRBPP/picture/BlenderToolbox'):
#     sys.path.append('/home/dell/zhaohang/IRBPP/picture/BlenderToolbox')
# else:
#     assert os.path.exists('/home/zhaohang/zhaohang/IRBPP/picture/BlenderToolbox')
#     sys.path.append('/home/zhaohang/zhaohang/IRBPP/picture/BlenderToolbox') # change this to your path to “path/to/BlenderToolbox/
import BlenderToolBox as bt
import numpy as np

allColor = [
  bt.derekBlue,
  bt.coralRed,
  bt.iglGreen,
  bt.caltechOrange,
  bt.royalBlue,
  bt.royalYellow,
  bt.white,
  bt.black,
  bt.cb_black,
  bt.cb_orange,
  bt.cb_skyBlue,
  bt.cb_green,
  bt.cb_yellow,
  bt.cb_blue,
  bt.cb_vermillion,
  bt.cb_purple,
]
# Fan Wang Container
boxBrown = np.array([0.6, 0.3, 0.1])
allColor.append(boxBrown)
# ICLR COLOR
allColor.append(np.array([215, 155, 0]) * 1.0 / 255) # deep brown
allColor.append(np.array([251, 232, 222]) * 1.0 / 255) # light brown
allColor.append(np.array([108, 141, 190]) * 1.0 / 255) # deep blue
allColor.append(np.array([220, 239, 255]) * 1.0 / 255) # light blue
allColor.append(np.array([84,  130, 53]) * 1.0 / 255) # deep green
allColor.append(np.array([217, 241, 221]) * 1.0 / 255) # light green
allColor.append(np.array([205, 158, 166]) * 1.0 / 255) # dark red
allColor.append(np.array([146, 206, 80]) * 1.0 / 255) # figure3 green
allColor.append(np.array([159, 199, 192]) * 1.0 / 255) # figure3 dark green
allColor.append(np.array([155, 194, 230]) * 1.0 / 255) # figure3 bule
allColor.append(np.array([197, 181, 239]) * 1.0 / 255) # figure3 green
allColor.append(np.array([255, 202, 204]) * 1.0 / 255) # figure3 pink
allColor.append(np.array([255, 123, 127]) * 1.0 / 255) # figure3 red
allColor.append(np.array([244, 175, 132]) * 1.0 / 255) # figure3 oringe
allColor.append(np.array([245, 244, 194]) * 1.0 / 255) # figure3 ricewhite
allColor.append(np.array([255, 217, 102]) * 1.0 / 255) # figure3 yellow
# qijin color
allColor.append(np.array([241, 175, 176]) * 1.0 / 255) # robot pink
allColor.append(np.array([183, 234, 150]) * 1.0 / 255) # robot green
allColor.append(np.array([234, 209, 110]) * 1.0 / 255) # robot yellow
allColor.append(np.array([134, 204, 203]) * 1.0 / 255) # robot cyan
allColor.append(np.array([109, 135, 212]) * 1.0 / 255) # robot blue
allColor.append(np.array([151, 131, 205]) * 1.0 / 255) # robot purple
allColor.append(np.array([222, 79,  79]) * 1.0 / 255) # robot red
allColor.append(np.array([146, 168, 215]) * 1.0 / 255) # robot dark blue
allColor.append(np.array([223, 174, 255]) * 1.0 / 255) # paper purple
allColor.append(np.array([255, 220, 151]) * 1.0 / 255) # paper yellow
allColor.append(np.array([153, 204, 255]) * 1.0 / 255) # paper light blue
allColor.append(np.array([96,  108, 245]) * 1.0 / 255) # paper deep blue
allColor.append(np.array([220, 89,  80]) * 1.0 / 255) # paper red