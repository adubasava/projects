# Generated by Django 5.0 on 2023-12-25 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_course_group_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='rating',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
