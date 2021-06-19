# Generated by Django 3.2.3 on 2021-05-26 01:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lenguage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leng', models.CharField(help_text='Insira a lingua do livro', max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='lenguage',
            field=models.ForeignKey(help_text='Selecione uma lingua para esse livro', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.lenguage'),
        ),
    ]