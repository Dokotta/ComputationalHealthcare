from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import ArrayField
from chlib.entity.enums import CTYPE


class Dataset(models.Model):
    identifier = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    linked = models.BooleanField(default=False)
    base_dir = models.CharField(max_length=200)
    states = ArrayField(models.CharField(max_length=10))
    years = ArrayField(models.IntegerField())
    patients_count = models.IntegerField(default=0)
    linked_count = models.IntegerField(default=0)
    unlinked_count = models.IntegerField(default=0)
    aggregate_visits = models.BooleanField(default=False)
    aggregate_readmits = models.BooleanField(default=False)
    aggregate_revisits = models.BooleanField(default=False)
    aggregate_patients = models.BooleanField(default=False)


class SCount(models.Model):
    dataset = models.ForeignKey(Dataset)
    state = models.CharField(max_length=10)
    patients_count = models.IntegerField(default=0)
    linked_count = models.IntegerField(default=0)
    unlinked_count = models.IntegerField(default=0)


class STCount(models.Model):
    dataset = models.ForeignKey(Dataset)
    state = models.CharField(max_length=10)
    visit_type = models.PositiveSmallIntegerField()
    linked = models.BooleanField(default=False)
    count = models.IntegerField(default=0)


class SYTCount(models.Model):
    dataset = models.ForeignKey(Dataset)
    state = models.CharField(max_length=10)
    year = models.IntegerField()
    linked = models.BooleanField(default=False)
    visit_type = models.PositiveSmallIntegerField()
    count = models.IntegerField(default=0)


class Code(models.Model):
    code = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    indexed = models.BooleanField(default=False)
    dataset = models.ForeignKey(Dataset)
    code_type = models.CharField(max_length=5,default="")


class CodeCount(models.Model):
    dataset_identifier = models.CharField(max_length=10)
    code = models.CharField(max_length=50)
    code_type = models.CharField(max_length=5)
    count = models.IntegerField(default=0)
    visit_type = models.PositiveSmallIntegerField()
    state = models.CharField(max_length=10)
    year = models.IntegerField()
    linked = models.BooleanField(default=False)


class TextSearch(models.Model):
    code = models.CharField(max_length=30)
    description = models.TextField()
    datasets_count = models.IntegerField()
    code_type = models.CharField(max_length=5,default="")