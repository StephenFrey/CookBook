'''
╔═══════════════════════════════════════════════════════════════
║    					:SPACE ESCAPE:
║	This minimal game was writen with the intention to help others with 
║	game development using the scene module in pythonista. The coding style
║	is None.. The way code was deigned was an attempt to provide examples of
║	the deferent ways of implementing aspects of a game environment. 
║	
║	None of this is meant to diplay the most "correct" or proformnce 
║	effecient way of writing a game.
║	
║		SPACE ESCAPE is a very simple "Flappy Bird" style game (pres and hold 
║	to Asend. you are an alientrying to escape an enemy mining base while 
║	harvesters deliver Ore backto the Refinery. grab as many Shield PowerUps
║	as you can. this grants you a 30 sec shield with 100 
║	durability.. you get up to 2 choices topass the harvesters. 
║	
║		- Soft Ore (Darker)
║		- Short Stacks. (Over the top)
║		
║		The Rich ore will turn read and deal damage if you pass through it,
║	the Soft ore will Turn Green. as a bonus you grab a hand full of 
║	soft ore as you pass and store it. 
║	the damage is too your Equipment and if you run out your strap will
║	break and and jet flying off to explode as you fall so be carfull.. 
║	the jetpaxk is nuklear powered and wont be a small kaboom..
║	
║	..the nerd stuff aside.. 
║
║	Provided are breif comments on the classes and a couple Methods. All 
║	questions or comment requests are welcome. I didnt comment everything 
║	so the code is easy to read and i attempted at mainly using a iscriptive
║	naminh scheme. 
║	
║	Never Ending level.
║	
║	Hopfully everyone enjoys and  and i hope this helps someone out there.
╚═══════════════════════════════════════════════════════════════
'''

from scene import *
import random
import math
import time

a = Action

'''
╔═══════════════════════════════════════════════════════════════
║        :Config:
║	Easy access Variables. I use it for debuging and I either 
║	keep it as first class of script or i give it its own module
║	in this case I'm using it just like a settings object that
║	can be used in  setting menu.
║	
║	Lway have my Color Pallet and textual settings like Font 
║	Family
╚═══════════════════════════════════════════════════════════════
'''
class Config:
	#Debugging
	def ViewTriggers():return False
	
	# Score
	def points():return 5
	
	
	#Timers
	def ShieldTimer():return 30
	def ShieldSpawnTimer():return 30
	
	def ObsticleSpawnTimer():
		return random.randrange(3, 6)
		
	#Damage
	def MeteorHitDamage(): return 30
	def MotorHitDamage(): return 80
	
	#text
	def font():return 'Marker Felt'
	def fontSize():return 28
	
	@classmethod
	def Font(cls, f=None, s=None):
		f=cls.font() if f == None else f
		s=cls.fontSize() if s == None else s
		return (f, s)
		
		
	
	#Colors
	def Black(): return '#000'
	def Gray(): return '#888'
	def White(): return '#fff'
	def Blue(): return '#00f'
	def Red(): return '#f00'
	def Geen(): return '#0f0'
	def Yellow(): return '#ff0'
	def SkyBlue(): return '#0ff'
	def Lime(): return '#0f8'
	def Purplw(): return '#80f'
	def Magenta(): return '#f0f'
	def Pink(): return '#f8f'
	def Brown(): return '#840'
	def Gold(): return '#fb2'
'''
╔═══════════════════════════════════════════════════════════════
║       :EventManager:
║	Used as a bridge between objects that normaly would
║	never see eachother. Alo alows access between objects sooner
║	than normal
║
║	by using →  def Include(cls, other): 
║	you can then override Tick method aswell as the Touch methods
║	from SceneNode. EventManager will then pass data long as it
║	recieves it. Technically most of your game can be controlled
║	from here as long as you call Include in all your class 
║	__init__ constructors.
║	
║	Handles Object Spawns aswell
╚═══════════════════════════════════════════════════════════════
'''
class EventManager:
	
	dependents=[]
	main=None
	spawnQue=[]
	runTime=float(0.0)
	gameObjects=None
	player=None
	powerUps=[]
	
	needsTouch=[]
	allTouches=[]
	canClose=False
	closeTimer=4
	powerUpTimer=0
	
	@classmethod
	def Setup(cls, other):
		if(cls.main is None):
			cls.main = other
			
			
	@classmethod
	def Include(cls, other):
		cls.dependents.append(other)
	
	
	@classmethod
	def PowerUpSpawner(cls, dt, game):
		if(cls.powerUpTimer > 0):
			cls.powerUpTimer-=dt
			if(cls <= 0):
				cls.powerUps.append(game)
				
	@classmethod
	def QueSpawn(cls, data):
		cls.spawnQue.append(data)
		
	@classmethod
	def Spawner(cls, dt, game):
		if(cls.spawnQue and not game.gameOver):
			cls.spawnQue[0].timer -= dt
			if(cls.spawnQue[0].timer < 0):
				if(cls.powerUps):
					cls.spawnQue[0].brush.add_child(cls.powerUps[0])
					cls.powerUps.remove(cls.powerUps[0])
				cls.main.add_child(cls.spawnQue[0].brush)
				cls.spawnQue.remove(cls.spawnQue[0])
				
	@classmethod
	def Pass(cls, dt, game):
	
		cls.Spawner(dt, game)
		if(cls.dependents):
			for dep in cls.dependents:
				if(hasattr(dep, 'Tick')):
					dep.Tick(game, dt, cls.runTime)
				if(hasattr(dep, 'position') ):
					if(dep.position[0] < -128):
						game.Obsticle_Out_Of_Bounds(dep)
						cls.dependents.remove(dep)
		if(game.gameOver):
			if(cls.closeTimer > 0):
				cls.closeTimer -= dt
				if(cls.closeTimer < 0):
					cls.canClose=True
					
	def touch_began(cls, touch):
		if(cls.needsTouch):
			for node in cls.needsTouch:
				node.touch_began(touch)
		cls.player.touch_began(touch)
		cls.allTouches.append(touch)
		
	def touch_moved(cls, touch):
		if(cls.needsTouch):
			for node in cls.needsTouch:
				node.touch_moved(touch)
		cls.player.touch_moved(touch)
		
	def touch_ended(cls, touch):
		if(cls.needsTouch):
			for node in cls.needsTouch:
				node.touch_ended(touch)
		cls.player.touch_ended(touch)


'''
╔═══════════════════════════════════════════════════════════════
║        :Spawn:
║	Simple 'Form' i call it to pass to EventManager for Spawning
║	Objects
╚═══════════════════════════════════════════════════════════════
'''
class Spawn:
	def __init__(self, brush, timer):
		self.brush=brush
		self.timer=timer
