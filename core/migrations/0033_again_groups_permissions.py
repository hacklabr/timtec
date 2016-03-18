# -*- coding: utf-8 -*-
from south.v2 import DataMigration


class Migration(DataMigration):
    depends_on = (
        ('activities', '0008_create_permissions'),
        ('course_material', '0001_initial'),
        ('forum', '0005_auto__add_field_question_hidden_justification'),
        ('notes', '0001_initial'),
    )

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName".
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.

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
    }
    symmetrical = True
