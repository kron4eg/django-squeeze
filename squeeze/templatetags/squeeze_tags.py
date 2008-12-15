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
    def __init__(self, ftype, result_file, files):
        self.ftype = ftype
        self.result_file = result_file
        self.files = files

    def render(self, context):
        try:
            return SQUEEZE_CACHE[self.result_file]
        except KeyError:
            pass
        result_file = path.join(settings.MEDIA_ROOT, resolve_variable(self.result_file, context))
        if self.ftype == 'css':
            minifyer = squeeze.CSSMinify()
            tpl = '<link href="%s" rel="stylesheet" type="text/css" media="screen" />'
        else:
            minifyer = squeeze.JavascriptMinify()
            tpl = '<script type="text/javascript" src="%s"></script>'
        files = resolve_variable(self.files, context)
        files = [path.join(settings.MEDIA_ROOT, x) for x in files.split(',')]
        buf = StringIO()
        for f in files:
            tmp = open(f, 'rb').read()
            buf.write(tmp)
        buf.seek(0)
        res = open(result_file, 'w+')
        minifyer.minify(buf, res)
        res.close()
        SQUEEZE_CACHE[self.result_file] = tpl % urljoin(settings.MEDIA_URL, resolve_variable(self.result_file, context))
        return SQUEEZE_CACHE[self.result_file]



@register.tag
def css_squeeze(parser, token):
    """
    {% css_squeeze "css/dynamic_minifyed.css" "css/style1.css,css/style2.css" %}
    will produce MEDIA_ROOT/css/dynamic_minifyed.css
    """
    bits = token.split_contents()
    if len(bits) != 3:
        raise template.TemplateSyntaxError, "%r tag requires exactly two argument" % bits[0]
    return SqueezeNode('css', *bits[1:])


@register.tag
def js_squeeze(parser, token):
    """
    {% js_squeeze "js/dynamic_minifyed.js" "js/script1.js,js/script2.js" %}
    will produce MEDIA_ROOT/js/dynamic_minifyed.js
    """
    bits = token.split_contents()
    return SqueezeNode('js', *bits[1:])

