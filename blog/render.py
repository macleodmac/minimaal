import os


class RenderFileMixin(object):

    @property
    def path(self):
        raise NotImplementedError

    @property
    def directory(self):
        return os.path.dirname(self.path)

    @property
    def html(self):
        raise NotImplementedError

    def render(self, file_handle):
        file_handle.writelines(self.html)
