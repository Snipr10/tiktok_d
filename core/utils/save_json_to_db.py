import datetime

from core.models import Author, AuthorDescription, Music, Post, PostContent, Hashtag, PostHashtag
from core.utils.utils import get_sphinx_id, get_md5_text
from tiktok.settings import batch_size


def save(result_posts):
    print("save")
    posts = []
    posts_content = []
    music = []
    hashtags = []
    post_hashtag = []
    authors = []
    authors_description = []
    s = 0
    try:
        for post in result_posts:
            try:
                music_id = post.get('music', {}).get('id')
                if music_id =="":
                    music_id = None
                print("save post" + str(post['id']))
                url = f"https://www.tiktok.com/@{post['author']['uniqueId']}/video/{post['id']}"
                print(s)
                s += 1
                posts.append(Post(
                    id=post['id'],
                    user_id=post.get('author', {}).get('id'),
                    music_id=music_id,
                    created_date=datetime.datetime.fromtimestamp(post['createTime']),
                    url=url,
                    likes=post.get('stats', {}).get('diggCount'),
                    reposts=post.get('stats', {}).get('shareCount'),
                    viewed=post.get('stats', {}).get('playCount'),
                    sphinx_id=get_sphinx_id(url),
                    content_hash=get_md5_text(post.get('desc')),
                    comments=post.get('stats', {}).get('commentCount')
                )
                )
                # print("try save post")
                # try:
                #     print("try save post" + post['id'])
                #     music_id = post.get('music', {}).get('id')
                #     if music_id == "":
                #         music_id = None
                #     Post.objects.create(
                #         id=post['id'],
                #         user_id=post.get('author', {}).get('id'),
                #         music_id=music_id,
                #         created_date=datetime.datetime.fromtimestamp(post['createTime']),
                #         url=url,
                #         likes=post.get('stats', {}).get('diggCount'),
                #         reposts=post.get('stats', {}).get('shareCount'),
                #         viewed=post.get('stats', {}).get('playCount'),
                #         sphinx_id=get_sphinx_id(url),
                #         content_hash=get_md5_text(post.get('desc')),
                #         comments=post.get('stats', {}).get('commentCount')
                #     )
                # except Exception as e:
                #     print("try save post " + str(e))

                try:
                    print("save append " + str(post['id']))
                    posts_content.append(PostContent(id=post['id'], description=post.get('desc')))
                except Exception:
                    pass
                try:
                    if post['music']['id']:
                        music.append(
                            Music(id=post['music']['id'], author_nickname=post.get('music', {}).get('authorName'),
                                  title=post['music']['title'])
                        )
                except Exception:
                    pass
                try:
                    createTime = post["author"].get("createTime", None)
                except Exception:
                    createTime = None
                if createTime is not None:
                    try:
                        createTime = datetime.datetime.fromtimestamp(createTime)
                    except Exception:
                        pass
                try:
                    authors.append(
                        Author(
                            id=post["author"]["id"],
                            username=post.get("author", {}).get("uniqueId"),
                            nickname=post.get("author", {}).get("nickname"),
                            created_date=createTime,
                            url=f"https://www.tiktok.com/@{post.get('author', {}).get('uniqueId')}",
                            followers=post.get("authorStats", {}).get("followerCount"),
                            following=post.get("authorStats", {}).get("followingCount"),
                            likes=post.get("authorStats", {}).get("heartCount"),
                            digg=post.get("authorStats", {}).get("diggCount")
                        )
                    )
                except Exception:
                    pass
                try:
                    authors_description.append(
                        AuthorDescription(id=post["author"]["id"], description=post["author"]["signature"]))
                except Exception:
                    pass
                for hashtag in post.get("challenges", []):
                    try:
                        hashtags.append(Hashtag(id=hashtag["id"], name=hashtag['title']))
                        post_hashtag.append(PostHashtag(post_id=post['id'], hashtag_id=hashtag["id"]))
                    except Exception:
                        pass
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
    print(" Post.objects.bulk_create(posts, batch_size=batch_size, ignore_conflicts=True)")

    try:
        Post.objects.bulk_create(posts, batch_size=batch_size, ignore_conflicts=True)
    except Exception as e:
        print("save Post :" + str(e))
    try:
        PostContent.objects.bulk_create(posts_content, batch_size=batch_size, ignore_conflicts=True)
    except Exception as e:
        print("save PostContent :" + str(e))
    try:
        Music.objects.bulk_create(music, batch_size=batch_size, ignore_conflicts=True)
    except Exception as e:
        print("save Music :" + str(e))
    try:
        PostHashtag.objects.bulk_create(post_hashtag, batch_size=batch_size, ignore_conflicts=True)
    except Exception as e:
        print("save PostHashtag :" + str(e))
    try:
        Hashtag.objects.bulk_create(hashtags, batch_size=batch_size, ignore_conflicts=True)
    except Exception as e:
        print("save Hashtag :" + str(e))
    try:
        Author.objects.bulk_create(authors, batch_size=batch_size, ignore_conflicts=True)
    except Exception as e:
        print("save Author :" + str(e))
    try:
        AuthorDescription.objects.bulk_create(authors_description, batch_size=batch_size, ignore_conflicts=True)
    except Exception as e:
        print("save AuthorDescription :" + str(e))
