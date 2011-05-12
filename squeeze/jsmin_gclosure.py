#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib, urllib2, json

class JSMinify_GClosure(object):
    def __init__(self, compilation_level="SIMPLE_OPTIMIZATIONS"):
        self.params = [
            ('compilation_level', compilation_level),
            ('output_format', 'json'),
            ('output_info', 'compiled_code'),
            ('output_info', 'errors'),
        ]
        self.headers = { 'Content-type': 'application/x-www-form-urlencoded' }

    def minify(self, files, outstream):
        self.params.extend([('code_url', file) for file in files])
        params = urllib.urlencode(self.params)
        req = urllib2.Request('http://closure-compiler.appspot.com/compile', params, self.headers)
        conn = urllib2.urlopen(req)
        data = json.loads(conn.read())
        if 'serverErrors' in data or 'errors' in data:
            raise IOError('Errors while compiling')
        else:
            outstream.write(data['compiledCode'])
        conn.close()

if __name__ == '__main__':
    import sys
    gclos = JSMinify_GClosure()
    gclos.minify(sys.argv)
