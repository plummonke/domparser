class Element:
    def __init__(self, tag, count, data="", **attributes):
        self.tag = tag
        self.attrs = attributes
        self.children = []
        self.ancestor_count = count
        self.data = data
        self.set_close_type(tag)

    def set_close_type(self, tag):
        bool = self.tag in ("meta", "link", "br", "img", "text", "comment", "doc")
        self.auto_close = bool
        self.closed = bool

    def __repr__(self):
        return self.convert_to_string()

    def __str__(self):
        return self.convert_to_string()

    def convert_to_string(self):
        indent = "\t" * self.ancestor_count
        return self._select_output_template().format(
                indent=indent,
                content=self._stringify_children(),
                attrs=self._stringify_attributes(),
                tag=self.tag,
                data=self.data
            )

    def _select_output_template(self):
        if self.tag == "text":
            return "{indent}{data}"
        elif self.tag == "comment":
            return "{indent}<!-- {data} -->"
        elif self.tag == "doc":
            return "<!{data}>"
        elif self.auto_close:
            return "{indent}<{tag} {attrs}>"
        elif self.tag == "":
            return "{content}"
        else:
            return "{indent}<{tag} {attrs}>{content}{indent}</{tag}>"

    def _stringify_children(self):
        if len(self.children) > 0:
            return "".join([child.convert_to_string() for child in self.children])
        return ""

    def _stringify_attributes(self):
        if len(self.attrs) > 0:
            return " ".join([f"{key}='{self.attrs[key]}'" for key in self.attrs.keys()])
        return ""

    def close_tag(self):
        for child in self.children[::-1]:
            if not child.is_closed():
                child.close_tag()
                return

        self.closed = True

    def add_child(self, tag, data="", **attributes):
        for child in self.children[::-1]:
            if not child.is_closed():
                child.add_child(tag, data=data, **attributes)
                return

        self.children.append(Element(tag, self.ancestor_count + 1, data, **attributes))

    def is_closed(self):
        return self.closed

    def remove_child(self, index):
        return self.children.pop(index)

    def clear_children_from(self, tag):
        target = self.search_tag(tag)

        try:
            target[0].clear_children()
        except IndexError:
            pass

    def clear_children(self):
        self.children.clear()

    def search_attributes(self, attr, value):
        return self._search_attributes(attr, value, [])

    def _search_attributes(self, attr, value, results):
        if value in self.attrs.get(attr, ""):
            results.append(self)

        for child in self.children:
            results = child._search_attributes(attr, value, results)

        return results

    def search_tag(self, tag):
        return self._search_tag(tag, [])

    def _search_tag(self, tag, results):
        if self.tag == tag:
            results.append(self)

        for child in self.children:
            results = child._search_tag(tag, results)

        return results

    def change_tag(self, new_tag):
        self.tag = new_tag
        self.set_close_type(tag)

    def clear_attributes(self):
        self.attrs.clear()

    def adopt_child_into(self, child, tag):
        target = self.search_tag(tag)

        try:
            target[0].adopt_child(child)
        except IndexError:
            pass

    def adopt_child(self, child):
        child.change_ancestry(self.ancestor_count + 1)
        self.children.append(child)

    def change_ancestry(self, num):
        self.ancestor_count = num

if __name__ == "__main__":
    root = Element("html", 0)
    root.add_child("meta")
    x = root.search_tag("meta")
    x[0].add_child("link")
    print(root.search_tag("link"))
    root.add_child("doc", data="DOCTYPE html")
    print(root)