'''
╔═══════════════════════════════════════════════════════════════
║        :Screen:
║	Handle or screen positioning and Sizing
╚═══════════════════════════════════════════════════════════════


'''
class Screen:
	def Width():
		return get_screen_size()[0]
		
	def Hieght():
		return get_screen_size()[1]
	
	
	def Full():
		return get_screen_size()
	
	@classmethod
	def Center(cls, offsetX=0, offsetY=0):
		x=cls.Width()/2-offsetX
		y=cls.Hieght()/2-offsetY
		return Point(x, y)
		
	@classmethod
	def TopCenter(cls, offsetX=0, offsetY=128):
		x=cls.Width()/2-offsetX
		y=cls.Hieght()-offsetY
		return Point(x, y)
	
	def BottomCenter(cls, offsetX=0, offsetY=128):
		x=cls.Width()/2-offsetX
		y=cls.Hieght()+offsetY
		return Point(x, y)
	
	@classmethod
	def Orientation(cls):
		return PORTRAIT if cls.Width() < cls.Hieght() else LANDSCAPE
		
'''
╔═══════════════════════════════════════════════════════════════
║        :Animations:
║	container class or Game Animation Templates.
║	can either Create instance for each object or just cll as 
║	class for each animation when needed i.e
║		self.animation=Nimation(self)
║					or
║		Animation(self).Pulse(-1, 0.3)
║	
║	not all Methodbsignatures are the same.
╚═══════════════════════════════════════════════════════════════
'''
class Animation:
	def __init__(self, node):
		self.node=node
		
		
	def ScoreTravel(self, x, meth,  t=TIMING_LINEAR):
		self.node.run_action(
		a.group(
		a.sequence(
		a.move_to(x[0]-95, x[1]-165, 2, t),
		a.wait(0),
		a.call(meth)),
		a.sequence(
		a.scale_to(3, 2, t),
		a.scale_to(0, 3, t)),
		a.sequence(
		a.fade_to(1, 2, t),
		a.fade_to(0, 3, t),
		a.remove())
		))
		
	def ForceField(self, speed, repeat=-1, t=TIMING_ELASTIC_IN_OUT):
		def color_to(node, progress):
			node.color='#09dfff' if random.random() < 0.5 else '#0016ff'
		fade=[]
		scale=[]
		rotate=[]
		for x in range(100):
			val=random.random()
			if val < 0.5:
				val = 0.5
			mod=random.random()
			fade.append(a.fade_to(val-0.4, speed, t))
			fade.append(a.call(color_to, 0.1))
			if val < 0.6:
				val = 0.8
			rotate.append(a.rotate_by(val*5, speed, t))
			scale.append(a.scale_y_to(val, speed, t))
			scale.append(a.scale_x_to(val, speed, t))
		self.node.run_action(
		a.repeat(
		a.group(
		a.sequence(fade),a.sequence(scale), a.sequence(rotate)),repeat))
		
		
	def Shine(self, speed, repeat=-1, t=TIMING_LINEAR):
		self.node.run_action(
		a.repeat(
		a.group(
		a.sequence(
		a.rotate_by(10, speed, t),
		a.rotate_by(7, speed, t)),
		a.sequence(
		a.scale_to( 0.5, speed, t),
		a.scale_to(0.1, speed, t))
		
		),repeat))
		
	def PowerUpFloat(self, speed, repeat=-1, t=TIMING_LINEAR):
		self.node.run_action(
		a.repeat(
		a.group(
		a.sequence(
		a.move_to(100, 800, speed, t),
		a.move_to(100, self.node.position[1]-200, speed, t)),
		
		a.sequence(
		a.rotate_to(-0.10, speed, t),
		a.rotate_to(0.10, speed, t))
		
		),repeat))
		
	def Vibrate(self, repeat, speed, t=TIMING_LINEAR):
		self.node.run_action(
		a.repeat(
		a.group(
		a.sequence(
		a.move_by( 5, 5, speed, t),
		a.move_by(-5,-5, speed, t),
		a.move_by(-5, 5, speed, t),
		a.move_by( 5,-5, speed, t)),
		a.sequence(
		a.scale_y_by( 0.1, speed, t),
		a.scale_y_by(-0.1, speed, t),
		a.scale_y_by( 0.1, speed, t),
		a.scale_y_by(-0.1, speed, t))
		),repeat))
	def Drive(self, repeat, speed, t=TIMING_LINEAR):
		self.node.run_action(a.move_to(
		-Screen.Width()+128, self.node.position[1], speed,t))
		
	def Bounce(self, repeat, speed, t=TIMING_LINEAR):
		self.node.run_action(
		a.repeat(
		a.group(
		a.sequence(
		a.move_by(0, 5, speed, t),
		a.move_by(0,-5, speed, t),
		a.move_by(0, 5, speed, t),
		a.move_by(0,-5, speed, t)),
		a.sequence(
		a.scale_y_by( 0.1, speed, t),
		a.scale_y_by(-0.1, speed, t),
		a.scale_y_by( 0.1, speed, t),
		a.scale_y_by(-0.1, speed, t))
		),repeat))
		
	def Spin(self, repeat, speed, t=TIMING_LINEAR):
		self.node.run_action(
		a.repeat(
		a.group(
		a.sequence(
		a.rotate_by(1, speed, t))
		),repeat))
		
	def Pulse(self, mod=0, repeat=-1, speed=0.5, t=TIMING_LINEAR):
		def color_to(node, progress):
			node.color='#aef4ff' if random.random() < 0.5 else '#00deff'
		fade=[]
		scale=[]
		
		for x in range(100):
			val=random.random()
			if val < 0.5:
				val = 0.5
			mod=random.random()
			fade.append(a.fade_to(val-0.2, speed, t))
			fade.append(a.call(color_to, 0.1))
			if val < 0.6:
				val = 0.8
			scale.append(a.scale_y_to(val+val*mod, speed, t))
		self.node.run_action(
		a.repeat(
		a.group(
		a.sequence(fade),a.sequence(scale)),repeat))
		
	def Hover(self, repeat, speed, t=TIMING_SINODIAL):
		def color_to(node, progress):
			node.color='#b1ff00' if random.random() < 0.5 else '#6fff00'
		move=[]
		rotate=[]
		scale=[]
		for x in range(100):
			mv=random.randrange(25, 50)
			move.append(a.move_by(0, mv, speed*0.5, t))
			move.append(a.move_by(0, -mv, speed*0.5, t))
			rotate.append(a.rotate_by(-random.randrange(1, 10)*random.random(), speed*5, TIMING_LINEAR))
			rotate.append(a.rotate_by(random.randrange(1, 10)*random.random(), speed*5, TIMING_LINEAR))
			
		for x in range(100):
			ry=random.random()
			rx=random.random()
			if rx < 0.85:
				rx=0.85
			if ry < 0.85:
				ry=0.85
			scale.append(a.scale_y_to(ry, speed*rx*0.1, t))
			scale.append(a.scale_y_to(1, speed*ry*0.1, TIMING_ELASTIC_IN_OUT))
			scale.append(a.scale_x_to(rx, speed*rx*0.1, t))
			scale.append(a.scale_x_to(1, speed*ry*0.1, TIMING_ELASTIC_IN_OUT))
			
		self.node.run_action(
		a.repeat(
		a.group(
		a.sequence(move),
		a.sequence(rotate),
		a.sequence(scale)),repeat))
		
	def Descend(self, repeat=0, duration=10, t=TIMING_LINEAR):
		self.node.run_action(
		a.repeat(
		a.group(
		a.sequence(
		a.move_by(0, -32, duration, t))
		),repeat), 'playerMove')
		
	def Ascend(self, repeat=0, duration=10, t=TIMING_LINEAR):
		self.node.run_action(
		a.repeat(
		a.group(
		a.sequence(
		a.move_by(0, 32, duration, t))
		),repeat), 'playerMove')
		
	def ActivatePowerup(self, t=TIMING_LINEAR):
		self.node.run_action(
			a.group(
				a.sequence(
					a.move_to(Screen.Width()/2, Screen.Hieght()-128, 1, t),
					a.wait(3),
					a.move_to(30.00, 340.00, 1, t)),
				a.sequence(
					a.scale_to(4, 1, t),
					a.wait(4),
					a.fade_to(0.0, 2, t)),
				a.sequence(
					a.wait(5),
					a.scale_to(0, 1.5, t),
					a.wait(3),
					a.remove())),'powerup activated')
		
	def ResizeBar(self, val, t=TIMING_LINEAR):
		self.node.run_action(a.scale_x_to(val, 0.5, t))
		
	def QuitMessage(self, t=TIMING_LINEAR):
		self.node.run_action(
		a.group(a.sequence(
		a.scale_to(3, 2, t),
		a.scale_to(0, 3, t)),
		a.sequence(
		a.wait(2),
		a.rotate_by(999, 4, t)),
		a.sequence(
		a.wait(5),
		a.remove())),'powerup activated')
		
		
	def PlayerShield(self, speed=0.1, t=TIMING_ELASTIC_IN_OUT):
		def color_to(node, progress):
			node.color='#0016ff' if random.random() < 0.5 else '#0059ff'
		fade=[]
		scale=[]
		rotate=[]
		for x in range(100):
			val=random.random()
			if val < 0.5:
				val = 0.5
			mod=random.random()
			fade.append(a.fade_to(val-0.2, speed, t))
			fade.append(a.call(color_to, 0.1))
			if val < 0.6:
				val = 0.8
			rotate.append(a.rotate_by(val*5, speed, t))
			scale.append(a.scale_y_to(val, speed, t))
			scale.append(a.scale_x_to(val, speed, t))
		self.node.run_action(
		a.repeat(
		a.group(
		a.sequence(fade),a.sequence(scale), a.sequence(rotate)),-1))
		
