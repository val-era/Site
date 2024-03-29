# Generated by Django 4.1.2 on 2022-10-13 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(verbose_name='Айди пользователя')),
                ('data', models.DateTimeField(verbose_name='Дата сообщения')),
                ('text', models.TextField(verbose_name='Текст сообщения')),
                ('text_lit', models.CharField(max_length=15, verbose_name='Текст отображение')),
                ('user_info', models.TextField(verbose_name='О Человеке')),
                ('is_answer', models.BooleanField(verbose_name='Ответ')),
                ('img', models.TextField(verbose_name='Картинка')),
                ('is_read', models.BooleanField(verbose_name='Прочитанно')),
                ('is_lth_pnch', models.BooleanField(verbose_name='Переключение на консультанта')),
                ('type_msg', models.CharField(max_length=15, verbose_name='Тип сообщения')),
                ('msg_id', models.IntegerField(verbose_name='Айди сообщения')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(verbose_name='Айди пользователя')),
                ('img', models.ImageField(upload_to='img/', verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Фото',
                'verbose_name_plural': 'Фотографии',
            },
        ),
        migrations.CreateModel(
            name='ToJson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(verbose_name='Дата')),
                ('question', models.TextField(verbose_name='Вопрос для добавления в JSON')),
            ],
            options={
                'verbose_name': 'Вопрос для добавления',
                'verbose_name_plural': 'Вопросы для добавления',
            },
        ),
    ]
