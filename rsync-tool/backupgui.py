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
#       adbla, adblb, bdir_text, fdir_text, ldir_text, ldi2_text, sudo_button, time_text, verbosity
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
            c.set_image(gtk.image_new_from_icon_name('document-open',gtk.ICON_SIZE_BUTTON))
            c.connect("clicked",self.callback,["tog",f,t])
            tbox.pack_start(t,False,False,0)
            tbox.pack_start(c,False,False,0)
            t.show()
            c.show()
        tbox.show()
        box.pack_start(tbox, False, False, 0)
        if len(box.get_children()) < 5:
            window.set_size_request(300,len(box.get_children())*25+32)
#       else: window.set_size_request(300,157)
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
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('Configuration Editor')
        self.window.connect("delete_event",self.delete_event)
        self.window.set_border_width(10)

        text_box = gtk.VBox(False,12)
        bdir_label = gtk.Label("Destination: ")
        bdir_label.set_alignment(0,0.5)
        fdir_label = gtk.Label("Source: ")
        fdir_label.set_alignment(0,0.5)
        ldir_label = gtk.Label("Log file: ")
        ldir_label.set_alignment(0,0.5)
        ldi2_label = gtk.Label("Extended log: ")
        ldi2_label.set_alignment(0,0.5)
        text_box.pack_start(fdir_label, False, False, 0)
        text_box.pack_start(bdir_label, False, False, 0)
        text_box.pack_start(ldir_label, False, False, 0)
        text_box.pack_start(ldi2_label, False, False, 0)

        bdir_box = gtk.HBox(False,0)
        self.bdir_text = gtk.Entry(max=0)
        self.bdir_text.set_editable(True)
        bdir_button = gtk.Button()
        bdir_button.set_image(gtk.image_new_from_icon_name('document-open',gtk.ICON_SIZE_BUTTON))
        bdir_button.connect("clicked",self.callback,["folder",self.bdir_text])
        bdir_box.pack_start(self.bdir_text, True, True, 0)
        bdir_box.pack_start(bdir_button, False, False, 0)

        fdir_box = gtk.HBox(False,0)
        self.fdir_text = gtk.Entry(max=0)
        self.fdir_text.set_editable(True)
        fdir_button = gtk.Button()
        fdir_button.set_image(gtk.image_new_from_icon_name('document-open',gtk.ICON_SIZE_BUTTON))
        fdir_button.connect("clicked",self.callback,["folder",self.fdir_text])
        fdir_box.pack_start(self.fdir_text, True, True, 0)
        fdir_box.pack_start(fdir_button, False, False, 0)

        ldir_box = gtk.HBox(False,0)
        self.ldir_text = gtk.Entry(max=0)
        self.ldir_text.set_editable(True)
        ldir_button = gtk.Button()
        ldir_button.set_image(gtk.image_new_from_icon_name('document-open',gtk.ICON_SIZE_BUTTON))
        ldir_button.connect("clicked",self.callback,["file",self.ldir_text])
        ldir_box.pack_start(self.ldir_text, True, True, 0)
        ldir_box.pack_start(ldir_button, False, False, 0)

        ldi2_box = gtk.HBox(False,0)
        self.ldi2_text = gtk.Entry(max=0)
        self.ldi2_text.set_editable(True)
        ldi2_button = gtk.Button()
        ldi2_button.set_image(gtk.image_new_from_icon_name('document-open',gtk.ICON_SIZE_BUTTON))
        ldi2_button.connect("clicked",self.callback,["file",self.ldi2_text])
        ldi2_box.pack_start(self.ldi2_text, True, True, 0)
        ldi2_box.pack_start(ldi2_button, False, False, 0)

        reta_box = gtk.VBox(False,0)
        reta_label = gtk.Label("Levels to retain")
        reta_label.set_alignment(0,0.5)
        reta_box.pack_start(reta_label, False, False, 0)

        self.adbla_cont = gtk.ScrolledWindow()
        self.adbla_cont.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_ALWAYS)
        self.adbla_cont.set_border_width(10)
        self.adbla_cont.set_size_request(400,157)
        self.adbla = gtk.VBox(True,0)
        self.adbla.show()
        self.addwidget(None,self.adbla,True,self.adbla_cont)
        self.adbla_cont.show()
        self.adbla_cont.add_with_viewport(self.adbla)
        reta_box.pack_start(self.adbla_cont, False, False, 0)

        reta_add_button = gtk.Button()
        reta_add_button.set_image(gtk.image_new_from_icon_name('edit-add',gtk.ICON_SIZE_BUTTON))
        reta_add_button.connect('clicked',self.addwidget,self.adbla,True,self.adbla_cont)
        reta_rem_button = gtk.Button()
        reta_rem_button.set_image(gtk.image_new_from_icon_name('edit-clear',gtk.ICON_SIZE_BUTTON))
        reta_rem_button.connect('clicked',self.remwidget,self.adbla,self.adbla_cont)
        adrem_box = gtk.HBox(False,0)
        adrem_box.pack_end(reta_add_button, False, False, 0)
        adrem_box.pack_end(reta_rem_button, False, False, 0)
        adrem_box.show()
        reta_box.pack_start(adrem_box, False, False, 0)

        excl_box = gtk.VBox(False,0)
        excl_label = gtk.Label("Exclusions")
        excl_label.set_alignment(0,0.5)
        excl_box.pack_start(excl_label, False, False, 0)

        self.adblb_cont = gtk.ScrolledWindow()
        self.adblb_cont.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_ALWAYS)
        self.adblb_cont.set_border_width(10)
        self.adblb_cont.set_size_request(400,157)
        self.adblb = gtk.VBox()
        self.adblb.show()
        self.addwidget(None,self.adblb,False,self.adblb_cont)
        self.adblb_cont.show()
        self.adblb_cont.add_with_viewport(self.adblb)
        excl_box.pack_start(self.adblb_cont, True, True, 0)

        excl_add_button = gtk.Button()
        excl_add_button.set_image(gtk.image_new_from_icon_name('edit-add',gtk.ICON_SIZE_BUTTON))
        excl_add_button.connect('clicked',self.addwidget,self.adblb,False,self.adblb_cont)
        excl_rem_button = gtk.Button()
        excl_rem_button.set_image(gtk.image_new_from_icon_name('edit-clear',gtk.ICON_SIZE_BUTTON))
        excl_rem_button.connect('clicked',self.remwidget,self.adblb,self.adblb_cont)
        bdrem_box = gtk.HBox(False,0)
        bdrem_box.pack_end(excl_add_button, False, False, 0)
        bdrem_box.pack_end(excl_rem_button, False, False, 0)
        bdrem_box.show()
        excl_box.pack_start(bdrem_box, False, False, 0)

        pass_box = gtk.HBox(False,0)
        pass_label = gtk.Label("User password for sudo authentication: ")
        self.pass_text = gtk.Entry(max=0)
        self.pass_text.set_visibility(False)
        pass_box.pack_start(pass_label)
        pass_box.pack_start(self.pass_text)

        time_box = gtk.HBox(False,10)
        time_label = gtk.Label("Backup delay: ")
        self.time_text = gtk.SpinButton(gtk.Adjustment(0,0,600,30,90))
        time_box.pack_start(time_label,False, False, 0)
        time_box.pack_start(self.time_text, False, False, 0)

        self.sudo_button = gtk.CheckButton("Run as super user")
        self.sudo_button.connect('clicked',self.check,self.pass_text)
        time_box.pack_start(self.sudo_button, False, False, 0)

        verb_box = gtk.HBox(False, 8)
        verb_label = gtk.Label("Notification level: ")
        self.verbosity = gtk.HScale(gtk.Adjustment(1,0,2,1))
        self.verbosity.set_digits(0)
        self.verbosity.set_value_pos(gtk.POS_LEFT)
        verb_box.pack_start(verb_label, False, False, 0)
        verb_box.pack_start(self.verbosity, True, True, 0)
        verb_label.show()
        self.verbosity.show()
        verb_box.show()

        comm_box = gtk.HBox(False,0)
        okay_button = gtk.Button("   OK   ")
        okay_button.connect("clicked",self.callback,"Okay")
        canc_button = gtk.Button("Cancel")
        canc_button.connect("clicked", self.delete_event,'clicked')
        appl_button = gtk.Button("Apply")
        appl_button.connect("clicked", self.callback, "Apply")
        comm_box.pack_end(appl_button, False, False, 0)
        comm_box.pack_end(canc_button, False, False, 0)
        comm_box.pack_end(okay_button, False, False, 0)

        fils_box = gtk.VBox(False,0)
        fils_box.show()
        fils_box.pack_start(bdir_box, False, False, 0)
        fils_box.pack_start(fdir_box, False, False, 0)
        fils_box.pack_start(ldir_box, False, False, 0)
        fils_box.pack_start(ldi2_box, False, False, 0)

        fil2_box = gtk.HBox(False,0)
        fil2_box.show()
        fil2_box.pack_start(text_box, False, False, 0)
        fil2_box.pack_start(fils_box, True, True, 0)

        win_box = gtk.VBox(False,0)
        win_box.pack_start(fil2_box, False, False, 5)
        win_box.pack_start(time_box, False, False, 5)
        win_box.pack_start(pass_box, False, False, 5)
        win_box.pack_start(verb_box, False, False, 5)
        win_box.pack_start(reta_box, False, False, 5)
        win_box.pack_start(excl_box, True, True, 5)
        win_box.pack_start(comm_box, False, False, 5)
        win_box.show()

        self.window.add(win_box)

        labels = [ldir_label,ldi2_label,reta_label,bdir_label,fdir_label,reta_label,excl_label,time_label,pass_label]
        buttons = [ldir_button,ldi2_button,bdir_button,fdir_button,okay_button,canc_button,appl_button,\
            reta_add_button,reta_rem_button,excl_add_button,excl_rem_button, self.sudo_button]
        boxes = [text_box,bdir_box,fdir_box,ldir_box,ldi2_box,reta_box,excl_box,comm_box,time_box,pass_box]
        entries = [self.bdir_text,self.fdir_text,self.ldir_text,self.ldi2_text,self.time_text,self.pass_text]

        self.showall(labels + buttons + boxes + entries)
        self.populate()
        self.window.show()
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
        elif tim[0:4] == '00:0':
            tim = tim[4:]
        elif tim[0:2] == '00':
            tim = tim[2:]
        timetill = ''
        if tim != '': timetill = ' in ' + tim

#   if os.path.exists('/tmp/backup.pid'):
        if self.clobber.exists() or self.clobber.locked():
            self.log.log('Backup already in progress. Please try again later.')
            self.notification('Backup already in progress. Please try again later.','dialog-error')
            exit()

        self.notification(action.title() + ' backup is scheduled to run' +\
             timetill + '. Please ensure that the backup device is connected.','dialog-warning')
    #   with open('/tmp/backup.pid','w') as f: f.write(str(os.getpid()))
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
