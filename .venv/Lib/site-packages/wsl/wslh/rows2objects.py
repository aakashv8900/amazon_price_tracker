from .datatypes import Value, Struct, Option, Set, List, Dict, Query


def find_child_rows(cols, rows, objs, query, database):
    assert len(rows) == len(objs)

    freshidxs = tuple(i for i, v in enumerate(query.variables) if v in query.freshvariables)
    fkeyvars = [v for v in query.variables if v not in query.freshvariables]
    fkey_local = tuple(query.variables.index(v) for v in fkeyvars)
    fkey_foreign = tuple(cols.index(v) for v in fkeyvars)

    index = {}

    for row, obj in zip(rows, objs):
        key = tuple(row[i] for i in fkey_foreign)
        index[key] = row, obj, []

    newcols = cols + query.freshvariables
    newrows = []
    newobjs = []

    for row in database[query.table]:
        key = tuple(row[i] for i in fkey_local)
        frow, fobj, flist = index[key]
        newrow = frow + tuple(row[i] for i in freshidxs)
        flist.append(newrow)
        newrows.append(newrow)
        newobjs.append(fobj)

    return newcols, newrows, newobjs, index.values()


def value2objects(cols, rows, objs, spec, database):
    if spec.query is not None:
        newcols, newrows, newobjs, _ = find_child_rows(cols, rows, objs, spec.query, database)
    else:
        newcols, newrows, newobjs = cols, rows, objs

    idx = newcols.index(spec.variable)
    return [(newobj, newrow[idx]) for newobj, newrow in zip(newobjs, newrows)]


def struct2objects(cols, rows, objs, spec, database):
    structs = [{} for _ in objs]
    ids = range(len(objs))

    for i in ids:
        structs[i] = {}

    for key in spec.childs:
        pairs = any2objects(cols, rows, ids, spec.childs[key], database)
        for i, val in pairs:
            structs[i][key] = val

    return list(zip(objs, structs))


def option2objects(cols, rows, objs, spec, database):
    values = [None] * len(objs)
    ids = range(len(objs))

    newcols, newrows, newids, _ = find_child_rows(cols, rows, ids, spec.query, database)

    pairs = any2objects(newcols, newrows, newids, spec.childs['_val_'], database)
    for i, val in pairs:
        values[i] = val

    return list(zip(objs, values))


def set2objects(cols, rows, objs, spec, database):
    sets = [set() for _ in objs]

    newcols, newrows, newobjs, _ = find_child_rows(cols, rows, sets, spec.query, database)

    pairs = any2objects(newcols, newrows, newobjs, spec.childs['_val_'], database)

    for set_, value in pairs:
        set_.add(value)

    return list(zip(objs, sets))


def list2objects(cols, rows, objs, spec, database):
    lsts = [[] for _ in objs]

    newcols, newrows, newobjs, _ = find_child_rows(cols, rows, lsts, spec.query, database)

    idxpairs = any2objects(newcols, newrows, newobjs, spec.childs['_idx_'], database)
    valpairs = any2objects(newcols, newrows, newobjs, spec.childs['_val_'], database)
    assert len(idxpairs) == len(valpairs)
    for (lst1, idx), (lst2, val) in zip(idxpairs, valpairs):
        assert lst1 is lst2
        lst1.append((idx, val))

    return [(obj, [val for idx, val in sorted(lst)]) for (obj, lst) in zip(objs, lsts)]


def dict2objects(cols, rows, objs, spec, database):
    dcts = [{} for _ in objs]

    newcols, newrows, newobjs, _ = find_child_rows(cols, rows, dcts, spec.query, database)

    keypairs = any2objects(newcols, newrows, newobjs, spec.childs['_key_'], database)
    valpairs = any2objects(newcols, newrows, newobjs, spec.childs['_val_'], database)
    assert len(keypairs) == len(valpairs)
    for (dct1, key), (dct2, val) in zip(keypairs, valpairs):
        assert dct1 is dct2
        dct1[key] = val

    return list(zip(objs, dcts))


def any2objects(cols, rows, objs, spec, database):
    assert len(rows) == len(objs)

    typ = type(spec)

    if typ == Value:
        return value2objects(cols, rows, objs, spec, database)

    elif typ == Struct:
        return struct2objects(cols, rows, objs, spec, database)

    elif typ == Option:
        return option2objects(cols, rows, objs, spec, database)

    elif typ == Set:
        return set2objects(cols, rows, objs, spec, database)

    elif typ == List:
        return list2objects(cols, rows, objs, spec, database)

    elif typ == Dict:
        return dict2objects(cols, rows, objs, spec, database)

    else:
        raise TypeError()  # or missing case?


def rows2objects(schema, spec, database):
    if not any(isinstance(spec, t) for t in [Value, Struct, Option, Set, List, Dict]):
        raise TypeError()
    if not isinstance(database, dict):
        raise TypeError()

    [(topobj, subobj)] = any2objects((), [()], [None], spec, database)
    assert topobj is None

    return subobj
