# Generated by Django 2.2.2 on 2019-07-11 07:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("poems", "0018_auto_20190711_1106"),
    ]

    operations = [
        migrations.RenameField(
            model_name="poem", old_name="created_at", new_name="date"
        ),
        migrations.AlterField(
            model_name="changepassword",
            name="date",
            field=models.DateTimeField(default="2019-07-11 12:52", editable=False),
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "notification_type",
                    models.CharField(
                        choices=[("Rate", "Rate"), ("Review", "Review")], max_length=64
                    ),
                ),
                ("notification_data", models.TextField()),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "poem",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="poems.Poem"
                    ),
                ),
                (
                    "receiver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="receiver",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sender",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
