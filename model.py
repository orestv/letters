import gtk;
import MySQLdb;
import gobject;
from MySQLdb.constants import FIELD_TYPE


class TableModel(gtk.GenericTreeModel):
    '''This class represents the model of a tree.  The iterators used
    to represent positions are converted to python objects when passed
    to the on_* methods.  This means you can use any python object to
    represent a node in the tree.  The None object represents a NULL
    iterator.

    In this tree, we use simple tuples to represent nodes, which also
    happen to be the tree paths for those nodes.  This model is a tree
    of depth 3 with 5 nodes at each level of the tree.  The values in
    the tree are just the string representations of the nodes.'''

    COLUMNS = {0: ('id', gobject.TYPE_INT), 
               1: ('organization', gobject.TYPE_STRING),
               2: ('subject', gobject.TYPE_STRING),
               3: ('sent', gobject.TYPE_STRING),
               4: ('received', gobject.TYPE_STRING),
               5: ('receipt', gobject.TYPE_BOOLEAN)}
    def __init__(self):
        '''constructor for the model.  Make sure you call
        PyTreeModel.__init__'''
        gtk.GenericTreeModel.__init__(self)
        my_conv = {FIELD_TYPE.LONG: int,
                   FIELD_TYPE.BIT : lambda t : t == '\x01'}
        self.cn = MySQLdb.connect(read_default_file='~/.mysql.cnf',
                                  db='letters', conv=my_conv)
        self.update_data()
        
    def update_data(self):
        self.cn.query('''SELECT letters.id, organization, subject, 
                      sent, received, receipt FROM letters 
                      LEFT OUTER JOIN recipients
                      ON letters.recipient_id = recipients.id''')
        self.data = self.cn.store_result()
        self.data = self.data.fetch_row(maxrows=0, how=1)
        print self.data

    def set_data(self, path, col, data):
        column_name = self.COLUMNS[col][0]
        path = int(path)
        old_data = self.get_value(self.get_iter(path), col)
        if old_data == data:
            return
        id = self.data[path]['id']
        query = '''UPDATE letters SET %s = '%s' WHERE
                      id = %s;''' % (column_name, data, id)
        self.cn.query('''UPDATE letters SET `%s` = '%s' WHERE
                      id = %s;''' % (column_name, data, id))
        self.update_data()


    def on_get_flags(self):
        return gtk.TREE_MODEL_LIST_ONLY

    def on_get_n_columns(self):
        return len(self.data[0])

    def on_get_column_type(self, index):
        return self.COLUMNS[index][1]

    def on_get_iter(self, path):
        return path[0]

    def on_get_value(self, node, column):
        return self.data[node][self.COLUMNS[column][0]]

    def on_iter_next(self, node):
        if node != None:
            if node < len(self.data)-1:
                return node+1
            else:
                return None

    def on_iter_children(self, node):
        return None

    def on_iter_has_child(self, node):
        return False

    def on_iter_n_children(self, node):
        if not node:
            return len(self.data)
        else:
            return 0

    def on_iter_nth_child(self, node, n):
        if not node:
            return self.data[n]
        else:
            return None
        
    def on_iter_parent(self, node):
        return None
