import random
import copy
import json
from collections import Counter
import numpy as np

def normalize_probs(probs):
    probs = np.array(probs)
    return (probs/np.sum(probs)).tolist()

def get_applicable_schedules(remained_time, schedules, extra_time=0):
    applicable_scheds = []

    for idx, scheds in enumerate(schedules):

        if (remained_time + extra_time) >= schedules[idx].get('time') and \
                schedules[idx].get('probability') > 0:
            applicable_scheds += [scheds]
    return applicable_scheds


# Function to create a daily schedule with customizable work time
def create_daily_schedule(schedules, daily_work_time, priority_sort= False, extra_time=0):
    available_time = daily_work_time
    applicable_scheds = copy.deepcopy(schedules)
    probes = lambda scheds: [s['probability'] for s in scheds]
    
    daily_tasks = []
    
    while available_time > 0 and len(applicable_scheds) > 0:
        selected_sched = random.choices(applicable_scheds, weights=probes(applicable_scheds), k=1)[0]
        
        daily_tasks += [copy.deepcopy(selected_sched)]
        applicable_scheds = adjust_probabilities(applicable_scheds, selected_sched, daily_work_time)
        # print(probes(daily_tasks))
        available_time -= selected_sched['time']
        
        applicable_scheds = get_applicable_schedules(available_time, applicable_scheds, extra_time=random.choice([0, 1])*extra_time)        

    if priority_sort:
        daily_tasks= sorted(daily_tasks, key=lambda x: x["priority"])

    return daily_tasks

# Function to adjust probabilities based on the total hours spent
def adjust_probabilities(schedules, selected_sched, work_time):
    for idx, sched in enumerate(schedules):
        if  schedules[idx]['title'] != selected_sched['title']:
            continue
        allocated_prob = schedules[idx]['time']/work_time
        schedules[idx]['probability'] -= allocated_prob
        schedules[idx]['probability'] = max(schedules[idx]['probability'], 0)
        break
    return schedules


def get_spent_time(schedule):
    total_time = sum(sum(task['time'] for task in tasks) for tasks in schedule.values())

    counts = {
        'week': {},
        'total_time': total_time
    }
    for day, tasks in schedule.items():
        counts[day] = {}
        for t in tasks:
            if t['title'] not in counts[day]:
                counts[day][t['title']] = 0
            if t['title'] not in counts['week']:
                counts['week'][t['title']] = 0
            counts[day][t['title']] += t['time']/total_time
            counts['week'][t['title']] += t['time']/total_time
    return counts

def get_weekly_schedule(schedule_file, daily_work_time, extra_time=0, days=None):
    # Load schedules from JSON
    file = open(schedule_file, 'r')
    schedules = json.load(file)

    original_probabilities = np.array([schedule['probability'] for schedule in schedules])
    normalized_probs = normalize_probs(original_probabilities)

    for idx, sched in enumerate(schedules):
        schedules[idx]['probability'] = normalized_probs[idx]

    if not days:
        days = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    weekly_schedule = {}
    for d in days:
        weekly_schedule[d] = create_daily_schedule((schedules), daily_work_time, priority_sort=True, extra_time=extra_time)

    return weekly_schedule


