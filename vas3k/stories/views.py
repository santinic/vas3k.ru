from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.signing import Signer, BadSignature
from django.db.models import F
from django.http import Http404
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from comments.models import Comment
from stories.models import Story

signer = Signer()


def index(request):
    top_blog = Story.objects.\
        filter(is_visible=True, type="blog").\
        order_by("-created_at").\
        first()

    top_gallery = Story.objects.\
        filter(is_visible=True, type="gallery").\
        order_by("-created_at").\
        first()

    top_featured = Story.objects.\
        filter(is_visible=True, is_featured=True).\
        exclude(id__in=(top_blog.id, top_gallery.id)).\
        order_by("?")[:2]

    stories = Story.objects.\
        filter(is_visible=True, type__in=("blog", "gallery", "events")).\
        order_by("-created_at").\
        select_related()

    paginator = Paginator(stories, settings.MAIN_PAGE_SIZE)
    try:
        stories = paginator.page(request.GET.get("page"))
    except PageNotAnInteger:
        stories = paginator.page(1)
    except EmptyPage:
        stories = paginator.page(paginator.num_pages)

    return render(request, "index.html", {
        "stories": stories,
        "top_blog": [top_blog],
        "top_gallery": [top_gallery],
        "top_featured": top_featured
    })


def story_list(request, story_type):
    items = Story.objects.\
        filter(type=story_type, is_visible=True).\
        order_by("-created_at").\
        select_related()

    if story_type in settings.STORIES_LIST_PAGE_SIZE:
        page_size = settings.STORIES_LIST_PAGE_SIZE[story_type]
    else:
        page_size = settings.STORIES_LIST_DEFAULT_PAGE_SIZE

    paginator = Paginator(items, page_size)
    try:
        stories = paginator.page(request.GET.get("page"))
    except PageNotAnInteger:
        stories = paginator.page(1)
    except EmptyPage:
        stories = paginator.page(paginator.num_pages)

    try:
        return render(request, "lists/%s.html" % story_type, {
            "stories": stories,
            "story_type": story_type
        })
    except TemplateDoesNotExist:
        raise Http404()


def story_show(request, story_type, story_slug):
    preview = request.GET.get("preview", False)
    try:
        if preview:
            story = Story.objects.get(type=story_type, slug=story_slug)
        else:
            story = Story.objects.get(type=story_type, slug=story_slug, is_visible=True)
    except Story.DoesNotExist:
        raise Http404()

    Story.objects.filter(id=story.id).update(views_count=F("views_count") + 1)

    comments = Comment.objects.filter(story=story, is_visible=True).order_by("id")

    if not story.password:
        is_allowed_to_read = True
    elif request.REQUEST.get("password"):
        is_allowed_to_read = request.REQUEST["password"] == story.password
    elif request.COOKIES.get("password"):
        try:
            is_allowed_to_read = signer.unsign(request.COOKIES["password"]) == story.password
        except BadSignature:
            is_allowed_to_read = False
    else:
        is_allowed_to_read = False

    try:
        response = render(request, "full/%s.html" % story_type, {
            "story": story,
            "comments": comments,
            "story_type": story_type,
            "is_allowed_to_read": is_allowed_to_read
        })
    except TemplateDoesNotExist:
        raise Http404()

    # one-time passwords for reading, WOW SUCH SECURITE :3
    if request.REQUEST.get("password"):
        response.set_cookie("password", signer.sign(request.REQUEST["password"]), httponly=True)

    return response
