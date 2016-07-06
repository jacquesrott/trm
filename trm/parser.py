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

    element_classes = [
        TitleElement,
        ItemElement,
        CheckboxElement,
        ContentElement,
    ]

    def __init__(self, lines):
        self.lines = lines
        self.tree = RootElement()

    def parse(self):
        leaf = self.tree
        for line in self.lines:
            for element_cls in self.element_classes:
                element = element_cls.match(line)
                if element is None:
                    continue
                leaf = leaf.push(element)
                break
        return self.tree
