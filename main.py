__version__ = '1.0' #declare the app version. Will be used by buildozer

from kivy.app import App 
from kivy.uix.floatlayout import FloatLayout 
from plyer import camera 
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
import os, random,shutil
from kivy.uix.image import Image
from kivy.uix.camera import Camera
from kivy.graphics import Rotate,PushMatrix,PopMatrix,Translate,BorderImage
from kivy.core.window import Window
import uuid

count=0
sm = ScreenManager()

Builder.load_string("""

<MainScreen>:
	center_image:_center_image
	random_btn:random_btn
	take_pictures:take_picture
	fade_imgs:fade_img
	RelativeLayout:
		canvas:
			Color:
				rgba: 0, 0, 0.12, 1
			Rectangle:
            	pos: self.pos
            	size: self.size
		Label:
			color:0.95,0.95,0.95,1
			canvas.before:
				Color:
					rgba: 0,0, 0.5, 1
				Rectangle:
					pos:(0,root.height-root.height/5)
					size:(root.width,root.height/5)
			text:'rand0m person '
			font_name:'main.ttf'
			pos_hint:{'x':.0, 'y':.74}
			size_hint:(1,.3)
			halign: 'center'
			valign: 'middle'
			font_size:root.width/13
		Button:
			color:0.7,0.7,0.7,1
			font_name:'main.ttf'
			background_color: (0,0,1,1)
			id:take_picture
			pos_hint:{'x':.02, 'y':.0}
			size_hint:(.30, .20)
		    on_press:root.take_picture()			
			font_size:root.width/30
			border:(0,0,0,0)
			halign: 'center'
			valign: 'middle'
		Button:
			id:random_btn
			color:0.7,0.7,0.7,1
			font_name:'main.ttf'
			background_color: (0,0,1,1)
			text_size: self.width-20,None
			pos_hint:{'x':.35, 'y':.0}
			size_hint:(.30, .20)
			on_press:root.random_pic()
			font_size:root.width/30
			halign: 'center'
			valign: 'middle'			
			border:(0,0,0,0)
		Button:
			color:0.7,0.7,0.7,1
			font_name:'main.ttf'
			background_color: (0,0,1,1)
			id:delete_all
			pos_hint:{'x':.68, 'y':.0}
			size_hint:(.30, .20)
			on_press:root.delete_all()			
			font_size:root.width/30
			border:(0,0,0,0)
			halign: 'center'
			valign: 'middle'
		Image:
			id:fade_img
			source: "transparent.png"
			allow_stretch:True
			keep_ratio:False
		Image:
			id:_center_image
			source: "init_pic.png"
			pos_hint:{'x':.15, 'y':.25}
			size_hint:(.70,.47)
			allow_stretch:True
			keep_ratio:False
				
				
""")


class MainScreen(Screen):
	def __init__(self,**kwargs):
		Clock.unschedule(self.callback)
		super(MainScreen, self).__init__(**kwargs)
		self.picture_path = '/storage/sdcard0/rand0mpics/' 
		if not os.path.exists(self.picture_path):
			os.makedirs(self.picture_path)
		self.ids['random_btn'].text="PICK\nRANDOM"
		self.ids['take_picture'].text="TAKE\nPICTURE"	
		self.ids['delete_all'].text="DELETE\nALL\nPICTURES"	
		
	def random_pic(self):
		for dirpath, dirnames, files in os.walk(self.picture_path):
			if files:
				self.ids['fade_img'].source="back.png"
				Clock.schedule_interval(self.callback, 0.1)
	def callback(self,dt):
		self.ids['random_btn'].disabled=True
		self.ids['take_picture'].disabled=True
		self.ids['delete_all'].disabled=True
		self.ids['_center_image'].source=self.picture_path + random.choice(os.listdir(self.picture_path))
		with self.ids['_center_image'].canvas.before:
			Rotate(angle=10,axis=(0,0,1),origin=self.center)
			
		global count
		count=count+1 
		if (count==100):
					Clock.unschedule(self.callback)
					Clock.schedule_once(self.rotate_main, 4)

							
					
	def rotate_main(self,dt):
		self.ids['fade_img'].source="transparent.png"
		global count
		count=0
		self.ids['_center_image'].canvas.before.clear()
		self.ids['random_btn'].disabled=False
		self.ids['take_picture'].disabled=False
		self.ids['delete_all'].disabled=False
		self.ids['_center_image'].source="init_pic.png"

					
	
	def take_picture(self):
		outname = str(uuid.uuid4())
		self.ids['_center_image'].source='init_pic.png'
		Clock.unschedule(self.callback)		
		camera.take_picture(self.picture_path+outname+'.jpg', self.done)
		

	def done(self):
		pass
	
	def delete_all(self):
		for the_file in os.listdir(self.picture_path):
			file_path = os.path.join(self.picture_path, the_file)
			try:
				if os.path.isfile(file_path):
					os.unlink(file_path)
					self.ids['_center_image'].source='init_pic.png'
			except:
				pass
	
sm.add_widget(MainScreen(name="main"))
	
class rand0m(App): 
	def build(self):
		return sm
	def on_pause(self):
		return True
	def on_resume(self):
		pass

if __name__ == '__main__':	
	rand0m().run()
