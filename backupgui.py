import ConfigParser
import gtk

class BackupGUI:
	
	def __init__(self):
		return

	def callback(self,widget,data):
		print "Button was pressed: {0}".format(data)
		print self.text1.get_text()
		return

	def delete_event(self,widget,event,data=None):
		gtk.main_quit()
		return False

	def start(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title('Configuration Editor')
		self.window.connect("delete_event",self.delete_event)
		self.window.set_border_width(10)
		self.box1 = gtk.HBox(False, 0)
		self.window.add(self.box1)
		self.button1 = gtk.Button("Button 1")
		self.button1.connect("clicked",self.callback,'Button 1')
		self.box1.pack_start(self.button1,True, True, 0)
		self.button1.show()
		self.button2 = gtk.Button("Button 2")
		self.button2.connect("clicked", self.callback, "button 2")
		self.box1.pack_start(self.button2, True, True, 0)
		self.text1 = gtk.Entry(max=0)
		self.text1.set_editable(True)
		self.box1.pack_start(self.text1,True,True,0)
		self.text1.show()
		self.button2.show()
		self.box1.show()
		self.window.show()
		return self.text1.get_text()

hello = BackupGUI()
print hello.start()
gtk.main()
