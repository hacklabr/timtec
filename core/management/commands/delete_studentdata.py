from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from core.models import StudentProgress, ProfessorMessage, CourseStudent
from forum.models import Question, QuestionVote, Answer, AnswerVote
import activities

User = get_user_model()


class Command(BaseCommand):
    args = ''
    help = 'Remove all student related data'

    def handle(self, *args, **options):
        User.objects.all() \
                    .exclude(groups__name="professor") \
                    .exclude(is_superuser=True) \
                    .exclude(is_staff=True) \
                    .exclude(professorcourse_set__isnull=False) \
                    .delete()
        Question.objects.all().delete()
        QuestionVote.objects.all().delete()
        Answer.objects.all().delete()
        AnswerVote.objects.all().delete()
        ProfessorMessage.objects.all().delete()
        activities.models.Answer.objects.all().delete()
        CourseStudent.objects.all().delete()
        StudentProgress.objects.all().delete()
