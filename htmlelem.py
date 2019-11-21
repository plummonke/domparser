class Element:
    def __init__(self, tag, count, data="", **attributes):
        self.tag = tag
        self.attrs = attributes
        self.children = []
        self.ancestor_count = count
        self.data = data

        if self.tag in ("meta", "link", "br", "img", "text"):
            self.closed = True
            self.auto_close = True
        else:
            self.closed = False
            self.auto_close = False

    def convert_to_string(self):
        indent = "\n" + "\t" * self.ancestor_count
        content = self._stringify_children()
        attrs = self._stringify_attributes()
        if self.tag == "text":
            return f"{indent}{self.data}"
        elif self.auto_close:
            return f"{indent}<{self.tag} {attrs}>"
        elif self.tag == "":
            return f"{content}"
        else:
            return f"{indent}<{self.tag} {attrs}>{content}{indent}</{self.tag}>"

    def _stringify_children(self):
        if len(self.children) > 0:
            return "".join([child.convert_to_string() for child in self.children])
        return ""

    def _stringify_attributes(self):
        if len(self.attrs) > 0:
            return " ".join([f"{key}='{self.attrs[key]}'" for key in self.attrs.keys()])
        return ""

    def add_child(self, tag, data="", **attributes):
        for child in self.children[::-1]:
            if not child.is_closed():
                child.add_child(tag, data=data, **attributes)
                return

        self.children.append(Element(tag, self.ancestor_count + 1, data, **attributes))

    def remove_child(self, index):
        self.children.pop(index)

    def close(self):
        for child in self.children[::-1]:
            if not child.is_closed():
                child.close()
                return
        self.closed = True

    def is_closed(self):
        return self.closed
