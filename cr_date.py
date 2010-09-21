import gtk;
import time, datetime;

DATE_FORMAT = '%d %b %Y'

class CellRendererDate(gtk.CellRendererText):
    __qtype_name__ = 'CellRendererDate'
    
    def __init__(self):
        gtk.CellRendererText.__init__(self)
        self.calendar_window = None
        self.calendar = None

    def _create_calendar(self, treeview):
        self.calendar_window = gtk.Dialog(parent = treeview.get_toplevel())
        self.calendar_window.set_decorated(False)
        #self.calendar_window.action_area.hide()
        self.calendar_window.set_property('skip-taskbar-hint', True)

        self.calendar = gtk.Calendar()
        self.calendar.display_options(gtk.CALENDAR_SHOW_DAY_NAMES |
                                      gtk.CALENDAR_SHOW_HEADING)
        self.calendar.connect('day-selected-double-click', self._day_selected,
                              None)
        self.calendar.connect('key-press-event', self._day_selected)
        self.calendar.connect('focus-out-event', self._selection_cancelled)

        self.calendar_window.set_transient_for(None)
        self.calendar_window.vbox.pack_start(self.calendar)

        self.calendar.show()
        self.calendar_window.realize()

    def do_start_editing(self, event, treeview, path, background_area,
                         cell_area, flags):
        if not self.get_property('editable'):
            return

        if not self.calendar_window:
            self._create_calendar(treeview)

        if self.get_property('text'):
            date = datetime.datetime.strptime(self.get_property('text'),
                                              DATE_FORMAT)
        else:
            date = datetime.datetime.today()
        self.calendar.freeze()
        (year, month, day) = (date.year, date.month-1, date.day)
        self.calendar.select_month(int(month), int(year))
        self.calendar.select_day(int(day))
        self.calendar.thaw()

        (tree_x, tree_y) = treeview.get_bin_window().get_origin()
        (tree_w, tree_h) = treeview.window.get_geometry()[2:4]
        (calendar_w, calendar_h) = self.calendar_window.window.get_geometry()[2:4]
        x = tree_x + min(cell_area.x, tree_w - calendar_w +
                         treeview.get_visible_rect().x)
        y = tree_y + min(cell_area.y, tree_h - calendar_h +
                         treeview.get_visible_rect().y)
        self.calendar_window.move(x, y)

        response = self.calendar_window.run()

        if response == gtk.RESPONSE_OK:
            (year, month, day) = self.calendar.get_date()
            date = datetime.date(year, month+1,
                                 day)
            date = date.strftime(DATE_FORMAT)
            print 'Selected date:', date
            self.emit('edited', path, date)
            self.calendar_window.hide()

        return None


    def _day_selected(self, calendar, event):
        if not event or event.type == gtk.gdk.KEY_PRESS and gtk.gdk.keyval_name(event.keyval) == 'Return':
            self.calendar_window.response(gtk.RESPONSE_OK)
            return True

    def _selection_cancelled(self, calendar, event):
        self.calendar_window.response(gtk.RESPONSE_CANCEL)
        return True
