from django.db import models
from django.shortcuts import reverse

from .school import School


class Debater(models.Model):
    first_name = models.CharField(max_length=32,
                                  blank=False)

    last_name = models.CharField(max_length=32,
                                 blank=False)

    school = models.ForeignKey(School,
                               on_delete=models.SET_NULL,
                               related_name='debaters',
                               blank=True,
                               null=True)

    # WHAT IF AFFILIATION CHANGES ?  Considered new debater

    NOVICE = 0
    VARSITY = 1
    STATUS = (
        (VARSITY, 'Varsity'),
        (NOVICE, 'Novice')
    )
    status = models.IntegerField(choices=STATUS,
                                 default=VARSITY)

    @property
    def name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('core:debater_detail', kwargs={'pk': self.id})

    def __str__(self):
        return self.name