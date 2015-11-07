import traceback


def format_exception(exception):
    """Format an exception as diagnostics output.

    exception is the tuple as expected from sys.exc_info.
    """
    exception_lines = traceback.format_exception(*exception)
    # The lines returned from format_exception do not strictly contain
    # one line per element in the list (i.e. some elements have new
    # line characters in the middle). Normalize that oddity.
    lines = ''.join(exception_lines).splitlines(True)
    return format_as_diagnostics(lines)


def format_as_diagnostics(lines):
    """Format the lines as diagnostics output by prepending the diagnostic #.

    This function makes no assumptions about the line endings.
    """
    return ''.join(['# ' + line for line in lines])
