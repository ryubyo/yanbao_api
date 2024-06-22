# Generated by Django 5.0.1 on 2024-01-20 12:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appaccounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="LogModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("username", models.CharField(max_length=50, verbose_name="用户名")),
                ("app", models.CharField(max_length=50, null=True, verbose_name="应用名")),
                (
                    "event",
                    models.CharField(max_length=50, null=True, verbose_name="事件"),
                ),
                ("msg", models.CharField(max_length=200, null=True, verbose_name="详情")),
                (
                    "createtime",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
            ],
            options={
                "verbose_name": "log",
                "verbose_name_plural": "log",
                "ordering": ("id",),
            },
        ),
        migrations.RenameField(
            model_name="accountmodel",
            old_name="ende",
            new_name="end",
        ),
    ]