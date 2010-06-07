import gtk;
import MySQLdb;
import gobject;

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

    TREE_DEPTH = 1
    TREE_SIBLINGS = 9
    def __init__(self):
        '''constructor for the model.  Make sure you call
        PyTreeModel.__init__'''
        gtk.GenericTreeModel.__init__(self)
        self.cn = MySQLdb.connect(read_default_file='~/.mysql.cnf',
                                  db='letters')
        self.update_data()
        
    def update_data(self):
        self.cn.query('''SELECT letters.id, organization, subject, 
                      sent, received, receipt FROM letters 
                      LEFT OUTER JOIN recipients
                      ON letters.recipient_id = recipients.id''')
        self.data = self.cn.store_result()
        self.data = self.data.fetch_row(maxrows=0, how=0)


    def on_get_flags(self):
        return 0

    def on_get_n_columns(self):
        return len(self.data[0])

    def on_get_column_type(self, index):
        return gobject.TYPE_STRING

    def on_get_iter(self, path):
        return path[0]

    def on_get_value(self, node, column):
        return self.data[node][column]

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
