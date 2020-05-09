Space Escape Episode 01
===

***to begin lets create a python script called `lib.py`***

> To start lets move our `scene` import into this file so we have access to all the needed objects from `scene` and `ui` in this episode we will start our Settings class so lets add `sound` import also.

```python
from scene import *
from sound import *
```

## Clamp():
> Clamp will be used quite often in you game development. if you dont have it in your personel lib file in `site-packages` id suggest adding this today. 

```python
def Clamp(val, min, max):
    if val <= min:
        return min
    if val >= max:
        return max
    return val
```

## GAME_STATE:
> Our first Enumerator. Used to monitor what our game is currently doing. The Constant members should never be 0, but Enum constants  can be nearly anything. in a future Episode we will use functions.

```python
class GameState(Enum):
    MAIN_MENU=1
    CHARACTER_MENU=2
    IN_LEVEL=3
    CLOSING_GAME=4
```

## Screen:
> Convenience access to screen size functions.

```python
class Screen(object):
    x, y = get_screen_size()
    half_x, half_y, = x/2, y/2

    @classmethod
    def center(cls, offset_x, offset_y):
        return (cls.half_x-offset_x, cls.half_y-offset_y)

    @classmethod
    def Full(cls):
        return (cls.x, cls.y)

    def Perc(cls, px, py):
        return(cls.x/100*px, cls.y/100*py)
```

## Settings:
> Here we will set asmany game related values. this makes debugging, tuneing and testing  so much easier. today we just setup `sound` volume.
we also use `@property` decorator. when you do this you can call the method(now property) without `()` but our main purpose is to set both `Settings.efx_volume` and `sound.set_volume` at the same time. you can set a `setter` , `getter` and `deleter` for each property. here we only need the `setter` because `getter` is automaticaly set when we call `@property`

```python
class Settings(object):
    def __init__(self, efx_volume=0.5, **kwargs):
        self.efx_volume=efx_volume
        sound.set_volume(self.efx_volume)

        self.game_dificulty=2
    
    @property
    def Volume(self):
        return self.efx_volume

    @Volume.setter
    def Volume(self, val):
        self.efx_volume=Clamp(val, 0.0, 1.0)
        sound.set_volume(Clamp(val, 0.0, 1.0))
```

## Menu_Button:
> Just a custom button. this will be changed over time. 

```python
class Menu_Button(ui.View):
    def __init__(self, menu, text, position, action=None,  *args, **kwargs):
        self.background_color='#c9a277'
        self.width=menu.width/3*2
        self.height=menu.height/5
        self.x, self.y = position
        self.flex='WH'
        self.border_color='#000000'
        self.border_width=5
        self.corner_radius=10
        self.button=ui.Button()
        self.button.x=10
        self.button.y=10
        self.button.width=self.width-20
        self.button.height=self.height-20
        self.button.bg_color='#f5c591'
        self.button.tint_color='#683905'
        self.button.border_color='#fff0b9'
        self.button.title=text
        self.button.action=action
        self.add_subview(self.button)
```

## Menu:
> at the moment justa visual container. this will be more interesting later. right now just has quit method to close the game.

```python
class Menu(ui.View):
    def __init__(self, *args, **kwargs):
        self.background_color='#818181'
        self.border_color='#000000'
        self.border_width=10
        self.corner_radius=8
        self.width, self.height = (300, 500)
        self.x, self.y = Screen.center(self.width/2, self.height/2)
        self.add_subview(Menu_Button(self, 'New Game', (50, 50)))
        self.add_subview(Menu_Button(self, 'Load Game', (50, 150)))
        self.add_subview(Menu_Button(self, 'Settings', (50, 250)))
        self.add_subview(Menu_Button(self, 'Quit', (50, 350), action=self.quit))
        
    def quit(self, sender):
        self.superview.close()
```

*before we close this one out we have just a couple changes inside `main.py` to make..*

first we need to replace `from scene import *` with `from lib import *`

>easy enough now we just need change the following..
- set out HUD.background_color to `#66492a` or whatever you like.
- then change our `SceneView.frame` to `frame=(5, 5, Screen.x-10, Screen.y-10)`  
