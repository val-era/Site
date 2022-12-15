from django.db import models


class Message(models.Model):
    user_id = models.BigIntegerField('Айди пользователя')
    data = models.DateTimeField('Дата сообщения')
    text = models.TextField('Текст сообщения')
    text_lit = models.CharField('Текст отображение', max_length=15)
    user_info = models.TextField('О Человеке')
    is_answer = models.BooleanField('Ответ')
    img = models.TextField('Картинка')
    is_read = models.BooleanField('Прочитанно')
    is_lth_pnch = models.BooleanField('Переключение на консультанта')
    type_msg = models.CharField('Тип сообщения', max_length=15)
    msg_id = models.IntegerField('Айди сообщения')

    def __str__(self):
        return self.user_info

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Photo(models.Model):
    user_id = models.BigIntegerField('Айди пользователя')
    img = models.ImageField('Картинка', upload_to='img/')

    def __str__(self):
        return str(self.user_id)

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фотографии"


class ToJson(models.Model):
    data = models.TextField('Дата')
    question = models.TextField('Вопрос для добавления в JSON')

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Вопрос для добавления"
        verbose_name_plural = "Вопросы для добавления"
