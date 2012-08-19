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
		tbox.pack_start(f,True,True,0)
		f.show()
		if spin:
			b = gtk.SpinButton(gtk.Adjustment(1,1,99,1))
			tbox.pack_start(b,False,False,0)
			b.show()
		else:
			c = gtk.Button()
			c.set_image(gtk.image_new_from_icon_name('folder',gtk.ICON_SIZE_BUTTON))
			c.connect("clicked",self.callback,["file",f])
			tbox.pack_start(c,False,False,0)
			c.show()
		tbox.show()
		box.pack_start(tbox, False, False, 0)
		sz = self.window.get_size()
		#self.window.set_geometry_hints(self.window,max_height=sz[1])
		return

	def remwidget(self,widget,box):
		print 'removing'
		chi = box.get_children()
		if len(chi) > 1:
			box.remove(chi[len(chi)-1])
			self.noresize(self.window)
#			sz = self.window.get_size()
#			self.window.resize(sz[0],10)
		return

	def noresize(self,widget,data=None):
		sz = widget.get_size()
		print 'done'
		widget.disconnect(self.toblock)
		widget.resize(sz[0],10) 
		self.toblock = self.window.connect("check-resize",self.noresize)
		return

	def showall(self,wids):
		for w in wids:
			w.show()
		return

	def start(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title('Configuration Editor')
		self.window.connect("delete_event",self.delete_event)
		self.toblock = self.window.connect("check-resize",self.noresize)
		self.window.set_border_width(10)

		table = gtk.Table(4,6,False)

		text_box = gtk.VBox(True,0)
		bdir_label = gtk.Label("Destination: ")
		bdir_label.set_alignment(0,0.5)
		fdir_label = gtk.Label("Source: ")
		fdir_label.set_alignment(0,0.5)
		ldir_label = gtk.Label("Log file: ")
		ldir_label.set_alignment(0,0.5)
		ldi2_label = gtk.Label("Extended log: ")
		ldi2_label.set_alignment(0,0.5)
		text_box.pack_start(fdir_label, False, True, 0)
		text_box.pack_start(bdir_label, False, True, 0)
		text_box.pack_start(ldir_label, False, True, 0)
		text_box.pack_start(ldi2_label, False, True, 0)

		bdir_box = gtk.HBox(False,0)
		self.bdir_text = gtk.Entry(max=0)
		self.bdir_text.set_editable(True)
		bdir_button = gtk.Button()
		bdir_button.set_image(gtk.image_new_from_icon_name('folder',gtk.ICON_SIZE_BUTTON))
		bdir_button.connect("clicked",self.callback,["folder",self.bdir_text])
		bdir_box.pack_start(self.bdir_text, True, True, 0)
		bdir_box.pack_start(bdir_button, False, False, 0)

		fdir_box = gtk.HBox(False,0)
		self.fdir_text = gtk.Entry(max=0)
		self.fdir_text.set_editable(True)
		fdir_button = gtk.Button()
		fdir_button.set_image(gtk.image_new_from_icon_name('folder',gtk.ICON_SIZE_BUTTON))
		fdir_button.connect("clicked",self.callback,["folder",self.fdir_text])
		fdir_box.pack_start(self.fdir_text, True, True, 0)
		fdir_box.pack_start(fdir_button, False, False, 0)

		ldir_box = gtk.HBox(False,0)
		self.ldir_text = gtk.Entry(max=0)
		self.ldir_text.set_editable(True)
		ldir_button = gtk.Button()
		ldir_button.set_image(gtk.image_new_from_icon_name('folder',gtk.ICON_SIZE_BUTTON))
		ldir_button.connect("clicked",self.callback,["file",self.ldir_text])
		ldir_box.pack_start(self.ldir_text, True, True, 0)
		ldir_box.pack_start(ldir_button, False, False, 0)

		ldi2_box = gtk.HBox(False,0)
		self.ldi2_text = gtk.Entry(max=0)
		self.ldi2_text.set_editable(True)
		ldi2_button = gtk.Button()
		ldi2_button.set_image(gtk.image_new_from_icon_name('folder',gtk.ICON_SIZE_BUTTON))
		ldi2_button.connect("clicked",self.callback,["file",self.ldi2_text])
		ldi2_box.pack_start(self.ldi2_text, True, True, 0)
		ldi2_box.pack_start(ldi2_button, False, False, 0)

		reta_box = gtk.VBox(False,0)
		reta_label = gtk.Label("Levels to retain")
		reta_label.set_alignment(0,0.5)
		reta_box.pack_start(reta_label, False, False, 0)

#		levels = [(gtk.Entry(max=15), gtk.SpinButton(gtk.Adjustment(1,1,99,1)))]

		self.adbla = gtk.VBox(True,0)

		reta_box.pack_start(self.adbla, False, False, 0)
		self.adbla.show()
		self.addwidget(None,self.adbla,True)

		reta_add_button = gtk.Button()
		reta_add_button.set_image(gtk.image_new_from_icon_name('edit-add',gtk.ICON_SIZE_BUTTON))
		reta_add_button.connect('clicked',self.addwidget,self.adbla,True)
		reta_rem_button = gtk.Button()
		reta_rem_button.set_image(gtk.image_new_from_icon_name('edit-clear',gtk.ICON_SIZE_BUTTON))
		reta_rem_button.connect('clicked',self.remwidget,self.adbla)

		adrem_box = gtk.HBox(False,0)
		adrem_box.pack_end(reta_add_button, False, False, 0)
		adrem_box.pack_end(reta_rem_button, False, False, 0)

		reta_add_button.show()
		reta_rem_button.show()
		adrem_box.show()

		reta_box.pack_start(adrem_box, False, False, 0)

		excl_box = gtk.VBox(False,0)
		excl_label = gtk.Label("Exclusions")
		excl_label.set_alignment(0,0.5)
		excl_label.show()
		excl_box.pack_start(excl_label, False, False, 0)
		self.adblb = gtk.VBox(False,0)

		excl_box.pack_start(self.adblb, False, False, 0)
		self.adblb.show()
		self.addwidget(None,self.adblb,False)

		excl_add_button = gtk.Button()
		excl_add_button.set_image(gtk.image_new_from_icon_name('edit-add',gtk.ICON_SIZE_BUTTON))
		excl_add_button.connect('clicked',self.addwidget,self.adblb,False)
		excl_rem_button = gtk.Button()
		excl_rem_button.set_image(gtk.image_new_from_icon_name('edit-clear',gtk.ICON_SIZE_BUTTON))
		excl_rem_button.connect('clicked',self.remwidget,self.adblb)

		bdrem_box = gtk.HBox(False,0)
		bdrem_box.pack_end(excl_add_button, False, False, 0)
		bdrem_box.pack_end(excl_rem_button, False, False, 0)

		excl_add_button.show()
		excl_rem_button.show()
		bdrem_box.show()

		excl_box.pack_start(bdrem_box, False, False, 0)

		comm_box = gtk.HBox(False,0)
		okay_button = gtk.Button("OK")
		okay_button.connect("clicked",self.callback,"Okay")
		canc_button = gtk.Button("Cancel")
		canc_button.connect("clicked", self.delete_event,'clicked')
		appl_button = gtk.Button("Apply")
		appl_button.connect("clicked", self.callback, "Apply")
		comm_box.pack_start(okay_button, False, False, 0)
		comm_box.pack_start(canc_button, False, False, 0)
		comm_box.pack_start(appl_button, False, False, 0)

		self.window.add(table)

		fils_box = gtk.VBox(False,0)
		fils_box.show()
		fils_box.pack_start(bdir_box, True, True, 0)
		fils_box.pack_start(fdir_box, False, False, 0)
		fils_box.pack_start(ldir_box, False, False, 0)
		fils_box.pack_start(ldi2_box, False, False, 0)

		fil2_box = gtk.HBox(False,0)
		fil2_box.show()
		fil2_box.pack_start(text_box, False, False, 0)
		fil2_box.pack_start(fils_box, True, True, 0)

		#win_box

		table.attach(fil2_box, 0,1,0,1)
		table.attach(reta_box, 0,1,1,2)		
		table.attach(excl_box, 0,1,2,3)	
		table.attach(comm_box, 0,1,3,4)

		labels = [ldir_label,ldi2_label,reta_label,bdir_label,fdir_label]
		buttons = [ldir_button,ldi2_button,bdir_button,fdir_button,okay_button,canc_button,appl_button]
		boxes = [text_box,bdir_box,fdir_box,ldir_box,ldi2_box,reta_box,excl_box,comm_box]
		entries = [self.bdir_text,self.fdir_text,self.ldir_text,self.ldi2_text]

		self.showall(labels + buttons + boxes + entries + [table, self.window])

		table.show()
		self.window.show()
		gtk.main()
		return

hello = BackupGUI()
print hello.start()
