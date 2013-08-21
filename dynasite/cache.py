"""
Modified version to use request.build_absolute_uri()
This module contains helper functions for controlling caching. It does so by
managing the "Vary" header of responses. It includes functions to patch the
header of response objects directly and decorators that change functions to do
that header-patching themselves.

For information on the Vary header, see:

    http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.44

Essentially, the "Vary" HTTP header defines which headers a cache should take
into account when building its cache key. Requests with the same path but
different header content for headers named in "Vary" need to get different
cache keys to prevent delivery of wrong content.

An example: i18n middleware would need to distinguish caches by the
"Accept-language" header.
"""
from __future__ import unicode_literals

import hashlib
import re
import time

from django.conf import settings
from django.core.cache import get_cache
from django.utils.encoding import iri_to_uri, force_bytes, force_text
from django.utils.http import http_date
from django.utils.timezone import get_current_timezone_name
from django.utils.translation import get_language

from django.utils.cache import cc_delim_re, _i18n_cache_key_suffix

def _generate_cache_key(request, method, headerlist, key_prefix):
    """Returns a cache key from the headers given in the header list."""
    ctx = hashlib.md5()
    for header in headerlist:
        value = request.META.get(header, None)
        if value is not None:
            ctx.update(force_bytes(value))
    path = hashlib.md5(force_bytes(iri_to_uri(request.build_absolute_uri())))
    cache_key = 'views.decorators.cache.cache_page.%s.%s.%s.%s' % (
        key_prefix, method, path.hexdigest(), ctx.hexdigest())
    return _i18n_cache_key_suffix(request, cache_key)

def _generate_cache_header_key(key_prefix, request):
    """Returns a cache key for the header cache."""
    path = hashlib.md5(force_bytes(iri_to_uri(request.build_absolute_uri())))
    cache_key = 'views.decorators.cache.cache_header.%s.%s' % (
        key_prefix, path.hexdigest())
    return _i18n_cache_key_suffix(request, cache_key)

def get_cache_key(request, key_prefix=None, method='GET', cache=None):
    """
    Returns a cache key based on the request path and query. It can be used
    in the request phase because it pulls the list of headers to take into
    account from the global path registry and uses those to build a cache key
    to check against.

    If there is no headerlist stored, the page needs to be rebuilt, so this
    function returns None.
    """
    if key_prefix is None:
        key_prefix = settings.CACHE_MIDDLEWARE_KEY_PREFIX
    cache_key = _generate_cache_header_key(key_prefix, request)
    if cache is None:
        cache = get_cache(settings.CACHE_MIDDLEWARE_ALIAS)
    headerlist = cache.get(cache_key, None)
    if headerlist is not None:
        return _generate_cache_key(request, method, headerlist, key_prefix)
    else:
        return None

def learn_cache_key(request, response, cache_timeout=None, key_prefix=None, cache=None):
    """
    Learns what headers to take into account for some request path from the
    response object. It stores those headers in a global path registry so that
    later access to that path will know what headers to take into account
    without building the response object itself. The headers are named in the
    Vary header of the response, but we want to prevent response generation.

    The list of headers to use for cache key generation is stored in the same
    cache as the pages themselves. If the cache ages some data out of the
    cache, this just means that we have to build the response once to get at
    the Vary header and so at the list of headers to use for the cache key.
    """
    if key_prefix is None:
        key_prefix = settings.CACHE_MIDDLEWARE_KEY_PREFIX
    if cache_timeout is None:
        cache_timeout = settings.CACHE_MIDDLEWARE_SECONDS
    cache_key = _generate_cache_header_key(key_prefix, request)
    if cache is None:
        cache = get_cache(settings.CACHE_MIDDLEWARE_ALIAS)
    if response.has_header('Vary'):
        headerlist = ['HTTP_'+header.upper().replace('-', '_')
                      for header in cc_delim_re.split(response['Vary'])]
        cache.set(cache_key, headerlist, cache_timeout)
        return _generate_cache_key(request, request.method, headerlist, key_prefix)
    else:
        # if there is no Vary header, we still need a cache key
        # for the request.get_full_path()
        cache.set(cache_key, [], cache_timeout)
        return _generate_cache_key(request, request.method, [], key_prefix)

