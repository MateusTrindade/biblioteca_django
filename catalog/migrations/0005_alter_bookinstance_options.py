# Generated by Django 3.2.3 on 2021-06-09 22:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_alter_bookinstance_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Set book as returned'), ('can_see_all_borrowed', 'See all borroed books'))},
        ),
    ]
