try:
	from gi.repository import Gtk
except:
	print('Cannot import Gtk')
	exit(1)

class BackupGUI:
	def __init__(self):
		return

	def fchoose(self,folder=True):
		typ = Gtk.FileChooserAction.OPEN
		if folder: typ = Gtk.FileChooserAction.SELECT_FOLDER
		choo = Gtk.FileChooserDialog("Open..",
			None, typ,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		response = choo.run()
		choo.destroy()
		return choo.get_filename()

	def addwidget(self,widget,data):
		box = data[0]
		spin = data[1]
		tbox = Gtk.Box()
		f = Gtk.Entry()
		tbox.pack_start(f,True,True,0)
		f.show()
		if spin:
			b = Gtk.SpinButton()
			b.set_adjustment(Gtk.Adjustment(1,1,99,1))
			tbox.pack_start(b,False,False,0)
			b.show()
		else:
			t = Gtk.ToggleButton("File")
			c = Gtk.Button()
			c.set_image(Gtk.Image.new_from_icon_name('document-open',Gtk.IconSize.BUTTON))
			c.connect("clicked",self.callback,["tog",f,t])
			tbox.pack_start(t,False,False,0)
			tbox.pack_start(c,False,False,0)
			t.show()
			c.show()
		tbox.show()
		box.pack_start(tbox, False, False, 0)
		return

	def remwidget(self,widget,box):
		chi = box.get_children()
		if len(chi) > 1:
			box.remove(chi[len(chi)-1])
		return

	def scrollable_resize(self,widget,window):
		num = len(widget.get_children())
		if num < 5:
			window.set_size_request(300,num*25+32)		
		return

	def callback(self,widget,data):
		print('Button was pressed: {0}'.format(data))
		if data[0] == 'Okay':
			self.settings()
			self.delete_event(widget,'delete_event',data)
		elif data[0] == 'Apply':
			self.settings()
		elif data[0] == "folder":
			self.builder.get_object(data[1]+'_text').set_text(self.fchoose())
		elif data[0] == 'file':
			self.builder.get_object(data[1]+'_text').set_text(self.fchoose(False))
		elif data[0] == 'tog':
			data[1].set_text(self.fchoose(not data[2].get_active()))
		return

	def delete_event(self,widget,event=None,data=None):
		Gtk.main_quit()
		return False

	def pass_check(self,widget,text):
			text.set_editable(widget.get_active())

	def start(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file('layout_backup.glade')
		self.fdir_text = self.builder.get_object('fdir_text')
		self.bdir_text = self.builder.get_object('bdir_text')
		self.ldir_text = self.builder.get_object('ldir_text')
		self.ldi2_text = self.builder.get_object('ldi2_text')
		self.time_text = self.builder.get_object('time_text')
		self.sudo_bton = self.builder.get_object('sudo_bton')
		self.verbosity = self.builder.get_object('verbosity')
		self.adbla_box = self.builder.get_object('adbla_box')
		self.adblb_box = self.builder.get_object('adblb_box')
		self.pass_text = self.builder.get_object('pass_text')

#		for name in ['bdir','fdir','ldir','ldi2']:
#			button = self.builder.get_object(name+'_button')
#			button.set_image(Gtk.Image.new_from_icon_name('document-open', Gtk.IconSize.BUTTON))
#			button.connect('clicked',self.callback,['folder',name])

		icons = ['document-open']*4
		icons += ['gtk-add','gtk-delete']*2
		names = ['bdir','fdir','ldir','ldi2','reta_add','reta_rem','excl_add','excl_rem']
		method = [self.callback]*4
		method += [self.addwidget,self.remwidget]*2
		data = [['folder',names[0]],['folder',names[1]],['file',names[2]],['file',names[3]],\
			(self.adbla_box,True),self.adbla_box,(self.adblb_box,False),self.adblb_box]

		for i in range(4):
			button = self.builder.get_object(names[i]+'_button')
			button.set_image(Gtk.Image.new_from_icon_name(icons[i], Gtk.IconSize.BUTTON))
			button.connect('clicked',method[i],data[i])

		self.builder.get_object('okay_button').connect('clicked',self.callback,['Okay'])
		self.builder.get_object('appl_button').connect('clicked',self.callback,['Apply'])

		self.builder.connect_signals(self)

		window = self.builder.get_object('window')
		window.show_all()
		Gtk.main()

hello = BackupGUI()
hello.start()
