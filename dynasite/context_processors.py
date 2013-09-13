from django.conf import settings
from django.template import RequestContext
from django.contrib.sites.models import Site, RequestSite

from models import get_current_site

def dynasite_context_processor(request):

    try:
        dynasite = { 'site': get_current_site(request) }
        dynasite['site_url'] = 'http%s://%s' % ('s' if request.is_secure else '', dynasite['site'].domain, )
    except:
        dynasite = None


    return { 'dynasite': dynasite }