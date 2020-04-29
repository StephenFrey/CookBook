'''
					     ::Tick::
	Acts as a bridge from Gameloop object to
	other objects that need regular pdates.
					    Properties
				  val ⤇ 	Time between frames 'DeltaTime'
			last_tick ⤇		val for last Tick
	objects_to_update ⤇		list of updated class'.
	
	Managed Objects must have an Update() method (case sensitive)
	
					      Methods
				 dt ⤇ 		Returns current Tick rounded to 3 decimal places
				set ⤇ 		Sets Tick.val to gameloop delta
			   size ⤇ 		Returns amount of objects being updated
				add ⤇ 		Add object to be updated
			_update ⤇ 		update loop to update every Tick.intervals
			
	LabelNode from Pythonista's scene module to display Tick info on screen.
	
'''
import scene
class Tick:
	val=0.0 
	last_tick=0.0
	intervals=1.0
	objects_to_update=[]
	label=scene.LabelNode(text='Tick: ', color=(0.0, 0.0, 0.0, 1.0), 
					size=scene.Size(50, 35), anchor_point=(0.0, 0.0))
	
	@classmethod
	def dt(cls): 
		return round(cls.val, 3)
		
	@classmethod
	def set(cls, val):
		cls.last_tick=cls.val
		cls.val=val
		if cls.val < cls.last_tick:
			cls.label.color=(0.0, 0.75, 0.0)
			cls.label.text=f'Tick: {cls.dt()}'
		else:
			cls.label.color=(0.75, 0.0, 0.0)
			cls.label.text=f'Tick: {cls.dt()}'
      
	@classmethod
	def size(cls):
		return len(cls.objects_to_update)
		
	@classmethod
	def Add(cls, object): 
		cls.objects_to_update.append(object)
		
	@classmethod
	def _update(cls, GameLoop):
		cls.set(GameLoop.dt)
		if cls.objects_to_update:
			for child in cls.objects_to_update:
				child.update()

class GameLoop(scene.Scene):
	def setup(self):
		pass
	
	def update(self):
		Tick._update(self)
		
