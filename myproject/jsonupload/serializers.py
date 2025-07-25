from rest_framework import serializers

class JsonItemSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=49)
    date = serializers.DateTimeField(format="%Y-%m-%d_%H:%M", input_formats=["%Y-%m-%d_%H:%M"])
