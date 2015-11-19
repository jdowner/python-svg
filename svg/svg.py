import copy


class Attributes(dict):
    def __init__(self, *args, **kwargs):
        super(Attributes, self).__init__(*args, **kwargs)

    def __repr__(self):
        return " ".join('{}="{}"'.format(k, v) for k, v in self.items())


class Leaf(object):
    def __init__(self, name, **attrs):
        self.attrs = Attributes(attrs)
        self.name = name

    def open_repr(self):
        return '<{name} {attrs}>{{}}</{name}>'.format(
                name=self.name,
                attrs=self.attrs,
                )

    def closed_repr(self):
        return '<{name} {attrs} />'.format(name=self.name, attrs=self.attrs)

    @property
    def id(self):
        return self.attrs.get("id", None)


class Element(Leaf):
    def __init__(self, name, **attrs):
        super(Element, self).__init__(name, **attrs)
        self.children = list()

    def __repr__(self):
        if not self.children:
            return self.closed_repr()

        return self.open_repr().format("".join(repr(c) for c in self.children))


class Definitions(Element):
    def __init__(self):
        super(Definitions, self).__init__("defs")

    def __contains__(self, id):
        return any(c.id == id for c in self.children)


class Svg(Element):
    def __init__(self):
        super(Svg, self).__init__("svg")

        self.definitions = Definitions()
        self.children.insert(0, self.definitions)

        self.attrs["xmlns"] = "http://www.w3.org/2000/svg"
        self.attrs["xmlns:xlink"] = "http://www.w3.org/1999/xlink"

    def add_definition(self, id, element):
        if id in self.definitions:
            raise KeyError("A definition with that ID already exists")

        definition = copy.copy(element)
        definition.attrs["id"] = id

        self.definitions.children.append(definition)


class Group(Element):
    def __init__(self, **attrs):
        super(Group, self).__init__("g", **attrs)


class Use(Element):
    def __init__(self, name, **attrs):
        attrs["xlink:href"] = "#{}".format(name)
        super(Use, self).__init__("use", **attrs)


class Rect(Element):
    def __init__(self, x=0, y=0, height=0, width=0, **attrs):
        attrs = Attributes(attrs)
        attrs.update(dict(x=x, y=y, height=height, width=width))
        super(Rect, self).__init__("rect", **attrs)