'''
╔═══════════════════════════════════════════════════════════════
║        :Sprite⇒SpriteNode⇒Node:
║	
║	Simple Sprite Class to add some propertie to all SpriteNode
║	Objects when Subclassed.
╚═══════════════════════════════════════════════════════════════
'''
class Sprite(SpriteNode):
	def __init__(self,texture, tag='UISprite', anchor_point=(0.0, 0.0),
	*args, **kwargs):
		self.anchor_point=anchor_point
		self.animate=Animation(self)
		self.tag=tag
		self.texture=texture
		super().__init__(texture=self.texture,
		anchor_point=self.anchor_point, *args, **kwargs)
		
'''
╔═══════════════════════════════════════════════════════════════
║        	:Block⇒9Sprit⇒SpriteNode⇒Node:
║	
║	Used as building locks for Brushes but can also be use as
║	standalong GameObjects. i.e. Stone, Dirt, Grass and sky are 
║	not used in brushes but also i try not to Animate a block 
║	alone by it self but it doest hurt to do so.
╚═══════════════════════════════════════════════════════════════
'''
class Block(Sprite):
	def __init__(self, texture, isGapObject=False, *args, **kwargs):
		self.animate=Animation(self)
		self.isGapObject=isGapObject
		super().__init__(texture=texture, *args, **kwargs)
		EventManager.Include(self)
		
		
	def Tick(self, game, dt, runTime):
		if(self.tag != 'effect'):
			pass
'''
╔═══════════════════════════════════════════════════════════════
║       				 :Brush:
║	Consists of multiple Block Objects. Generally Brush objects
║	are what you see on the screen other than UI elements. the 
║	two brushes in this game is the Obsticle and Shield PowerUp.
║	the powerup mostly is visual effects where the obsticle is
║	used for User Imersion. what i mean by this is it has Blocks
║	and animations that look familier to a large group of gamers.
║	this allows for you, the developer, some extra space to play
║	with your own creativity. in this case i used this extra
║	creative "space" on the player object.
║	
║	Pretty much you can think of Blocks as Legos and Brushes as
║	the structures you make with them. then bring them to life
║	with Actions (Animations)
╚═══════════════════════════════════════════════════════════════
'''	
class Brush(Node):
	def __init__(self, isObsticle, tag, spawnTimer=5, *args, **kwargs):
		EventManager.Include(self)
		self.animate=Animation(self)
		self.isObsticle=isObsticle
		self.tag=tag
		self.size=Size(32, 32)
		self.spawnTimer=random.randrange(2, 7)
		self.spawn=Spawn(self, self.spawnTimer)
		super().__init__(*args, **kwargs)
		
	def Brush_Should_Spawn(self):
		EventManager.QueSpawn(self.spawn)
		pass
		
	def __call__(self):
		self.Brush_Should_Spawn()
		return self.spawnTimer
		
	def Tick(self, sender, dt, runTime):
		pass
'''
╔═══════════════════════════════════════════════════════════════
║       				 :PowerUp:
║	Simple Powerup/Bonus/Buff type Object. Usually this object
	class would be more robust but i made just basic functionality
╚═══════════════════════════════════════════════════════════════
'''
class PowerUp(SpriteNode):
	def __init__(self,texture, tag='PowerUp', Duration=None, speedMod=None, clearPath=False, shieldBoost=False, *args, **kwargs):
		self.animate=Animation(self)
		self.anchor_point=(0.5, 0.5)
		self.tag=tag
		self.texture=texture
		self.duration=Duration
		self.shieldBoost=shieldBoost
		self.respawnTime=10
		super().__init__(texture=self.texture,
		anchor_point=self.anchor_point, *args, **kwargs)
		EventManager.Include(self)
		
	def Tick(self, sender, dt, runTime):
		pass
		
	def Activate(self):
		self.remove_all_actions()
		self.position=Point(Screen.Width()/2, Screen.Hieght()/2)
		self.animate.ActivatePowerup()
		
		
