Installation
============

Put squeeze somewhere in PYTHONPATH, and make it appear in INSTALLED_APPS in settings.

    INSTALLED_APPS += (
        'squeeze',
    )


Usage
=====

In template

    {% load squeeze_tags %}


CSS minification
----------------

    {% css_squeeze "css/dynamic_minifyed.css" "css/style1.css,css/style2.css" %}

Will write minified

    {{ MEDIA_ROOT }}css/dynamic_minifyed.css

file and return (assumed "/static/" is you MEDIA_URL)

    <link href="/static/css/dynamic_minifyed.css" rel="stylesheet" type="text/css" media="screen" />


JavaScript minification
-----------------------

    {% js_squeeze "js/dynamic_minifyed.js" "js/script1.js,js/script2.js" %}

Will write minified

    {{ MEDIA_ROOT }}js/dynamic_minifyed.js

and return (assumed "/static/" is you MEDIA_URL)

    <script type="text/javascript" src="/static/js/dynamic_minifyed.js"></script>


Regeneration
------------

Those files will be regenerated every time project reloads
