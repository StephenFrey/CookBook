#!python3
# -*- coding: UTF-8 -*-
'''OMZ
This shows a scrolling row or grid of special characters in the Pythonista Keyboard. The view supports both the 'minimized' mode (above the QWERTY keyboard) and the 'expanded' mode with the grid filling most of the keyboard.

Note: This script is designed for the Pythonista Keyboard. You can enable it in the Settings app (under General > Keyboard > Keyboards > Add New Keyboard...). Please check the documentation for more information.
⚄┈┈┈┈┈┈┈┈┈┈┈┈┈┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┈┈┈┈┈┈┈┈┈┈┈┈┈⚄
Extended:
	Everything is still the Same Concept. additions and changes are as follows...
		⚀ Multi-tier menu for Unicode Grouping. 
		⚁ Resizing buttons to make best use of screen width while still providing 
		  enoigh area for Text.
		⚂ For Performance different catagories of Unicode are placed in separate
		  .txt files.
		⚃ Larger selection of Characters and Symbols.
		⚄ ⏎ button to send user back to menu without having to reload Script.
		⚅ Easily add more Files and Unicode without having to touch the code itself.
		
Adding To Collection:
	Scripts ↷
		⚀ To add more Script type retrieve the chart from source
		⚁ open `Scripts.txt`. on the first available empty line and paste unicode.
		⚂ Keeping each script within a single line separating name from code with `:`
			`script name:ABCDEFG...`
		⚃ once file saved new script will be ready to use.
	Emoji and Symbold ↷
		⚀ inside respective file `💪 ⇒ Emoji.txt` and `♳✯✟ ⇒ Misc.txt` place each
		  grouping together in one line.
		⚁ And thats all! the first item in the line will be the display button Image.
	
	Premade Smilies ↷
		⚀ Inside `Faces.txt` place each face on a single line. 
		⚁ Once file saves Custom Faces will be Available!
		
	For seamless Use, change Script file name to `Special Characters.py` and
	place inside `Examples/Keyboard/` replacing original script. This way will use 
	new Version instead without the need to Setup inside Pythonista settings.
	
	THANKYOU!
		Enjoy!
			Stephen Frey
'''
import keyboard
import ui


FILE=open('Options.txt', "r+", encoding="utf-8")



class CharsView (ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		self.background_color = '#333'
		self.dict = dict({})
		self.scroll_view = ui.ScrollView(frame=self.bounds, flex='WH')
		self.scroll_view.shows_horizontal_scroll_indicator = False
		self.add_subview(self.scroll_view)
		self.buttons = []
		self.bw=125
		for line in FILE:
			line=line.replace('\n', '')
			self.new_button(line, 'Options')
			
	def new_button(self, k, v):
		btn = ui.Button(title=k)
		btn.name = v
		btn.font = ('<System>', 12)
		btn.background_color = (0, 0, 1, 0.5) if k == '⏎' else (1, 1, 1, 0.1)
		btn.tint_color = 'white'
		btn.corner_radius = 4
		btn.action = self.button_action
		self.scroll_view.add_subview(btn)
		self.buttons.append(btn)
		
	def Rebuild(self, dict, bw):
		FILE.close()
		for sv in self.scroll_view.subviews:
			self.scroll_view.remove_subview(sv)
			
		self.buttons.clear()
		for k, v in self.dict.items():
			self.new_button(k, v)
			
		self.dict.clear()
		self.bw = bw
		self.layout()
		
	def layout(self):
		rows = max(1, int(self.bounds.h / 36))
		bw = self.bw
		h = (self.bounds.h / rows) - 4
		x, y = 2, 2
		
		for btn in self.buttons:
			btn.frame = (x, y, bw, h)
			y += h + 4
			if y + h > self.bounds.h:
				y = 2
				x += bw + 4
		self.scroll_view.content_size = ((len(self.buttons)/rows + 1) * (bw + 4), 0)
		
	def button_action(self, sender):
		if sender.title == '⏎':
			self.bw = 125
			FILE=open(f'Options.txt', "r+", encoding="utf-8")
			for line in FILE:
				line=line.replace('\n', '')
				self.dict[line]='Options'
			self.Rebuild(self.dict, 125)
			return
		if sender.title == 'Faces':
			self.bw = 125
			FILE=open(f'{sender.title}.txt', "r+", encoding="utf-8")
			for line in FILE:
				line=line.replace('\n', '')
				if line.strip() == '':
					continue
				
				self.dict[line]=line
			self.Rebuild(self.dict, 40)
			return
		if sender.name == 'Options':
			self.bw = 125
			FILE=open(f'{sender.title}.txt', "r+", encoding="utf-8")
			for line in FILE:
				line=line.replace('\n', '')
				if line.strip() == '':
					continue
				if ':' in line:
					k,v=line.split(':')
					self.dict[k]='⏎'+v
				else:
					self.dict[line[0]]='⏎'+line
			self.Rebuild(self.dict, 40)
			return
		
		if sender.name == sender.title:
			self.bw = 40
			if keyboard.is_keyboard():
				keyboard.insert_text(sender.name)
				return
			else:
				print('Keyboard input:', sender.title)
				return
		if ':' not in sender.name:
			self.dict.clear()
			for char in sender.name:
				self.dict[char]=char
			self.Rebuild(self.dict, 40)
			return
		

def main():
	v = CharsView(frame = (0, 0, 320, 40))
	if keyboard.is_keyboard():
		keyboard.set_view(v, 'current')
	else:
		v.name = 'Keyboard Preview'
		v.present('sheet')


if __name__ == '__main__':
	
	main()
