# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    depends_on = (
        ('activities', '0007_expected_empty'),
        ('forum', '0005_auto__add_field_question_hidden_justification'),
        ('core', '0025_empty.py'),
        ('notes', '0001_initial'),
    )
    needed_by = (
        ("core", "0026_auto__add_field_courseprofessor_picture__add_field_courseprofessor_nam"),
    )

    def forwards(self, orm):
        # Changing field 'Answer.user'
        db.alter_column(u'activities_answer', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ifs.IfUser']))

        ## Core ##
        # Changing field 'ProfessorMessage.professor'
        db.alter_column(u'core_professormessage', 'professor_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ifs.IfUser']))

        # Changing field 'CourseProfessor.user'
        db.alter_column(u'core_courseprofessor', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ifs.IfUser']))

        # Changing field 'CourseStudent.user'
        db.alter_column(u'core_coursestudent', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ifs.IfUser']))

        # Changing field 'Class.assistant'
        db.alter_column(u'core_class', 'assistant_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['ifs.IfUser']))

        # Changing field 'StudentProgress.user'
        db.alter_column(u'core_studentprogress', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ifs.IfUser']))

        ## Forum ##
        # Changing field 'Question.user'
        db.alter_column(u'forum_question', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ifs.IfUser']))

        # Changing field 'Question.hidden_by'
        db.alter_column(u'forum_question', 'hidden_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['ifs.IfUser']))

        # Changing field 'Answer.user'
        db.alter_column(u'forum_answer', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ifs.IfUser']))

        # Changing field 'Vote.user'
        db.alter_column(u'forum_vote', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ifs.IfUser']))

        ## Notes ##
        # Changing field 'Note.user'
        db.alter_column(u'notes_note', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ifs.IfUser']))

    def backwards(self, orm):

        # Changing field 'Answer.user'
        db.alter_column(u'activities_answer', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.TimtecUser']))

        ## Core ##
        # Changing field 'ProfessorMessage.professor'
        db.alter_column(u'core_professormessage', 'professor_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.TimtecUser']))

        # Changing field 'CourseProfessor.user'
        db.alter_column(u'core_courseprofessor', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.TimtecUser']))

        # Changing field 'CourseStudent.user'
        db.alter_column(u'core_coursestudent', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.TimtecUser']))

        # Changing field 'Class.assistant'
        db.alter_column(u'core_class', 'assistant_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['accounts.TimtecUser']))

        # Changing field 'StudentProgress.user'
        db.alter_column(u'core_studentprogress', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.TimtecUser']))

        ## Forum ##
        # Changing field 'Question.user'
        db.alter_column(u'forum_question', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.TimtecUser']))

        # Changing field 'Question.hidden_by'
        db.alter_column(u'forum_question', 'hidden_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['accounts.TimtecUser']))

        # Changing field 'Answer.user'
        db.alter_column(u'forum_answer', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.TimtecUser']))

        # Changing field 'Vote.user'
        db.alter_column(u'forum_vote', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.TimtecUser']))

        ## Notes ##
        # Changing field 'Note.user'
        db.alter_column(u'notes_note', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.TimtecUser']))

    models = {
        u'accounts.timtecuser': {
            'Meta': {'object_name': 'TimtecUser'},
            'accepted_terms': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'biography': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'site': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'activities.activity': {
            'Meta': {'ordering': "['id']", 'object_name': 'Activity'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'data': ('jsonfield.fields.JSONField', [], {}),
            'expected': ('jsonfield.fields.JSONField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'activities'", 'null': 'True', 'to': u"orm['core.Unit']"})
        },
        u'activities.answer': {
            'Meta': {'ordering': "['timestamp']", 'object_name': 'Answer'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['activities.Activity']"}),
            'given': ('jsonfield.fields.JSONField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ifs.IfUser']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.class': {
            'Meta': {'object_name': 'Class'},
            'assistant': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'professor_classes'", 'null': 'True', 'to': u"orm['ifs.IfUser']"}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'classes'", 'blank': 'True', 'to': u"orm['ifs.IfUser']"})
        },
        u'core.course': {
            'Meta': {'object_name': 'Course'},
            'abstract': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'application': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'default_class': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'default_course'", 'unique': 'True', 'null': 'True', 'to': u"orm['core.Class']"}),
            'home_position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'home_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'home_thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro_video': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Video']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'professors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'professorcourse_set'", 'symmetrical': 'False', 'through': u"orm['core.CourseProfessor']", 'to': u"orm['ifs.IfUser']"}),
            'pronatec': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'publication': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'requirement': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '64'}),
            'structure': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'studentcourse_set'", 'symmetrical': 'False', 'through': u"orm['core.CourseStudent']", 'to': u"orm['ifs.IfUser']"}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'workload': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'core.courseprofessor': {
            'Meta': {'unique_together': "(('user', 'course'),)", 'object_name': 'CourseProfessor'},
            'biography': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'assistant'", 'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ifs.IfUser']"})
        },
        u'core.coursestudent': {
            'Meta': {'unique_together': "(('user', 'course'),)", 'object_name': 'CourseStudent'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ifs.IfUser']"})
        },
        u'core.emailtemplate': {
            'Meta': {'object_name': 'EmailTemplate'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'template': ('django.db.models.fields.TextField', [], {})
        },
        u'core.lesson': {
            'Meta': {'ordering': "['position']", 'object_name': 'Lesson'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lessons'", 'to': u"orm['core.Course']"}),
            'desc': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '255', 'populate_from': "'name'", 'unique_with': '()'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'draft'", 'max_length': '64'})
        },
        u'core.professormessage': {
            'Meta': {'object_name': 'ProfessorMessage'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Course']", 'null': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'professor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ifs.IfUser']"}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'messages'", 'symmetrical': 'False', 'to': u"orm['ifs.IfUser']"})
        },
        u'core.studentprogress': {
            'Meta': {'unique_together': "(('user', 'unit'),)", 'object_name': 'StudentProgress'},
            'complete': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_access': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'progress'", 'to': u"orm['core.Unit']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ifs.IfUser']"})
        },
        u'core.unit': {
            'Meta': {'ordering': "['lesson', 'position']", 'object_name': 'Unit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'units'", 'to': u"orm['core.Lesson']"}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'side_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Video']", 'null': 'True', 'blank': 'True'})
        },
        u'core.video': {
            'Meta': {'object_name': 'Video'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'youtube_id': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'forum.answer': {
            'Meta': {'object_name': 'Answer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': u"orm['forum.Question']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forum_answers'", 'to': u"orm['ifs.IfUser']"})
        },
        u'forum.answervote': {
            'Meta': {'object_name': 'AnswerVote', '_ormbases': [u'forum.Vote']},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': u"orm['forum.Answer']"}),
            u'vote_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['forum.Vote']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'forum.question': {
            'Meta': {'object_name': 'Question'},
            'correct_answer': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'+'", 'unique': 'True', 'null': 'True', 'to': u"orm['forum.Answer']"}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Course']"}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hidden_by': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'hidden_questions'", 'null': 'True', 'blank': 'True', 'to': u"orm['ifs.IfUser']"}),
            'hidden_justification': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'forum_questions'", 'null': 'True', 'to': u"orm['core.Lesson']"}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '255', 'populate_from': "'title'", 'unique_with': '()'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forum_questions'", 'to': u"orm['ifs.IfUser']"})
        },
        u'forum.questionvote': {
            'Meta': {'object_name': 'QuestionVote', '_ormbases': [u'forum.Vote']},
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': u"orm['forum.Question']"}),
            u'vote_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['forum.Vote']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'forum.vote': {
            'Meta': {'object_name': 'Vote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ifs.IfUser']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        u'ifs.ifuser': {
            'Meta': {'object_name': 'IfUser'},
            'accepted_terms': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'biography': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'campus': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'course': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'cpf': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ifid': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_if_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'klass': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'siape': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'site': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'notes.note': {
            'Meta': {'object_name': 'Note'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'create_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_edit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ifs.IfUser']"})
        }
    }

    complete_apps = ['core', 'activities', 'forum', 'notes', 'ifs']
