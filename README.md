Installation
============

Put it somewhere in PYTHONPATH, and make it appear in INSTALLED_APPS in settings

    INSTALLED_APPS += (
        'squeeze',
    )


Usage
=====

In template

    {% load squeeze_tags %}

CSS minification
----------------

    {% css_squeeze "css/dynamic_minifyed.css" "css/style1.css,css/style2.css" %} will produce MEDIA_ROOT/css/dynamic_minifyed.css

JavaScript minification
-----------------------

    {% js_squeeze "js/dynamic_minifyed.js" "js/script1.js,js/script2.js" %} will produce MEDIA_ROOT/js/dynamic_minifyed.js

those files will regenerate every project reload
