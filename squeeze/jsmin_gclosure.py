#!/usr/bin/python
# -*- coding: utf-8 -*-

import httplib, urllib, sys

class JSMinify_GClosure(object):
    # TODO: add error's and warning's handling
    def __init__(self, compilation_level):
        self.params = [
            ('compilation_level', (compilation_level and compilation_level or "SIMPLE_OPTIMIZATIONS")),
            ('output_format', 'text'),
            ('output_info', 'compiled_code'),
        ]
        self.headers = { 'Content-type': 'application/x-www-form-urlencoded' }

    def minify(self, files, outstream):
        self.params.extend([('code_url', file) for file in files])
        params = urllib.urlencode(self.params)
        conn = httplib.HTTPConnection('closure-compiler.appspot.com')
        conn.request('POST', '/compile', params, self.headers)
        response = conn.getresponse()
        outstream.write(response.read());
        conn.close()

if __name__ == '__main__':
    gclos = JSMinify_GClosure()
    gclos.minify(sys.argv)
