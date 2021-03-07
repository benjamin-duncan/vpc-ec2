# for drf
from rest_framework import serializers
from tweets.redis import redis
class StartupSerializer(serializers.ModelSerializer):
    def to_representation(self,instance):
        return {
            "id": instance.id,
            "text": instance.text,
            "tweet_id": instance.tweet_id,
            "lat": instance.lat,
            "lon": instance.lon,
            "timestamp_ms": instance.timestamp_ms,
            "html": redis.get(f"html_{instance.id}"),
        }