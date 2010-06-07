import os,sys;
#coding: utf-8
import gtk, pygtk;
import gtk.glade
pygtk.require('2.0')
import model;

COLUMNS = {0: '№', 1: 'Отримувач', 2: 'Тема', 
           3: 'Відіслано', 4: 'Отримано', 
           5: 'Квитанція'}

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
            cell.set_property('editable', True)
            cell.set_data('column', i)
            cell.connect('edited', self.on_cell_edited, model)
            self.tvLetters.append_column(
                gtk.TreeViewColumn(COLUMNS[i], cell, text=i))

        self.window.show_all()

    def on_cell_edited(self, cell, path, new_text, model):
        column = cell.get_data('column')
        self.tvLetters.get_model().set_data(path, column, new_text)


if __name__ == '__main__':
    Window()
    gtk.main()