'''
╔═══════════════════════════════════════════════════════════════
║        :GameObjects:
║	Container/factory class for the Sprites and Blocks used in 
║	Brushes.
║
║	*Annotations apon request
╚═══════════════════════════════════════════════════════════════
'''
class GameObjects:
	def __init__(self, pNode):
		self.pNode=pNode
		self.SkyBlockSize=64
		self.GoundBlockSize=64
		self.GroundHeight=3
		self.Floor=self.GroundHeight*self.GoundBlockSize
		self.WheelSize=120
		self.EngineSize=128
		self.GeneratorSize=64
		self.CrateSize=48
		self.CrateBuffer=16
		self.SkyColor='#056472'
		self.meteorID=0
		self.meteorTextures=[  'spc:MeteorGrayBig1',    'spc:MeteorGrayBig2', 
		'spc:MeteorGrayBig3',  'spc:MeteorGrayBig4',    'spc:MeteorGrayMed1',
		'spc:MeteorGrayMed2',  'spc:MeteorGraySmall1',  'spc:MeteorGraySmall2', 
		'spc:MeteorGrayTiny1', 'spc:MeteorGrayTiny2']
							
		
	def Shield(self, z):
		b=PowerUp(texture=Texture('spc:ShieldSilver'),tag='powerup shield')
		b.position=Point(0, 0)
		b.shielBoost=True
		b.duration=Config.ShieldTimer()
		b.color='#2cff00'
		b.z_poition=z
		b.scale=1.25
		return b
		
	def ShineyPoint(self, z):
		b=Block(texture=Texture('spc:Star1'), tag='effect')
		b.position=Point(12, 12)
		b.anchor_point=(0.5, 0.5)
		b.animate.Shine(0.5)
		b.z_poition=z
		return b
		
	def Bubble_A(self, z):
		b=Block(texture=Texture('spc:Shield1'),
		tag='effect')
		b.position=Point(0, 0)
		b.anchor_point=(0.5, 0.5)
		b.animate.ForceField(0.3, t=TIMING_LINEAR)
		b.size=Size(80, 80)
		b.rotation=5
		b.z_poition=z
		return b
		
	def Bubble_B(self, z):
		b=Block(texture=Texture('spc:Shield2'),
		tag='effect')
		b.position=Point(0, 0)
		b.anchor_point=(0.5, 0.5)
		b.animate.ForceField(0.5, t=TIMING_EASE_IN_OUT)
		b.size=Size(80, 80)
		b.rotation=10
		b.z_poition=z
		return b
		
	def Bubble_C(self, z):
		b=Block(texture=Texture('spc:TurretBaseBig'),
		tag='effect')
		b.position=Point(0, 0)
		b.anchor_point=(0.5, 0.5)
		b.animate.ForceField(0.05)
		b.size=Size(80, 80)
		b.z_position=0
		b.alpha=0.25
		b.rotation=3
		b.z_poition=0
		return b
		
	def Grass(self, x, y):
		b=Sprite(texture=Texture('plf:Ground_GrassMid'),
		parent=self.pNode)
		b.size=Size(self.GoundBlockSize, self.GoundBlockSize)
		b.position=(self.GoundBlockSize*x, self.GoundBlockSize*y)
		return b
		
	def Dirt(self, x, y):
		b=Sprite(texture=Texture('plf:Ground_GrassCenter'),
		parent=self.pNode)
		b.size=Size(self.GoundBlockSize, self.GoundBlockSize)
		b.position=(self.GoundBlockSize*x, self.GoundBlockSize*y)
		return b
		
	def Stone(self, x, y):
		b=Sprite(texture=Texture('plf:Ground_DirtCenter'),
		parent=self.pNode)
		b.size=Size(self.GoundBlockSize, self.GoundBlockSize)
		b.position=(self.GoundBlockSize*x, self.GoundBlockSize*y)
		return b
		
	def meteor(self, y, x=0, z=1, isGap=False):
		chosen=(random.choice(self.meteorTextures))
		b=Block(isGapObject=isGap,
		texture=Texture(chosen),
		tag=f'Meteor {self.meteorID}',
		size=Size(64, 64))
		self.meteorID+=1
		b.color='#fbfbfb'
		b.position=Point(x, y)
		b.z_position=z
		b.rotation=random.randrange(1, 9)
		b.anchor_point=(0.5, 0.5)
		b.animate.Hover(-1, 2)
		
		return b
		
	def meteorGap(self, y, x=0, z=1, isGap=True):
		chosen=(random.choice(self.meteorTextures))
		b=Block(isGapObject=isGap,
		texture=Texture(chosen),
		tag=f'gap')
		self.meteorID+=1
		b.color='#5e3100'
		b.size=Size(self.CrateSize, self.CrateSize)
		b.position=Point(x, y)
		b.z_position=z
		b.rotation=random.randrange(1, 5)
		b.anchor_point=(0.5, 0.5)
		b.animate.Hover(-1, 2)
		
		return b
		
	def Sky(self, x, y):
		b=Block(texture=Texture('plf:Ground_PlanetCenter'),
		tag='effect',
		parent=self.pNode)
		b.size=Size(self.SkyBlockSize, self.SkyBlockSize)
		b.position=(self.SkyBlockSize*x, Screen.Hieght()-self.SkyBlockSize*y)
		b.color=self.SkyColor
		b.alpha=1.0
		return b
		
	def Wheel(self, z, x=0):
		b=Block(texture=Texture('plf:Enemy_Saw_dead'),
		tag='effect',
		parent=self.pNode)
		b.anchor_point=(0.5, 0.5)
		b.size=Size(self.WheelSize, self.WheelSize)
		b.position=(x, b.size[1]/2-12)
		b.z_position=z
		b.alpha=1.0
		b.animate.Spin(-1, 0.8)
		return b
		
	def Engine(self, z, x=0):
		b=Block(texture=Texture('plf:LaserDown'),
		tag='engine',
		parent=self.pNode)
		b.anchor_point=(0.5, 0.6)
		b.size=Size(self.EngineSize, self.EngineSize)
		b.position=(x, b.size[1]/2-10)
		b.z_position=z
		b.alpha=1.0
		b.rotation=math.radians(90)
		b.animate.Vibrate(-1, 0.05)
		return b
		
	def Generator(self, z, x=0):
		b=Block(texture=Texture('spc:Engine2'),
		tag='effect',
		parent=self.pNode)
		b.anchor_point=(0.5, 0.0)
		b.size=Size(self.GeneratorSize, self.GeneratorSize)
		b.position=(x, 100)
		b.z_position=z
		b.alpha=1.0
		b.animate.Bounce(-1, 0.05)
		return b
		
	def Beam(self, z, x=0):
		b=Block(texture=Texture('spc:Fire18'),
		tag='effect',
		parent=self.pNode)
		b.anchor_point=(0.5, 0.0)
		b.size=Size(self.GeneratorSize, self.GeneratorSize*4)
		b.position=(x, 160)
		b.z_position=z
		b.alpha=random.random()
		b.animate.Pulse(mod=0, repeat=-1, speed=0.1)
		return b

