# -*- coding: utf-8 -*-
from south.v2 import DataMigration
from django.contrib.contenttypes.management import update_contenttypes
from django.contrib.auth.management import create_permissions
from django.db.models import get_app, get_models


class Migration(DataMigration):
    depends_on = (
        ('activities', '0007_expected_empty'),
        ('course_material', '0001_initial'),
        ('forum', '0005_auto__add_field_question_hidden_justification'),
        ('notes', '0001_initial'),
    )

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName".
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        update_contenttypes(get_app('notes'), get_models())
        create_permissions(get_app('notes'), get_models(), 0)

        # permissions are app, codename tuples
        group_permissions = {
            'students': [
                ('notes', 'add_note'),
                ('notes', 'change_note'),
                ('notes', 'delete_note'),
                ('activities', 'add_answer'),
                ('core', 'add_coursestudent'),
                ('activities', 'change_answer'),
                ('core', 'change_coursestudent'),
                ('core', 'delete_coursestudent'),
                ('core', 'add_studentprogress'),
                ('core', 'change_studentprogress'),
                ('core', 'delete_studentprogress'),
                ('forum', 'add_answer'),
                ('forum', 'change_answer'),
                ('forum', 'add_answervote'),
                ('forum', 'change_answervote'),
                ('forum', 'delete_answervote'),
                ('forum', 'add_question'),
                ('forum', 'change_question'),
                ('forum', 'add_questionvote'),
                ('forum', 'change_questionvote'),
                ('forum', 'delete_questionvote'),
                ],
            'professors': [
                ('activities', 'add_activity'),
                ('activities', 'change_activity'),
                ('activities', 'delete_activity'),
                ('activities', 'add_answer'),
                ('activities', 'change_answer'),
                ('activities', 'delete_answer'),
                ('core', 'add_course'),
                ('core', 'change_course'),
                ('core', 'delete_course'),
                ('core', 'add_courseprofessor'),
                ('core', 'change_courseprofessor'),
                ('core', 'delete_courseprofessor'),
                ('core', 'add_coursestudent'),
                ('core', 'change_coursestudent'),
                ('core', 'delete_coursestudent'),
                ('core', 'add_lesson'),
                ('core', 'change_lesson'),
                ('core', 'delete_lesson'),
                ('core', 'add_studentprogress'),
                ('core', 'change_studentprogress'),
                ('core', 'delete_studentprogress'),
                ('core', 'add_unit'),
                ('core', 'change_unit'),
                ('core', 'delete_unit'),
                ('core', 'add_video'),
                ('core', 'change_video'),
                ('core', 'delete_video'),
                ('course_material', 'add_coursematerial'),
                ('course_material', 'change_coursematerial'),
                ('course_material', 'delete_coursematerial'),
                ('course_material', 'add_file'),
                ('course_material', 'change_file'),
                ('course_material', 'delete_file'),
                ('forum', 'add_answer'),
                ('forum', 'change_answer'),
                ('forum', 'delete_answer'),
                ('forum', 'add_answervote'),
                ('forum', 'change_answervote'),
                ('forum', 'delete_answervote'),
                ('forum', 'add_question'),
                ('forum', 'change_question'),
                ('forum', 'delete_question'),
                ('forum', 'add_questionvote'),
                ('forum', 'change_questionvote'),
                ('forum', 'delete_questionvote'),
                ],
        }

        # this will create groups, and add all permissions.
        for group_name, permissions in group_permissions.iteritems():
            group, created = orm['auth.Group'].objects.get_or_create(name=group_name)
            gp = group.permissions
            Permission = orm['auth.Permission']
            for app, codename in permissions:
                try:
                    p = Permission.objects.get(content_type__app_label=app, codename=codename)
                except:
                    print app, codename
                gp.add(p)
            group.save()

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'accounts.timtecuser': {
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
        u'activities.activity': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Activity'},
            'data': ('jsonfield.fields.JSONField', [], {}),
            'expected': ('jsonfield.fields.JSONField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
        u'core.course': {
            'Meta': {'object_name': 'Course'},
            'abstract': ('django.db.models.fields.TextField', [], {}),
            'application': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro_video': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Video']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'professors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'professorcourse_set'", 'symmetrical': 'False', 'through': u"orm['core.CourseProfessor']", 'to': u"orm['accounts.TimtecUser']"}),
            'pronatec': ('django.db.models.fields.TextField', [], {}),
            'publication': ('django.db.models.fields.DateField', [], {}),
            'requirement': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'draft'", 'max_length': '64'}),
            'structure': ('django.db.models.fields.TextField', [], {}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'studentcourse_set'", 'symmetrical': 'False', 'through': u"orm['core.CourseStudent']", 'to': u"orm['accounts.TimtecUser']"}),
            'workload': ('django.db.models.fields.TextField', [], {})
        },
        u'core.courseprofessor': {
            'Meta': {'unique_together': "(('user', 'course'),)", 'object_name': 'CourseProfessor'},
            'biography': ('django.db.models.fields.TextField', [], {}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'instructor'", 'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.TimtecUser']"})
        },
        u'core.coursestudent': {
            'Meta': {'unique_together': "(('user', 'course'),)", 'object_name': 'CourseStudent'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.TimtecUser']"})
        },
        u'core.lesson': {
            'Meta': {'ordering': "['position']", 'object_name': 'Lesson'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Course']"}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'draft'", 'max_length': '64'})
        },
        u'core.studentprogress': {
            'Meta': {'unique_together': "(('user', 'unit'),)", 'object_name': 'StudentProgress'},
            'complete': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_access': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'progress'", 'to': u"orm['core.Unit']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.TimtecUser']"})
        },
        u'core.unit': {
            'Meta': {'ordering': "['lesson', 'position']", 'object_name': 'Unit'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'units'", 'null': 'True', 'to': u"orm['activities.Activity']"}),
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
        }
    }

    complete_apps = ['core']
    symmetrical = True
