from flask import render_template, request
from app.badape import blueprint
from dotenv import load_dotenv
import os
import requests

load_dotenv()

REDDIT_CLIENT_ID = os.getenv('reddit_client_id')
REDDIT_CLIENT_SECRET = os.getenv('reddit_client_secret')
REDDIT_USER_AGENT = os.getenv('reddit_user_agent', 'thc-lab-badape/1.0')
TARGET_SUBREDDIT = 'Superstonk'


def get_reddit_token():
    auth = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)
    data = {'grant_type': 'client_credentials'}
    headers = {'User-Agent': REDDIT_USER_AGENT}
    resp = requests.post('https://www.reddit.com/api/v1/access_token',
                         auth=auth, data=data, headers=headers)
    resp.raise_for_status()
    return resp.json()['access_token']


def get_shillpoints(username):
    token = get_reddit_token()
    headers = {
        'Authorization': f'bearer {token}',
        'User-Agent': REDDIT_USER_AGENT,
    }

    post_karma = 0
    comment_karma = 0
    post_count = 0
    comment_count = 0

    for kind in ('submitted', 'comments'):
        after = None
        fetched = 0
        while fetched < 1000:
            params = {'limit': 100, 'after': after} if after else {'limit': 100}
            resp = requests.get(
                f'https://oauth.reddit.com/user/{username}/{kind}',
                headers=headers, params=params
            )
            if resp.status_code == 404:
                return None, None, None, None, 'User not found.'
            resp.raise_for_status()
            data = resp.json()['data']
            items = data['children']
            if not items:
                break
            for item in items:
                d = item['data']
                if d.get('subreddit', '').lower() == TARGET_SUBREDDIT.lower():
                    if kind == 'submitted':
                        post_karma += d.get('score', 0)
                        post_count += 1
                    else:
                        comment_karma += d.get('score', 0)
                        comment_count += 1
            after = data.get('after')
            fetched += len(items)
            if not after:
                break

    return post_karma, comment_karma, post_count, comment_count, None


@blueprint.route('/badape.html', methods=('GET', 'POST'))
def badape():
    if request.method == 'POST':
        username = request.form.get('Name', '').strip()
        if not username:
            return render_template('badape/badape.html', error='Enter a username.')

        try:
            post_karma, comment_karma, post_count, comment_count, error = get_shillpoints(username)
        except Exception as e:
            return render_template('badape/badape.html', error=f'Reddit API error: {e}')

        if error:
            return render_template('badape/badape.html', error=error)

        total = post_karma + comment_karma
        response = f'u/{username} has {total:,} ShillPoints™ on r/{TARGET_SUBREDDIT}'
        melt_posts = f'Posts: {post_count} ({post_karma:,} karma)'
        melt_comments = f'Comments: {comment_count} ({comment_karma:,} karma)'

        return render_template('badape/badape.html',
                               response=response,
                               meltPosts=melt_posts,
                               meltComments=melt_comments)
    else:
        return render_template('badape/badape.html')
