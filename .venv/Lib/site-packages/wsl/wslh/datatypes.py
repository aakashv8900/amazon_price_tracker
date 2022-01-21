class Value:
    def __init__(self, variable, query, primtype):
        assert variable is not None
        assert query is None
        assert isinstance(variable, str)
        self.variable = variable
        self.query = query
        self.primtype = primtype

    def __repr__(self):
        return 'Value %s (type %s)' %(self.variable, self.primtype)


class Struct:
    def __init__(self, childs, query):
        assert childs is not None
        assert query is None
        assert isinstance(childs, dict)
        self.childs = childs
        self.query = query

    def __repr__(self):
        return 'Struct %s' %(self.childs,)


class Option:
    def __init__(self, childs, query):
        assert childs is not None
        assert query is not None
        assert isinstance(childs, dict)
        self.childs = childs
        self.query = query

    def __repr__(self):
        return 'Option for %s %s' %(self.query, self.childs)


class Set:
    def __init__(self, childs, query):
        assert query is not None
        self.childs = childs
        self.query = query

    def __repr__(self):
        if self.query is not None:
            return 'for %s %s' %(self.query, self.childs['_val_'])
        else:
            return 'Set %s' %(self.childs['_val_'],)


class List:
    def __init__(self, childs, query):
        assert query is not None
        self.childs = childs
        self.query = query

    def __repr__(self):
        if self.query is not None:
            return 'for %s %s' %(self.query, self.childs['_val_'])
        else:
            return 'List %s' %(self.childs['_val_'],)


class Dict:
    def __init__(self, childs, query):
        assert query is not None
        self.childs = childs
        self.query = query

    def __repr__(self):
        if self.query is not None:
            return 'for %s (%s => %s)' %(self.query, self.childs['_key_'], self.childs['_val_'])
        else:
            return 'Value %s' %(self.childs['_val_'],)


class Reference:
    def __init__(self, name, index=None, child=None):
        """
        Args:
            name (str): A member name (relative to the root of the namespace or
                the preceding element)
            index (str): If *name* references a dict, *index* is the name of an
                in-scope variable that is used as an index into the dict.
                It must be *None* if *name* doesn't reference a dict.
                Otherwise it must be given if *child* is given, and is optional
                otherwise.
            child (Reference): If given, where the reference leads from here.
        """
        if name is not None and not isinstance(name, str):
            raise ValueError('"name" must be None or a str')
        if index is not None and not isinstance(index, str):
            raise ValueError('"index" must be None or a str')
        if child is not None and not isinstance(child, Reference):
            raise ValueError('"child" must be None or another Reference')

        self.name = name
        self.child = child
        self.index = index

    def __repr__(self):
        out = self.name
        if self.index is not None:
            out += "["
            out += self.index
            out += "]"
        if self.child is not None:
            out += "."
            out += str(self.child)
        return out


def _issorted(xs):
    assert isinstance(xs, list)
    return xs == sorted(xs)


class Query:
    def __init__(self, freshvariables, table, variables):
        assert isinstance(freshvariables, tuple)
        assert isinstance(table, str)
        assert isinstance(variables, tuple)
        assert all(v in variables for v in freshvariables)
        assert _issorted([variables.index(v) for v in freshvariables])
        self.freshvariables = freshvariables
        self.table = table
        self.variables = variables

    def __repr__(self):
        return '(%s) (%s %s)' %(', '.join(self.freshvariables), self.table, ', '.join(self.variables))
