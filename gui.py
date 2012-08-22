try:
	from gi.repository import Gtk
except:
	print('error')
else:
	print('what the actual fuck')

class BackupGUI:
	def __init__(self):
		print('Okay, some weird shit is going down.')
		return

	def fchoose(self,folder=True):
		choo = Gtk.FileChooserDialog("Open..",
			None,
			Gtk.FileChooserAction.OPEN,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		response = choo.run()
		choo.destroy()
		return response


hello = BackupGUI()
