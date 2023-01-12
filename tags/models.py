from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# The Tagged Item manger

class TaggedItemsManager(models.Manager): # inherits from the models.Manager class
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_from_model(obj_type)
        query_set = TaggedItem.objects.\
            select_related('tag').\
            filter(
                content_type = content_type, object_id = obj_id
            )
    # Returns a query set
        return query_set


# Create your models here.

class Tags(models.Model):
    label = models.CharField(max_length=255)

class TaggedItem(models.Model):
    # What tag is attached to what item
    tag = models.ForeignKey(Tags, on_delete =models.CASCADE)
    # We want to make this tag generic and not limited to product or store so for that we need two information
    # 1. Type of object -> Product, audio, video etc etc.
    # 2. ID of the object 
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey()
    
    # defining object of the TaggedItemManager class
    objects = TaggedItemsManager()

