import html.parser as hp

class Parser(hp.HTMLParser):
    def __init__(self, root):
        self.root = root
        hp.HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        self.root.add_child(tag, **dict(attrs))

    def handle_endtag(self, tag):
        self.root.close_tag()

    def handle_data(self, content):
        self.root.add_child("text", data=content)

    def handle_comment(self, data):
        self.root.add_child("comment", data=data)

    def handle_decl(self, decl):
        self.root.add_child("doc", data=decl)
