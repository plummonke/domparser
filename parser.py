import html.parser as hp
import io

class Parser(hp.HTMLParser):
    def __init__(self, root):
        self.root = root
        hp.HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        self.root.add_child(tag, **dict(attrs))

    def handle_endtag(self, tag):
        self.root.close()

    def handle_data(self, content):
        self.root.add_child("text", data=content)

