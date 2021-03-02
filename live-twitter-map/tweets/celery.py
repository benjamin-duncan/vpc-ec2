from __future__ import absolute_import, unicode_literals
import os
from tweets.consumers import TweetsConsumer
from asgiref.sync import async_to_sync
import channels.layers
from celery import Celery
import time
import json
#from django.db import models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
from tweets.redis import redis
from django.conf import settings
from django.core import serializers

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10, tweet_beat.s(), name='beat every 1 seconds')


@app.task
def tweet_beat(group=TweetsConsumer.GROUP, event='text_message'):
    from . import models
    import requests

    t = int(time.time())*1000
    max_tweet = models.Tweet.objects.filter(timestamp_ms__lt=t).order_by('-timestamp_ms')[0]
    max_id = max_tweet.id

    if redis.get('id')is None:
        redis.set('id', max_id)

    id = int(redis.get('id'))

    if not id:
        id = max_id
    print(f"Pre loop id: {id}")
    messages = models.Tweet.objects.filter(id__range=[id,max_id])
    channel_layer = channels.layers.get_channel_layer()
    if messages and max_id is not redis.get('max_id_chk'):
        id = max_id + 1
        print(f"start loop id: {id}")
        redis.set('id', id)
        redis.set('max_id_chk',max_id)

        for message in messages:


            try:      # Get HTML for embedding tweet
                url = "https://publish.twitter.com/oembed?url=https://twitter.com/i/status/" + str(message.tweet_id)
                response = requests.get(url)
                html = json.loads(response.text)['html']
                setattr(message,'html',html)    
            # message.save()
            # Send to consumers
            except:
                print(f"Message Error...\n {message}")
                continue
            async_to_sync(channel_layer.group_send)(group, {'type': event, 'message': serializers.serialize("json",[message,])})



    else:
        print(f"No Tweets in Range: {id} to {max_id}.\n Please Check if Database Stream is Live2")



    print(f"final id: {id}")
    print(f"redis id: {redis.get('id')}")