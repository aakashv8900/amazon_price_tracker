import io

from ..lexjson import make_make_jsonwriter, unlex_json_string
from .datatypes import Value, Struct, Option, Set, List, Dict


INDENTSPACES = '  '


def value2json(look, spec, indent, is_dict_child):
    fmter = look(spec.primtype, is_dict_child)
    if fmter is None:
        raise wsl.InvalidArgument('No primvalue formatter for type "%s"' %(spec,))
    def write_value(writer, data):
        writer.write(fmter(data))
    return write_value


def struct2json(look, spec, indent):
    items = []
    for key, sub_spec in sorted(spec.childs.items()):
        write_sub = any2json(look, sub_spec, indent + INDENTSPACES)
        items.append((key, write_sub))
    def write_struct(writer, data):
        writer.write('{')
        writer.write(indent)
        for i, (key, write_sub) in enumerate(items):
            if i:
                writer.write(',')
            writer.write('\n')
            writer.write(indent + INDENTSPACES)
            writer.write(unlex_json_string(key))
            writer.write(': ')
            write_sub(writer, data[key])
        writer.write('\n')
        writer.write(indent)
        writer.write('}')
    return write_struct


def option2json(look, spec, indent):
    sub_spec = spec.childs['_val_']
    write_sub = any2json(look, sub_spec, indent)
    def write_option(writer, data):
        if data is None:
            writer.write('null')
        else:
            write_sub(writer, data)
    return write_option


def set2json(look, spec, indent):
    sub_spec = spec.childs['_val_']
    write_sub = any2json(look, sub_spec, indent + INDENTSPACES)
    def write_set(writer, data):
        writer.write('[\n')
        i = None
        for i, item in enumerate(sorted(data)):
            if i:
                writer.write(',\n')
            writer.write(indent)
            writer.write(indent + INDENTSPACES)
            write_sub(writer, item)
        if i is not None:
            writer.write('\n')
        writer.write(indent)
        writer.write(']')
    return write_set


def list2json(look, spec, indent):
    sub_spec = spec.childs['_val_']
    write_sub = any2json(look, sub_spec, indent + INDENTSPACES)
    def write_list(writer, data):
        writer.write('[\n')
        i = None
        for i, item in enumerate(data):
            if i:
                writer.write(',\n')
            writer.write(indent + INDENTSPACES)
            write_sub(writer, item)
        if i is not None:
            writer.write('\n')
        writer.write(indent)
        writer.write(']')
    return write_list


def dict2json(look, spec, indent):
    key_spec = spec.childs['_key_']
    val_spec = spec.childs['_val_']
    assert type(key_spec) == Value
    write_key = any2json(look, key_spec, indent + INDENTSPACES, is_dict_child=True)
    write_val = any2json(look, val_spec, indent + INDENTSPACES)
    def write_dict(writer, data):
        writer.write('{')
        for i, (key, val) in enumerate(sorted(data.items())):
            if i:
                writer.write(',')
            writer.write('\n')
            writer.write(indent + INDENTSPACES)
            write_key(writer, key)
            writer.write(': ')
            write_val(writer, val)
        writer.write('\n')
        writer.write(indent)
        writer.write('}')
    return write_dict


def any2json(look, spec, indent, is_dict_child=False):
    typ = type(spec)

    if typ == Value:
        return value2json(look, spec, indent, is_dict_child)

    elif typ == Struct:
        return struct2json(look, spec, indent)

    elif typ == Option:
        return option2json(look, spec, indent)

    elif typ == Set:
        return set2json(look, spec, indent)

    elif typ == List:
        return list2json(look, spec, indent)

    elif typ == Dict:
        return dict2json(look, spec, indent)

    else:
        raise ParseError()  # or missing case?


def objects2json(schema, spec, data):
    write = any2json(make_make_jsonwriter(schema), spec, '', False)
    writer = io.StringIO()
    write(writer, data)
    return writer.getvalue()
