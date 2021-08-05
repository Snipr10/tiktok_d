import pytz

from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta


# Create your models here.

class User(AbstractUser):
    def __str__(self):
        return self.id


class UpdateIndex(models.Model):
    created_date = models.DateField(default=datetime.min)
    owner_id = models.IntegerField()
    network_id = models.IntegerField(default=8)
    sphinx_id = models.CharField(max_length=127)

    class Meta:
        db_table = 'prsr_update_index'


class AllProxy(models.Model):
    ip = models.CharField(primary_key=True, max_length=256)
    port = models.IntegerField()
    login = models.CharField(max_length=256)
    proxy_password = models.CharField(max_length=256)
    last_used = models.DateTimeField(null=True, blank=True)
    last_used_y = models.DateTimeField(null=True, blank=True)
    failed = models.IntegerField()
    errors = models.IntegerField()
    foregin = models.IntegerField()
    banned_fb = models.IntegerField()
    banned_y = models.IntegerField()
    banned_tw = models.IntegerField()
    valid_untill = models.DateTimeField(default=datetime.now() + timedelta(days=5))
    timezone = models.CharField(max_length=256)
    v6 = models.IntegerField()
    last_modified = models.DateTimeField(null=True, blank=True)
    checking = models.BooleanField()

    class Meta:
        db_table = 'prsr_parser_proxy'


class Proxy(models.Model):
    id = models.IntegerField(primary_key=True)
    taken = models.BooleanField(default=True)
    last_used = models.DateTimeField(null=True, blank=True)
    errors = models.IntegerField(default=0)
    banned = models.BooleanField(default=False)

    class Meta:
        db_table = 'prsr_parser_proxy_tik'


class Sources(models.Model):
    uid = models.IntegerField(default=0)
    published = models.IntegerField(default=1)
    status = models.BooleanField(default=0)
    type = models.CharField(default="profiles", max_length=4096)
    retro = models.DateField(null=True, blank=True)
    retro_max = models.DateField(null=True, blank=True)
    networks = models.IntegerField(default=0)
    last_modify = models.DateTimeField(null=True, blank=True)
    links_modify = models.DateTimeField(null=True, blank=True)
    n2_modify = models.DateTimeField(null=True, blank=True)
    taken = models.BooleanField(default=1)
    linking = models.BooleanField(default=0)
    sources = models.IntegerField(default=15)
    profiles = models.IntegerField(default=15)
    stats_params = models.CharField(null=True, blank=True, max_length=4096)

    class Meta:
        db_table = 'prsr_parser_sources'


class SourcesItems(models.Model):
    source_id = models.IntegerField()
    network_id = models.IntegerField(default=0)
    type = models.IntegerField(default=1)
    data = models.CharField(default='nexta_live', max_length=4096)
    last_modified = models.DateTimeField(null=True, blank=True)
    reindexed = models.DateTimeField(null=True, blank=True)
    taken = models.BooleanField(default=0)
    reindexing = models.BooleanField(default=0)
    disabled = models.BooleanField(default=0)
    forced = models.BooleanField(default=0)

    class Meta:
        db_table = 'prsr_parser_source_items'


class Keyword(models.Model):
    id = models.IntegerField(primary_key=True)
    network_id = models.IntegerField(default=0)
    keyword = models.CharField(default='nexta_live', max_length=4096)
    enabled = models.IntegerField(default=0)
    created_date = models.DateTimeField(null=True, blank=True)
    modified_date = models.DateTimeField(null=True, blank=True)
    depth = models.DateField(null=True, blank=True)
    last_modified = models.DateTimeField(null=True, blank=True)
    taken = models.BooleanField(default=0)
    reindexing = models.BooleanField(default=0)
    forced = models.BooleanField(default=0)

    class Meta:
        db_table = 'prsr_parser_keywords'


class KeywordSource(models.Model):
    keyword_id = models.IntegerField(primary_key=True)
    source_id = models.IntegerField()

    class Meta:
        db_table = 'prsr_parser_source_keywords'


class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    music_id = models.IntegerField()
    created_date = models.DateTimeField(null=True, blank=True)
    found_date = models.DateField(auto_now_add=True)
    last_modified = models.DateTimeField(default=datetime(1, 1, 1, 0, 0, tzinfo=pytz.UTC), null=True, blank=True)
    content_hash = models.CharField(max_length=32, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    likes = models.IntegerField(default=0)
    reposts = models.IntegerField(default=0)
    viewed = models.IntegerField(default=0)

    class Meta:
        db_table = 'prsr_parser_tik_posts'


class PostContent(models.Model):
    id = models.IntegerField(primary_key=True)
    content = models.CharField(max_length=4096, null=True, blank=True)

    class Meta:
        db_table = 'prsr_parser_tik_posts_description'
