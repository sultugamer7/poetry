# Generated by Django 2.2.2 on 2019-07-10 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("poems", "0015_auto_20190710_0943")]

    operations = [
        migrations.AlterField(
            model_name="changepassword",
            name="date",
            field=models.DateTimeField(default="2019-07-10 09:44", editable=False),
        ),
        migrations.AlterField(
            model_name="review", name="headline", field=models.CharField(max_length=64)
        ),
    ]
