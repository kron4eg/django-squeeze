#!/usr/bin/env python
from distutils.core import setup

setup(name = "django-squeeze-gclosure",
      version = '0.1',
      author = "Pavel Puchkin",
      author_email = "neoascetic@gmail.com",
      url = "http://github.com/neoascetic/django-squeeze",
      license = "BSD",
      description = "Squeeze CSS and JS (using Crockford algorithm or Google Closure REST API) files on the fly, for django.",
      packages = ['squeeze', 'squeeze.templatetags'],
      platforms = ['any'],
      classifiers = [
          'Development Status :: 4 - Beta',
          'Framework :: Django',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ]
)

