# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TimtecUser'
        db.create_table(u'core_timtecuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('occupation', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('site', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('biography', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'core', ['TimtecUser'])

        # Adding M2M table for field groups on 'TimtecUser'
        m2m_table_name = db.shorten_name(u'core_timtecuser_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('timtecuser', models.ForeignKey(orm[u'core.timtecuser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['timtecuser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'TimtecUser'
        m2m_table_name = db.shorten_name(u'core_timtecuser_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('timtecuser', models.ForeignKey(orm[u'core.timtecuser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['timtecuser_id', 'permission_id'])

        # Adding model 'Video'
        db.create_table(u'core_video', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('youtube_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['Video'])

        # Adding model 'Course'
        db.create_table(u'core_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('intro_video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Video'], null=True)),
            ('application', self.gf('django.db.models.fields.TextField')()),
            ('requirement', self.gf('django.db.models.fields.TextField')()),
            ('abstract', self.gf('django.db.models.fields.TextField')()),
            ('structure', self.gf('django.db.models.fields.TextField')()),
            ('workload', self.gf('django.db.models.fields.TextField')()),
            ('pronatec', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.CharField')(default='new', max_length=128)),
            ('publication', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'core', ['Course'])

        # Adding model 'CourseStudent'
        db.create_table(u'core_coursestudent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.TimtecUser'])),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Course'])),
        ))
        db.send_create_signal(u'core', ['CourseStudent'])

        # Adding unique constraint on 'CourseStudent', fields ['user', 'course']
        db.create_unique(u'core_coursestudent', ['user_id', 'course_id'])

        # Adding model 'CourseProfessor'
        db.create_table(u'core_courseprofessor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.TimtecUser'])),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Course'])),
            ('biography', self.gf('django.db.models.fields.TextField')()),
            ('role', self.gf('django.db.models.fields.CharField')(default='instructor', max_length=128)),
        ))
        db.send_create_signal(u'core', ['CourseProfessor'])

        # Adding unique constraint on 'CourseProfessor', fields ['user', 'course']
        db.create_unique(u'core_courseprofessor', ['user_id', 'course_id'])

        # Adding model 'Lesson'
        db.create_table(u'core_lesson', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Course'])),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'core', ['Lesson'])

        # Adding model 'Activity'
        db.create_table(u'core_activity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('data', self.gf('jsonfield.fields.JSONField')()),
            ('expected', self.gf('jsonfield.fields.JSONField')()),
        ))
        db.send_create_signal(u'core', ['Activity'])

        # Adding model 'Unit'
        db.create_table(u'core_unit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(related_name='units', to=orm['core.Lesson'])),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Video'], null=True, blank=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Activity'], null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'core', ['Unit'])

        # Adding model 'Answer'
        db.create_table(u'core_answer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Activity'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.TimtecUser'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('given', self.gf('jsonfield.fields.JSONField')()),
        ))
        db.send_create_signal(u'core', ['Answer'])

        # Adding model 'StudentProgress'
        db.create_table(u'core_studentprogress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.TimtecUser'])),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='progress', to=orm['core.Unit'])),
            ('complete', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_access', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['StudentProgress'])

        # Adding unique constraint on 'StudentProgress', fields ['user', 'unit']
        db.create_unique(u'core_studentprogress', ['user_id', 'unit_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'StudentProgress', fields ['user', 'unit']
        db.delete_unique(u'core_studentprogress', ['user_id', 'unit_id'])

        # Removing unique constraint on 'CourseProfessor', fields ['user', 'course']
        db.delete_unique(u'core_courseprofessor', ['user_id', 'course_id'])

        # Removing unique constraint on 'CourseStudent', fields ['user', 'course']
        db.delete_unique(u'core_coursestudent', ['user_id', 'course_id'])

        # Deleting model 'TimtecUser'
        db.delete_table(u'core_timtecuser')

        # Removing M2M table for field groups on 'TimtecUser'
        db.delete_table(db.shorten_name(u'core_timtecuser_groups'))

        # Removing M2M table for field user_permissions on 'TimtecUser'
        db.delete_table(db.shorten_name(u'core_timtecuser_user_permissions'))

        # Deleting model 'Video'
        db.delete_table(u'core_video')

        # Deleting model 'Course'
        db.delete_table(u'core_course')

        # Deleting model 'CourseStudent'
        db.delete_table(u'core_coursestudent')

        # Deleting model 'CourseProfessor'
        db.delete_table(u'core_courseprofessor')

        # Deleting model 'Lesson'
        db.delete_table(u'core_lesson')

        # Deleting model 'Activity'
        db.delete_table(u'core_activity')

        # Deleting model 'Unit'
        db.delete_table(u'core_unit')

        # Deleting model 'Answer'
        db.delete_table(u'core_answer')

        # Deleting model 'StudentProgress'
        db.delete_table(u'core_studentprogress')


    models = {
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
        u'core.activity': {
            'Meta': {'object_name': 'Activity'},
            'data': ('jsonfield.fields.JSONField', [], {}),
            'expected': ('jsonfield.fields.JSONField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'core.answer': {
            'Meta': {'object_name': 'Answer'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Activity']"}),
            'given': ('jsonfield.fields.JSONField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.TimtecUser']"})
        },
        u'core.course': {
            'Meta': {'object_name': 'Course'},
            'abstract': ('django.db.models.fields.TextField', [], {}),
            'application': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro_video': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Video']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'professors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'professorcourse_set'", 'symmetrical': 'False', 'through': u"orm['core.CourseProfessor']", 'to': u"orm['core.TimtecUser']"}),
            'pronatec': ('django.db.models.fields.TextField', [], {}),
            'publication': ('django.db.models.fields.DateField', [], {}),
            'requirement': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '128'}),
            'structure': ('django.db.models.fields.TextField', [], {}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'studentcourse_set'", 'symmetrical': 'False', 'through': u"orm['core.CourseStudent']", 'to': u"orm['core.TimtecUser']"}),
            'workload': ('django.db.models.fields.TextField', [], {})
        },
        u'core.courseprofessor': {
            'Meta': {'unique_together': "(('user', 'course'),)", 'object_name': 'CourseProfessor'},
            'biography': ('django.db.models.fields.TextField', [], {}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'instructor'", 'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.TimtecUser']"})
        },
        u'core.coursestudent': {
            'Meta': {'unique_together': "(('user', 'course'),)", 'object_name': 'CourseStudent'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.TimtecUser']"})
        },
        u'core.lesson': {
            'Meta': {'ordering': "['position']", 'object_name': 'Lesson'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Course']"}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'core.studentprogress': {
            'Meta': {'unique_together': "(('user', 'unit'),)", 'object_name': 'StudentProgress'},
            'complete': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_access': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'progress'", 'to': u"orm['core.Unit']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.TimtecUser']"})
        },
        u'core.timtecuser': {
            'Meta': {'object_name': 'TimtecUser'},
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
        u'core.unit': {
            'Meta': {'ordering': "['lesson', 'position']", 'object_name': 'Unit'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Activity']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'units'", 'to': u"orm['core.Lesson']"}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Video']", 'null': 'True', 'blank': 'True'})
        },
        u'core.video': {
            'Meta': {'object_name': 'Video'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'youtube_id': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['core']