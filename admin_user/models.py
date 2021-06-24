from django.db import models


class Job(models.Model):
    job_title = models.CharField(max_length=50)