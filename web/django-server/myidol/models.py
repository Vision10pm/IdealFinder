from django.db import models

# Create your models here.
class ImageInfo(models.Model):
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
