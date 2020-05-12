'''
Space Escape Episode 03
main.py
'''

from lib import *

def A():
    return Action

class EventManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, *arg, **kwargs):
        self.main=None
        self.hud=None
        self.game_state=None
    
    def start(self, main, hud):
        self.main=main
        self.hud=hud
        self.game_state=GameState.MAIN_MENU
        self.main.view.hidden=True
        self.hud.add_subview(MainMenu())
        
    def update(self, dt):
        pass

    def touch_began(self, touch):
        pass

    def touch_moved(self, touch):
        pass
  
    def touch_ended(self, touch):
        pass
                    
    def __getattr__(self, name):
        return getattr(self.instance, name)

class Main(Scene):
    def setup(self):
        self.event_manager=self.view.superview.event_manager
        
    def did_change_size(self):
        pass

    def update(self):
        self.event_manager.update(self.dt)

    def touch_began(self, touch):
        self.event_manager.touch_began(touch)

    def touch_moved(self, touch):
        self.event_manager.touch_moved(touch)

    def touch_ended(self, touch):
        self.event_manager.touch_ended(touch)

class HUD(ui.View):
    def __init__(self, *args, **kwargs):
        self.background_color='#66492a'
        self.event_manager=EventManager()
        
        # Game Window
        self.main = SceneView(
                scene=Main(), frame=(5, 5, Screen.x-10, Screen.y-10),
                anti_alias=True, frame_interval=1,
                shows_fps=True, background_color='#2c00ff')
        self.add_subview(self.main)
        self.event_manager.start(self.main.scene, self)
        
if __name__=='__main__':
    HUD().present('fullscreen', hide_title_bar=True)

