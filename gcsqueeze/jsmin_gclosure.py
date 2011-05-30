#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib, urllib2, json

class JSMinify_GClosure(object):
    def __init__(self, compilation_level):
        compilation_level = compilation_level and compilation_level or 'SIMPLE_OPTIMIZATIONS'
        self.params = [
            ('compilation_level', compilation_level),
            ('output_format', 'json'),
            ('output_info', 'compiled_code'),
            ('output_info', 'errors'),
            ('output_info', 'warnings'),
        ]
        self.headers = { 'Content-type': 'application/x-www-form-urlencoded' }

    def minify(self, files, outstream):
        self.params.extend([('code_url', file) for file in files])
        params = urllib.urlencode(self.params)
        req = urllib2.Request('http://closure-compiler.appspot.com/compile', params, self.headers)
        conn = urllib2.urlopen(req)
        data = json.loads(conn.read())
        print 'Warnings:'
        print json.dumps(data.get('warnings'), sort_keys=True, indent=4)
        if 'serverErrors' in data or 'errors' in data:
            print 'Server Errors:'
            print json.dumps(data.get('serverErrors'), sort_keys=True, indent=4)
            print 'Compiling Errors:'
            print json.dumps(data.get('errors'), sort_keys=True, indent=4)
            raise IOError('Errors while compiling')
        else:
            outstream.write(data['compiledCode'])
        conn.close()

if __name__ == '__main__':
    import sys, urlparse
    from optparse import OptionParser

    usage = 'usage: %prog [options] file1 file2 http://example.com/file3 outfile'
    parser = OptionParser(usage=usage)
    parser.add_option('-l', action='store', dest='compilation_level',
        help='compilation level, default SIMPLE_OPTIMIZATIONS')
    parser.add_option('-u', action='store', dest='url', help='this prefix will be added to each non-URL path to file')
    (opts, args) = parser.parse_args()

    gclos = JSMinify_GClosure(opts.compilation_level and opts.compilation_level)
    files = [urlparse.urljoin(opts.url, file) for file in args[:-1]]
    output = args[-1]

    result = open(output, 'w')
    gclos.minify(files, result)
    result.close()
