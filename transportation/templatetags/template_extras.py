from django import template
from django.template.defaultfilters import stringfilter
from django.utils.http import urlencode, urlquote
from django.utils.text import slugify

import hashlib

register = template.Library()


@register.filter
@stringfilter
def slug(value):
    replacements = [(u'ä', u'ae'),(u'ö', u'oe'),(u'ü', u'ue'), (u'ß', u'sz'), ]
    for (s, r) in replacements:
            value = value.replace(s, r)
    return slugify(value)


@register.simple_tag()
def get_gravatar_url(user, size, rating='g', default='identicon'):
    url = "https://www.gravatar.com/avatar/"
    hash = hashlib.md5(user.email.strip().lower().encode('utf-8')).hexdigest()
    data = urlencode([('d', urlquote(default)),
                      ('s', str(size)),
                      ('r', rating)])
    return "".join((url, hash, '?', data))