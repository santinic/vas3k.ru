from django.conf import settings
from django.db import models


class Comment(models.Model):
    story = models.ForeignKey("stories.Story", related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = models.CharField(max_length=32)
    author = models.CharField(max_length=32)
    text = models.TextField(null=True, blank=True)
    ip = models.IPAddressField()
    useragent = models.CharField(max_length=256)
    is_visible = models.BooleanField(default=True)

    class Meta:
        db_table = "comments"

    def get_absolute_url(self):
        return "/%s/%s/#comment%s" % (self.story.type, self.story.slug, self.id)

    @staticmethod
    def generate_avatar(author, story_id, ip):
        if author.lower() in settings.CUSTOM_AVATARS:
            return "%s.png" % author.lower()

        try:
            hash = (sum([int(l) for l in ip if l.isdigit()]) + int(story_id)) % 21
            return "%s.png" % hash
        except ValueError:
            return "1.png"
