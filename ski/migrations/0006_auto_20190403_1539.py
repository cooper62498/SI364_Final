# Generated by Django 2.1.5 on 2019-04-03 15:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ski', '0005_auto_20190403_0106'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mountain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ski.Mountain')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='mountain',
            name='favorites',
            field=models.ManyToManyField(related_name='favorite_mountain', through='ski.Fav', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='fav',
            unique_together={('mountain', 'user')},
        ),
    ]