'''
╔═══════════════════════════════════════════════════════════════
║      			  :Brushes:
║	Objexts used in the game such as powerups and obsticles
╚═══════════════════════════════════════════════════════════════
'''
class Brushes:
	def __init__(self, game):
		self.game=game
		self.crateMin=200
		self.crateMax=800
		self.gaps=list()
		self.gapSize=4
		self.gapMin=3
		self.gapMax=6
		self.gameObjects=self.game.gameObjects
		self.startPos=Point(Screen.Width()+128, self.gameObjects.Floor)
		self.ShieldBoost()
		
	def ShieldBoost(self):
		n=Brush(isObsticle=True,
		tag='powerup shield',
		spawnTimer=random.randrange(16,30),
		position=Point(100,400),
		z_position=20)
		
		n.animate.PowerUpFloat(2, t=random.randrange(0, 16))
		n.add_child(self.gameObjects.Shield(9))
		n.add_child(self.gameObjects.ShineyPoint(2))
		n.add_child(self.gameObjects.Bubble_A(3))
		n.add_child(self.gameObjects.Bubble_B(4))
		n.add_child(self.gameObjects.Bubble_C(0))
		EventManager.powerUps.append(n)
		
	def _buildPillar(self, node):
		gapSize=random.randrange(self.gapMin, self.gapMax)
		slots=round((self.crateMax-self.crateMin)/
		self.gameObjects.CrateSize)-gapSize
		
		gap_root=random.randrange(1, slots+1)
		gap=[]
		for slot in range(gap_root, gap_root + gapSize):
			gap.append(slot)
		self.gaps.append(gap)
		for i in range(1, slots+2):
			x=self.crateMin+(
			(self.gameObjects.CrateSize+self.gameObjects.CrateBuffer)*i)
			if i not in gap:
				m=self.gameObjects.meteor(x)
				self.game.items.append(m)
				node.add_child(m)
			else:
				gapCrate=self.gameObjects.meteorGap(
				x+self.gameObjects.CrateBuffer)
				gapCrate.alpha=0.5
				gapCrate.isGapObject=True
				node.add_child(gapCrate)
				
	def StandardObsticle(self):
		n=Brush(isObsticle=True,
		tag='Standard Obsticle',
		spawnTimer=random.randrange(3,6),
		position=self.startPos,
		z_position=11)
		n.add_child(self.gameObjects.Wheel(4))
		n.add_child(self.gameObjects.Engine(1))
		n.add_child(self.gameObjects.Generator(3))
		n.add_child(self.gameObjects.Beam(2))
		self._buildPillar(n)
		n.animate.Drive(0, 15)
		return n
'''
╔═══════════════════════════════════════════════════════════════
║    				    :Trigger:
║	Used as a "Behind the Scenes" collision detection. Trigger
║	Objects Align with the Block Objects at the Scene coordinate
║	Level and fires hit events with the Player object. Used to 
║	check if player is in a gap, hitting a wall or collecting a 
║	powerups
║	Setting Config.ViewTriggers to True will show the hitBox area
║	for Trigger and has different Colors acording to the Block 
║	Object it is attached to.
╚═══════════════════════════════════════════════════════════════
'''
class Trigger(SpriteNode):
	def __init__(self, t, target, brush, *args, **kwargs):
		EventManager.Include(self)
		self.hitboxTextures=['spc:PowerupBlueShield', 'spc:PowerupGreenStar', 'spc:PowerupYellow','spc:PowerupRedBolt']
		self.z_position=100 if Config.ViewTriggers() else -100
		self.texture=Texture(self.hitboxTextures[t])
		self.size=target.size
		self.target=target
		self.brush=brush
		self.alpha=0.5
		self.offset=GameObjects(self).Floor
		
	def Tick(self, game, dt, runTime):
	
		x=self.brush.position[0]+self.target.position[0]
		y=self.target.position[1]+self.offset
		self.position=Point(x, y)
		
		if(x < -128):
			self.run_action(a.remove())
'''
╔═══════════════════════════════════════════════════════════════
║        :InfoBox:
║	A Basic hud display for the player data.
║		- Hitpoints (as bar)
║		- Shield Points (as bar)
║		- Score
║		
║	I use two LabelNodes for the Score to give the Shadow effect
║	There are many ways of doing this but this was a simple 
║	example.
╚═══════════════════════════════════════════════════════════════
'''
class InfoBox(SpriteNode):
	def __init__(self, player):
		self.player=player
		self.texture=Texture('plf:Tile_Sign')
		self.color='#ffe792'
		self.size=Size(200, 250)
		self.z_position=100
		self.score=0
		self.anchor_point=(0.0, 0.0)
		self.position=Point(5, GameObjects(self).Floor-5)
		self.hpIcon=SpriteNode(
		Texture('plf:HudHeart_full'),
		color='#ff0000',
		size=Size(36, 36),
		position=Point(25, self.size[1]-64),
		parent=self)
		
		self.hpBarBg=SpriteNode(
		texture=None,
		color='#c10000',
		anchor_point=(0.0, 0.5),
		size=Size(125, 20),
		position=Point(60, self.size[1]-64),
		parent=self)
		
		self.hpBar=SpriteNode(
		texture=None,
		color='#00c111',
		z_position=1,
		anchor_point=(0.0, 0.5),
		x_scale=self.player.hitPoints/100,
		size=Size(125, 20),
		position=Point(60, self.size[1]-64),
		parent=self)
		
		self.shieldIcon=SpriteNode(
		Texture('spc:ShieldSilver'),
		color='#dcfbff',
		size=Size(32, 32),
		position=Point(25, self.size[1]-100),
		parent=self)
		
		self.shieldBarBg=SpriteNode(
		texture=None,
		color='#c10000',
		anchor_point=(0.0, 0.5),
		size=Size(125, 20),
		position=Point(60, self.size[1]-100),
		parent=self)
		
		self.shieldBar=SpriteNode(
		texture=None,
		color='#006bb0',
		x_scale=self.player.shieldPoints/100,
		z_position=1,
		
		anchor_point=(0.0, 0.5),
		size=Size(125, 20),
		position=Point(60, self.size[1]-100),
		parent=self)
		
		self.scoreIcon=SpriteNode(
		Texture('spc:MeteorBrownMed2'),
		color='#dcfbff',
		size=Size(42, 42),
		position=Point(25, self.size[1]-140),
		parent=self)
		
		self.scoreVal=LabelNode(
		text=str(self.player.scene.score),
		font=Config.Font(s=24),
		anchor_point=(0.0, 0.5),
		y_scale=1.5,
		x_scale=1,
		color='#000000',
		position=Point(57, self.size[1]-142),
		parent=self)
		
		self.scoreVal2=LabelNode(
		text=str(self.player.scene.score),
		font=Config.Font(s=24),
		y_scale=1.5,
		x_scale=1,
		anchor_point=(0.0, 0.5),
		color='#ffc800',
		z_position=1,
		position=Point(60, self.size[1]-140),
		parent=self)
		
	def UpdateData(self):
		pass
		
	def AnimateHP(self, val):
		Animation(self.hpBar).ResizeBar(val)
		
	def AnimateShield(self, val):
		Animation(self.shieldBar).ResizeBar(val)
		
