"""Module wsl.domain: Built-in WSL domain parsers.

Users can add their own domains by providing a parser following the example of
the built-in ones.
"""

from .exceptions import LexError
from .exceptions import UnlexError
from .exceptions import ParseError
from .exceptions import FormatError
from .lexwsl import lex_wsl_space
from .lexwsl import lex_wsl_newline
from .lexwsl import lex_wsl_identifier
from .lexwsl import lex_wsl_relation_name
from .lexwsl import lex_wsl_string_without_escapes
from .lexwsl import lex_wsl_string_with_escapes
from .lexwsl import lex_wsl_int
from .lexwsl import unlex_wsl_identifier
from .lexwsl import unlex_wsl_string_without_escapes
from .lexwsl import unlex_wsl_string_with_escapes
from .lexwsl import unlex_wsl_int
from .lexjson import lex_json_int
from .lexjson import lex_json_string
from .lexjson import unlex_json_int
from .lexjson import unlex_json_string


def split_opts(line):
    opts = []
    for word in line.split():
        if '=' in word:
            key, val = word.split('=', 1)
        else:
            key, val = word, None
        opts.append((key, val, word))
    return opts


def parse_ID_domain(line):
    """Parser for ID domain declarations.

    No special syntax is recognized. Only the bare "ID" is allowed.
    """
    if line:
        raise ParseError('Construction of ID domain does not receive any arguments')
    class IDDomain:
        decode = ID_decode
        encode = ID_encode
        wsllex = lex_wsl_identifier
        wslunlex = unlex_wsl_identifier
        jsonlex = lex_json_string
        jsonunlex = unlex_json_string
    return IDDomain


def parse_String_domain(line):
    opts = split_opts(line)
    escape = False
    for key, val, orig in opts:
        if key == 'escape' and val is None:
            escape = True
        else:
            raise ParseError('Did not understand String parameterization: %s' %(orig,))
    if escape:
        class StringDomain:
            decode = String_decode
            encode = String_encode
            wsllex = lex_wsl_string_with_escapes
            wslunlex = unlex_wsl_string_with_escapes
            jsonlex = lex_json_string
            jsonunlex = unlex_json_string
    else:
        class StringDomain:
            decode = String_decode
            encode = String_encode
            wsllex = lex_wsl_string_without_escapes
            wslunlex = unlex_wsl_string_without_escapes
            jsonlex = lex_json_string
            jsonunlex = unlex_json_string
    return StringDomain


def parse_Int_domain(line):
    if line:
        raise ParseError('Construction of Integer domain does not receive any arguments')
    class IntDomain:
        decode = Int_decode
        encode = Int_encode
        wsllex = lex_wsl_int
        wslunlex = unlex_wsl_int
        jsonlex = lex_json_int
        jsonunlex = unlex_json_int
    return IntDomain


class EnumBase:
    """An enumeration type. Essentially a list of possible identifiers"""
    def __init__(self, strings):
        self.strings = list(strings)


class EnumValue:
    """An option representing a particular choice of value for a given Enum"""
    def __init__(self, base, string):
        self.base = base
        self.string = string
        self.integer = base.strings.index(string)

    def __repr__(self):
        return self.string

    def __str__(self):
        return self.string

    def __hash__(self):
        return self.integer

    def _compare(comp):
        def compare(self, other):
            if not isinstance(other, EnumValue):
                raise TypeError('Cannot compare Enum to %s value' %(type(other),))
            if self.base is not other.base:
                raise TypeError('Cannot compare EnumValues %s and %s: not of the same enumeration base type (%s and %s)' %(self, other, self.base, other.base))
            return comp(self.integer, other.integer)
        return compare

    __eq__ = _compare(lambda i, j: i == j)
    __ne__ = _compare(lambda i, j: i != j)
    __le__ = _compare(lambda i, j: i <= j)
    __ge__ = _compare(lambda i, j: i >= j)
    __lt__ = _compare(lambda i, j: i < j)
    __gt__ = _compare(lambda i, j: i > j)


def parse_Enum_domain(line):
    strings = line.split()
    base = EnumBase(strings)
    values = []
    for s in strings:
        values.append(EnumValue(base, s))
    class EnumDomain:
        decode = make_Enum_decode(values)
        encode = make_Enum_encode(values)
        wsllex = lex_wsl_identifier
        wslunlex = unlex_wsl_identifier
        jsonlex = lex_json_string
        jsonunlex = unlex_json_string
    return EnumDomain


def parse_IPv4_domain(line):
    if line.strip():
        raise ParseError('IPv4 domain doesn\'t take any arguments')
    class IPv4:
        decode = IPv4_decode
        encode = IPv4_encode
        wsllex = lex_wsl_identifier
        wslunlex = unlex_wsl_identifier
        jsonlex = lex_json_string
        jsonunlex = unlex_json_string
    return IPv4


def ID_decode(token):
    return token


def ID_encode(value):
    return value


def String_decode(token):
    return token


def String_encode(value):
    return value


def Int_decode(token):
    try:
        return int(token)
    except ValueError as e:
        raise ParseError('Failed to parse integer') from e


def Int_encode(value):
    return str(value)


def make_Enum_decode(values):
    def Enum_decode(token):
        for enumValue in values:
            if enumValue.string == token:
                return enumValue
    return Enum_decode


def make_Enum_encode(values):
    def Enum_encode(value):
        if not isinstance(value, EnumValue):
            raise ValueError('Not a valid enum value: %s' %(value,))
        return value.string
    return Enum_encode


class IPv4Domain(tuple):
    def __new__(cls, ip):
        if not isinstance(ip, tuple) or len(ip) != 4 or any((not isinstance(x, int) or not 0 <= x < 256)  for x in ip):
            raise ValueError('IPv4 must be 4-tuple of 8-bit integers (0-255), got: %s' %(ip,))
        return super().__new__(cls, ip)

    def __str__(self):
        return '%s.%s.%s.%s' % self


def IPv4_decode(token):
    ws = token.split('.')
    if len(ws) == 4:
        try:
            ip = tuple(map(int, ws))
            return IPv4Domain(ip)
        except ValueError as e:
            # XXX: ParseError is not right here
            raise ParseError('IPv4 address', '', 0, 0, 'Failed to decode "%s" as IPv4 address' %(token,)) from e


def IPv4_encode(ip):
    try:
        a,b,c,d = ip
        for x in [a,b,c,d]:
            if not isinstance(x, int) or not 0 <= x < 256:
                raise ValueError()
        return '%d.%d.%d.%d' %ip
    except ValueError as e:
        raise FormatError('Not a valid ip address (need 4-tuple of integers in [0,255])')


_builtin_domain_parsers = {
    'ID': parse_ID_domain,
    'String': parse_String_domain,
    'Enum': parse_Enum_domain,
    'Int': parse_Int_domain,
    'IPv4': parse_IPv4_domain,
}


def get_builtin_domain_parsers():
    """Get a dict containing all domain parsers built-in to this library.

    The dict is freshly created, so can be modified by the caller.

    Returns:
        dict: A dictionary mapping the names of all built-in parsers to the parsers.
    """
    return dict(_builtin_domain_parsers)


if __name__ == '__main__':
    parse_ID_domain('')
    parse_String_domain('')
    parse_String_domain('escape')
    parse_IPv4_domain('')
