__version__ = '1.0' #declare the app version. Will be used by buildozer


from kivy.app import App #for the main app
from kivy.uix.floatlayout import FloatLayout #the UI layout
from plyer import camera #object to read the camera
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
import os, random,shutil
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.camera import Camera
from kivy.properties import ObjectProperty
import uuid


count=0
sm = ScreenManager()

Builder.load_string("""

<MainScreen>:
	center_image:_center_image
	FloatLayout:
		canvas:
        	#Color:
            	#rgba: 0.3, 0.4, 1, 1
        	Rectangle:
            	pos: self.pos
            	size: self.size
            	source: 'backg.jpg'
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
			font_size:root.width/15	
		Image:
			id:_center_image
			source: "init_pic.png"
			pos_hint:{'x':.3, 'y':.3}
			size_hint:(.4,.4)
			allow_stretch:True
			keep_ratio:False
		Button:
			color:0.7,0.7,0.7,1
			font_name:'main.ttf'
			background_color: (0,0,1,1)
			text:'TAKE PICTURE'
			id:'take_picture'
			pos_hint:{'x':.02, 'y':.0}
			size_hint:(.30, .20)
			on_press:root.take_picture()			
			font_size:root.width/60
			border:(0,0,0,0)
		Button:
			color:0.7,0.7,0.7,1
			font_name:'main.ttf'
			background_color: (0,0,1,1)
			text:'PICK RANDOM'
			id:'pick_random'
			pos_hint:{'x':.35, 'y':.0}
			size_hint:(.30, .20)
			on_press:root.random_pic()
			font_size:root.width/60
			border:(0,0,0,0)
		Button:
			color:0.7,0.7,0.7,1
			font_name:'main.ttf'
			background_color: (0,0,1,1)
			text:'DELETE ALL PICS'
			id:'delete_all'
			pos_hint:{'x':.68, 'y':.0}
			size_hint:(.30, .20)
			on_press:root.delete_all()			
			font_size:root.width/60
			border:(0,0,0,0)
		

""")


class MainScreen(Screen):
	def __init__(self,**kwargs):
		super(MainScreen, self).__init__(**kwargs)
		self.picture_path = '/storage/sdcard0/rand0mpics/' 
		if not os.path.exists(self.picture_path):
			os.makedirs(self.picture_path)
		#center_image=ObjectProperty(None)
	
	def callback(self,dt):
		for dirpath, dirnames, files in os.walk(self.picture_path):
			if files:
				

				self.ids['_center_image'].source=self.picture_path + random.choice(os.listdir(self.picture_path))
				global count
				count=count+1
				if (count==50):
					count=0
					Clock.unschedule(self.callback)
			else:
				self.ids['_center_image'].source="init_pic.png"
		
	def random_pic(self):	
		Clock.schedule_interval(self.callback, 0.1)
		#anim = Animation(x=50, size=(50, 50), t='in_out_bounce')
		#anim += Animation(pos=(200,70),t='in_out_back')
		#anim &= Animation(size=(100,50))
		#anim.start(self.center_image)
	
	def take_picture(self):
		outname = str(uuid.uuid4())
		self.ids['_center_image'].source='init_pic.png'
		camera.take_picture(self.picture_path+outname+'.jpg', self.done)

	def done(self):
		pass
	
	def delete_all(self):
		for the_file in os.listdir(self.picture_path):
			file_path = os.path.join(self.picture_path, the_file)
			try:
				if os.path.isfile(file_path):
					os.unlink(file_path)
        			#elif os.path.isdir(file_path): shutil.rmtree(file_path)
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

	
rand0m().run()
