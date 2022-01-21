import io

import wsl
from .datatypes import Value, Struct, Option, Set, List, Dict


INDENTSPACES = '    '


def add_whitespace(spec, sub_spec, write):
    if type(sub_spec) == Value:
        if type(spec) in [Struct, Option, Dict]:
            def spnl(writer, data):
                writer.write(' ')
                write(writer, data)
                writer.write('\n')
            return spnl
        else:
            def nl_after(writer, data):
                write(writer, data)
                writer.write('\n')
            return nl_after
    elif type(sub_spec) == Option:
        def sp(writer, data):
            writer.write(' ')
            write(writer, data)
        return sp
    else:
        def nl(writer, data):
            writer.write('\n')
            write(writer, data)
        return nl


def value2text(look, spec, indent):
    fmter = look(spec.primtype)
    if fmter is None:
        raise wsl.InvalidArgument('No primvalue formatter for type "%s"' %(spec,))
    def write_value(writer, data):
        writer.write(fmter(data))
    return write_value


def struct2text(look, spec, indent):
    items = []
    for key, sub_spec in sorted(spec.childs.items()):
        write_sub = any2text(look, sub_spec, indent + INDENTSPACES)
        items.append((key, add_whitespace(spec, sub_spec, write_sub)))
    def write_struct(writer, data):
        for key, write_sub in items:
            writer.write(indent)
            writer.write(':')
            writer.write(key)
            write_sub(writer, data[key])
    return write_struct


def option2text(look, spec, indent):
    sub_spec = spec.childs['_val_']
    write_sub = any2text(look, sub_spec, indent)
    write_sub = add_whitespace(spec, sub_spec, write_sub)
    def write_option(writer, data):
        if data is None:
            writer.write('?\n')
        else:
            writer.write('!')
            write_sub(writer, data)
    return write_option


def set2text(look, spec, indent):
    sub_spec = spec.childs['_val_']
    write_sub = any2text(look, sub_spec, indent + INDENTSPACES)
    write_sub = add_whitespace(spec, sub_spec, write_sub)
    def write_set(writer, data):
        for item in sorted(data):
            writer.write(indent)
            write_sub(writer, item)
    return write_set


def list2text(look, spec, indent):
    sub_spec = spec.childs['_val_']
    write_sub = any2text(look, sub_spec, indent + INDENTSPACES)
    write_sub = add_whitespace(spec, sub_spec, write_sub)
    def write_list(writer, data):
        for item in data:
            writer.write(indent)
            write_sub(writer, item)
    return write_list


def dict2text(look, spec, indent):
    key_spec = spec.childs['_key_']
    val_spec = spec.childs['_val_']
    assert type(key_spec) == Value
    write_key = any2text(look, key_spec, indent + INDENTSPACES)
    write_val = any2text(look, val_spec, indent + INDENTSPACES)
    write_val = add_whitespace(spec, val_spec, write_val)
    def write_dict(writer, data):
        for key, val in sorted(data.items()):
            writer.write(indent)
            write_key(writer, key)
            write_val(writer, val)
    return write_dict


def any2text(look, spec, indent):
    typ = type(spec)

    if typ == Value:
        return value2text(look, spec, indent)

    elif typ == Struct:
        return struct2text(look, spec, indent)

    elif typ == Option:
        return option2text(look, spec, indent)

    elif typ == Set:
        return set2text(look, spec, indent)

    elif typ == List:
        return list2text(look, spec, indent)

    elif typ == Dict:
        return dict2text(look, spec, indent)

    else:
        raise TypeError()  # or missing case?


def objects2text(schema, spec, data):
    write = any2text(wsl.make_make_wslwriter(schema), spec, '')
    writer = io.StringIO()
    write(writer, data)
    return writer.getvalue()
