"""
UI factory
"""

def app_factory(interface=None):
    if not interface or interface == 'fremantle':
        from diabetto.ui.fremantle_ui.fremantle_ui import MainWidget
        return MainWidget
    elif interface == 'diablo':
        from diabetto.ui.diablo_ui.diablo_ui import MainWidget
        return MainWidget
    else:
        raise ValueError('%s: unsupported UI type' % interface)
