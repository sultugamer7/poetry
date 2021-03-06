# Generated by Django 2.2.2 on 2019-07-06 12:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("poems", "0005_auto_20190706_1027"),
    ]

    operations = [
        migrations.AddField(
            model_name="poem",
            name="average_rating",
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=3),
        ),
        migrations.AlterField(
            model_name="changepassword",
            name="date",
            field=models.DateTimeField(default="2019-07-06 18:03", editable=False),
        ),
        migrations.CreateModel(
            name="Rating",
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
                    "rating",
                    models.IntegerField(
                        choices=[
                            (1, "1"),
                            (2, "2"),
                            (3, "3"),
                            (4, "4"),
                            (5, "5"),
                            (6, "6"),
                            (7, "7"),
                            (8, "8"),
                            (9, "9"),
                            (10, "10"),
                        ]
                    ),
                ),
                (
                    "poem",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="poems.Poem"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
