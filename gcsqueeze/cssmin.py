#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


comments_remove_re = r'/\*.*?\*/'
comments_remove = re.compile(comments_remove_re)

class CSSMinify(object):
    def minify(self, instream, outstream):
        ins = instream.readlines()
        res = []
        for x in ins:
            res.append(x.strip().replace(', ', ','))
        outstream.write(comments_remove.sub('', ''.join(res)))
        instream.close()


if __name__ == '__main__':
    import sys
    cssm = CSSMinify()
    cssm.minify(sys.stdin, sys.stdout)
