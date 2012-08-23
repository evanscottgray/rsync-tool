import configparser
import keyring
import getpass
import os
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
		if response == Gtk.ResponseType.CANCEL:
			fil = ''
		elif response == Gtk.ResponseType.OK:
			fil = choo.get_filename()
		choo.destroy()
		return fil

	def settings(self):
		parser = configparser.ConfigParser()
		if os.path.exists(self.conf):
			try:
				parser.read(self.conf)
			except:
				print('File cannot be read')
			else:
				parser.remove_section('backup')
				parser.remove_section('retain')
				parser.remove_section('exclusions')
		else:
			parser.read(self.conf)

		parser.add_section('backup')
		parser.set('backup','backup',self.fdir_text.get_text())
		parser.set('backup','directory',self.bdir_text.get_text())
		parser.set('backup','shortlog',self.ldir_text.get_text())
		parser.set('backup','longlog',self.ldi2_text.get_text())
		sup = 'False'
		if self.sudo_bton.get_active(): sup = 'True'
		parser.set('backup','super',sup)
		parser.set('backup','time',str(self.time_text.get_adjustment().get_value()))
		parser.set('backup','verbosity',str(self.verbosity.get_adjustment().get_value()))

		parser.add_section('retain')
		for a in self.adbla_box.get_children():
			name = a.get_children()[0].get_text()
			valu = a.get_children()[1].get_adjustment().get_value()
			if name not in [None,'','\n']:
				parser.set('retain',name,str(valu))

		parser.add_section('exclusions')
		kids = self.adblb_box.get_children()
		for a in range(len(kids)):
			setting = kids[a].get_children()[0].get_text()
			if setting not in [None,'','\n']:
				parser.set('exclusions',str(a),setting)

		keyring.set_password('Backup',getpass.getuser(),self.pass_text.get_text())
		with open(self.conf,'w') as f:
			parser.write(f)

	def populate(self):
		parser = configparser.ConfigParser()
		if os.path.exists(self.conf):
			try:
				parser.read(self.conf)
			except:
				print('File cannot be read')
		else:
			return

		self.fdir_text.set_text(parser.get('backup','backup'))
		self.bdir_text.set_text(parser.get('backup','directory'))
		self.ldir_text.set_text(parser.get('backup','shortlog'))
		self.ldi2_text.set_text(parser.get('backup','longlog'))
		self.sudo_bton.set_active(parser.get('backup','super') in ['True','true'])
		self.time_text.get_adjustment().set_value(float(parser.get('backup','time')))
		self.verbosity.get_adjustment().set_value(float(parser.get('backup','verbosity')))
		rets = parser.items('retain')
		for i in range(len(rets)):
			self.addwidget(None,(self.adbla_box,True,self.adbla_cont))
			chil = self.adbla_box.get_children()
			for a in range(len(chil)):
				kids = chil[a].get_children()
				kids[0].set_text(rets[a][0])
				kids[1].get_adjustment().set_value(float(rets[a][1]))
		rets = parser.items('exclusions')
		for i in range(len(rets)):
			self.addwidget(None,(self.adblb_box,False,self.adblb_cont))
			chil = self.adblb_box.get_children()
			for a in range(len(chil)):
				kids = chil[a].get_children()
				kids[0].set_text(rets[a][1])
		try: self.pass_text.set_text(keyring.get_password('Backup',getpass.getuser()))
		except: print('Cannot get password.')
		return

	def addwidget(self,widget,data):
		tbox = Gtk.Box()
		f = Gtk.Entry()
		tbox.pack_start(f,True,True,0)
		f.show()
		if data[1]:
			b = Gtk.SpinButton()
			b.set_adjustment(Gtk.Adjustment(1,1,99,1))
			tbox.pack_start(b,False,False,0)
			b.show()
		else:
			t = Gtk.ToggleButton("File")
			c = Gtk.Button()
			c.set_image(Gtk.Image.new_from_icon_name('document-open',Gtk.IconSize.SMALL_TOOLBAR))
			c.connect("clicked",self.callback,["tog",f,t])
			tbox.pack_start(t,False,False,0)
			tbox.pack_start(c,False,False,0)
			t.show()
			c.show()
		tbox.show()
		data[0].pack_start(tbox, False, False, 0)
		self.scrollable_resize(data[0],data[2])
		return

	def remwidget(self,widget,data):
		box = data[0]
		chi = box.get_children()
		if len(chi) > 2:
			box.remove(chi[len(chi)-1])
			self.scrollable_resize(data[0],data[1])
		return

	def scrollable_resize(self,widget,window):
		num = len(widget.get_children())
		if num < 5:
			window.set_size_request(300,num*28)	
		self.window.resize(self.window.get_size()[0],10)
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

	def pass_check(self,widget):
		self.pass_text.set_editable(self.sudo_bton.get_active())

	def start(self,fil):
		self.conf = fil
		self.builder = Gtk.Builder()
		self.builder.add_from_file('layout_backup.glade')
		self.window = self.builder.get_object('window')

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
		self.adbla_cont = self.builder.get_object('adbla_cont')
		self.adblb_cont = self.builder.get_object('adblb_cont')

		self.pass_text.set_editable(self.sudo_bton.get_active())

		self.populate()

		icons = ['document-open']*4
		icons += ['edit-add','edit-clear']*2
		names = ['bdir','fdir','ldir','ldi2','reta_add','reta_rem','excl_add','excl_rem']
		method = [self.callback]*4
		method += [self.addwidget,self.remwidget]*2
		data = [['folder',names[0]],['folder',names[1]],['file',names[2]],['file',names[3]],\
			(self.adbla_box,True,self.adbla_cont),(self.adbla_box,self.adbla_cont),\
			(self.adblb_box,False,self.adblb_cont),(self.adblb_box,self.adblb_cont)]

		for i in range(8):
			button = self.builder.get_object(names[i]+'_button')
			button.set_image(Gtk.Image.new_from_icon_name(icons[i], Gtk.IconSize.SMALL_TOOLBAR))
			button.connect('clicked',method[i],data[i])

		if len(self.adbla_box.get_children()) < 1: 
			self.addwidget(None,(self.adbla_box,True,self.adbla_cont))
		if len(self.adblb_box.get_children()) < 1:
			self.addwidget(None,(self.adblb_box,False,self.adblb_cont))
		self.addwidget(None,(self.adbla_box,True,self.adbla_cont))
		self.addwidget(None,(self.adblb_box,False,self.adblb_cont))

		self.builder.get_object('okay_button').connect('clicked',self.callback,['Okay'])
		self.builder.get_object('appl_button').connect('clicked',self.callback,['Apply'])

		self.builder.connect_signals(self)

		self.window.set_border_width(10)
		self.window.show_all()
		Gtk.main()

hello = BackupGUI()
hello.start('/etc/backup.conf')
