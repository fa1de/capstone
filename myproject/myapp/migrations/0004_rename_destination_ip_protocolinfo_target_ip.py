# Generated by Django 5.0.6 on 2024-06-08 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_rename_protocol_protocolinfo_protocol_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='protocolinfo',
            old_name='destination_ip',
            new_name='target_ip',
        ),
    ]
