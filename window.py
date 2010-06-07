import os,sys;
#coding: utf-8
import gtk, pygtk;
import gtk.glade
pygtk.require('2.0')
import model;

COLUMNS = {0: ('№', False), 1: ('Отримувач', False), 2: ('Тема', True), 
           3: ('Відіслано', True), 4: ('Отримано', True), 
           5: ('Квитанція', False)}

class Window:
    def __init__(self):
        self.gladefile = 'gui.glade'
        self.wTree = gtk.glade.XML(self.gladefile)
        self.window = self.wTree.get_widget('MainWindow')
        self.tvLetters = self.wTree.get_widget('tvLetters')

        dic = {'on_MainWindow_destroy' : gtk.main_quit}
        self.wTree.signal_autoconnect(dic)

        self.tvLetters.set_model(model.TableModel())
        for i in COLUMNS.keys():
            cell = gtk.CellRendererText()
            cell.set_data('column', i)
            if COLUMNS[i][1]:
                cell.connect('edited', self.on_cell_edited, model)
                cell.set_property('editable', True)
            self.tvLetters.append_column(
                gtk.TreeViewColumn(COLUMNS[i][0], cell, text=i))

        self.window.show_all()

    def on_cell_edited(self, cell, path, new_text, model):
        column = cell.get_data('column')
        self.tvLetters.get_model().set_data(path, column, new_text)


if __name__ == '__main__':
    Window()
    gtk.main()
