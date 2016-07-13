import re


class LeafElement(object):
    name = 'raw'
    pattern = re.compile(r'^(?P<content>.*)')
    weight = 9999

    def __init__(self, groups):
        self.groups = groups
        self.parent = None
        self.children = []

    def set_parent(self, parent):
        self.parent = parent
        self.parent.add_child(self)

    @classmethod
    def match(cls, content):
        match = cls.pattern.match(content)
        if match is None:
            return None

        groups = match.groupdict()
        return cls(groups)

    def add_child(self, child):
        self.children.append(child)

    def push(self, leaf):
        if leaf.weight > self.weight:
            leaf.set_parent(self)
            return leaf
        elif leaf.weight == self.weight:
            leaf.set_parent(self.parent)
            return leaf
        else:
            return self.parent.push(leaf)

    def __repr__(self):
        string = '<%s weight=%s groups=%s>\n' % (
            self.__class__.__name__, self.weight, self.groups)

        for child in self.children:
            tabs = '.' * self.parents_count
            string += '%s %s' % (tabs, str(child))
        return string

    @property
    def parents_count(self):
        count = 0
        current_parent = self.parent
        while current_parent is not None:
            count += 1
            current_parent = current_parent.parent
        return count


class RootElement(LeafElement):
    name = 'root'
    pattern = None
    weight = 0

    def __init__(self):
        super().__init__({})


class TitleElement(LeafElement):
    name = 'title'
    pattern = re.compile(r'^(?P<level>\#+) (?P<title>.*)')

    @property
    def weight(self):
        return len(self.groups['level'])


class ItemElement(LeafElement):
    name = 'item'
    pattern = re.compile(r'^([*-]|\d\.) (\`(?P<label>.*)\` )?(?P<item>.*)')
    weight = 10


class CheckboxElement(LeafElement):
    name = 'checkbox'
    pattern = re.compile(r'^((\.+)( *))\[(?P<checked>\s|x)\]( *)(?P<checkbox>.*)')
    weight = 20


class ContentElement(LeafElement):
    name = 'content'
    pattern = re.compile(r'^(\.+)(?P<line>.*)')
    weight = 20


class MarkdownParser(object):
    whitespaces = re.compile(r'^(?P<indent> +|\t+)(.*)')

    element_classes = [
        TitleElement,
        ItemElement,
        CheckboxElement,
        ContentElement,
    ]

    def __init__(self, lines, tab_spaces=4):
        self.lines = lines
        self.tree = RootElement()
        self.tab_spaces = tab_spaces

    def get_sanitised_lines(self):
        min_indent = None
        for i, line in enumerate(self.lines):
            match = self.whitespaces.match(line)
            if match is None:
                min_indent = None
                yield line
                continue
            indent = match.group('indent')
            if '\t' in indent:
                sanitised = indent.replace('\t', ' ' * self.tab_spaces)
            else:
                sanitised = indent

            if min_indent is None:
                min_indent = sanitised

            if len(sanitised) < len(min_indent):
                raise IndentationError('Wrong indentation at line %s' % (i + 1))

            sanitised = sanitised.replace(min_indent, '.' * len(min_indent), 1)
            yield line.replace(indent, sanitised)

    def parse(self):
        leaf = self.tree
        for line in self.get_sanitised_lines():
            for element_cls in self.element_classes:
                element = element_cls.match(line)
                if element is None:
                    continue
                leaf = leaf.push(element)
                break
        return self.tree
