# Generated by Django 2.2.2 on 2019-07-07 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("poems", "0011_auto_20190707_1201")]

    operations = [
        migrations.AlterField(
            model_name="changepassword",
            name="date",
            field=models.DateTimeField(default="2019-07-07 12:02", editable=False),
        )
    ]