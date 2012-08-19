import ConfigParser
import gtk

class BackupGUI:
	
	def __init__(self):
		return

	def callback(self,widget,data):
		print "Button was pressed: {0}".format(data)
		print self.bdir_text.get_text()
		if data == "Okay":
			self.delete_event(widget,'delete_event',data)
		if data[0] == "folder":
			data[1].set_text(self.fch())
		elif data[0] == 'file':
			data[1].set_text(self.fch(False))
		return

	def delete_event(self,widget,event,data=None):
		gtk.main_quit()
		return False

	def fch(self,folder=True):
		choo = gtk.FileChooserDialog("Open..",
			None,
			gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
			(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
			gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		if not folder:
			choo = gtk.FileChooserDialog("Open..",
				None,
				gtk.FILE_CHOOSER_ACTION_OPEN,
				(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
				gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		choo.set_default_response(gtk.RESPONSE_OK)
		response = choo.run()
		toret = -1
		if response == gtk.RESPONSE_OK:
			toret = choo.get_filename()
		choo.destroy()
		return toret

	def addwidget(self,widget,box,spin=True):
		print 'adding'
		tbox = gtk.HBox(False, 0)
		f = gtk.Entry(max=0)
		tbox.pack_start(f,False,False,0)
		f.show()
		if spin:
			b = gtk.SpinButton(gtk.Adjustment(1,1,99,1))
			tbox.pack_start(b,False,False,0)
			b.show()
		tbox.show()
		box.pack_start(tbox, False, False, 0)
		return

	def remwidget(self,widget,box):
		print 'removing'
		chi = box.get_children()
		if len(chi) > 1:
			box.remove(chi[len(chi)-1])
		return

	def showall(self,wids):
		for w in wids:
			w.show()
		return

	def start(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title('Configuration Editor')
		self.window.connect("delete_event",self.delete_event)
		self.window.set_border_width(10)

		self.table = gtk.Table(4,6,False)

		self.text_box = gtk.VBox(True,0)
		self.bdir_label = gtk.Label("Destination: ")
		self.bdir_label.set_alignment(0,0.5)
		self.fdir_label = gtk.Label("Source: ")
		self.fdir_label.set_alignment(0,0.5)
		self.ldir_label = gtk.Label("Log file: ")
		self.ldir_label.set_alignment(0,0.5)
		self.ldi2_label = gtk.Label("Extended log: ")
		self.ldi2_label.set_alignment(0,0.5)
		self.text_box.pack_start(self.fdir_label, False, True, 0)
		self.text_box.pack_start(self.bdir_label, False, True, 0)
		self.text_box.pack_start(self.ldir_label, False, True, 0)
		self.text_box.pack_start(self.ldi2_label, False, True, 0)

		self.bdir_box = gtk.HBox(False,0)
		self.bdir_text = gtk.Entry(max=0)
		self.bdir_text.set_editable(True)
		self.bdir_button = gtk.Button()
		self.bdir_button.set_image(gtk.image_new_from_icon_name('folder',gtk.ICON_SIZE_BUTTON))
		self.bdir_button.connect("clicked",self.callback,["folder",self.bdir_text])
		self.bdir_box.pack_start(self.bdir_text, False, False, 0)
		self.bdir_box.pack_start(self.bdir_button, False, False, 0)

		self.fdir_box = gtk.HBox(False,0)
		self.fdir_text = gtk.Entry(max=0)
		self.fdir_text.set_editable(True)
		self.fdir_button = gtk.Button()
		self.fdir_button.set_image(gtk.image_new_from_icon_name('folder',gtk.ICON_SIZE_BUTTON))
		self.fdir_button.connect("clicked",self.callback,["folder",self.fdir_text])
		self.fdir_box.pack_start(self.fdir_text, False, False, 0)
		self.fdir_box.pack_start(self.fdir_button, False, False, 0)

		self.ldir_box = gtk.HBox(False,0)
		self.ldir_text = gtk.Entry(max=0)
		self.ldir_text.set_editable(True)
		self.ldir_button = gtk.Button()
		self.ldir_button.set_image(gtk.image_new_from_icon_name('folder',gtk.ICON_SIZE_BUTTON))
		self.ldir_button.connect("clicked",self.callback,["file",self.ldir_text])
		self.ldir_box.pack_start(self.ldir_text, False, False, 0)
		self.ldir_box.pack_start(self.ldir_button, False, False, 0)

		self.ldi2_box = gtk.HBox(False,0)
		self.ldi2_text = gtk.Entry(max=0)
		self.ldi2_text.set_editable(True)
		self.ldi2_button = gtk.Button()
		self.ldi2_button.set_image(gtk.image_new_from_icon_name('folder',gtk.ICON_SIZE_BUTTON))
		self.ldi2_button.connect("clicked",self.callback,["file",self.ldi2_text])
		self.ldi2_box.pack_start(self.ldi2_text, False, False, 0)
		self.ldi2_box.pack_start(self.ldi2_button, False, False, 0)

		self.reta_box = gtk.VBox(False,0)
		self.reta_label = gtk.Label("Levels to retain")
		self.reta_box.pack_start(self.reta_label, False, False, 0)

#		self.levels = [(gtk.Entry(max=15), gtk.SpinButton(gtk.Adjustment(1,1,99,1)))]

		self.adbla = gtk.VBox(False,0)

		self.reta_box.pack_start(self.adbla, False, False, 0)
		self.adbla.show()
		self.addwidget(None,self.adbla,True)

		self.reta_add_button = gtk.Button()
		self.reta_add_button.set_image(gtk.image_new_from_icon_name('edit-add',gtk.ICON_SIZE_BUTTON))
		self.reta_add_button.connect('clicked',self.addwidget,self.adbla,True)
		self.reta_rem_button = gtk.Button()
		self.reta_rem_button.set_image(gtk.image_new_from_icon_name('edit-clear',gtk.ICON_SIZE_BUTTON))
		self.reta_rem_button.connect('clicked',self.remwidget,self.adbla)

		self.adrem_box = gtk.HBox(False,0)
		self.adrem_box.pack_start(self.reta_add_button, False, False, 0)
		self.adrem_box.pack_start(self.reta_rem_button, False, False, 0)

		self.reta_add_button.show()
		self.reta_rem_button.show()
		self.adrem_box.show()

		self.reta_box.pack_start(self.adrem_box, False, False, 0)

		self.excl_box = gtk.VBox(False,0)
		self.excl_label = gtk.Label("Exclusions")
		self.excl_label.show()
		self.excl_box.pack_start(self.excl_label, False, False, 0)
		self.adblb = gtk.VBox(False,0)

		self.excl_box.pack_start(self.adblb, False, False, 0)
		self.adblb.show()
		self.addwidget(None,self.adblb,False)

		self.excl_add_button = gtk.Button()
		self.excl_add_button.set_image(gtk.image_new_from_icon_name('edit-add',gtk.ICON_SIZE_BUTTON))
		self.excl_add_button.connect('clicked',self.addwidget,self.adblb,False)
		self.excl_rem_button = gtk.Button()
		self.excl_rem_button.set_image(gtk.image_new_from_icon_name('edit-clear',gtk.ICON_SIZE_BUTTON))
		self.excl_rem_button.connect('clicked',self.remwidget,self.adblb)

		self.bdrem_box = gtk.HBox(False,0)
		self.bdrem_box.pack_start(self.excl_add_button, False, False, 0)
		self.bdrem_box.pack_start(self.excl_rem_button, False, False, 0)

		self.excl_add_button.show()
		self.excl_rem_button.show()
		self.bdrem_box.show()

		self.excl_box.pack_start(self.bdrem_box, False, False, 0)

		self.comm_box = gtk.HBox(False,0)
		self.okay_button = gtk.Button("OK")
		self.okay_button.connect("clicked",self.callback,"Okay")
		self.canc_button = gtk.Button("Cancel")
		self.canc_button.connect("clicked", self.delete_event,'clicked')
		self.appl_button = gtk.Button("Apply")
		self.appl_button.connect("clicked", self.callback, "Apply")
		self.comm_box.pack_start(self.okay_button, False, False, 0)
		self.comm_box.pack_start(self.canc_button, False, False, 0)
		self.comm_box.pack_start(self.appl_button, False, False, 0)

		self.window.add(self.table)

		fils_box = gtk.VBox(False,0)
		fils_box.show()
		fils_box.pack_start(self.bdir_box, False, False, 0)
		fils_box.pack_start(self.fdir_box, False, False, 0)
		fils_box.pack_start(self.ldir_box, False, False, 0)
		fils_box.pack_start(self.ldi2_box, False, False, 0)

		fil2_box = gtk.HBox(False,0)
		fil2_box.show()
		fil2_box.pack_start(self.text_box, False, False, 0)
		fil2_box.pack_start(fils_box, False, False, 0)

		self.table.attach(fil2_box, 0,1,0,1)
		self.table.attach(self.reta_box, 0,1,1,2)		
		self.table.attach(self.excl_box, 0,1,2,3)	
		self.table.attach(self.comm_box, 0,1,3,4)

		labels = [self.ldir_label,self.ldi2_label,self.reta_label,self.bdir_label,self.fdir_label]
		buttons = [self.ldir_button,self.ldi2_button,self.bdir_button,self.fdir_button,self.okay_button,self.canc_button,self.appl_button]
		boxes = [self.text_box,self.bdir_box,self.fdir_box,self.ldir_box,self.ldi2_box,self.reta_box,self.excl_box,self.comm_box]
		entries = [self.bdir_text,self.fdir_text,self.ldir_text,self.ldi2_text]

		self.showall(labels + buttons + boxes + entries + [self.table, self.window])

		self.table.show()
		self.window.show()
		gtk.main()
		return

hello = BackupGUI()
print hello.start()