'''
╔═══════════════════════════════════════════════════════════════
║        Player Class
║        Connects with:
║                EventManager
║                GameObjects
║
║        Dmonstrates setting up Sprites for player states:
║                - ilde (standing)
║                - Falling/gliding
║                - climbing/ascending
║                - death
║                - 2 separate jetPack flames
║                - initial dual flame hover(only at game start)
║                - Activated Shield
╚═══════════════════════════════════════════════════════════════
'''
class Player(SpriteNode):
	def __init__(self):
		self.texture=Texture('spc:Shield1')
		self.color='#ffffff'
		self.anchor_point=(0.0, 0.0)
		self.size=Size(80, 80)
		self.tag='Player'
		self.z_position=99
		self.animate=Animation(self)
		self.shieldActive=False
		EventManager.player=self
		EventManager.Include(self)
		
		self.gameObjects=GameObjects(self)
		
		self.up=Sprite(texture=Texture('plf:AlienPink_swim1'))
		self.up.alpha=1.0
		self.up.rotation=0
		self.up.z_position=9
		self.up.position=Point(0.0, 0.0)
		
		self.idle=Sprite(texture=Texture('plf:AlienPink_stand'))
		self.idle.alpha=0.0
		self.idle.rotation=0
		self.idle.z_position=9
		self.idle.position=Point(0.0, 0.0)
		
		self.down=Sprite(texture=Texture('plf:AlienPink_hit'))
		self.down.alpha=0.0
		self.down.rotation=0
		self.down.z_position=9
		self.down.position=Point(0.0, 0.0)
		
		self.jetpack=Sprite(texture=Texture('spc:Gun2'))
		self.jetpack.alpha=1.0
		self.jetpack.rotation=-0.2
		self.jetpack.scale=1
		self.jetpack.x_scale=1
		self.jetpack.z_position=5
		self.jetpack.position=Point(3, 10)
		
		self.idleJet=Sprite(texture=Texture('spc:Fire1'))
		self.idleJet.alpha=0.0
		self.idleJet.rotation=0.0
		self.idleJet.scale=1
		self.idleJet.y_scale=0.75
		self.idleJet.x_scale=1
		self.idleJet.color='#00deff'
		self.idleJet.z_position=1
		self.idleJet.anchor_point=(0.0, 1.0)
		self.idleJet.position=Point(0, 0)
		self.idleJet.animate.Pulse(mod=0, speed=1)
		self.jetpack.add_child(self.idleJet)
		
		self.liftJet=Sprite(texture=Texture('spc:Fire9'))
		self.liftJet.scale=2
		self.liftJet.y_scale=3
		self.liftJet.x_scale=0.5
		self.liftJet.color='#00deff'
		self.liftJet.z_position=1
		self.liftJet.anchor_point=(0.0, 1.0)
		self.liftJet.position=Point(5, 0)
		self.liftJet.animate.Pulse(mod=3, speed=0.01  )
		self.jetpack.add_child(self.liftJet)
		
		self.shield=SpriteNode(texture=Texture('spc:TurretBaseBig'))
		self.shield.scale=1
		self.shield.color='#00deff'
		self.shield.z_position=50
		self.shield.anchor_point=(0.5, 0.5)
		self.shield.size=Size(135, 140)
		self.shield.position=Point(32, 32)
		Animation(self.shield).PlayerShield(speed=0.2, t=TIMING_LINEAR)
		
		self.dead=Sprite(texture=Texture('plf:AlienPink_duck'))
		self.dead.alpha=0.0
		self.dead.rotation=0
		self.dead.z_position=9
		self.dead.position=Point(0.0, 0.0)
		
		self.add_child(self.dead)
		self.add_child(self.up)
		self.add_child(self.down)
		self.add_child(self.idle)
		
		self.add_child(self.jetpack)
		self.ChangePose(2)
		self.position=Point(Screen.Width()/2 ,Screen.Hieght()/2)
		
		self.PowerUpTimer=0.0
		
		self.hitPoints=100
		self.shieldPoints=0
		self.AnimationQue=[]
		
		self.inQue=False
		self.isDead=False
		
	def StartSheild(self):
		self.add_child(self.shield)
		self.AddSP(100)
		self.PowerUpTimer=Config.ShieldTimer()
		self.shieldActive=True
		
	def EndSheild(self):
		self.shield.remove_from_parent()
		self.shieldPoints=0
		Animation(self.scene.infoBox.shieldBar).ResizeBar(0)
		self.PowerUpTimer=0.0
		self.shieldActive=False
		
	def touch_began(self, touch):
		self.ChangePose(1)
		self.idleJet.remove_from_parent()
		self.jetpack.add_child(self.liftJet)
		self.animate.Ascend(duration=0.15)
		
		if self.isDead != False:
			self.scene.gameOver=True
			self.isDead=True
			self.ChangePose(4)
	def touch_moved(self, touch):
		pass
		
	def touch_ended(self, touch):
		self.ChangePose(2)
		self.animate.Descend(duration=0.2)
		self.liftJet.remove_from_parent()
		self.jetpack.add_child(self.idleJet)
		
	'''
╔═══════════════════════════════════════════════════════════════
║	RemoveSP/AddSP and RemoveHP/AddHP
║	Controls for increasing nd decreaing HitPoints (Helth)
║	and ShieldPoints.
║	Talks to InfoBox through Main (SceneNode) to adjust gui
║	values.
╚═══════════════════════════════════════════════════════════════
	'''
	def RemoveSP(self, val):
		sp=self.shieldPoints-val
		if(sp > 0):
			self.shieldPoints = sp
			Animation(self.scene.infoBox.shieldBar).ResizeBar(sp/100)
		elif(sp < 0):
			self.shieldPoints = 0
			Animation(self.scene.infoBox.shieldBar).ResizeBar(0)
			self.EndSheild()
			
	def AddSP(self, val):
		sp=self.shieldPoints + val
		if(sp > 100):
			self.shieldPoints=100
			Animation(self.scene.infoBox.shieldBar).ResizeBar(1)
		else:
			self.shieldPoints = sp
			Animation(self.scene.infoBox.shieldBar).ResizeBar(sp/100)
			
	def RemoveHP(self, val):
		hp=self.hitPoints - val
		if(hp > 0):
			self.hitPoints = hp
			Animation(self.scene.infoBox.hpBar).ResizeBar(hp/100)
		else:  
			self.hitPoints=0
			Animation(self.scene.infoBox.hpBar).ResizeBar(0)
			
			self.isDead=True
			self.ChangePose(4)
			
	def AddHP(self, val):
		hp=self.hitPoints + val
		if(hp < 100):
			self.hitPoints = hp
			Animation(self.scene.indfoBox.hpBar).ResizeBar(hp/100)
		else:
			self.hitPoints=100
			self.scene.infoBox.hpBar.x_scale=1
	
	'''
	╔═══════════════════════════════════════════════════════════════
	║	RunQue is used to insure we dont miss any collissions.
	║	out actual shieldPoints will be correct but its very easy
	║	for the Bar to get interupted and having a chance to show
	║	incorrect readings.
	║	
	║	Alternativly you could use EventManager and Tick methon to chect
	║	if they are the correct values. generallybthis is what developers
	║	do but i wanted to show you alternate Approches.
	╚═══════════════════════════════════════════════════════════════
	'''
	@ui.in_background
	def RunQue(self, game):
		self.inQue=True
		for x in self.AnimationQue:
			Animation(game.infoBox.shieldBar).ResizeBar(1)
		self.inQue = False

	def Tick(self, game, dt, runTime):
		if(len(self.AnimationQue) >= 1 and self.inQue == False):
			self.RunQue(game)
		if(self.PowerUpTimer > 0.00):
			self.PowerUpTimer-=dt
			#display timer
			if(self.PowerUpTimer < 0.0):
				self.EndSheild()
				
				
	def ChangePose(self, pose):
		if(pose == 1):
			self.up.run_action(a.fade_to(1.0, 0.01))
			self.down.run_action(a.fade_to(0.0, 0.01))
			self.idle.run_action(a.fade_to(0.0, 0.01))
			
		elif(pose == 2):
			self.up.run_action(a.fade_to(0.0, 0.01))
			self.down.run_action(a.fade_to(1.0, 0.01))
			self.idle.run_action(a.fade_to(0.0, 0.01))
			
		elif(pose == 3):
			self.up.run_action(a.fade_to(0.0, 0.01))
			self.down.run_action(a.fade_to(0.0, 0.01))
			self.idle.run_action(a.fade_to(1.0, 0.05))
			
		elif(pose == 4):
			self.isDead=True
			self.shield.remove_from_parent()
			self.up.remove_from_parent()
			self.down.remove_from_parent()
			self.idle.remove_from_parent()
			self.jetpack.run_action(
			a.group(
			a.sequence(
			a.fade_to(1, 0.1),
			a.rotate_by(999, 3)),
			a.sequence(
			a.move_to(200, 600, 3),
			a.call(self.Explode))))
			self.dead.run_action(
			a.group(
			a.sequence(
			a.fade_to(1, 0.1),
			a.rotate_by(math.radians(360), 6)),
			a.sequence(
			a.move_by(0, -1000, 5),
			a.call(self.scene.Game_Over))))
			
	'''
	╔═══════════════════════════════════════════════════════════════
	║			This section  is to show one way
	║			to handle Sprite Animations
	║	
	║	On player death the JetPack flys away and explodes.
	║	first a screen flash for dramatic effect (also hides the
	║	abrupt starting of the Fire sequence), then explosion and
	║	ends with a fading smoke cloud.	
	╚═══════════════════════════════════════════════════════════════
	'''
	def MakeTex(self, str):
		return Texture(ui.Image.named(str))
		
	@ui.in_background
	def Fire(self):
		smoke=SpriteNode(
		Texture('shp:BlackSmoke15'),
		color='#fdffdc',
		size=get_screen_size(),
		position=self.jetpack.position,
		parent=self,
		z_position=997,
		alpha=1.0)
		smoke.run_action(a.group(
		a.sequence(
		a.fade_to(0.7, 1),
		a.fade_to(0, 10)),
		a.sequence(
		a.move_to(1000, 1000, 40),
		a.remove())))
		s=[]
		s.append(self.MakeTex('shp:Explosion00'))
		s.append(self.MakeTex('shp:Explosion01'))
		s.append(self.MakeTex('shp:Explosion02'))
		s.append(self.MakeTex('shp:Explosion03'))
		s.append(self.MakeTex('shp:Explosion04'))
		s.append(self.MakeTex('shp:Explosion05'))
		s.append(self.MakeTex('shp:Explosion06'))
		s.append(self.MakeTex('shp:Explosion07'))
		s.append(self.MakeTex('shp:Explosion08'))
		for x in s:
			self.jetpack.alpha=0.0
			node=SpriteNode(x, parent=self, position=self.jetpack.position)
			node.run_action(a.sequence([a.fade_to(0,1),a.remove()]))
			time.sleep(0.15)
		self.jetpack.remove_from_parent()
	@ui.in_background
	def Explode(self):
		self.liftJet.remove_from_parent()
		self.idleJet.remove_from_parent()
		self.jetpack.remove_all_actions()
		flash=SpriteNode(
		None,
		color='#fdffdc',
		size=get_screen_size(),
		position=Point(Screen.Width()/2, Screen.Hieght()/2),
		parent=self.scene,
		z_position=999,
		alpha=1.0)
		flash.run_action(
		a.group(
		a.sequence(
		a.fade_to(0.8, 2),
		a.fade_to(0, 2.6),
		a.remove()),
		a.sequence(
		a.wait(0.6),
		a.call(self.Fire))))

