# Generated by Django 3.0.4 on 2020-11-14 17:18

from django.db import migrations
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0006_auto_20201111_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='DetVentas',
            name='user_creation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='user_creation', to=settings.AUTH_USER_MODEL),
        ),

    ]
