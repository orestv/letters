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
        print '------------------------------'
        self.gladefile = 'gui.glade'
        self.wTree = gtk.glade.XML(self.gladefile)
        self.window = self.wTree.get_widget('MainWindow')
        self.tvLetters = self.wTree.get_widget('tvLetters')

        dic = {'on_MainWindow_destroy' : gtk.main_quit}
        self.wTree.signal_autoconnect(dic)

        self.tvLetters.set_model(model.TableModel())
        for i in range(6):
            cell = gtk.CellRendererText()
            self.tvLetters.append_column(
                gtk.TreeViewColumn(COLUMNS[i], cell, text=i))

        self.window.show_all()


if __name__ == '__main__':
    Window()
    gtk.main()
