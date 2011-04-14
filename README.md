Installation
============

Put `squeeze` somewhere in `PYTHONPATH`, make it appear in `INSTALLED_APPS` in settings

    INSTALLED_APPS += (
        'squeeze',
    )

and add `django.core.context_processors.request` to your `TEMPLATE_CONTEXT_PROCESSORS`:
    
    TEMPLATE_CONTEXT_PROCESSORS += (
        'django.core.context_processors.request',
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

file and return (assumed "/static/" is you `settings.MEDIA_URL`)

    <link href="/static/css/dynamic_minifyed.css" rel="stylesheet" type="text/css" media="screen" />


JavaScript minification
-----------------------

    {% js_squeeze "js/dynamic_minifyed.js" "js/script1.js,js/script2.js" %}

Will write minified

    {{ MEDIA_ROOT }}js/dynamic_minifyed.js

and return (assumed "/static/" is you `settings.MEDIA_URL`)

    <script type="text/javascript" src="/static/js/dynamic_minifyed.js"></script>


JavaScript minification using Google Closure Compiler REST API
--------------------------------------------------------------

    {% js_gclosure "js/dynamic_minifyed_closure.js" "js/script1.js,js/script2.js" %}

Will write minified

    {{ MEDIA_ROOT }}js/dynamic_minifyed_closure.js

and return (assumed "/static" is you `settings.MEDIA_URL`)

    <script type="text/javascript" src="/static/js/dynamic_minifyed_closure.js"></script>

As additional parameter, you can put compression level string in Closure API terms just like:

    {% js_gclosure "js/dynamic_minifyed_closure.js" "js/script1.js,js/script2.js" "WHITESPACE_ONLY" %}

Default compression level is "SIMPLE_OPTIMIZATIONS"

Regeneration
------------

Those files will be regenerated only in case original files changed.
