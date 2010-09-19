#coding: utf-8
import gtk;
import sqlite3 as sqlite;
import gobject;
import time, calendar
import cr_date;

DATABASE_PATH = 'letters.db'
def format_date_down(t):
    t = int(t)
    return time.strftime(cr_date.DATE_FORMAT, time.localtime(t))

def format_date_up(s):
    return time.mktime(time.strptime(s, cr_date.DATE_FORMAT))


COLUMNS = {0: {'name':'id', 'type':gobject.TYPE_INT}, 
           1: {'name':'sender', 'type':gobject.TYPE_STRING},
           2: {'name':'recipient', 'type':gobject.TYPE_STRING},
           3: {'name':'subject', 'type':gobject.TYPE_STRING},
           4: {'name':'sent', 'type':gobject.TYPE_STRING},
           5: {'name':'received', 'type':gobject.TYPE_STRING},
           6: {'name':'receipt', 'type':gobject.TYPE_BOOLEAN}}


class TableModel(gtk.GenericTreeModel):
    column_names = ['id', '№', 'Відправник', 'Отримувач', 
                    'Тема', 'Відіслано', 'Отримано', 'Квитанція']
    column_names_sql = ['id', 'number', 'sender_id', 'recipient', 
                        'subject', 'sent', 'received', 'receipt']
    column_renderers = [gtk.CellRendererText, gtk.CellRendererText,
                        gtk.CellRendererCombo, gtk.CellRendererText,
                        gtk.CellRendererText, cr_date.CellRendererDate,
                        cr_date.CellRendererDate, gtk.CellRendererToggle]
    column_types = [int, str, int, str, str, str, str, int]
    column_processors_down = [None, None, None, None, 
                              None, format_date_down, format_date_down, None]
    column_processors_up = [None, None, None, None, 
                            None, format_date_up, format_date_up, None]
    def __init__(self):
        gtk.GenericTreeModel.__init__(self)
        self.conn = sqlite.connect(DATABASE_PATH)
        if not is_db_intact(self.conn):
            generate_db_structure(self.conn)
        self.download_data()

    def download_data(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT letters.id AS letter_id, number, senders.id,
                       recipient, subject, sent,
                       received, receipt FROM letters
                       LEFT OUTER JOIN senders ON letters.sender_id = 
                       senders.id''')
        self.data = cursor.fetchall()
        for n in range(len(self.data)):
            self.data[n] = list(self.data[n])
        cursor.close()

    def set_data(self, row, col, value):
        print value
        row, col = int(row), int(col)
        proc = self.column_processors_up[col]
        if proc:
            value = proc(value)
        self.data[row][col] = value

        cursor = self.conn.cursor()
        cursor.execute('UPDATE letters SET ' + self.column_names_sql[col] +
                       '= ? WHERE id = ?', (unicode(value), self.data[row][0]))
        self.conn.commit()
        cursor.close()

    def get_column_names(self):
        return self.column_names

    def get_column_renderers(self):
        return self.column_renderers

    def on_get_n_columns(self):
        return len(self.column_names)

    def on_get_column_type(self, n):
        return self.column_types[n]

    def on_get_flags(self):
        return gtk.TREE_MODEL_LIST_ONLY|gtk.TREE_MODEL_ITERS_PERSIST

    def on_get_iter(self, path):
        return path[0]

    def on_get_path(self, iter):
        return data[iter][0]

    def on_get_value(self, rowref, nCol):
        #print 'RowRef: ', rowref, ', nCol: ', nCol
        proc = self.column_processors_down[nCol]
        if rowref < len(self.data):
            value = self.data[rowref][nCol]
            if proc:
                value = proc(value)
            return value
        else:
            return None

    def on_iter_next(self, rowref):
        if rowref < len(self.data)-1:
            return rowref+1
        else:
            return None

    def on_iter_has_child(self, iter):
        print 'children?'
        return False

    def on_iter_children(self, iter):
        if iter:
            return None
        else:
            return self.data[0]

    def on_iter_nth_child(self, iter, n):
        if iter:
            return None
        try:
            return self.data[n]
        except IndexError:
            return None


def is_db_intact(conn):
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT id FROM letters LIMIT 1')
    except sqlite.OperationalError:
        return False
    return True

def generate_db_structure(conn):
    print 'Generating structure!'
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE letters 
                   (id INTEGER PRIMARY KEY,
                   number TEXT, sender_id INTEGER, recipient TEXT, 
                   subject TEXT, sent INTEGER,
                   received INTEGER, receipt INTEGER)''')
    cursor.execute('''CREATE TABLE senders 
                   (id INTEGER PRIMARY KEY,
                   name TEXT)''')
    cursor.execute('''INSERT INTO senders (name) VALUES ('Сирова Таня');''')
    cursor.execute('''INSERT INTO senders (name) VALUES ('Ващук Оксана');''')
    cursor.execute('''INSERT INTO letters (id, number, sender_id, recipient,
                   subject, sent, received, receipt)
                   VALUES(NULL, '5/10', 1, 'Seth', 'asdf', 555, 999, 0)''')
    cursor.execute('''INSERT INTO letters (id, number, sender_id, recipient,
                   subject, sent, received, receipt)
                   VALUES(NULL, '5/10', 2, 'Seth', 'asdf', 555, 999, 0)''')
    conn.commit()

