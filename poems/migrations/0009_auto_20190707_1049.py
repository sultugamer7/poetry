# Generated by Django 2.2.2 on 2019-07-07 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("poems", "0008_auto_20190706_1910")]

    operations = [
        migrations.AlterField(
            model_name="changepassword",
            name="date",
            field=models.DateTimeField(default="2019-07-07 10:49", editable=False),
        ),
        migrations.AlterField(
            model_name="rating", name="poem", field=models.IntegerField()
        ),
        migrations.AlterField(
            model_name="rating",
            name="rating",
            field=models.DecimalField(
                choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
                decimal_places=1,
                max_digits=2,
            ),
        ),
    ]
