django-dynasite
===============

Tools to dynamically manage multiple Django Web sites in a single app the way you need to.


=====
Usage
=====

django-dynasite was developed to:
 * manage multiple sites in a single Django app

Installation
============

Available on PyPi::

    pip install django-dynasite

Configuration
=============

Add to your installed apps in your setting.py file::

    INSTALLED_APPS = (
    ...
    'dynasite',
    )

Get the Site from SITE_ID or host name
=============

django.contrib.sites.models.get_current_site Replacement
Instead, use:
    from dynasite.models import get_current_site
    ...
    site = get_current_site(request)

Will fetch the site from the SITE_ID setting if defined. Otherwise, will try to match the hostname to a domain defined in django.contrib.sites.models.Site. Caching is used.

Add site variables to context to use in your Web app templates
=============

Simply add this middleware to your settings:

    TEMPLATE_CONTEXT_PROCESSORS = (
    	...
        'dynasite.context_processors.dynasite_context_processor',
        ...
    )

Then, in your template, you have access to the 'dynasite' variable:

    dynasite.site  -> returns the current site
    dynasite.site_url  -> returns the current site's complete url. Takes into account if in secure mode or not.

Replace cache middleware to take into account varying host names
=============

By default, Django uses the full path of pages when creating keys for caching. However, it doesn't take into account the full URI when building the keys. If page templates change by host name, change your caching middleware:

    MIDDLEWARE_CLASSES = (
        'dynasite.middleware.UpdateCacheMiddleware',
        ...
        'dynasite.middleware.FetchFromCacheMiddleware',
        ...

LICENSE
=======

Copyright (c) 2013 Jerome Paradis and contributors

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.