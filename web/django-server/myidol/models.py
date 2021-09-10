from django.db import models
from django.contrib.postgres.fields import ArrayField
import numpy as np
import json
# Create your models here.
class ImageInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(blank=False, max_length=30, null=False)
    file_name = models.CharField(blank=False, max_length=30, null=False)
    format = models.CharField(blank=False, max_length=10, null=False)
    gender = models.CharField(blank=False, max_length=10, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_file_name(self):
        return f'{self.file_name}.{self.format}'
    
class ClusterInfo(models.Model):
    image_id = models.OneToOneField(ImageInfo, on_delete=models.CASCADE, verbose_name="image_id")
    cluster = models.CharField(blank=False, max_length=20, null=False)
    # subject__startswith

class EmbeddingInfo(models.Model):
    image_id = models.OneToOneField(ImageInfo, on_delete=models.CASCADE, verbose_name='image_id')
    embedding= ArrayField(
        models.FloatField(blank=False, null=False),
        128, null=False, default=0
    )
    def get_embedding(self):
        return json.loads(self.embedding)