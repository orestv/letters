import os,sys;
#coding: utf-8
import gtk, pygtk;
import gtk.glade
pygtk.require('2.0')
import model;

COLUMNS = {0: {'name':'№', 'editable':False, 
               'renderer':gtk.CellRendererText, 'type':'text'}, 
           1: {'name':'Отримувач', 'editable':False,  
               'renderer':gtk.CellRendererText, 'type':'text'}, 
           2: {'name':'Тема', 'editable':True,  
               'renderer':gtk.CellRendererText, 'type':'text'}, 
           3: {'name':'Відіслано', 'editable':True,  
               'renderer':gtk.CellRendererText, 'type':'text'}, 
           4: {'name':'Отримано', 'editable':True,  
               'renderer':gtk.CellRendererText, 'type':'text'}, 
           5: {'name':'Квитанція', 'editable':False,  
               'renderer':gtk.CellRendererToggle, 'type':'active'}}

class Window:
    def __init__(self):
        print '------------------------'
        self.gladefile = 'gui.glade'
        self.wTree = gtk.glade.XML(self.gladefile)
        self.window = self.wTree.get_widget('MainWindow')
        self.tvLetters = self.wTree.get_widget('tvLetters')

        dic = {'on_MainWindow_destroy' : gtk.main_quit}
        self.wTree.signal_autoconnect(dic)

        self.tvLetters.set_model(model.TableModel())
        for i in COLUMNS.keys():
            cell = COLUMNS[i]['renderer']()
            cell.set_data('column', i)
            if COLUMNS[i]['editable']:
                cell.connect('edited', self.on_cell_edited, model)
                cell.set_property('editable', True)
            column = gtk.TreeViewColumn(COLUMNS[i]['name'], cell)
            column.add_attribute(cell, COLUMNS[i]['type'], i)
            self.tvLetters.append_column(column)

        self.window.show_all()

    def on_cell_edited(self, cell, path, new_text, model):
        column = cell.get_data('column')
        self.tvLetters.get_model().set_data(path, column, new_text)


if __name__ == '__main__':
    Window()
    gtk.main()
