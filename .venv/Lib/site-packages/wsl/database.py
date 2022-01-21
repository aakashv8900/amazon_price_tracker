"""Module wsl.database: Database instances and tuples that can follow references"""

import wsl


def follow_reference(row, key, table_index):
    """Follow a foreign key reference, returning the row that is referenced by the given one

    >>> row = ('foo', 'bar', 'baz')
    >>> key = (1, 2)
    >>> table_index = { ('bar', 'baz'): 42 }
    >>> follow_reference(row, key, table_index)
    42

    Args:
        row (tuple): Database tuple
        key (tuple): A tuple of indices into the row that are used to reference
            the target table.
        table_index (dict): An index of the target table that maps row keys to rows.
    """
    keycolumns = tuple(row[i] for i in key)
    try:
        return table_index[keycolumns]
    except KeyError as e:
        raise wsl.IntegrityError('Failed to follow foreign key reference from %s using %s. Did you build the indices?' %(row, keycolumns)) from e


def make_dbtuple_type(clsname):
    """Make a database tuple type

    The returned type can be embellished with properties that are essentially
    (back-) reference followers. This is for getting the most out of foreign key
    information in Python code.
    """
    def add_reference_property(cls, name, key, table_index):
        """Add a reference property to a class that was erturned by *make_dbtuple_type*"""
        prop = property(lambda row: follow_reference(row, key, table_index))
        setattr(cls, name, prop)

    funcs = {}
    funcs['add_reference_property'] = classmethod(add_reference_property)
    return type(clsname, (tuple,), funcs)


class Database:
    """Database instance.

    Attributes:
        schema (wsl.Schema): The WSL schema of which this database is an instance.
        tuple_types (dict): The dynamically created tuple types. There is one
            for each table in the schema.
        tables: A dict mapping table name to lists of table rows.
        indices: A dict mapping *(tablename, column indices)* pairs to table rows.
    """
    def __init__(self, schema, reference_followers=None):
        """Create a Database instance.

        schema (wsl.Schema):
            The WSL schema of which a database instance should be created.

        reference_followers:
            A list of *(foreign_key_name, member)* pairs, where *foreign key
            name* is the name of a foreign key reference in the given schema and
            *member* is the name of a property to create on tuples of the table
            that is constrained by the foreign key reference.

            *reference_followers* indicates what follower properties should be
            created. If it is *None* then reference followers for all foreign
            keys in the WSL schema are created in their respective tuple types.
            Member name is *ref_KEYNAME* where KEYNAME is the name of the key on
            the foreign table (which must always exist).
        """
        if reference_followers is None:
            reference_followers = []
            for fkey in schema.foreignkeys.values():
                follower = (fkey.name, 'ref_%s' %(fkey.name,))
                reference_followers.append(follower)

        for fkeyname, membername in reference_followers:
            assert fkeyname in schema.foreignkeys

        tuple_types = {}
        for tablename in schema.tables:
            tuple_types[tablename] = make_dbtuple_type(tablename)

        # raw tables are simple lists
        tables = {}
        for tablename in schema.tables:
            tables[tablename] = []

        # all indices indexed by (tablename, columns)
        indices = {}
        for table in schema.tables.values():
            x = (table.name, tuple(range(len(table.columns))))
            assert x not in indices
            indices[x] = {}
        for key in schema.keys.values():
            x = key.table, key.columns
            if x not in indices:
                indices[x] = {}
        for fkey in schema.foreignkeys.values():
            x = fkey.reftable, fkey.refcolumns
            if x not in indices:
                indices[x] = {}

        # create followers
        for fkeyname, membername in reference_followers:
            fkey = schema.foreignkeys[fkeyname]
            member = membername
            key = fkey.columns
            table_index = indices[(fkey.reftable, fkey.refcolumns)]
            tp = tuple_types[fkey.table]
            tp.add_reference_property(member, key, table_index)

        self.schema = schema
        self.tuple_types = tuple_types
        self.tables = tables
        self.indices = indices

    def insert(self, tablename, row):
        table = self.tables[tablename]
        tablespec = self.schema.tables[tablename]
        key = tuple(range(len(tablespec.columns)))
        tp = self.tuple_types[tablename]
        val = tp(row)
        table.append(val)

    def build_indices(self):
        """Build all indices. Currently this must be called precisely once, after all rows are parsed"""
        for (tablename, columns), idx in self.indices.items():
            for row in self.tables[tablename]:
                keycolumns = tuple(row[i] for i in columns)
                idx[keycolumns] = row


if __name__ == '__main__':
    row = ('foo', 'bar', 'baz')
    key = (1, 2)
    table_index = { ('bar', 'baz'): 42 }
    x = follow_reference(row, key, table_index)
    assert x == 42

    tp = make_dbtuple_type('tp')
    tp.add_reference_property('barbaz', key, table_index)
    val = tp(row)
    x = val.barbaz
    assert x == 42
