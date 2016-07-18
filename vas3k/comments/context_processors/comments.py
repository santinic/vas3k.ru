from comments.models import Comment


def last_comments_processor(request):
    return {
        "last_comments": Comment.objects.filter(is_visible=True).order_by("-id")[:40]
    }