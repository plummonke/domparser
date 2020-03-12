import io
import os
import os.path
import sys

import htmlelem
import myparser

def fully_qual(root):
    def func(file):
        return os.path.join(root, file)
    return func

def filter_html(file):
    return "html" in file

def main():
    if len(sys.argv) < 3:
        print("Missing arguments. This program needs:\n"
                "\tA directory housing the original files; and\n"
                "\ta template for the new files."
                )
        exit()

    root = sys.argv[len(sys.argv) - 2]
    local_files = map(fully_qual(root), os.listdir(root))
    try:
        os.mkdir(os.path.join(root, "pages"))
    except FileExistsError:
        pass

    dirs = filter(os.path.isdir, map(fully_qual(root), os.listdir(root)))
    files = filter(os.path.isfile, filter(filter_html, local_files))

    # Parse template file into a root.
    hp = myparser.Parser(htmlelem.Element("", -1))
    hp.feed(io.open(sys.argv[len(sys.argv) - 1]).read())
    template_root = hp.root

    # Create new root and connect to HTML myparser.
    HTML_root = htmlelem.Element("", -1)
    hp.root = HTML_root

    for file in files:
        with io.open(file, mode="r", encoding="utf-8", errors="ignore") as f:
            hp.feed(f.read())
        
        HTML_root = hp.root

        try:
            template_root.adopt_child_into(HTML_root.search_attributes("id", "content")[0], "main")
        except IndexError:
            pass

        hp.reset()
        HTML_root.clear_children()

        with io.open(file, mode="w", newline="", encoding="utf-8", errors="ignore") as f:
            f.write(template_root.convert_to_string())

        template_root.search_tag("main")[0].clear_children()

    for dir in dirs:
        local_files = map(fully_qual(dir), os.listdir(dir))
        files = filter(os.path.isfile, filter(filter_html, local_files))

        local_dir = os.path.split(dir)[1]

        for file in files:
            with io.open(file, mode="r", encoding="utf-8", errors="ignore") as f:
                hp.feed(f.read())

            HTML_root = hp.root
            article = htmlelem.Element("article", 0)

            ids = ("ab", "bb", "bsi", "cankers", "csi", "fd", "fid", "iwp", "mistletoes", "nid", "rd", "sap", "scrp", "sds", "wb")
            for id in ids:
                try:
                    article.adopt_child(HTML_root.search_attributes("id", id + "-pg")[0]) 
                except IndexError:
                    continue
                
            try:
                article.adopt_child(HTML_root.search_attributes("id", "content")[0])
            except IndexError:
                pass

            template_root.adopt_child_into(article, "main")
            hp.reset()
            HTML_root.clear_children()
            
        output = os.path.join(root, "pages", local_dir + "_index.shtml")
        with io.open(output, mode="w+", newline="", encoding="utf-8", errors="ignore") as f:
            f.write(template_root.convert_to_string())

        template_root.search_tag("main")[0].clear_children()

main()
