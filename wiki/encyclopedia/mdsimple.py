"""
A very basic markdown to HTML convertor, implementing a small number of features:
    - headings          (# = h1, ## = h2 and so on)
    - boldface text     (**text** becomes <strong>text</strong>)
    - unordered lists   ( * item 1 * item 2 * item 3)
    - links             ( [Python](/wiki/Python) becomes <a href="/wiki/Python">Python</a> )
    - paragraphs        ( <p>text</p> where text starts with CRLF and not a < character)
"""

import re

# The MarkdownPattern class defines a collection of attributes used to replace a particular markdown character sequence
# with the appropriate HTML tags. For complex markdown replacements, cascading MarkdownPatterns can be created to 
# achieve the desired result.
class MarkdownPattern:
    def __init__(self, name, pattern, replace) : 
        self.name = name            # a unique identifier for a specific MarkdownPattern instance, required.
        self.pattern = pattern      # a regex pattern with a named capture group 'keep', required.
        self.replace = replace      # a parameterised string used to create replacement text.

# a list of MarkdownPattern names, used to determine processing order
process_order = [
    "strong",                                           # bold text
    "a1", "a2",                                         # links with title and typical flavours
    "h6",    "h5",    "h4",    "h3",    "h2",    "h1",  # headings, note reverse order!
    "ul_a",    "li",    "ul_b",    "ul_c",              # unordered lists, using a cascading approach
    "p"                                                 # paragraphs
]

# A dictionary of MarkdownPattern instances. In each pattern, named capture groups add clarity but are not required.
# The capture groups are used to replace parameters in the replacement text. Parameters are identified as &1, &2 and
# so, with the integers corresponding to the capture groups from the regex pattern.
patterns = {
    "strong": MarkdownPattern("strong", re.compile(r"\*{2}(?P<strongtext>\S.*?)\*{2}"), "<strong>&1</strong>"),

    # links come in several flavours
    "a1":    MarkdownPattern("a1", re.compile(r"\[(?P<linktext>.*?)\]\((?P<href>.*?) \"(?P<title>.*?)\"\)"), "<a href='&2' title='&3'>&1</a>"), 
    "a2":    MarkdownPattern("a2", re.compile(r"\[(?P<linktext>.*?)\]\((?P<href>.*?)\)"), "<a href='&2'>&1</a>"), 
    
    # headings are processed in the reverse order h6 to h1 
    "h1":     MarkdownPattern("h1",     re.compile(r"\#{1}\s(?!\#)(?P<heading>.*)"), "<h1>&1</h1>"),
    "h2":     MarkdownPattern("h2",     re.compile(r"\#{2}\s(?!\#)(?P<heading>.*)"), "<h2>&1</h2>"),
    "h3":     MarkdownPattern("h3",     re.compile(r"\#{3}\s(?!\#)(?P<heading>.*)"), "<h3>&1</h3>"),
    "h4":     MarkdownPattern("h4",     re.compile(r"\#{4}\s(?!\#)(?P<heading>.*)"), "<h4>&1</h4>"),
    "h5":     MarkdownPattern("h5",     re.compile(r"\#{5}\s(?!\#)(?P<heading>.*)"), "<h5>&1</h5>"),
    "h6":     MarkdownPattern("h6",     re.compile(r"\#{6}\s(?!\#)(?P<heading>.*)"), "<h6>&1</h6>"),
    
    # use a multi-step process to handle unordered lists
    "ul_a":   MarkdownPattern("ul_a",   re.compile(r"\n\*\s(?P<wholelist>.*)"), "<ula>&1</ula>"),
    "li":     MarkdownPattern("li",     re.compile(r"<\/ula><ula>(?P<itemboundary>)"), "</li>\n<li>"),
    "ul_b":   MarkdownPattern("ul_b",   re.compile(r"<ula>(?P<liststart>)"), "\n<ul>\n<li>"),
    "ul_c":   MarkdownPattern("ul_c",   re.compile(r"</ula>(?P<listend>)"), "</li>\n</ul>"),

    # paragraphs
    "p":      MarkdownPattern("p",   re.compile(r"\n{1}(?!<)(?!\n)(?P<para>.*)"), "\n<p>&1</p>"),
}

# This method replaces markdown elements in a body of text with HTML tags using a list of named
# MarkdownPatterns. The appropriate MarkdownPattern instance is retreived by name from a dictionary 
# of MarkdownPatterns.
def markdown(text):

    for name in process_order:
        mdp =  patterns.get(name) # get MarkdownPattern from the list
        x = re.search(mdp.pattern, text) # priming search
        
        while x is not None:
            # use regex to create the replacement string for this occurrence of the pattern
            replacement = mdp.replace
            i = 1
            while i <= len(x.groups()):
                replacement = re.sub(re.compile(f"&{i}"), x.group(i), replacement, 1 )
                i = i + 1
            # end while i

            # replace the first matched occurence of the pattern with the replacement string
            text = re.sub(mdp.pattern, replacement, text, 1) # 1 indicates first occurrence
            x = re.search(mdp.pattern, text) # search again to find another occurrence           
        # end while x
    return text   
# end def markdown()

# Some sample markdown text that is useful for testing this module. A main method is also supplied
# to facilitate running this module from the command line for testing purposes.
sample = """* first
* second

# Lorem ipsum
Lorem ipsum dolor sit amet, consectetur adipiscing elit. 

## Lorem ipsum

### Proin bibendum
Proin bibendum, **lacus vitae congue mattis**, felis ** sapien ornare elit, eu porta diam neque id lorem. Vivamus pretium viverra augue nec interdum. Donec augue tortor, **sagittis vel sagittis a**, accumsan sed ex. Aenean nec arcu enim. Suspendisse sit amet fermentum libero, quis tempor est. 

* item 1
* item 2
* item 3

### Pellentesque 
volutpat odio mattis, http://nodeca.github.io/pica/demo/ ultricies erat eget, commodo ante. Aliquam nec tellus velit. Vestibulum consectetur aliquam augue, at bibendum quam porttitor varius. Here is a random \* to make sure I am taking care of escaped substrings.

# Django

Django is a web framework written using [Python](/wiki/Python) that allows for the design of web applications that generate [HTML](/wiki/HTML) dynamically.

You can get your own copy of lorem ipsum text at [Lorem Ipsum](https://www.lipsum.com/).
[Lorem Ipsum](https://www.lipsum.com/).
Here is a link [link text](/dev/nodeca) inside some text.
[link with title](http://nodeca.github.io/pica/demo/ "title text!")
"""

# The main method to test the md module.
def main():
    html = markdown(sample)
    print(f"HERE IS THE OUTPUT:\n {html}")


if __name__ == "__main__":
    main()
