import asyncio

# Create your views here.
from core.models import Post
from core.scrapping.scrapers.hashtag import parsing_by_hashtag


def parsing(hashtag):
    url = f"https://www.tiktok.com/tag/{hashtag}"
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(asyncio.wait_for(parsing_by_hashtag(url), 3000))

    if not result.success:
        return False
    posts = []
    posts_conten = []
    for post in result.body:
        posts.append(Post(id=post['id']))

        # id = models.IntegerField()
        # user_id = models.IntegerField()
        # music_id = models.IntegerField()
        # created_date = models.DateTimeField(null=True, blank=True)
        # found_date = models.DateField(auto_now_add=True)
        # last_modified = models.DateTimeField(default=datetime(1, 1, 1, 0, 0, tzinfo=pytz.UTC), null=True, blank=True)
        # content_hash = models.CharField(max_length=32, null=True, blank=True)
        # url = models.CharField(max_length=255, null=True, blank=True)
        # likes = models.IntegerField(default=0)
        # reposts = models.IntegerField(default=0)
        # viewed = models.IntegerField(default=0)

    print("ok")
