from django.db import models
from django.shortcuts import reverse
from django.conf import settings

from core.utils.points import (
    team_points_for_size,
    speaker_points_for_size,
    novice_points_for_size
)
from core.models.school import School


class Tournament(models.Model):
    name = models.CharField(max_length=128,
                            blank=False)

    num_rounds = models.IntegerField(default=5,
                                     verbose_name='Rounds')

    host = models.ForeignKey(School,
                             on_delete=models.SET_NULL,
                             related_name='hosted_tournaments',
                             blank=True,
                             null=True)

    season = models.CharField(choices=settings.SEASONS,
                              default=settings.DEFAULT_SEASON,
                              max_length=16)

    num_teams = models.IntegerField(null=False,
                                    verbose_name='Teams',
                                    default=-1)
    num_novice_teams = models.IntegerField(null=False,
                                           verbose_name='Novice Teams',
                                           default=-1)

    num_debaters = models.IntegerField(null=False,
                                       verbose_name='Debaters',
                                       default=-1)
    num_novice_debaters = models.IntegerField(null=False,
                                              verbose_name='Novice Debaters',
                                              default=-1)

    date = models.DateField(blank=False)

    qual = models.BooleanField(default=True,
                               verbose_name='QUAL',
                               help_text='Does this tournament give qual points?')
    noty = models.BooleanField(default=True,
                               verbose_name='NOTY',
                               help_text='Does this tournament give NOTY points?')
    soty = models.BooleanField(default=True,
                               verbose_name='SOTY',
                               help_text='Does this tournament give SOTY points?')
    toty = models.BooleanField(default=True,
                               verbose_name='TOTY',
                               help_text='Does this tournament give TOTY points?')

    autoqual_bar = models.IntegerField(default=0,
                                       verbose_name='Autoqual Bar',
                                       help_text='If this tournament gives autoquals, this value represents the highest place that receivs the autoqual')

    NONE = 0
    ELECTIONS = 1
    MEETING = 2
    GM = 3

    NAME_SUFFIXES = (
        (NONE, ''),
        (ELECTIONS, ' (Elections)'),
        (MEETING, ' (APDA Meeting)'),
        (GM, ' (Gender Minority)'),
    )

    name_suffix = models.IntegerField(default=NONE,
                                      choices=NAME_SUFFIXES)

    # REPEATED TO PREVENT CIRCULAR IMPORTS
    POINTS = 0
    BRANDEIS = 1
    YALE = 2
    NORTHAMS = 3
    EXPANSION = 4
    WORLDS = 5
    NAUDC = 6
    PROAMS = 7
    NATIONALS = 8
    NOVICE = 9

    QUAL_TYPES = (
        (POINTS, 'Regular (Points)'),
        (BRANDEIS, 'Brandeis IV'),
        (YALE, 'Yale IV'),
        (NORTHAMS, 'NorthAms'),
        (EXPANSION, 'Expansion'),
        (WORLDS, 'Worlds'),
        (NAUDC, 'NAUDC'),
        (PROAMS, 'ProAms'),
        (NATIONALS, 'Nationals'),
        (NOVICE, 'Novice'),
    )

    TOURNAMENT_TYPES = {
        POINTS: {
            'toty': True,
            'soty': True,
            'noty': True,
            'qual': True,
        },
        BRANDEIS: {
            'toty': False,
            'soty': False,
            'noty': False,
            'qual': False,
            'autoqual_bar': 4,
            'suffix': ' IV',
        },
        YALE: {
            'toty': False,
            'soty': False,
            'noty': False,
            'qual': False,
            'autoqual_bar': 8,
            'suffix': ' IV',
        },
        NORTHAMS: {
            'toty': False,
            'soty': False,
            'noty': False,
            'qual': False,
            'autoqual_bar': 8,
            'suffix': ' NorthAms',
        },
        EXPANSION: {
            'toty': True,
            'soty': True,
            'noty': True,
            'qual': True,
            'autoqual_bar': 1,
            'suffix': ' (Expansion)'
        },
        WORLDS: {
            'toty': False,
            'soty': False,
            'noty': False,
            'qual': False,
            'autoqual_bar': 48,
            'suffix': ' (Worlds)',
        },
        NAUDC: {
            'toty': False,
            'soty': False,
            'noty': False,
            'qual': False,
            'autoqual_bar': 8,
            'suffix': ' NAUDC'
        },
        PROAMS: {
            'toty': False,
            'soty': True,
            'noty': False,
            'qual': False,
            'suffix': ' ProAms'
        },
        NATIONALS: {
            'toty': False,
            'soty': False,
            'noty': False,
            'qual': False,
            'suffix': ' Nationals'
        },
        NOVICE: {
            'toty': False,
            'soty': False,
            'noty': False,
            'qual': False,
            'suffix': ' Novice'
        }
    }
    qual_type = models.IntegerField(choices=QUAL_TYPES,
                                    default=POINTS,
                                    verbose_name='Tournament Type')


    def get_qualled(self, place):
        if self.qual_bar < 1:
            return False

        return place <= self.qual_bar
        
        
    def get_qual_points(self, place):
        if not self.qual:
            return 0

        return team_points_for_size(self.num_teams,
                                    place)


    def get_toty_points(self, place):
        if not self.toty:
            return 0

        return self.get_qual_points(place)


    def get_soty_points(self, place):
        if not self.soty:
            return 0

        return speaker_points_for_size(self.num_teams,
                                       place)


    def get_noty_points(self, place):
        if not self.noty:
            return 0

        return novice_points_for_size(self.num_novice_debaters,
                                      place)

    def get_absolute_url(self):
        return reverse('core:tournament_detail', kwargs={'pk': self.id})


    def __str__(self):
        return self.name

    @property
    def display(self):
        return self.name.split(' (')[0]

    def save(self, *args, **kwargs):
        previous_tournaments = Tournament.objects.filter(
            season=self.season
        ).filter(
            host=self.host
        ).filter(
            qual_type=self.qual_type
        ).filter(
            date__lt=self.date
        ).exclude(
            id=self.id
        ).count()
        
        suffix = ''
        
        if self.qual_type == self.POINTS and previous_tournaments:
            suffix += ' '
            suffix += 'I' * (previous_tournaments + 1)
        elif self.qual_type in self.TOURNAMENT_TYPES and not self.qual_type == self.POINTS:
            suffix += self.TOURNAMENT_TYPES[self.qual_type]['suffix']
            
        self.name = self.host.name + suffix + self.get_name_suffix_display()

        if self.qual_type in self.TOURNAMENT_TYPES:
            for key, value in self.TOURNAMENT_TYPES[self.qual_type].items():
                if key == 'noty' and self.date.month < 10 and str(self.date.year) == self.season:
                    setattr(self, key, False)
                else:
                    setattr(self, key, value)

        super().save(*args, **kwargs)

    class Meta:
        ordering = ('date',)
