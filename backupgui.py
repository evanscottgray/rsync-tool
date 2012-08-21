import ConfigParser
import gtk
import os
import sys
import time
import datetime
import pynotify
import keyring
import getpass

class BackupGUI:
	
	def __init__(self,configfile=None,clobinst=None,loggerinst=None):
		self.conf = configfile
		self.clobber = clobinst
		self.log = loggerinst
		if configfile == None or clobinst == None or loggerinst == None:
			self.confrm = False
		else: self.confrm = True
		pynotify.init('Backup')
		return

	def callback(self,widget,data):
#		adbla, adblb, bdir_text, fdir_text, ldir_text, ldi2_text, sudo_button, time_text, verbosity
		print "Button was pressed: {0}".format(data)
		if data == "Okay":
			self.settings()
			self.delete_event(widget,'delete_event',data)
		if data == 'Apply':
			self.settings()
		if data[0] == "folder":
			data[1].set_text(self.fch())
		elif data[0] == 'file':
			data[1].set_text(self.fch(False))
		elif data[0] == 'tog':
			if data[2].get_active():
				data[1].set_text(self.fch(False))
			else: data[1].set_text(self.fch())
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
		toret = ''
		if response == gtk.RESPONSE_OK:
			toret = choo.get_filename()
		choo.destroy()
		return toret

	def check(self,widget,text):
		print 'checked!'
		if widget.get_active() == False:
			print 'Nope'
			text.set_editable(False)
			text.show()
		if widget.get_active() == True:
			print 'Yup'
			text.set_editable(True)
			text.show()

	def addwidget(self,widget,box,spin,window):
		tbox = gtk.HBox(False, 0)
		f = gtk.Entry(max=0)
		tbox.pack_start(f,True,True,0)
		f.show()
		if spin:
			b = gtk.SpinButton(gtk.Adjustment(1,1,99,1))
			tbox.pack_start(b,False,False,0)
			b.show()
		else:
			t = gtk.ToggleButton("File")
			c = gtk.Button()
			c.set_image(gtk.image_new_from_icon_name('folder',gtk.ICON_SIZE_BUTTON))
			c.connect("clicked",self.callback,["tog",f,t])
			tbox.pack_start(t,False,False,0)
			tbox.pack_start(c,False,False,0)
			t.show()
			c.show()
		tbox.show()
		box.pack_start(tbox, False, False, 0)
		if len(box.get_children()) < 5:
			window.set_size_request(300,len(box.get_children())*25+32)
