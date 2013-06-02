from django import template
register = template.Library()
import simplejson


@register.filter
def to_json_linkpreview(value, item = None):
    if(item):
        new_val = simplejson.loads(value)
        #import ipdb;ipdb.set_trace()
        return new_val[item]
    else:
        return simplejson.loads(value)


register.filter('json_lp', to_json_linkpreview)
