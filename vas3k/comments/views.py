from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from comments.models import Comment
from stories.models import Story


def send(request):
    if request.method == "POST":
        # Simple antispam
        if request.POST.get("site", "").strip() or request.POST.get("web", "").strip() or request.POST.get("url", "").strip():
            return render(request, "comments/error.html", {
                "message": "Спамер!"
            })

        try:
            antibot = request.POST.get("email", "").strip()
            if antibot != "":
                raise Exception("Вы - бот!")

            story_id = request.POST.get("story_id", "").strip()
            if story_id == "":
                raise Exception("ID пустое")

            author = request.POST.get("author", "").strip()
            if author == "":
                raise Exception("Поле автор должно быть заполнено")

            if len(author) > 20:
                raise Exception("Ник слишком длинный")

            text = request.POST.get("text", "").strip()
            if text == "":
                raise Exception("Напишите текст комментария")

            ip = request.META.get("HTTP_X_REAL_IP") \
                 or request.META.get("HTTP_X_FORWARDED_FOR") \
                 or request.environ["REMOTE_ADDR"]

            useragent = request.META.get("HTTP_USER_AGENT", "")
        except Exception as e:
            return render(request, "comments/error.html", {
                "message": e
            })

        story = get_object_or_404(Story, id=story_id)

        if not story.is_commentable:
            return render(request, "comments/error.html", {
                "message": "Нельзя комментировать этот пост"
            })

        try:
            comment = Comment.objects.create(
                story_id=story_id,
                avatar=Comment.generate_avatar(author, story_id, ip),
                author=author,
                text=text,
                ip=ip,
                useragent=useragent
            )
        except Exception as e:
            return render(request, "comments/error.html", {
                "message": e
            })

        response = redirect("/%s/%s/#comment%s" % (story.type, story.slug, comment.id))
        response.set_cookie("username", author, max_age=36000000)
        return response
    else:
        raise Http404()


def ip(request, ip):
    comments = Comment.objects.filter(ip=ip, is_visible=True).order_by("-created_at").select_related("story")[:50]
    for comment in comments:
        if comment.story.password:
            comment.text = "[комментарий в закрытом посте]"
    return render(request, "comments/list.html", {
        "comments": comments
    })
