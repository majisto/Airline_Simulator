import sge

class I_Obj(sge.dsp.Object):
    def __init__(self, x, y, sprite, obj_name, z=1):
        super(I_Obj, self).__init__(x=x, y=y, z=z, sprite=sprite)
        self.obj_name = obj_name
    def get_name(self):
        return self.obj_name