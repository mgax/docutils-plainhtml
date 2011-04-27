# code stolen from http://www.arnebrodowski.de/blog/write-your-own-restructuredtext-writer.html

from docutils.writers import html4css1
from docutils import nodes

class Writer(html4css1.Writer):
    """
    This docutils writer will use the HTMLTranslator class below.
    """
    def __init__(self):
        html4css1.Writer.__init__(self)
        self.translator_class = HTMLTranslator

class HTMLTranslator(html4css1.HTMLTranslator, object):
    """
    This is a translator class for the docutils system.
    It will produce a minimal set of html output.
    (No extry divs, classes oder ids.)
    """

    def __init__(self, *args, **kwargs):
        super(HTMLTranslator, self).__init__(*args, **kwargs)
        self.section_level = 1

    def visit_block_quote(self, node):
        self.body.append(self.starttag(node, 'blockquote'))

    def depart_block_quote(self, node):
        self.body.append('</blockquote>\n')

    def visit_paragraph(self, node):
        if self.should_be_compact_paragraph(node):
            self.context.append('')
        else:
            self.body.append(self.starttag(node, 'p', ''))
            self.context.append('</p>\n')

    def depart_paragraph(self, node):
        self.body.append(self.context.pop())

    def should_be_compact_paragraph(self, node):
        if(isinstance(node.parent, nodes.block_quote)):
            return 0
        return super(HTMLTranslator, self).should_be_compact_paragraph(node)

    def visit_section(self, node):
        self.section_level += 1

    def depart_section(self, node):
        self.section_level -= 1

    def visit_footnote(self, node):
        self.body.append(self.starttag(node, 'section',
                                       CLASS='docutils footnote'))
        self.footnote_backrefs(node)

    def footnote_backrefs(self, node):
        backlinks = []
        backrefs = node['backrefs']
        if self.settings.footnote_backlinks and backrefs:
            if len(backrefs) == 1:
                self.context.append('')
                self.context.append('</a>')
                self.context.append('<a class="fn-backref" href="#%s">'
                                    % backrefs[0])
            else:
                raise NotImplementedError # following block needs testing
                i = 1
                for backref in backrefs:
                    backlinks.append('<a class="fn-backref" href="#%s">%s</a>'
                                     % (backref, i))
                    i += 1
                self.context.append('<em>(%s)</em> ' % ', '.join(backlinks))
                self.context += ['', '']
        else:
            self.context.append('')
            self.context += ['', '']

    def visit_label(self, node):
        # Context added in footnote_backrefs.
        self.body.append(self.starttag(node, 'p', '%s[' % self.context.pop()))

    def depart_label(self, node):
        # Context added in footnote_backrefs.
        self.body.append(']%s\n%s' % (self.context.pop(), self.context.pop()))

    def depart_footnote(self, node):
        self.body.append('</p>\n'
                         '</section>\n')

out_tmpl = """<!doctype html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>%(title)s</title>
</head>
<body>
%(html_body)s
</body>
</html>
"""

def main():
    import sys
    from docutils.core import publish_parts
    text = sys.stdin.read()
    print (out_tmpl % publish_parts(text, writer=Writer())).encode('utf-8'),
