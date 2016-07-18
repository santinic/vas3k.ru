from django.contrib.syndication.views import Feed
from comments.models import Comment
from stories.models import Story
from stories.templatetags.text_filters import nl2br2, resized_image


class FullFeed(Feed):
    title = "vas3k.ru full"
    link = "/rss/"
    description = "Всё с vas3k.ru"

    def items(self):
        items = Story.objects.\
            filter(is_visible=True, type__in=("blog", "gallery", "events")).\
            order_by("-created_at").\
            select_related()[:20]
        return items

    def item_title(self, item):
        return item.title

    def author_name(self):
        return "vas3k"

    def item_copyright(self):
        return "vas3k.ru"

    def item_pubdate(self, item):
        return item.created_at

    def item_description(self, item):
        if item.password:
            pic = ""
            if item.image:
                pic = "<a href='http://vas3k.ru/{}/{}/'><img src='{}'></a><br/>".format(
                    item.type, item.slug, resized_image(item.image, 900)
                )
            return pic

        if item.type == "blog":
            pic = ""
            if item.image:
                pic = "<a href='http://vas3k.ru/blog/{}/'><img src='{}'></a><br/>".format(
                    item.slug, resized_image(item.image, 900)
                )
            return pic + nl2br2(item.text)
        elif item.type == "gallery":
            pic = ""
            if item.image:
                pic = "<a href='http://vas3k.ru/gallery/{}/'><img src='{}'></a><br/>".format(
                    item.slug, resized_image(item.image, 900)
                )
            return pic + nl2br2(item.text)
        elif item.type == "events":
            pic = ""
            if item.image:
                pic = "<a href='http://vas3k.ru/events/{}/'><img src='{}'></a><br/>".format(
                    item.slug, resized_image(item.image, 900)
                )
            return pic + nl2br2(item.text)

        return nl2br2(item.text)


class BlogFeed(Feed):
    title = "vas3k.ru blog"
    link = "/rss/blog/"
    description = "Блог vas3k.ru"

    def items(self):
        return Story.objects.\
            filter(is_visible=True, type="blog").\
            order_by("-created_at").\
            select_related()[:20]

    def item_title(self, item):
        return item.title

    def author_name(self):
        return "vas3k"

    def item_copyright(self):
        return "vas3k.ru"

    def item_pubdate(self, item):
        return item.created_at

    def item_description(self, item):
        if item.password:
            pic = ""
            if item.image:
                pic = "<a href='http://vas3k.ru/{}/{}/'><img src='{}'></a><br/>".format(
                    item.type, item.slug, resized_image(item.image, 900)
                )
            return pic

        pic = ""
        if item.image:
            pic = "<a href='http://vas3k.ru/blog/{}/'><img src='{}'></a><br/>".format(
                item.slug, resized_image(item.image, 900)
            )

        return pic + nl2br2(item.text[:5000])


class GalleryFeed(Feed):
    title = "vas3k.ru gallery"
    link = "/rss/gallery/"
    description = "Галерея vas3k.ru"

    def items(self):
        return Story.objects.\
            filter(is_visible=True, type="gallery").\
            order_by("-created_at").\
            select_related()[:20]

    def item_title(self, item):
        return item.title

    def author_name(self):
        return "vas3k"

    def item_copyright(self):
        return "vas3k.ru"

    def item_pubdate(self, item):
        return item.created_at

    def item_description(self, item):
        if item.password:
            pic = ""
            if item.image:
                pic = "<a href='http://vas3k.ru/{}/{}/'><img src='{}'></a><br/>".format(
                    item.type, item.slug, resized_image(item.image, 900)
                )
            return pic

        pic = ""
        if item.image:
            pic = "<a href='http://vas3k.ru/gallery/{}/'><img src='{}'></a><br/>".format(
                item.slug, resized_image(item.image, 900)
            )

        return pic + nl2br2(item.text[:5000])


class CommentFeed(Feed):
    title = "vas3k.ru comments"
    link = "/rss/comments/"
    description = "Комментарии vas3k.ru"

    def items(self):
        return Comment.objects.\
            filter(is_visible=True, story__password__isnull=True).\
            order_by("-created_at").\
            select_related("story")[:20]

    def item_title(self, item):
        return "Комментарий %s" % item.author

    def author_name(self):
        return "vas3k"

    def item_copyright(self):
        return "vas3k.ru"

    def item_pubdate(self, item):
        return item.created_at

    def item_description(self, item):
        return nl2br2(item.text[:5000])
