# Generated by Django 3.0.7 on 2020-06-28 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0016_auto_20200628_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmark', to='mainApp.Post'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='mainApp.Post'),
        ),
        migrations.AlterField(
            model_name='like',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like', to='mainApp.Post'),
        ),
    ]