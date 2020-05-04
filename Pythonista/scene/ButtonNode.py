import scene

class EventHandler:
	children=[]
	event_loop=None
	
	@classmethod
	def add_child(cls, node):
		cls.children.append(node)
		if cls.event_loop == None:
			cls.event_loop = node.scene
	
	@classmethod
	def count(cls):
		return len(cls.children)
	
	@classmethod
	def touch_began(cls, touch):
		for child in cls.children:
			if cls.event_loop.point_from_scene(touch.location) in child.frame:
				child.Button_Tapped()

class ButtonNode(scene.ShapeNode):
	def __init__(self,
			action,
			name=f'ButtonNode',
			bg_color='#d4d2ca',
			accessoryColor='#e80000', 
			icon=None,
			accessory='emj:Exclamation_Mark_2',
			anchor_point=(0.5, 0.5),
			font_family='Helvetica',
			font_size=16,
			parent=None, 
			position=(0, 0),
			size=(120, 45),
			corner_radius=8,
			border_size=20,
			borderColor='#000000',
			text='',
			text_color='#000000',
			tint='white', 
			enabled=True,
			*args, **kwargs):
		
		self.x, self.y = position
		self.w, self.h = size
		
		super().__init__(
			path=scene.ui.Path.rounded_rect(
				self.x,
				self.y,
				self.w,
				self.h,
				corner_radius),
			fill_color=bg_color,
			stroke_color=borderColor,
			shadow=None,
			parent=parent,
			*args, **kwargs)
		
		EventHandler.add_child(self)
		self.icon=self._init_textures(icon)
		self.accessory=self._init_textures(accessory)
		self.border_size=border_size
		self.name=name + ' ' + str(EventHandler.count())
		self.enabled=enabled
		self.text=text if text != '' else self.name
		self.tint=tint
		self.text_color=text_color
		self.borderColor=borderColor
		self.corner_radius=corner_radius
		self.showAccesory=False
		self.accessoryColor=accessoryColor
		self.parentNode=parent
		self.position=position
		self.size=size
		self.button_action=action
		self.anchor_point=anchor_point
		self.font_family=font_family
		self.font_size=font_size
		self.components=dict({
			'accessory':None,
			'icon':None,
			'label':None,
			'width':None,
			'height':None})
		self._setup(self.icon, self.accessory, self.components)
			
	def _init_textures(self, img):
		if type(img) == str or type(img) == scene.ui.Image:
			return scene.Texture(img)
		else:
			return None
			
	def _setup(self, i, a, c):
		
		if a != None:
			c['accessory']=scene.SpriteNode(
				texture=a,
				size=(self.size[1]/4, self.size[1]/5*1.5),
				position=scene.Point(-self.size[0]/2+7, self.size[1]/2-10),
				parent=self,
				z_position=4,
				color=self.accessoryColor)
			
		if i != None:
			c['icon']=scene.SpriteNode(
				texture=i,
				size=scene.Size(self.size[1]/2, self.size[1]/2),
				position=scene.Point(self.w/2 - self.size[1]/3 , 0),
				parent=self, 
				z_position=9)
				
		if self.text:
			c['label']=scene.LabelNode(
				text=self.text,
				font=(self.font_family, self.font_size),
				position=scene.Point(0 , 0),
				anchor_point=(0.5, 0.5),
				color=self.text_color,
				parent=self,
				z_position=10)
		
	def Button_Tapped(self):
		if self.components['accessory'].alpha > 0:
			self.components['accessory'].alpha = 0
		if self.enabled:
			self.button_action(self)
#---------------------------------------------------------------------------

def my_button_action(sender):
	print(f'{sender.name}: {sender.text}..')

class main(scene.Scene):
	def setup(self):
		self.background_color='#f2f2f2'
		self.my_button_up=ButtonNode(
					text='', 
					parent=self,
					position=scene.Point(self.size[0]/2, self.size[1]/2+100),
					action=my_button_action)
		self.my_button_right=ButtonNode(
					text='right', 
					parent=self,
					position=scene.Point(self.size[0]/2+100, self.size[1]/2),
					action=my_button_action)
		self.my_button_down=ButtonNode(
					text='down', 
					parent=self,
					position=scene.Point(self.size[0]/2, self.size[1]/2-100),
					action=my_button_action)
		self.my_button_left=ButtonNode(
					text='left', 
					parent=self,
					position=scene.Point(self.size[0]/2-100, self.size[1]/2),
					action=my_button_action)
	
	def touch_began(self, touch):
		EventHandler.touch_began(touch)

scene.run(main())
