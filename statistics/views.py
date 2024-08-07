from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView, ListView
from django.forms import formset_factory, modelformset_factory
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template import RequestContext
from .services import return_goallist, return_playerstats, return_goal_combinations, return_race_count
from .services import return_timestamp, return_first_last_races, return_tournament_url


def goals(request, year, phase):
	goal_df_repr = return_goallist(phase, year=year)
	total_races, total_completed_bingos = return_race_count(phase, year=year)
	timestamp = return_timestamp(phase, year)
	tournament_url = return_tournament_url(year)

	return render(request, 'statistics/goals.html', {'goals': goal_df_repr, 'racecount': total_races,
	                                      'bingocount': total_completed_bingos, 'phase': phase,
	                                      'year': year, 'url': tournament_url, 'timestamp': timestamp})


def players(request, year, phase):
	player_df_repr = return_playerstats(phase, year=year)
	total_races, total_completed_bingos = return_race_count(phase, year=year)
	timestamp = return_timestamp(phase, year)
	tournament_url = return_tournament_url(year)

	return render(request, 'statistics/players.html', {'players': player_df_repr, 'racecount': total_races,
	                                        'bingocount': total_completed_bingos, 'year': year,
	                                        'url': tournament_url, 'timestamp': timestamp, 'phase': phase})


def combinations(request, year):
	goal_combi_repr = return_goal_combinations(year=year)
	total_races_swiss, total_completed_bingos_swiss = return_race_count(year=year, mode='swiss')
	total_races_top16, total_completed_bingos_top16 = return_race_count(year=year, mode='top16')
	total_races = total_races_swiss+total_races_top16
	total_completed_bingos = total_completed_bingos_swiss+total_completed_bingos_top16
	timestamp = return_timestamp('swiss', year)
	tournament_url = return_tournament_url(year)

	return render(request, 'statistics/combinations.html', {'combinations': goal_combi_repr, 'racecount': str(total_races),
	                                             'bingocount': total_completed_bingos, 'url': tournament_url,
	                                             'year': year, 'timestamp': timestamp})


def frequency(request):
	return render(request, 'statistics/frequency.html')


def players_era(request, version):
	player_df_repr = return_playerstats('swiss', year=version)
	total_races, total_completed_bingos = return_race_count('swiss', year=version)
	first_last = return_first_last_races(version)
	timestamp = return_timestamp('', version)
	return render(request, 'statistics/players_era.html', {'players': player_df_repr, 'racecount': total_races,
	                                            'bingocount': total_completed_bingos, 'timestamp': timestamp,
	                                            'version': version, 'firstrace': first_last['first'], 'lastrace': first_last['last']})


def goals_era(request, version):
	goal_df_repr = return_goallist('swiss', year=version)
	total_races, total_completed_bingos = return_race_count('swiss', year=version)
	first_last = return_first_last_races(version)
	timestamp = return_timestamp('', version)

	return render(request, 'statistics/goals_era.html', {'goals': goal_df_repr, 'racecount': total_races,
	                                          'bingocount': total_completed_bingos, 'timestamp': timestamp,
	                                          'version': version, 'firstrace': first_last['first'],
	                                          'lastrace': first_last['last']})


def combinations_era(request, version):
	goal_combi_repr = return_goal_combinations(year=version)
	total_races, total_completed_bingos = return_race_count(year=version, mode='swiss')
	first_last = return_first_last_races(version)
	timestamp = return_timestamp('', version)

	return render(request, 'statistics/combinations_era.html', {'combinations': goal_combi_repr, 'racecount': str(total_races),
	                                                 'bingocount': total_completed_bingos,
	                                                 'timestamp': timestamp, 'version': version,
	                                                 'firstrace': first_last['first'], 'lastrace': first_last['last']})
