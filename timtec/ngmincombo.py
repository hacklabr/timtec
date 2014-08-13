from pipeline.compressors.uglifyjs import UglifyJSCompressor
from pipeline.conf import settings


class NgminComboCompressor(UglifyJSCompressor):
    def compress_js(self, js):
        ngminified = self.execute_command(settings.PIPELINE_NGMIN_BINARY, js)
        return super(NgminComboCompressor, self).compress_js(ngminified)
