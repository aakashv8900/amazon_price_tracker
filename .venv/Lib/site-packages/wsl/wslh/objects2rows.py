from .datatypes import Value, Struct, Option, Set, List, Dict, Query


class Settable():
    def __init__(self):
        self.x = None

    def __repr__(self):
        if self.x is None:
            return '?'
        else:
            return '!%s' %(self.x,)

    def set(self, x):
        self.x = x

    def get(self):
        return self.x


def add_rows(query, cols, rows, database):
    key = tuple(cols.index(v) for v in query.variables)
    table = database.setdefault(query.table, [])
    for row in rows:
        table.append(tuple(row[i].get() for i in key))


def value2rows(cols, rows, objs, spec, database):
    if spec.query is not None:
        nextcols = cols + spec.query.freshvariables
        nextrows = []
        nextobjs = []
        for row, obj in zip(rows, objs):
            if obj is not None:
                nextrows.append(row + tuple(Settable() for _ in spec.query.freshvariables))
                nextobjs.append(obj)
    else:
        nextcols = cols
        nextrows = rows
        nextobjs = objs
    idx = nextcols.index(spec.variable)
    for nextrow, nextobj in zip(nextrows, nextobjs):
        nextrow[idx].set(nextobj)
    if spec.query is not None:
        add_rows(spec.query, nextcols, nextrows, database)


def struct2rows(cols, rows, objs, spec, database):
    nextcols = cols
    nextrows = rows
    nextobjs = { key: [] for key in spec.childs }
    for obj in objs:
        assert obj is not None
        for key in spec.childs:
            if key not in obj:
                raise ValueError('Expected member "%s" but got object with these keys: %s' %(key, ', '.join(str(k) for k in obj.keys())))
            nextobjs[key].append(obj[key])
    for key in spec.childs:
        any2rows(nextcols, nextrows, nextobjs[key], spec.childs[key], database)


def option2rows(cols, rows, objs, spec, database):
    nextcols = cols + spec.query.freshvariables
    nextrows = []
    nextobjs = []
    for row, obj in zip(rows, objs):
        if obj is not None:
            nextrows.append(row + tuple(Settable() for _ in spec.query.freshvariables))
            nextobjs.append(obj)

    any2rows(nextcols, nextrows, nextobjs, spec.childs['_val_'], database)

    add_rows(spec.query, nextcols, nextrows, database)


def set2rows(cols, rows, objs, spec, database):
    nextcols = cols + spec.query.freshvariables
    nextrows = []
    nextobjs_idxs = []
    nextobjs_vals = []
    for row, set_ in zip(rows, objs):
        for item in set_:
            nextrows.append(row + tuple(Settable() for _ in spec.query.freshvariables))
            nextobjs_vals.append(item)
    any2rows(nextcols, nextrows, nextobjs_vals, spec.childs['_val_'], database)
    add_rows(spec.query, nextcols, nextrows, database)


def list2rows(cols, rows, objs, spec, database):
    nextcols = cols + spec.query.freshvariables
    nextrows = []
    nextobjs_idxs = []
    nextobjs_vals = []
    for row, lst in zip(rows, objs):
        for i, item in enumerate(lst):
            nextrows.append(row + tuple(Settable() for _ in spec.query.freshvariables))
            nextobjs_idxs.append(i)
            nextobjs_vals.append(item)
    any2rows(nextcols, nextrows, nextobjs_idxs, spec.childs['_idx_'], database)
    any2rows(nextcols, nextrows, nextobjs_vals, spec.childs['_val_'], database)
    add_rows(spec.query, nextcols, nextrows, database)


def dict2rows(cols, rows, objs, spec, database):
    nextcols = cols + spec.query.freshvariables
    nextrows = []
    nextobjs_keys = []
    nextobjs_vals = []
    for row, dct in zip(rows, objs):
        for key, val in dct.items():
            nextrows.append(row + tuple(Settable() for _ in spec.query.freshvariables))
            nextobjs_keys.append(key)
            nextobjs_vals.append(val)
    any2rows(nextcols, nextrows, nextobjs_keys, spec.childs['_key_'], database)
    any2rows(nextcols, nextrows, nextobjs_vals, spec.childs['_val_'], database)
    add_rows(spec.query, nextcols, nextrows, database)


def any2rows(cols, rows, objs, spec, database):
    assert len(rows) == len(objs)

    typ = type(spec)

    if typ == Value:
        value2rows(cols, rows, objs, spec, database)

    elif typ == Struct:
        struct2rows(cols, rows, objs, spec, database)

    elif typ == Option:
        option2rows(cols, rows, objs, spec, database)

    elif typ == Set:
        set2rows(cols, rows, objs, spec, database)

    elif typ == List:
        list2rows(cols, rows, objs, spec, database)

    elif typ == Dict:
        dict2rows(cols, rows, objs, spec, database)

    else:
        raise TypeError()  # or missing case?


def objects2rows(schema, spec, objs):
    if not any(isinstance(spec, t) for t in [Value, Struct, Option, Set, List, Dict]):
        raise TypeError()

    database = {}

    any2rows((), [()], [objs], spec, database)

    for table in database.values():
        table.sort()

    return database
