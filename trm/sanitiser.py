import re

whitespaces = re.compile(r'^(?P<indent> +|\t+)(.*)')


def sanitise(lines, tab_spaces=4):
    min_indent = None
    for i, line in enumerate(lines):
        match = whitespaces.match(line)
        if match is None:
            min_indent = None
            yield line
            continue
        indent = match.group('indent')
        if '\t' in indent:
            sanitised = indent.replace('\t', ' ' * tab_spaces)
        else:
            sanitised = indent

        if min_indent is None:
            min_indent = sanitised

        if len(sanitised) < len(min_indent):
            raise IndentationError('Wrong indentation at line %s' % (i + 1))

        sanitised = sanitised.replace(min_indent, '.' * len(min_indent), 1)
        yield line.replace(indent, sanitised)
