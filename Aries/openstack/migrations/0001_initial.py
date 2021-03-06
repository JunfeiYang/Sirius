# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-01 15:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=100, verbose_name='\u9879\u76ee\u540d')),
                ('username', models.CharField(max_length=50, verbose_name='\u8d1f\u8d23\u4eba')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='\u53d1\u8868\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
        ),
        migrations.CreateModel(
            name='ModeList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameuser', models.CharField(max_length=30, verbose_name='\u63d2\u4ef6\u540d\u79f0')),
                ('urlname', models.CharField(max_length=50, verbose_name='URL')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='\u53d1\u8868\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('mlistm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.List')),
            ],
        ),
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='\u6807\u9898')),
                ('hostname', models.CharField(max_length=50, verbose_name='\u9879\u76ee\u540d')),
                ('username', models.CharField(max_length=50, verbose_name='\u7533\u8bf7\u4eba')),
                ('email', models.CharField(max_length=50, verbose_name='\u90ae\u7bb1\u5730\u5740')),
                ('status', models.IntegerField(verbose_name='\u72b6\u6001')),
                ('data', models.TextField(verbose_name='\u8bf4\u660e')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='\u53d1\u8868\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('User_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StorData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(max_length=20, verbose_name='\u5f55\u5165\u65f6\u95f4')),
                ('username', models.CharField(max_length=50, verbose_name='\u7ef4\u62a4\u4eba')),
                ('title', models.CharField(max_length=20, verbose_name='\u6807\u9898')),
                ('date_time', models.CharField(max_length=20, verbose_name='\u7ef4\u62a4\u65f6\u95f4')),
                ('data', models.TextField(verbose_name='\u7ef4\u62a4\u8bb0\u5f55')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='\u53d1\u8868\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('data_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.List')),
            ],
        ),
    ]
