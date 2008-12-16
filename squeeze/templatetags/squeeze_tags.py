# -*- coding: utf-8 -*-
from os import path
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from urlparse import urljoin

from django import template
from django.conf import settings
from django.template import resolve_variable

import squeeze


register = template.Library()
SQUEEZE_CACHE = {}

class SqueezeNode(template.Node):
    def __init__(self, ftype, result_file, files, media=None):
        self.ftype = ftype
        self.result_file = result_file
        self.files = files
        self.media = media

    def render(self, context):
        try:
            return SQUEEZE_CACHE[self.result_file]
        except KeyError:
            pass
        result_file = path.join(settings.MEDIA_ROOT,
                resolve_variable(self.result_file, context))
        media = self.media and resolve_variable(self.media, context) or u'screen'
        if self.ftype == 'css':
            minifyer = squeeze.CSSMinify()
            tpl = u'<link href="%s" rel="stylesheet" type="text/css" media="' + media + '" />'
        else:
            minifyer = squeeze.JavascriptMinify()
            tpl = u'<script type="text/javascript" src="%s"></script>'
        files = resolve_variable(self.files, context)
        files = [path.join(settings.MEDIA_ROOT, x) for x in files.split(',')]
        buf = StringIO()
        for f in files:
            tmp = open(f, 'rb').read()
            buf.write(tmp)
        buf.seek(0)
        res = open(result_file, 'w')
        minifyer.minify(buf, res)
        res.close()
        url = urljoin(settings.MEDIA_URL,
                resolve_variable(self.result_file, context))
        SQUEEZE_CACHE[self.result_file] = tpl % url
        return SQUEEZE_CACHE[self.result_file]



@register.tag
def css_squeeze(parser, token):
    """
    {% css_squeeze "css/dynamic_minifyed.css" "css/style1.css,css/style2.css" %}
    will produce MEDIA_ROOT/css/dynamic_minifyed.css
    {% css_squeeze "css/dynamic_minifyed.css" "css/style1.css,css/style2.css" "screen,print" %}
    """
    bits = token.split_contents()
    if len(bits) not in [3, 4]:
        raise template.TemplateSyntaxError, "%r tag requires two or tree arguments" % bits[0]
    return SqueezeNode('css', *bits[1:])


@register.tag
def js_squeeze(parser, token):
    """
    {% js_squeeze "js/dynamic_minifyed.js" "js/script1.js,js/script2.js" %}
    will produce MEDIA_ROOT/js/dynamic_minifyed.js
    """
    bits = token.split_contents()
    if len(bits) != 3:
        raise template.TemplateSyntaxError, "%r tag requires exactly two arguments" % bits[0]
    return SqueezeNode('js', *bits[1:])

