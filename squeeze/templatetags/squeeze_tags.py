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
from django.contrib.sites.models import Site

import squeeze


register = template.Library()

def gettime(filename):
    time = localtime(getmtime(filename))
    return strftime('%Y%m%d%H%M', time)


class SqueezeNode(template.Node):
    def __init__(self, ftype, result_file, files, additional=None):
        self.ftype = ftype
        self.result_file = result_file
        self.files = files
        self.additional = additional

    def render(self, context):

        result_file = normpath(join(settings.STATIC_ROOT,
                resolve_variable(self.result_file, context)))
        url = urljoin(settings.STATIC_URL,
                resolve_variable(self.result_file, context))
        last_write_time = exists(result_file) and gettime(result_file) or '0'

        files = resolve_variable(self.files, context).split(',')
        fs_files = [normpath(join(settings.STATIC_ROOT, x)) for x in files]

        need_regeneration = False
        if exists(result_file):
            for f in fs_files:
                if not exists(f):
                    raise template.TemplateSyntaxError, "%s file doesn't exists" % f
                if last_write_time < gettime(f):
                    need_regeneration = True
                    break
        else:
            need_regeneration = True

        if self.ftype in ('js_gclosure', 'js'):
            tpl = u'<script type="text/javascript" src="%s"></script>'
        else: # this is css
            media = self.additional and resolve_variable(self.additional, context) or u'screen'
            tpl = u'<link href="%s" rel="stylesheet" type="text/css" media="' + media + '" />'

        if need_regeneration:

            res = open(result_file, 'w')
            if self.ftype == 'js_gclosure':
                compress_level = self.additional and \
                    resolve_variable(self.additional, context) or "SIMPLE_OPTIMIZATIONS"
                full_static_path = urljoin(u'http://%s/' %
                    (context['request'].get_host()), settings.STATIC_URL)
                files = ['%s?%s' % (urljoin(full_static_path, x), last_write_time) for x in files]
                try:
                    squeeze.JSMinify_GClosure(compress_level).minify(files, res)
                except IOError:
                    self.ftype = 'js'

            if self.ftype == 'js' or self.ftype == 'css':
                files = fs_files
                src = StringIO()
                for f in files:
                    tmp = open(f, 'rb').read()
                    src.write(tmp)
                src.seek(0)
                if self.ftype == 'js':
                    squeeze.JavascriptMinify().minify(src, res)
                else: # this is css
                    squeeze.CSSMinify().minify(src, res)

            res.close()

        last_write_time = last_write_time == '0' and gettime(result_file) or last_write_time
        return_tag = tpl % ('%s?%s' % (url, last_write_time))
        return return_tag


@register.tag
def css_squeeze(parser, token):
    """
    {% css_squeeze "css/dynamic_minifyed.css" "css/style1.css,css/style2.css" %}
    will produce STATIC_ROOT/css/dynamic_minifyed.css
    {% css_squeeze "css/dynamic_minifyed.css" "css/style1.css,css/style2.css" "screen,print" %}
    """
    bits = token.split_contents()
    if len(bits) not in [3, 4]:
        raise template.TemplateSyntaxError, "%r tag requires two or three arguments" % bits[0]
    return SqueezeNode('css', *bits[1:])

@register.tag
def js_squeeze(parser, token):
    """
    {% js_squeeze "js/dynamic_minifyed.js" "js/script1.js,js/script2.js" %}
    will produce STATIC_ROOT/js/dynamic_minifyed.js
    """
    bits = token.split_contents()
    if len(bits) != 3:
        raise template.TemplateSyntaxError, "%r tag requires exactly two arguments" % bits[0]
    return SqueezeNode('js', *bits[1:])

@register.tag()
def js_gclosure(parser, token):
    """
    {% js_gclosure "js/dynamic_minifyed.js" "js/script1.js,js/script2.js" %}
    will produce STATIC_ROOT/js/dynamic_minifyed.js
    {% js_gclosure "js/dynamic_minifyed.js" "js/script1.js,js/script2.js"
    "SIMPLE_OPTIMIZATIONS||WHITESPACE_ONLY||ADVANSED_OPTIMIZATIONS"%}
    """
    bits = token.split_contents()
    if len(bits) not in [3, 4]:
        raise template.TemplateSyntaxError, "%r tag requires two or three arguments" % bits[0]
    return SqueezeNode('js_gclosure', *bits[1:])
