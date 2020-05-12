Space Escape Episode 03
===

*** The reason im doing this tutorial in episodes instead of all at once is so it can evolve over time so to help the community as best it can. that said we have our first contribution! after the fact of losing standard functionality of classes with python by not using Instances i ran a few tests and found that we can return the built in functionality while maintaining only a single instance by creating a Singleton. Attribution for this Episode goes to @mikael for helping improve quality ***

> main focus this Episode will be converting our `EventManager` into a singleton.
> > *"The singleton pattern is a design pattern that restricts the instantiation of a class to one object."*
> we add the magic Dunder method `__new__` so we can set our classmethod `_instance` so we can maintain the singleton status by returning `cls._instance` if `cls._instance` is not `None` to `__init__`.

```python
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
```

> In `Main` we grab a refernce to `EventManager` from `HUD`

```python
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
```

> Inside HUD lets ceate our initial instance of `EventManager` since this is our Top Level Object. then after setting our `SceneView` we call start for `HUD.event_manager.start` which `main` and `hud` inside `HUD.event_manager` and set our game state andin turn present our main menu.

```python

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
```    

> we will call it here for this one and it wont feel like we did anything but in the long run this Episode will help our project 10-fold.
