"""
UI factory
"""

def app_factory(interface=None):
    if not interface or interface == 'fremantle':
        from diabetto.ui.fremantle_ui.fremantle_ui import FremantleDiabetto
        return FremantleDiabetto()
    elif interface == 'diablo':
        from diabetto.ui.diablo_ui.diablo_ui import DiabloDiabetto
        return DiabloDiabetto()
    else:
        raise ValueError('%s: unsupported UI type' % interface)