#		else: window.set_size_request(300,157)
		return

	def remwidget(self,widget,box,window):
		chi = box.get_children()
		if len(chi) > 1:
			box.remove(chi[len(chi)-1])
			sz = self.window.get_size()
			self.window.resize(sz[0],10)
			if len(box.get_children()) < 5:
				window.set_size_request(300,len(box.get_children())*25+32)
		return

	def showall(self,wids):
		for w in wids:
			w.show()
		return

	def settings(self):
		parser = ConfigParser.ConfigParser()
		parser.read(self.conf)
		parser.set('backup','backup',self.fdir_text.get_text())
		parser.set('backup','directory',self.bdir_text.get_text())
		parser.set('backup','shortlog',self.ldir_text.get_text())
		parser.set('backup','longlog',self.ldi2_text.get_text())
		parser.set('backup','super',self.sudo_button.get_active())
		parser.set('backup','time',self.time_text.get_adjustment().get_value())
		parser.set('backup','verbosity',self.verbosity.get_adjustment().get_value())
		parser.remove_section('retain')
		parser.add_section('retain')
		for a in self.adbla.get_children():
			parser.set('retain',a.get_children()[0].get_text(),a.get_children()[1].get_adjustment().get_value())
		parser.remove_section('exclusions')
		parser.add_section('exclusions')
		kids = self.adblb.get_children()
		for a in range(len(kids)):
			parser.set('exclusions',str(a),kids[a].get_children()[0].get_text())
		keyring.set_password('Backup',getpass.getuser(),self.pass_text.get_text())
		with open(self.conf,'w') as f:
			parser.write(f)

	def populate(self):
		parser = ConfigParser.ConfigParser()
		parser.read(self.conf)
		self.fdir_text.set_text(parser.get('backup','backup'))
		self.bdir_text.set_text(parser.get('backup','directory'))
		self.ldir_text.set_text(parser.get('backup','shortlog'))
		self.ldi2_text.set_text(parser.get('backup','longlog'))
		self.sudo_button.set_active(parser.get('backup','super') in ['True','true'])
		self.time_text.get_adjustment().set_value(float(parser.get('backup','time')))
		self.verbosity.get_adjustment().set_value(float(parser.get('backup','verbosity')))
		rets = parser.items('retain')
		for i in range(len(rets)-1):
			self.addwidget(None,self.adbla,True,self.adbla_cont)
			chil = self.adbla.get_children()
			for a in range(len(chil)):
				kids = chil[a].get_children()
				kids[0].set_text(rets[a][0])
				kids[1].get_adjustment().set_value(float(rets[a][1]))
		rets = parser.items('exclusions')
		for i in range(len(rets)-1):
			self.addwidget(None,self.adblb,False,self.adblb_cont)
			chil = self.adblb.get_children()
			for a in range(len(chil)):
				kids = chil[a].get_children()
				kids[0].set_text(rets[a][1])
		self.pass_text.set_text(keyring.get_password('Backup',getpass.getuser()))
		return

	def start(self):
		gtk.main()
		return

	def confirm(self,action,t,back_dir):
		if self.confrm != True:
			print "ERROR: Not all required arguments for this method have been provided."
			raise TypeError
		self.log.log('Checking for backup directory.')
		tim = str(datetime.timedelta(seconds=t)).zfill(8)
		if tim == '00:00:00':
			tim = ''
		elif tim[0:3] == '00:0':
			tim = time[4:]
		elif tim[0] + tim[1] == '00':
			tim = tim[2:]
		timetill = ''
		if tim != '': timetill = ' in ' + tim

#	if os.path.exists('/tmp/backup.pid'):
		if self.clobber.exists() or self.clobber.locked():
			self.log.log('Backup already in progress. Please try again later.')
			self.notification('Backup already in progress. Please try again later.','dialog-error')
			exit()

		self.notification(action.title() + ' backup is scheduled to run' +\
			 timetill + '. Please ensure that the backup device is connected.','dialog-warning')
	#	with open('/tmp/backup.pid','w') as f: f.write(str(os.getpid()))
		self.clobber.make()
		time.sleep(t)
		self.log.log('About to check...')
		if not (os.path.exists(back_dir)):
			self.log.log('Staring dialog...')
	
			dialog = gtk.MessageDialog(None, 0, gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK,\
				action.title() + ' backup is scheduled to run. Is the backup device mounted at ' + back_dir + '?')
			dialog.run()
	
			if not os.path.exists(back_dir):
				dialog_response = 0
				self.log.log('Starting second dialog...')
				dialog.destroy()
				dialog = gtk.MessageDialog(None,0,gtk.MESSAGE_INFO,gtk.BUTTONS_OK_CANCEL,'Please mount the device now.')
				dialog_response = dialog.run()
	
				if dialog_response != -5 or not os.path.exists(back_dir):
					self.notification(action.title() + ' backup failed: unable to locate backup device. Please try again later.','dialog-error')
					exit()
			dialog.destroy()
		else:
			self.notification(action.title() + ' backup is now running. Please do not remove backup device.','dialog-warning')
			try: self.clobber.lock()#os.rename('/tmp/backup.pid','/tmp/backup_lock.pid')
			except OSError as e: self.log.log('ERROR: could not rename lockfile {0} ({1}).\n\t{2}'.format(e.filename,e.errno,e.strerror))
		return

	def notification(self,string,icon):
		n = pynotify.Notification('Backup',string,icon)
		n.set_urgency(pynotify.URGENCY_CRITICAL)
		n.show()
		return

#hello = BackupGUI('/etc/backup.conf')
#print hello.start()
