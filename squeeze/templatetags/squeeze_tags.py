# -*- coding: utf-8 -*-
from os.path import join, exists, getmtime, normpath
from time import localtime, strftime

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

def gettime(filename):
    time = localtime(getmtime(filename))
    return strftime('%Y%m%d%H%M', time)


class SqueezeNode(template.Node):
    def __init__(self, ftype, result_file, files, media=None):
        self.ftype = ftype
        self.result_file = result_file
        self.files = files
        self.media = media

    def render(self, context):
        def generate(result_file, files, minifyer):
            buf = StringIO()
            for f in files:
                tmp = open(f, 'rb').read()
                buf.write(tmp)
            buf.seek(0)
            res = open(result_file, 'w')
            minifyer.minify(buf, res)
            res.close()

        result_file = normpath(join(settings.MEDIA_ROOT,
                resolve_variable(self.result_file, context)))
        last_write_time = exists(result_file) and gettime(result_file) or '0'
        media = self.media and resolve_variable(self.media, context) or u'screen'
        if self.ftype == 'css':
            minifyer = squeeze.CSSMinify()
            tpl = u'<link href="%s" rel="stylesheet" type="text/css" media="' + media + '" />'
        else:
            minifyer = squeeze.JavascriptMinify()
            tpl = u'<script type="text/javascript" src="%s"></script>'
        url = urljoin(settings.MEDIA_URL,
                resolve_variable(self.result_file, context))
        files = resolve_variable(self.files, context)
        files = [normpath(join(settings.MEDIA_ROOT, x)) for x in files.split(',')]
        need_regeneration = False
        if exists(result_file):
            for f in files:
                if not exists(f):
                    raise template.TemplateSyntaxError, "%s file doesn't exists" % f
                if last_write_time < gettime(f):
                    need_regeneration = True
        else:
            need_regeneration = True

        if need_regeneration:
            generate(result_file, files, minifyer)
        last_write_time = last_write_time == '0' and gettime(result_file) or last_write_time
        return_tag = tpl % ('%s?%s' % (url, last_write_time))
        return return_tag


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

