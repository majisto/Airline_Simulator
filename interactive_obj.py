import sge

class I_Obj(sge.dsp.Object):
    def __init__(self, x, y, sprite, obj_name, z=1, visible=True, check_collisions=False, active=False, tangible=True):
        super(I_Obj, self).__init__(x=x, y=y, z=z, sprite=sprite, visible=visible, checks_collisions=check_collisions,
                                    active=active, tangible=tangible)
        self.obj_name = obj_name
    def get_name(self):
        return self.obj_name

class Hud_Obj(sge.dsp.Object):
    def __init__(self, x, y, sprite, obj_name, z=1, visible=True, check_collisions=False, active=False, tangible=False):
        super(Hud_Obj, self).__init__(x=x, y=y, z=z, sprite=sprite, visible=visible, checks_collisions=check_collisions,
                                    active=active, tangible=tangible)
        self.obj_name = obj_name

    def get_name(self):
        return self.obj_name