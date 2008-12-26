#!/usr/bin/env python
from distutils.core import setup

setup(name = "django-squeeze",
      version = '0.1',
      author = "Artiom Diomin",
      author_email = "kron82@gmail.com",
      url = "http://github.com/kron4eg/django-squeeze",
      license = "BSD",
      description = "Squeeze JS/CSS files on the fly, for django",
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

