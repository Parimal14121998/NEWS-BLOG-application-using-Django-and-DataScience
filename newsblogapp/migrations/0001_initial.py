# Generated by Django 3.2 on 2022-12-25 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='newsblogmodel',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('genre', models.TextField()),
                ('crdt', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]