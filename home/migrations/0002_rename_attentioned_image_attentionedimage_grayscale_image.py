# Generated by Django 3.2.25 on 2025-03-31 19:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attentionedimage',
            old_name='attentioned_image',
            new_name='grayscale_image',
        ),
    ]
