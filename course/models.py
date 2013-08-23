from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify

class TimtecUser(AbstractUser):
    pass


class Video(models.Model):
    name = models.CharField(max_length=255)
    youtube_id = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Course(models.Model):
    STATES = (
        ('new', 'New'),
        ('private', 'Private'),
        ('public', 'Public'),
    )

    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    intro_video = models.ForeignKey(Video)
    application = models.TextField()
    requirement = models.TextField()
    abstract = models.TextField()
    structure = models.TextField()
    workload = models.TextField()
    pronatec = models.TextField()
    status = models.CharField(choices=STATES, default=STATES[0][0], max_length=128)
    publication = models.DateField()
    professors = models.ManyToManyField(TimtecUser, through='CourseProfessor')

    def __unicode__(self):
        return self.name

class CourseProfessor(models.Model):
    class Meta:
        unique_together = (('user', 'course'),)

    user = models.ForeignKey(TimtecUser)
    course = models.ForeignKey(Course)
    biography = models.TextField()

    def __unicode__(self):
        return unicode(self.user) + ' @ ' + unicode(self.course)


class Lesson(models.Model):
    slug = models.SlugField(max_length=255, editable=False, unique=True)
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    position = models.IntegerField()
    course = models.ForeignKey(Course)

    class Meta:
        ordering = ['position']

    def save(self, **kwargs):
        if not self.id and self.name:
            self.slug = slugify(self.name)
        super(Lesson, self).save(**kwargs)

    def __unicode__(self):
        return self.name

class Activity(models.Model):
    """
    Generic class to activities
    Data templates (data e type atributes):
    Multiple choice
        type: multiplechoice
        data: {question: "", choices: ["choice1", "choice2", ...]}
        expected_answer_data: {choices: [0, 2, 5]} # list of espected choices, zero starting
    Single choice
        type: singlechoice
        data: {question: "", choices: ["choice1", "choice2", ...]}
        expected_answer_data: {choice: 1}
    """
    type = models.CharField(max_length=255)
    data = JSONField()
    expected_answer = JSONField()

    class Meta:
        verbose_name_plural = "Activities"

    def __unicode__(self):
        return u'%s dt %s a %s' % (self.type, self.data, self.expected_answer)

class Unit(models.Model):
    lesson = models.ForeignKey(Lesson)
    video = models.ForeignKey(Video, null=True, blank=True)
    activity = models.ForeignKey(Activity, null=True, blank=True)
    position = models.IntegerField()

    class Meta:
        ordering = ['position']

    def __unicode__(self):
        return u'%s) %s - %s - %s' % (self.position, self.lesson, self.video, self.activity)

class Answer(models.Model):
    activity = models.ForeignKey(Activity)
    user = models.ForeignKey(TimtecUser)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    answer = models.TextField()
