# Generated by Django 2.2.2 on 2019-07-06 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("poems", "0007_auto_20190706_1910")]

    operations = [
        migrations.AlterField(
            model_name="poem",
            name="average_rating",
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=2),
        )
    ]
