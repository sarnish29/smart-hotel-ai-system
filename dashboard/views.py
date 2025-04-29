from django.shortcuts import render, redirect
from api.models import Readings, Dustbins

def dashboard_view(request):
    # latest_record = Readings.objects.order_by('-recorded_on')
    latest_record = Readings.objects.raw('SELECT * FROM api_readings WHERE (`recorded_on`) IN (SELECT MAX(`recorded_on`) FROM api_readings GROUP BY `dustbin_id`) ORDER BY dustbin_id ASC, recorded_on DESC')

    filled = []
    empty = []
    for rows in latest_record:
        filled.append(int(rows))
        empty.append(100 - int(rows))

    return render(request, 'dashboard/index.html', {'latest_record': latest_record , 'filled': filled, 'empty': empty })

def details_view(request, dustbin_id):
    location = Dustbins.objects.get(id=dustbin_id)
    # print(get_record.dustbin_id)
    get_record = Readings.objects.filter(dustbin_id=dustbin_id).order_by('-recorded_on')[0]
    level = get_record.level
    dustbin_id = get_record.dustbin_id
    empty = 100 - int(level)
    recorded_on = get_record.recorded_on
    location = location.location_name

    context = {}
    context['level'] = level
    context['dustbin_id'] = dustbin_id
    context['empty'] = empty
    context['recorded_on'] = recorded_on
    context['location'] = location

    return render(request, 'dashboard/details.html', context)

