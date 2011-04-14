#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib, urllib2, sys

class JSMinify_GClosure(object):
    # TODO: add error's and warning's handling
    def __init__(self, compilation_level="SIMPLE_OPTIMIZATIONS"):
        self.params = [
            ('compilation_level', compilation_level),
            ('output_format', 'text'),
            ('output_info', 'compiled_code'),
        ]
        self.headers = { 'Content-type': 'application/x-www-form-urlencoded' }

    def minify(self, files, outstream):
        self.params.extend([('code_url', file) for file in files])
        params = urllib.urlencode(self.params)
        req = urllib2.Request('http://closure-compiler.appspot.com/compile', params, self.headers)
        data = urllib2.urlopen(req).read()
        outstream.write(data)

if __name__ == '__main__':
    gclos = JSMinify_GClosure()
    gclos.minify(sys.argv)
