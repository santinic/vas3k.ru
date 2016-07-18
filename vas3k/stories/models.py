from collections import defaultdict
from django.db import models


class Story(models.Model):
    slug = models.CharField(max_length=32, db_index=True)
    type = models.CharField(max_length=16, db_index=True)
    icon = models.CharField(max_length=32, null=True, blank=True)
    author = models.CharField(max_length=32)
    title = models.CharField(max_length=256, null=True, blank=True)
    subtitle = models.CharField(max_length=256, null=True, blank=True)
    image = models.CharField(max_length=128, null=True, blank=True)
    image_preview = models.CharField(max_length=128, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    data = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField("stories.Category", null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    url = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    comments_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    is_commentable = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    hidden_blocks = models.TextField(null=True, blank=True)
    password = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        db_table = "stories"
        ordering = ("-created_at",)
        unique_together = ("slug", "type")

    def __init__(self, *args, **kwargs):
        super(Story, self).__init__(*args, **kwargs)
        self._cached_data = {}

    @models.permalink
    def get_absolute_url(self):
        return "story_show", (), {"story_type": self.type, "story_slug": self.slug}

    def reading_time(self):
        return int(self.text.count(" ") / 1.7 / 60)

    def size_x(self):
        size_x = 400
        if self.data and "cell_width" in self.data:
            if self.data["cell_width"] > 1:
                size_x = size_x * self.data["cell_width"] + 30 * (self.data["cell_width"] - 1)
        return size_x

    def fake_image(self):
        if self.type == "events" and not self.image:
            return Memory.objects.\
                filter(story=self, type__in=("picsmall", "picmedium", "picbig", "picsquare")).\
                order_by("created_at").\
                first().\
                image
        return None

    def memories_feed(self):
        memories = list(Memory.objects.filter(story=self).order_by("created_at"))
        feed = []
        already_appended = set()

        hidden_blocks = []
        if self.hidden_blocks:
            hidden_blocks = [b.strip() for b in self.hidden_blocks.split(",")]

        if "video" not in hidden_blocks:
            # видео
            block = {
                "type": "video",
                "memories": []
            }
            for memory in memories:
                if memory.type == "video":
                    block["memories"].append(memory)
                    already_appended |= {memory.id}

            if block["memories"]:
                feed.append(block)

        if "top" not in hidden_blocks:
            # верхний блок
            block = {
                "type": "top",
                "memories": defaultdict(list)
            }
            for memory in memories:
                if memory.type == "picsquare":
                    block["memories"][memory.type].append(memory)
                    already_appended |= {memory.id}
                elif memory.type == "text":
                    if len(block["memories"]["text"]) <= 8:
                        block["memories"][memory.type].append(memory)
                        already_appended |= {memory.id}

            if block["memories"]:
                feed.append(block)

        if "map" not in hidden_blocks:
            # блок с картой
            block = {
                "type": "map",
                "memories": []
            }
            for memory in memories:
                if memory.type in ("picsmall", "picmedium") and memory.latitude and memory.longitude:
                    block["latitude"] = memory.latitude
                    block["longitude"] = memory.longitude
                    block["memories"].append(memory)
                    already_appended |= {memory.id}
                if len(block["memories"]) >= 2:
                    break

            if block["memories"]:
                feed.append(block)

        if "timeline" not in hidden_blocks:
            # блоки таймлайны + большие
            block = {
                "type": "timeline",
                "memories": []
            }
            for memory in memories:
                if memory.id not in already_appended:
                    if memory.type in ("picbig", "textbig", "picnormal"):
                        if block["memories"]:
                            feed.append(block)
                        block = {
                            "type": memory.type,
                            "memories": [memory]
                        }
                        feed.append(block)
                        block = {
                            "type": "timeline",
                            "memories": []
                        }
                    else:
                        block["memories"].append(memory)

            feed.append(block)

        return feed


class Category(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        db_table = "categories"


class Memory(models.Model):
    slug = models.CharField(max_length=32, db_index=True)
    type = models.CharField(max_length=16, db_index=True)
    story = models.ForeignKey("stories.Story", null=True, related_name="memories")
    icon = models.CharField(max_length=32, null=True, blank=True)
    title = models.CharField(max_length=256, null=True, blank=True)
    subtitle = models.CharField(max_length=256, null=True, blank=True)
    image = models.CharField(max_length=128, null=True, blank=True)
    image_preview = models.CharField(max_length=128, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    data = models.TextField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    url = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=True)

    class Meta:
        db_table = "memories"
