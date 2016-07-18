from django import template

register = template.Library()


@register.inclusion_tag("comments/form.html")
def comment_form(story_id, username):
    return {
        "story_id": story_id,
        "username": username
    }
