from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from core.models import StudentProgress, ProfessorMessage, CourseStudent, CourseProfessor
from forum.models import Question, QuestionVote, Answer, AnswerVote
import activities

User = get_user_model()


class Command(BaseCommand):
    args = ''
    help = 'Remove all student related data'

    def handle(self, *args, **options):

        for course_professor in CourseProfessor.objects.all():
            course_professor.name = course_professor.user.get_full_name()
            course_professor.picture = course_professor.user.picture
            if not course_professor.biography:
                course_professor.biography = course_professor.user.biography
            course_professor.user = None
            course_professor.save()

        User.objects.all() \
                    .exclude(is_superuser=True) \
                    .delete()
        Question.objects.all().delete()
        QuestionVote.objects.all().delete()
        Answer.objects.all().delete()
        AnswerVote.objects.all().delete()
        ProfessorMessage.objects.all().delete()
        activities.models.Answer.objects.all().delete()
        CourseStudent.objects.all().delete()
        StudentProgress.objects.all().delete()
