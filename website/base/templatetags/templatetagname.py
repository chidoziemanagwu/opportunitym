from django import template
from base.models import speaker_applied_event, seeker_applied_job

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='speaker_already_apply')
def speaker_already_apply(user, event):
    try:
        applied_events = speaker_applied_event.objects.filter(event=event)
        for applied_event in applied_events:
            if user == applied_event.user:
                return True
    except Exception as e:
        print(e)

@register.filter(name='seeker_already_apply')
def seeker_already_apply(user, job_position):
    try:
        applied_jobs = seeker_applied_job.objects.filter(job_position=job_position)
        for applied_job in applied_jobs:
            if user == applied_job.user:
                return True
    except Exception as e:
        print(e)
