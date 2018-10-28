# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Transaction(models.Model):
    trans_id = models.CharField(max_length=512)
    sender = models.CharField(max_length=512)
    page_name = models.CharField(max_length=512)
    last_hash = models.CharField(max_length=512)
    timestamp = models.CharField(max_length=512)
    page_content = models.CharField(max_length=2000000, null=True)
    signature = models.CharField(max_length=512, null=True)

    def __unicode__(self):
        return self.trans_id
