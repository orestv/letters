import os,sys;
#coding: utf-8
import gtk, pygtk;
import gtk.glade
import time;
pygtk.require('2.0')
import model2 as model
import gobject;

def is_date(string):
    try:
        time.strptime(string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def is_string(string):
    return True


class Window:
    def __init__(self):
        print '------------------------'
        self.gladefile = 'gui.glade'
        self.wTree = gtk.glade.XML(self.gladefile)
        self.window = self.wTree.get_widget('MainWindow')
        self.tvLetters = self.wTree.get_widget('tvLetters')

        dic = {'on_MainWindow_destroy' : gtk.main_quit}
        self.wTree.signal_autoconnect(dic)
        m = model.TableModel()

        column_names = m.get_column_names()
        column_renderers = m.get_column_renderers()
        self.columns = [None] * len(column_names)

        for n in range(len(column_names)):
            cell = column_renderers[n]()
            self.columns[n] = gtk.TreeViewColumn(column_names[n], cell)

            if column_renderers[n] == gtk.CellRendererText:
                cell.set_property('editable', True)
                type = 'text'
            elif column_renderers[n] == gtk.CellRendererToggle:
                cell.set_property('activatable', True)
                cell.connect('toggled', self.on_set_cell_toggle, n)
                type = 'active'
            self.columns[n].add_attribute(cell, type, n)

            self.tvLetters.append_column(self.columns[n])

        self.tvLetters.set_model(m)


        self.window.show_all()

    def on_set_cell_text(self, cell, path, new_text, column):
        print cell, path, new_text, column
        if COLUMNS[column]['validator'](new_text):
            self.set_data(path, column, new_text)

    def on_set_cell_combo(self, combo, path, iter, column):
        self.set_data(path, column, iter)


    def on_set_cell_toggle(self, cell, path, column):
        self.set_data(path, column, not cell.get_active())

    def set_data(self, path, column, data):
        self.tvLetters.get_model().set_data(path, column, data)



if __name__ == '__main__':
    Window()
    gtk.main()
