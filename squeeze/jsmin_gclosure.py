#!/usr/bin/python
# -*- coding: utf-8 -*-

import httplib, urllib, sys

class JSMinify_GClosure(object):
	# TODO: add error's and warning's handling
	def minify(self, files_or_code, compilation_level="SIMPLE_OPTIMIZATIONS"):
		headers = { 'Content-type': 'application/x-www-form-urlencoded' }
		params = [
			('compilation_level', compilation_level),
			('output_format', 'text'),
			('output_info', 'compiled_code'),
		]
		params.extend(type(files_or_code).__name__ == 'str' and
			[('js_code', files_or_code)] or
			[('code_url', file) for file in files_or_code])
		print params
		params = urllib.urlencode(params)
		conn = httplib.HTTPConnection('closure-compiler.appspot.com')
		conn.request('POST', '/compile', params, headers)
		response = conn.getresponse()
		data = response.read()
		conn.close()
		return data

if __name__ == '__main__':
	gclos = JSMinify_GClosure()
	print gclos.minify(sys.argv[1])
