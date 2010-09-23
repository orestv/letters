#coding: utf-8
import gtk;
import sqlite3 as sqlite;
import gobject;
import time, calendar
import cr_date;
import re;

DATABASE_PATH = 'letters.db'
def format_date_down(t):
    if not t:
        return ''
    t = int(t)
    if t == 999:
        return ''
    return time.strftime(cr_date.DATE_FORMAT, time.localtime(t))

def format_date_up(s):
    if not s:
        return ''
    return time.mktime(time.strptime(s, cr_date.DATE_FORMAT))

def format_bool_up(b):
    if b:
        return 1
    else:
        return 0

def format_bool_down(b):
    return (b == 1)


class TableModel(gtk.GenericTreeModel):
    column_names = ['id', '№', 'Відправник', 'Отримувач', 
                    'Тема', 'Коментар', 'Відіслано', 'Отримано', 'Квитанція']
    column_names_sql = ['id', 'number', 'sender', 'recipient', 
                        'subject', 'comment', 'sent', 'received', 'receipt']
    column_renderers = [gtk.CellRendererText, gtk.CellRendererText,
                        gtk.CellRendererText, gtk.CellRendererText,
                        gtk.CellRendererText, gtk.CellRendererText,
                        cr_date.CellRendererDate,
                        cr_date.CellRendererDate, gtk.CellRendererToggle]
    column_types = [int, str, str, str, str, str, str, str, int]
    column_processors_down = [None, None, None, None, 
                              None, None, format_date_down, format_date_down, 
                             format_bool_down]
    column_processors_up = [None, None, None, None, 
                            None, None, format_date_up, format_date_up, 
                           format_bool_up]
    def __init__(self):
        gtk.GenericTreeModel.__init__(self)
        self.conn = sqlite.connect(DATABASE_PATH)
        if not is_db_intact(self.conn):
            generate_db_structure(self.conn)
        self.download_data()

    def download_data(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT id, number, sender,
                       recipient, subject, comment, sent,
                       received, receipt FROM letters''')
        self.data = cursor.fetchall()
        for n in range(len(self.data)):
            self.data[n] = list(self.data[n])
        cursor.close()
        #self.data.sort(lambda x, y : cmp(x[1], y[1]))


    def set_data(self, row, col, value):
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

    def add_letter(self, number, subject, sender, recipient,
                sent, received, comment, receipt):
        print received
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO letters (number, sender, recipient,
                       subject, comment, sent, received, receipt)
                       VALUES(?, ?, ?, ?, ?, ?, ?, ?);''', 
                       (unicode(number), unicode(sender), unicode(recipient),
                       unicode(subject), unicode(comment),
                       format_date_up(sent), format_date_up(received),
                       format_bool_up(receipt)))
        self.conn.commit()
        cursor.close()
        self.download_data()
        nRow = len(self.data)-1
        path = (nRow,)
        iter = self.get_iter(path)
        self.row_inserted(path, iter)

    def del_letter(self, iter):
        if not iter:
            return
        id = int(self.get_value(iter, 0))
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM letters WHERE id = ?''', (id,))
        self.conn.commit()
        cursor.close()
        self.download_data()
        for n in range(len(self.data)):
            if self.data[n][0] == id:
                break
        self.row_deleted((n,))

    def get_new_number(self):
        cursor = self.conn.cursor()        
        cursor.execute('''SELECT number FROM letters WHERE strftime('%Y', 'now')
                       = strftime('%Y', datetime(sent, 'unixepoch'));''')
        nums = cursor.fetchall()
        nums = [n[0] for n in nums]
        cursor.close()
        strYear = time.strftime('%y', time.localtime())
        if nums:
            r = re.compile('[0-9]*')
            nMax =  max([int(r.match(n).group(0)) for n in nums])
            nNew = nMax + 1
        else:
            nNew = 1
        return str(nNew) + '/' + strYear


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
        if self.data:
            return path[0]
        else:
            return None

    def on_get_value(self, rowref, nCol):
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
        return False

    def on_iter_children(self, iter):
        if iter:
            return None
        else:
            if self.data:
                return self.data[0]
            else:
                return None

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
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE letters 
                   (id INTEGER PRIMARY KEY,
                   number TEXT, sender TEXT, recipient TEXT, 
                   subject TEXT, comment TEXT, sent DATE,
                   received DATE, receipt INTEGER)''')
    #cursor.execute('''INSERT INTO letters (id, number, sender, recipient,
    #               subject, sent, received, receipt)
    #               VALUES(NULL, '5/10', 'Smile', 'Seth', 'asdf', 999, 999, 0)''')
    conn.commit()

