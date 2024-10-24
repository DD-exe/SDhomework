# Generated by Django 5.1.2 on 2024-10-24 10:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='用户ID')),
                ('name', models.CharField(max_length=64, verbose_name='用户名')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
        ),
        migrations.CreateModel(
            name='SiteCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='分类名')),
                ('weight', models.IntegerField(blank=True, default=0, verbose_name='分类的权重')),
                ('description', models.TextField(blank=True, default='', max_length=200, verbose_name='分类的描述')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user', verbose_name='用户')),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类',
                'ordering': ['-weight', 'user', 'name'],
            },
        ),
        migrations.CreateModel(
            name='SiteNav',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='网站链接')),
                ('backup_url', models.URLField(blank=True, default='', verbose_name='网站备用链接')),
                ('name', models.CharField(blank=True, default='', max_length=64, verbose_name='网站名')),
                ('weight', models.IntegerField(blank=True, default=0, verbose_name='网站的权重')),
                ('description', models.TextField(blank=True, default='', max_length=200, verbose_name='网站的描述')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.sitecategory', verbose_name='网站的分类')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user', verbose_name='用户')),
            ],
            options={
                'verbose_name': '网站',
                'verbose_name_plural': '网站',
                'ordering': ['-weight', 'user', 'url'],
                'constraints': [models.UniqueConstraint(fields=('user', 'url'), name='unique_url_user')],
            },
        ),
        migrations.AddConstraint(
            model_name='sitecategory',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='unique_name_user'),
        ),
    ]
