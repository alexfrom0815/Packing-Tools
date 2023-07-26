class colorObj(object):
    def __init__(self, RGBA, \
    H = 0.5, S = 1.0, V = 1.0,\
    B = 0.0, C = 0.0):
        self.H = H # hue 色调
        self.S = S # saturation 饱和
        self.V = V # value 明度
        self.RGBA = RGBA
        self.B = B # birghtness 亮度
        self.C = C # contrast 对比度