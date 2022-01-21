def compute_line_and_column(text, i):
    lines = text[:i].split('\n')
    lineno = len(lines)
    charno = i + 1 - sum(len(l) + 1 for l in lines[:-1])
    return lineno, charno


class WslValueError(ValueError):
    """Base class for all WSL exceptions"""


class ParseError(WslValueError):
    """Raised on general parsing errors"""

    def __init__(self, context, text, startpos, errorpos, errormsg):

        assert isinstance(context, str)
        assert isinstance(text, str)
        assert isinstance(startpos, int)
        assert isinstance(errorpos, int)
        assert isinstance(errormsg, str)

        startline, startcolumn = compute_line_and_column(text, startpos)
        errorline, errorcolumn = compute_line_and_column(text, errorpos)
        message = 'While parsing %s (starting at line %d char %d): At line %d char %d: %s' %(context, startline, startcolumn, errorline, errorcolumn, errormsg)

        super().__init__(message)

        self.context = context
        self.text = text
        self.startpos = startpos
        self.errorpos = errorpos
        self.errormsg = errormsg


class LexError(WslValueError):
    """LexError represents WSL text format token lexing errors

    Attributes:
        lexicaltype (str): Name of the lexical type of the value that could not be lexed.
        text (str): The *str* buffer from which the value could not be lexed.
        startpos (int): Position in *text* from which the lexing of the value started.
        errorpos (int): Position in *text* where the lexing error occurred.
        errormsg (str): Description of the lexing error.
    """

    def __init__(self, lexicaltype, text, startpos, errorpos, errormsg):

        assert isinstance(lexicaltype, str)
        assert isinstance(text, str)
        assert isinstance(startpos, int)
        assert isinstance(errorpos, int)
        assert isinstance(errormsg, str)

        startline, startcolumn = compute_line_and_column(text, startpos)
        errorline, errorcolumn = compute_line_and_column(text, errorpos)

        message = 'While lexing %s (starting at line %d char %d): At line %d char %d: %s' %(lexicaltype, startline, startcolumn, errorline, errorcolumn, errormsg)

        super().__init__(message + '\nThe whole input: \n' + text + '\n')

        self.lexicaltype = lexicaltype
        self.text = text
        self.startpos = startpos
        self.errorpos = errorpos
        self.errormsg = errormsg


class FormatError(WslValueError):
    """Raised on database formatting errors"""

    def __init__(self, context, value, errormsg):

        assert isinstance(context, str)
        assert isinstance(errormsg, str)

        super().__init__()

        self.context = context
        self.value = value
        self.errormsg = errormsg


class UnlexError(WslValueError):
    """UnlexError represents errors that occurred while unlexing tokens to WSL text format"""

    def __init__(self, lexicaltype, token, errormsg):

        assert isinstance(lexicaltype, str)
        assert isinstance(token, str)
        assert isinstance(errormsg, str)

        super().__init__()

        self.lexicaltype = lexicaltype
        self.token = token
        self.errormsg = errormsg


class IntegrityError(WslValueError):
    """Raised on database inconsistencies"""


class UniqueConstraintViolation(IntegrityError):

    def __init__(self, key, row):

        assert isinstance(key, str)
        assert isinstance(row, tuple)

        self.key = key
        self.row = row


class ForeignKeyConstraintViolation(IntegrityError):

    def __init__(self, foreignkey, row):

        assert isinstance(foreignkey, str)
        assert isinstance(row, tuple)

        self.foreignkey = foreignkey
        self.row = row
