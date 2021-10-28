from django.db import models
from django.utils.translation import gettext as _


class Task(models.Model):

    title = models.CharField(max_length=100, verbose_name=_('Заголовок'))
    text = models.TextField(verbose_name=_('Описание'))
    deadline = models.DateTimeField(_('Срок исполнения'))
    is_done = models.BooleanField(default=False, verbose_name=_('Выполнено'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Задача')
        verbose_name_plural = _('Задачи')