'''
╔═══════════════════════════════════════════════════════════════
║        :GFX:
║	Used as example Type that can be used for Effects. in this
║	case its used for the Shield Powerup. 
║		- sets z_position so all effects objects are on the
║			same plane
║		- provides Animation access
║	nothing really special.. can be done with any subclass of
║	SpriteNode. I would o this for Type chevking but i tend to 
║	use string properties like tag or ID
╚═══════════════════════════════════════════════════════════════
'''
class GFX(SpriteNode):
	def __init__(self,texture, *args, **kwargs):
		self.animate=Animation(self).ActivatePowerup
		self.texture=texture
		self.z_position=100
		super().__init__(texture=self.texture, *args, **kwargs)
		self.animate()
'''
╔═══════════════════════════════════════════════════════════════
║        :GameOver:
║	Displays the clasic Game Over Text and provides means of 
║	closing the game other than the "x" button.
╚═══════════════════════════════════════════════════════════════
'''
class GameOver(LabelNode):
	def __init__(self, position,  *args, **kwargs):
		self.position=position
		self.z_position=105
		LabelNode.__init__(self, position=self.position, *args, **kwargs)
		self.text='GAME OVER'
		self.font=(Config.Font(s=60))
		self.anchor_point=(0.5, 0.5)
		self.color=Config.Black()
		self.overlayText=LabelNode(self.text, self.font, parent=self)
		self.overlayText.anchor_point=(0.5, 0.5)
		self.overlayText.color=Config.White()
		self.overlayText.position=Point(4, 4)
		self.Instruction=LabelNode(
		'Tap to close',
		font=Config.Font(s=30),
		parent=self)
		self.Instruction.z_position=100
		self.Instruction.anchor_point=(0.5, 0.5)
		self.Instruction.color=Config.Black()
		self.Instruction.position=Point(0, 80)
		self.InstructionOverlay=LabelNode(
		'Tap to close',
		font=Config.Font(s=30),
		parent=self)
		self.InstructionOverlay.z_position=101
		self.InstructionOverlay.anchor_point=(0.5, 0.5)
		self.InstructionOverlay.color=Config.White()
		self.InstructionOverlay.position=Point(3, 83)
		self.run_action(
		a.repeat(
		a.sequence(
		a.move_by(0, 20, 3),
		a.move_by(0, -20, 2.5),), -1))
'''
╔═══════════════════════════════════════════════════════════════
║        :NodeTimer:
║	Object used for Timers inside the Scene class. 
║	just one of many ways of using timers in your games.
╚═══════════════════════════════════════════════════════════════
'''
class NodeTimer(Node):
	def __init__(self, timer):
		self.timer=timer
	def Start(self):
		self.run_action(
		a.sequence(
		a.wait(self.timer),
		a.call(self.scene.EndTimer),
		a.remove()))
		
		
		self.up=Sprite(texture=Texture('plf:AlienPink_swim1'))
		self.up.alpha=1.0
		self.up.rotation=0
		self.up.z_position=9
		self.up.position=Point(0.0, 0.0)
		
		self.idle=Sprite(texture=Texture('plf:AlienPink_stand'))
		self.idle.alpha=0.0
		self.idle.rotation=0
		self.idle.z_position=9
		self.idle.position=Point(0.0, 0.0)
		
		self.down=Sprite(texture=Texture('plf:AlienPink_hit'))



						
		
