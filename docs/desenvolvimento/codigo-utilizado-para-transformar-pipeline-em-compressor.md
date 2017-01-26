Criar um comando django:

```
from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):

    def handle(self, *args, **options):
        css = settings.PIPELINE.get('STYLESHEETS')
        js = settings.PIPELINE.get('JAVASCRIPT')

        new_css = {}
        for pipeline_name, content in css.items():
            new_compressor_content = "{% compress css %}\n"
            for file in content.get('source_filenames'):
                file = "{%% static '%s' %%}" % file
                new_compressor_content += '<link rel="stylesheet" href="{}" type="text/css" />\n'.format(file)
            new_compressor_content += "{% endcompress %}\n"
            new_css[pipeline_name] = new_compressor_content

        new_js = {}
        for pipeline_name, content in js.items():
            new_compressor_content = "{% compress js %}\n"
            for file in content.get('source_filenames'):
                file = "{%% static '%s' %%}" % file
                new_compressor_content += '<script type="text/javascript" src="{}"></script>\n'.format(file)
            new_compressor_content += "{% endcompress %}\n"
            new_js[pipeline_name] = new_compressor_content

        for root, dirs, files in os.walk("../timtec-theme-if"):
            for file in files:
                file = os.path.join(root, file)
                if file.endswith('.html'):

                    is_changed = False
                    with open(file) as handle:
                        data = handle.read()

                    data = data.replace("{% load pipeline %}", "{% load compress %}\n{% load static %}")

                    for label, content in new_css.items():
                        for pipeline_tag in ("{%% stylesheet '%s' %%}" % label, '{%% stylesheet "%s" %%}' % label):
                            if pipeline_tag in data:
                                data = data.replace(pipeline_tag, content)
                                is_changed = True

                    for label, content in new_js.items():
                        for pipeline_tag in ("{%% javascript '%s' %%}" % label, '{%% javascript "%s" %%}' % label):
                            if pipeline_tag in data:
                                data = data.replace(pipeline_tag, content)
                                is_changed = True

                    if is_changed:
                        with open(file, 'w') as output:
                            output.write(data)
                            print file
```
