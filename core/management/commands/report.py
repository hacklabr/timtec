# coding: utf-8

import csv
import cStringIO
import codecs
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Course, CourseStudent


User = get_user_model()


class DictUnicodeWriter(object):

    def __init__(self, f, fieldnames, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(self.queue, fieldnames, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, D):
        self.writer.writerow({k:v.encode("utf-8") for k,v in D.items()})
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for D in rows:
            self.writerow(D)

    def writeheader(self):
        self.writer.writeheader()


class Command(BaseCommand):
    args = 'course_slug output_file user_emails'
    help = 'Help'

    def handle(self, *args, **options):
#         import ipdb;ipdb.set_trace()
#         report = {}
        lessons_progress = []
        avg_length = 0
#         try:
        emails_file = open(args[2])
        course = Course.objects.get(slug=args[0])

        for email in emails_file.readlines():
            email = email[:-1]
            try:
                user = User.objects.get(email=email)
                course_student = CourseStudent.objects.filter(user=user, course=course).first()
                if not course_student:
                    fake_progress = {}
                    fake_progress['user_name'] = user.first_name + user.last_name
                    fake_progress['email'] = user.email
                    fake_progress['name'] = u''
                    fake_progress['slug'] = u''
                    fake_progress['progress'] = u'Não começou o curso'
                    lessons_progress.append(fake_progress)
                else:
                    for progress in course_student.percent_progress_by_lesson():
                        progress['user_name'] = user.first_name + user.last_name
                        progress['email'] = user.email
                        progress['progress'] = str(progress['progress'])
                        lessons_progress.append(progress)
                        avg_length += 1
            except User.DoesNotExist:
                fake_progress = {}
                fake_progress['user_name'] = ''
                fake_progress['email'] = email
                fake_progress['name'] = u''
                fake_progress['slug'] = u''
                fake_progress['progress'] = u'Não se inscreveu na plataforma'
                lessons_progress.append(fake_progress)
#         except:
#             self.stdout.write(u'Erro ao abrir arquivo de emails dos usuários. Forneça o path completo.')

        with open(args[1], 'wb') as output_file:
            writer = DictUnicodeWriter(output_file, fieldnames=['name', 'slug', 'progress', 'user_name', 'email'], delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#             writer.writeheader()
            writer.writerows(lessons_progress)

        lessons_progress_avg = {}
        for progress in lessons_progress:
            try:
                progress_int = int(progress['progress'])
                if progress['slug'] in lessons_progress_avg.keys():
                    lessons_progress_avg[progress['slug']] += progress_int
                else:
                    lessons_progress_avg[progress['slug']] = progress_int
            except ValueError:
                pass
        lessons_progress_avg_list = []
        for key, value in lessons_progress_avg.items():
            try:
                lessons_progress_avg[key] = str(value / avg_length)
                lessons_progress_avg_list.append({key: str(value / avg_length)})
            except:
                pass
        import ipdb;ipdb.set_trace()
        with open('lessons' + args[1], 'wb') as output_file:
            writer = DictUnicodeWriter(output_file, fieldnames=lessons_progress_avg.keys(), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#             writer.writeheader()
            writer.writerows(lessons_progress_avg_list)