'''
╔═══════════════════════════════════════════════════════════════
║        :Main:
║	SceneNode, Your Games Event Loop.
║	most Scripts ive seen put almost all their code inside this 
║	class. As you have seen i like to do most of my "work" 
║	outside of this class and do as little as i can directly 
║	inside.
║	
║	I dout there is any kind of gain in doing this. but it is 
║	the way im comfortable in writing. probably comes from my 
║	experience with C#.
╚═══════════════════════════════════════════════════════════════
'''
class Main (Scene):
	def setup(self):
		self.noHitTimer=None
		self.gameOver=False
		self.score=0
		EventManager.Setup(self)
		self.background_color='#00deff'
		self.gameObjects=GameObjects(self)
		self.brushes=Brushes(self)
		self.items=list()
		self.Generate_Land()
		self.Generate_Sky()
		self.player=Player()
		self.add_child(self.player)
		self.maxObsticles=5
		self.minSpawnCoolDown=4
		self.maxSpawnCoolDown=5
		self.curSpawnCoolDown=0
		self.spawnedObsticles=[]
		self.brushes.StandardObsticle()()
		self.infoBox=InfoBox(self.player)
		self.add_child(self.infoBox)
		
		
	def Generate_Sky(self):
		for y in range(self.GetSkyHieght()):
			for x in range(int(Screen.Width()/self.gameObjects.SkyBlockSize)):
				self.add_child(self.gameObjects.Sky(x, y))
				
	def Generate_Land(self):
		for y in range(self.gameObjects.GroundHeight):
			for x in range(int(Screen.Width()/self.gameObjects.GoundBlockSize)):
				if y==self.gameObjects.GroundHeight-1:
					self.add_child(self.gameObjects.Grass(x, y))
				elif y==self.gameObjects.GroundHeight-2:
					self.add_child(self.gameObjects.Dirt(x, y))
				else:
					self.add_child(self.gameObjects.Stone(x, y))
					
	def GetSkyHieght(self):
		val1 = (Screen.Hieght() - (self.gameObjects.GoundBlockSize * self.gameObjects.GroundHeight)) / self.gameObjects.SkyBlockSize
		return int(val1 + 1)
		
	def Game_Over(self):
		self.add_child(GameOver(self.size/2))
		self.gameOver=True
		
	def Obsticle_Out_Of_Bounds(self, brush):
		if(brush.children):
			if(type(brush.children[-1]) == type(brush)):
				EventManager.powerUps.append(brush.children[-1])
		self.brushes.StandardObsticle()()
		brush.run_action(a.remove())
		
	def add_child(self, node):
		if(hasattr(node, 'isObsticle')):
			for x in node.children:
				if(x.tag.startswith('engine')):
					t=Trigger(3, x, node)
					self.items.append(t)
					self.add_child(t)
				if(x.tag.startswith('Meteor')):
					t=Trigger(0, x, node)
					self.items.append(t)
					self.add_child(t)
				if(x.tag.startswith('gap')):
					t=Trigger(1, x, node)
					self.items.append(t)
					self.add_child(t)
				if(x.tag.startswith('powerup')):
					t=Trigger(2, x, node)
					self.items.append(t)
					self.add_child(t)
			self.spawnedObsticles.append(node)
			self.curSpawnCoolDown=random.randrange(
					self.minSpawnCoolDown, self.maxSpawnCoolDown)
			
		super().add_child(node)
		
	def did_change_size(self):
		pass
		
		
	'''
╔═══════════════════════════════════════════════════════════════
║	Methods StartTimer and EndTimer Along with Property noHitTimer
║	and Class NodeTimer... are to show how you can use Nodes as
║	timers. there are more than one way. this is just a quick put
║	together
║	
║	ORDER:
║	- Player hits Target (meteor)
║	- (StartTimer) noHitTimer is Assigned a NodeTimer with 3sec
║	- Action Sequince started containing wait(3)
║	- (EndTimer) noHitTimer assigned as None allowing player
║	collisions again.
╚═══════════════════════════════════════════════════════════════
	'''
	def StartTimer(self):
		end=self.EndTimer
		self.noHitTimer=NodeTimer(3)
		self.add_child(self.noHitTimer)
		self.noHitTimer.Start()
		
	def EndTimer(self):
		
		self.noHitTimer.remove_from_parent()
		self.noHitTimer=None

	
	
	def check_item_collisions(self):
		if self.items:
			for x in self.items:
				if(x.frame.intersects(self.player.frame)):
					if(x.target.tag.startswith('M')):
						if(self.noHitTimer == None):
							x.target.color='#ff0000'
							if(self.player.shieldActive):
								self.player.RemoveSP(Config.MeteorHitDamage())
							else:
								self.player.RemoveHP(Config.MeteorHitDamage())
							x.run_action(a.remove())
							self.items.remove(x)
							self.StartTimer()
					if(x.target.tag.startswith('engine')):
						if(self.noHitTimer == None):
							x.target.color='#ffe600'
							if(self.player.shieldActive):
								self.player.RemoveSP(Config.MotorHitDamage())
							else:
								self.player.RemoveHP(Config.MotorHitDamage())
							x.run_action(a.remove())
							self.items.remove(x)
							self.StartTimer()
					if(x.target.tag.startswith('gap')):
						self.AddScore()
						x.target.color='#00ff16'
						x.run_action(a.remove())
						self.items.remove(x)
					if(x.target.tag.startswith('powerup')):
						self.player.StartSheild()
						x.target.run_action(a.remove())
						self.ShieldPickUp()
						x.run_action(a.remove())
						self.items.remove(x)
						
						
	def ShieldPickUp(self):
		EventManager.powerUpTimer=Config.ShieldSpawnTimer()
		self.add_child(GFX(
			Texture('spc:ShieldSilver'),
			color='#97d6ff',
		
		position=Point(Screen.Width()/2, Screen.Hieght()-320),
		z_position=101))
		
	def GrantScore(self):
		self.score+=Config.points()
		self.infoBox.scoreVal.text=f'{self.score}'
		self.infoBox.scoreVal2.text=f'{self.score}'
		
	def AddScore(self):
		node=LabelNode(
		text=f'{Config.points()}',
		font=Config.Font(),
		position=self.player.position,
		z_position=105,
		color='#ffd43a',
		parent=self)
		target=self.infoBox.scoreVal.point_to_scene(self.infoBox.scoreVal.position)
		Animation(node).ScoreTravel(target, self.GrantScore)
		
	def update(self):
		self.check_item_collisions()
		EventManager.Pass(self.dt, self)
		
		
		if(self.player.position[1] <= self.gameObjects.Floor):
			self.player.remove_action('playerMove')
			self.player.position = Point(Screen.Width()/2, self.gameObjects.Floor+5)
			self.player.ChangePose(3)
			
			
		if(self.curSpawnCoolDown > 0):
			self.curSpawnCoolDown -= self.dt
			if(self.curSpawnCoolDown < 0):
				self.curSpawnCoolDown=0.0
				if(len(self.spawnedObsticles) < self.maxObsticles):
					self.brushes.StandardObsticle()()
					
					
	def touch_began(self, touch):
		if(self.gameOver == False):
			EventManager().touch_began(touch)
		if(EventManager.canClose and self.gameOver):
			self.view.close()
	def touch_moved(self, touch):
		if(self.gameOver == False):
			EventManager().touch_moved( touch)
			
	def touch_ended(self, touch):
		if(self.gameOver == False):
			EventManager().touch_ended( touch)
			
			
if __name__ == '__main__':
	run(Main(), show_fps=True)
