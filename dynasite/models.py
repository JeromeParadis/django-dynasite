# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.sites.models import Site

SITES_CACHE = {}

def get_current_site(request):
    """
    Get current site by SITE_ID if defined or use host otherwise
    """
    if hasattr(settings, 'SITE_ID') and settings.SITE_ID:
        return Site.objects.get_current()

    host = request.get_host()
    if host == 'testserver' and hasattr(settings, 'DEFAULT_SITE_ID'):
        return Site.objects.get(pk=settings.DEFAULT_SITE_ID)

    # Get from host cache if exists
    # -----------------------
    if host in SITES_CACHE:
        return SITES_CACHE[host]

    # Try by raw hostname
    # -----------------------
    try:
        site = Site.objects.get(domain=host)
        SITES_CACHE[host] = site
        return site
    except Site.DoesNotExist:
        pass

    # Try by hostname without port
    # -----------------------
    shost = host.rsplit(':', 1)[0] # only host, without port
    if shost != host:
        if shost in SITES_CACHE:
            return SITES_CACHE[shost]
        try:
            site = Site.objects.get(domain=shost)
            SITES_CACHE[host] = site
            return site
        except Site.DoesNotExist:
            pass

    raise Site.DoesNotExist
