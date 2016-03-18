from pipeline.compressors.uglifyjs import UglifyJSCompressor
from pipeline.conf import settings


class NgminComboCompressor(UglifyJSCompressor):
    def compress_js(self, js):
        # ngminified = self.execute_command('ng-annotate -a - ', js)
        command = settings.PIPELINE_NGANNOTATE_BINARY + ' -a - '
        ngminified = self.execute_command(command, js)
        return super(NgminComboCompressor, self).compress_js(ngminified)
