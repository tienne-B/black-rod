from dal import autocomplete

from django import forms
from django.forms import formset_factory

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from core.models.debater import Debater
from core.models.school import School
from core.models.tournament import Tournament
from core.models.team import Team

from core.models.results.team import TeamResult
from core.models.results.speaker import SpeakerResult


class DebaterForm(forms.ModelForm):
    school = forms.ModelChoiceField(
        queryset=School.objects.all(),
        widget=autocomplete.ModelSelect2(url='core:school_autocomplete')
    )

    class Meta:
        model = Debater
        fields = ('first_name', 'last_name', 'school')


class TournamentForm(forms.ModelForm):
    host = forms.ModelChoiceField(
        queryset=School.objects.all(),
        widget=autocomplete.ModelSelect2(url='core:school_autocomplete')
    )

    class Meta:
        model = Tournament
        fields = ('host',
                  'season',
                  'date',
                  'num_teams',
                  'num_novice_debaters',
                  'qual_type',
                  'name_suffix',
                  'manual_name')


class TeamForm(forms.ModelForm):
    debaters = forms.ModelMultipleChoiceField(
        queryset=Debater.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='core:debater_autocomplete')
    )

    class Meta:
        model = Team
        fields = ('debaters',)

    def clean(self):
        cleaned_data = super().clean()

        if not len(cleaned_data.get('debaters')) == 2:
            raise forms.ValidationError(
                'All teams must have 2 debaters'
            )


class TournamentDetailForm(forms.Form):
    num_teams = forms.IntegerField(label="Number of teams")
    num_novices = forms.IntegerField(label="Number of novices")


class TournamentImportForm(forms.Form):
    url = forms.CharField(label='URL',
                          help_text='Please enter the URL for the tournament without any trailing slashes but including http://.  For example: "http://mit.nu-tab.com"',
                          validators=[URLValidator()])


class TournamentSelectionForm(forms.Form):
    tournament = forms.ModelChoiceField(
        queryset=Tournament.objects.all(),
        widget=autocomplete.ModelSelect2(url='core:tournament_autocomplete')
    )


class TeamResultForm(forms.Form):
    debater_one = forms.ModelChoiceField(
        label="Debater One",
        queryset=Debater.objects.all(),
        widget=autocomplete.ModelSelect2(url='core:debater_autocomplete'),
        required=False
    )

    debater_two = forms.ModelChoiceField(
        label="Debater Two",
        queryset=Debater.objects.all(),
        widget=autocomplete.ModelSelect2(url='core:debater_autocomplete'),
        required=False
    )

    class Meta:
        model = TeamResult
        fields = []


class SpeakerResultForm(forms.ModelForm):
    speaker = forms.ModelChoiceField(
        label="",
        queryset=Debater.objects.all(),
        widget=autocomplete.ModelSelect2(url='core:debater_autocomplete'),
        required=False
    )

    class Meta:
        model = SpeakerResult
        fields = ('speaker',)

VarsityTeamResultFormset = formset_factory(TeamResultForm, extra=16, max_num=16)
NoviceTeamResultFormset = formset_factory(TeamResultForm, extra=8, max_num=8)

VarsitySpeakerResultFormset = formset_factory(SpeakerResultForm, extra=10, max_num=10)
NoviceSpeakerResultFormset = formset_factory(SpeakerResultForm, extra=10, max_num=10)


class SchoolReconciliationForm(forms.Form):
    id = forms.FloatField(widget=forms.HiddenInput())

    server_name = forms.CharField(label='Server School Name')

    school = forms.ModelChoiceField(
        queryset=School.objects.all(),
        widget=autocomplete.ModelSelect2(url='core:school_autocomplete'),
        required=False
    )


class DebaterReconciliationForm(forms.Form):
    id = forms.FloatField(widget=forms.HiddenInput())
    school_id = forms.FloatField(widget=forms.HiddenInput())
    status = forms.FloatField(widget=forms.HiddenInput())

    server_name = forms.CharField(label='Server Debater Name')
    server_school_name = forms.CharField(label='Server School Name',
                                         disabled=True)
    server_hybrid_school_name = forms.CharField(label='Server Hybrid School Name',
                                                disabled=True,
                                                required=False)

    school = forms.ModelChoiceField(
        queryset=School.objects.all(),
        widget=autocomplete.ModelSelect2(url='core:school_autocomplete'),
        required=False
    )

    debater = forms.ModelChoiceField(
        queryset=Debater.objects.all(),
        widget=autocomplete.ModelSelect2(url='core:debater_autocomplete', forward=['school']),
        required=False
    )


SchoolReconciliationFormset = formset_factory(SchoolReconciliationForm, extra=0)
DebaterReconciliationFormset = formset_factory(DebaterReconciliationForm, extra=0)
