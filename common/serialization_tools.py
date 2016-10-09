'''
Taken http://stackoverflow.com/questions/36789597/why-doesnt-django-serialize-filefield-to-the-file-url-when-using-aws-s3
Resolves the serialization without full url issue
'''
from django.core import serializers

JSONSerializer = serializers.get_serializer("json")

class JSONWithURLSerializer(JSONSerializer):

    def handle_field(self, obj, field):
        value = field.value_from_object(obj)

        if value and hasattr(value, 'url'):
            self._current[field.name] = value.url
        else:
            return super(JSONWithURLSerializer, self).handle_field(obj, field)