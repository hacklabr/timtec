from django.dispatch import receiver
from django.db.models.signals import post_save

from core.models import StudentProgress
from activities.models import Activity, Answer
from django.utils import timezone


@receiver(post_save, sender=Answer)
def update_student_progress(sender, instance, **kwargs):
    answer = instance
    progress, _ = StudentProgress.objects.get_or_create(user=answer.user,
                                                        unit=answer.activity.unit)

    correct = True
    for activity in Activity.objects.filter(unit=answer.activity.unit):
        try:
            ans = Answer.objects.filter(activity=activity).order_by('-timestamp')[:1].get()
        except Answer.DoesNotExist:
            correct = False
            break
        correct = ans.is_correct()
        if not correct:
            break

    if correct:
        progress.complete = timezone.now()

    progress.save()
