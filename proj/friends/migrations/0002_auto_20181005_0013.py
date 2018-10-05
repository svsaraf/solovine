# Generated by Django 2.1 on 2018-10-05 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='circleentry',
            name='circle',
            field=models.CharField(choices=[('a', 'alpha'), ('b', 'bravo'), ('c', 'charlie'), ('d', 'delta'), ('e', 'echo'), ('f', 'foxtrot'), ('g', 'golf'), ('h', 'hotel'), ('i', 'india'), ('j', 'juliett'), ('z', 'zulu')], default='a', max_length=1),
        ),
    ]
