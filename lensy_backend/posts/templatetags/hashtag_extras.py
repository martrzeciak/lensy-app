import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def link_hashtags(text):
    def repl(match):
        tag = match.group(1)
        return (
            f'<a href="/posts/hashtag/{tag.lower()}/" '
            f'class="text-primary text-decoration-none">#{tag}</a>'
        )

    return mark_safe(re.sub(r'#(\w+)', repl, text))