'''
Space Escape Episode 02
main.py
'''


from lib import *


def A():
    return Action

class EventManager(object):
    main=None
    hud=None
    game_state=GameState.MAIN_MENU
    
    @classmethod
    def setup(cls, *args):
        cls.main=args[0]
        cls.hud=args[1]
        # FIXME: Added if block
        if cls.game_state == GameState.MAIN_MENU:
            cls.main.view.hidden=True
            cls.hud.add_subview(Menu(name='main-menu'))

    @classmethod
    def update(cls, dt):
        pass

    @classmethod
    def touch_began(cls, touch):
        pass

    @classmethod
    def touch_moved(cls, touch):
        pass

    @classmethod
    def touch_ended(cls, touch):
        pass

class Main(Scene):
    def setup(self):
        pass

    def did_change_size(self):
        pass

    def update(self):
        EventManager.update(self.dt)

    def touch_began(self, touch):
        EventManager.touch_began(touch)

    def touch_moved(self, touch):
        EventManager.touch_moved(touch)

    def touch_ended(self, touch):
        EventManager.touch_ended(touch)

class HUD(ui.View):
    def __init__(self, *args, **kwargs):
        self.background_color='#66492a'

        # Game Window
        self.main = SceneView(
                scene=Main(), frame=(5, 5, Screen.x-10, Screen.y-10),
                anti_alias=True, frame_interval=1,
                shows_fps=True, background_color='#2c00ff')
        self.add_subview(self.main)
        EventManager.setup(self.main.scene, self)
        
        

if __name__=='__main__':
    HUD().present('fullscreen', hide_title_bar=True)

