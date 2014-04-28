from pymouse import PyMouse

class DotaCamera:
    """
    API for controlling a Dota 2 replay camera.
    Since Dota 2 has no way to control a replay camera directly, we simulate this
    by using Python mouse events to click on the minimap.
    
    For now, this supports only 2560x1440 resolution.
    """
    
    MAP_SIZE = (17408, 15872)
    #MINIMAP = (14, 1080, 361, 343)
    MINIMAP = (1000, 500, 100, 100)
    
    def __init__(self):
        """
        Initialize with the specified screen resolution width and height.
        """
        
        self.mouse = PyMouse()
        
    def set(self, x, y):
        """
        Sets the camera to the specified location.
        
        Args:
            x   the x coordinate in game units
            y   the y coordinate in game units
        """
        
        MINIMAP = DotaCamera.MINIMAP
        MAP_SIZE = DotaCamera.MAP_SIZE
        
        # y actually starts at bottom, not top
        y = -y
        
        # Translate coordinates
        x += MAP_SIZE[0] / 2
        y += MAP_SIZE[1] / 2
        
        # Scale to minimap coordinates
        new_x = (float(x) / MAP_SIZE[0]) * MINIMAP[2] + MINIMAP[0]
        new_y = (float(y) / MAP_SIZE[1]) * MINIMAP[3] + MINIMAP[1]
        
        self.mouse.click(new_x, new_y)
    