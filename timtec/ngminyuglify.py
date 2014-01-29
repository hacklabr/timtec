from pipeline.compressors.yuglify import YuglifyCompressor


class NgminYuglifyCompressor(YuglifyCompressor):
    def compress_js(self, js):
        ngminified = self.execute_command('ngmin', js)
        return super(NgminYuglifyCompressor, self).compress_js(ngminified)
