Space Escape Episode 01
===

***First step is to setup our Scene, View, and EventManager***

### Import:

> `ui` Module is imported within `scene` Module and by importing scene using the `*` wildcard we can access `ui` through scene.
>using `*` is the same as saying:

> `from scene import all`

>there is no Performance gain from this and if you import ui yourself it will use the same instance used within scene. only gain here is ww save a line of code.

>*Create a new script named `main.py`*

```python

from scene import *

```

---

## Globals:
> Avoid using Global Variables. Couple reasons for this is scene's EventLoop doesnt handle them properly and second there is no functionality to them. with a function you can apply Logic before returning the value and you return a new object each time so our Event loop does not need to maintain a reference to it. 

`A() => Action` will be used for creating Animations In Later Episodes.

```python

def A():
	return Action

```

---

## EventManager
> We will only have one `EventManager` each game session. Therefore we will not be using `self` to refer to an instance. Instead we will us `cls` to refer to the `class` object. Everything works just about the same only bug difference is we will be uing a Decorator for our methods called `@classmethod` this provides access to our `class` `variables` just like we would using `self`. 

*`@classmethod` stores a copy of the class `dict` inside `cls`*

> `EventManager` will be used to handle all the interactions between our game objects and Touch Events.  We will Alo hanle and Timers we need to here. 

- `EventManager.main` 
- - reference to our `Scene` object

- `EventManager.hud`[^hud]
- - reference to our `View` object.

```python
class EventManager(object):
    main=None
    hud=None
```

- `EventManager.setup(*args)`[^args]
- - Called before `Scene.setup()` inside our `HUD.__init__()`


```python
    @classmethod
    def setup(cls, *args):
        cls.main=args[0]
        cls.hud=args[1]
        
```

- `EventManager.update(dt)`[^dt]
- - Called every frame from `Scene.update` and passed dt to be used with timers


```python
    @classmethod
    def update(cls, dt):
        pass
```

- `EventManager.touch_began()`, `EventManager.touch_moved()`, `EventManager.touch_ended()`
- - Touch events send from `Scene` object

```python
    @classmethod
    def touch_began(cls, touch):
        pass

    @classmethod
    def touch_moved(cls, touch):
        pass
    
    @classmethod
    def touch_ended(cls, touch):
        pass
```
---

## Main:
> Standard `Scene` setup providing all event calls to `EventManager`

```python
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
```

## HUD:
> main `view` container to hold all our ui elements. we are only setting our `SceneView` to display our Game's windown and calling `EventManager.setup` passing our `HUD` and `Main` refrences.

```python
class HUD(ui.View):
	def __init__(self, *args, **kwargs):
		# Game Window
		self.main = SceneView(
			scene=Main(), frame=(5, 5, 600, 800),
			anti_alias=True,frame_interval=1,
			shows_fps=True, background_color='#2c00ff')
		self.add_subview(self.main)
		EventManager.setup(self.main.scene, self)
```

>Finally if we are running this Script and not Importing it then present our game Windows!

if __name__=='__main__':
    HUD().present('fullscreen', hide_title_bar=True)


---

In the next Episode we will start some Presetting And Setup Our Draft of the main menu



---

[^args]: args, kwargs, list arguments and dict keyword arguments 
[^hud]: hud, Heads Up Diplay.
[^dt]: dt, DeltaTime, Time passed since last Frame. Set every Frame.
