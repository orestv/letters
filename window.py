import os,sys;
#coding: utf-8
import gtk, pygtk;
import gtk.glade
import time;
pygtk.require('2.0')
import model2 as model
import gobject;
import cr_date;
gobject.type_register(cr_date.CellRendererDate)

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

        lsSenders = gtk.ListStore(int, str)
        senders = [(1, 'me'), (2, 'her')]
        for row in senders:
            lsSenders.append(row)

        dic = {'on_MainWindow_destroy' : gtk.main_quit,
               'btnNew_clicked' : self.btnNew_clicked}
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
                cell.connect('edited', self.on_set_cell_text, n)
                type = 'text'
            elif column_renderers[n] == cr_date.CellRendererDate:
                cell.set_property('editable', True)
                cell.connect('edited', self.on_set_cell_date, n)
                type = 'text'
            elif column_renderers[n] == gtk.CellRendererToggle:
                cell.set_property('activatable', True)
                cell.connect('toggled', self.on_set_cell_toggle, n)
                type = 'active'
            elif column_renderers[n] == gtk.CellRendererCombo:
                cell.set_property('editable', True)
                cell.connect('edited', self.on_set_cell_combo, n)
                cell.set_property('model', lsSenders)
                cell.set_property('text-column', 1)

            self.columns[n].add_attribute(cell, type, n)

            self.tvLetters.append_column(self.columns[n])

        self.tvLetters.set_model(m)
        self.window.show_all()

    def on_set_cell_date(self, cell, path, new_text, column):
        self.set_data(path, column, new_text)

    def on_set_cell_text(self, cell, path, new_text, column):
        self.set_data(path, column, new_text)

    def on_set_cell_combo(self, combo, path, iter, column):
        model = combo.get_property('model')
        self.set_data(path, column, iter)


    def on_set_cell_toggle(self, cell, path, column):
        self.set_data(path, column, not cell.get_active())

    def set_data(self, path, column, data):
        self.tvLetters.get_model().set_data(path, column, data)

    def btnNew_clicked(self, event):
        self.new_row_popup()

    def new_row_popup(self):
        model = self.tvLetters.get_model()

        popup = self.wTree.get_widget('dlgNewLetter')

        eNumber = self.wTree.get_widget('eNumber')
        eSubject = self.wTree.get_widget('eSubject')
        eSender = self.wTree.get_widget('eSender')
        eRecipient = self.wTree.get_widget('eRecipient')
        calSent = self.wTree.get_widget('calSent')
        calReceived = self.wTree.get_widget('calReceived')
        chkReceived = self.wTree.get_widget('chkReceived')
        eComment = self.wTree.get_widget('eComment')
        chkReceipt = self.wTree.get_widget('chkReceipt')

        def chkReceived_toggle(event):
            calReceived.set_sensitive(chkReceived.get_active())

        chkReceived.connect('toggled', chkReceived_toggle)

        strNum = model.get_new_number()
        eNumber.set_text(strNum)

        response = popup.run()
        if response == gtk.RESPONSE_OK:
            print 'OK!'
        popup.hide()


if __name__ == '__main__':
    Window()
    gtk.main()
