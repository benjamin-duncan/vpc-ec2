from django.db import models

# Create your models here.



class Tweet(models.Model):
    id = models.AutoField(primary_key=True)
    text =  models.TextField()
    tweet_id = models.BigIntegerField()
    lat = models.FloatField()
    lon = models.FloatField()
    timestamp_ms = models.BigIntegerField()
    html = models.TextField()

    class Meta:
        db_table = "tweets" 