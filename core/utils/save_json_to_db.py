import datetime

from core.models import Author, AuthorDescription, Music, Post, PostContent, Hashtag, PostHashtag
from core.scrapping.scrapers.hashtag import parsing_by_hashtag
from core.utils.utils import get_sphinx_id, get_md5_text
from tiktok.settings import batch_size


def save(result_posts):
    posts = []
    posts_content = []
    music = []
    hashtags = []
    post_hashtag = []
    authors = []
    authors_description = []
    for post in result_posts:
        url = f"https://www.tiktok.com/@{post['author']['uniqueId']}/video/{post['id']}"
        posts.append(Post(
            id=post['id'],
            user_id=post['author']['id'],
            music_id=post['music']['id'],
            created_date=datetime.datetime.fromtimestamp(post['createTime']),
            url=url,
            likes=post['stats']['diggCount'],
            reposts=post['stats']['shareCount'],
            viewed=post['stats']['playCount'],
            sphinx_id=get_sphinx_id(url),
            content_hash=get_md5_text(post['desc']),
            comments=post['stats']['commentCount']
            )
        )
        posts_content.append(PostContent(id=post['id'], content=post['desc']))
        music.append(
            Music(id=post['music']['id'], author_nickname=post['music']['authorName'], title=post['music']['title'])
        )
        createTime = post["author"].get("createTime", None)
        if createTime is not None:
            try:
                createTime = datetime.datetime.fromtimestamp(createTime)
            except Exception:
                pass
        authors.append(

                Author(
                    id=post["author"]["id"],
                    username=post["author"]["uniqueId"],
                    nickname=post["author"]["nickname"],
                    created_date=createTime,
                    url=f"https://www.tiktok.com/@{post['author']['uniqueId']}",
                    followers=post["authorStats"]["followerCount"],
                    following=post["authorStats"]["followingCount"],
                    likes=post["authorStats"]["heartCount"],
                    digg=post["authorStats"]["diggCount"]
                )
            )

        authors_description.append(AuthorDescription(id=post["author"]["id"], description=post["author"]["signature"]))
        for hashtag in post.get("challenges", []):
            hashtags.append(Hashtag(id=hashtag["id"], name=hashtag['title']))
            post_hashtag.append(PostHashtag(post_id=post['id'], hashtag_id=hashtag["id"]))

    Post.objects.bulk_create(posts, batch_size=batch_size, ignore_conflicts=True)
    PostContent.objects.bulk_create(posts_content, batch_size=batch_size, ignore_conflicts=True)
    Music.objects.bulk_create(music, batch_size=batch_size, ignore_conflicts=True)
    PostHashtag.objects.bulk_create(post_hashtag, batch_size=batch_size, ignore_conflicts=True)
    Hashtag.objects.bulk_create(hashtags, batch_size=batch_size, ignore_conflicts=True)
    Author.objects.bulk_create(authors, batch_size=batch_size, ignore_conflicts=True)
    AuthorDescription.objects.bulk_create(authors_description, batch_size=batch_size, ignore_conflicts=True)