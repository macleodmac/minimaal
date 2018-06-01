import os


class RenderFileMixin(object):

    @property
    def path(self):
        raise NotImplementedError

    @property
    def directory(self):
        return os.path.dirname(self.path)

    @property
    def file_name(self):
        _, file_name = os.path.split(self.path)
        return file_name

    @property
    def html(self):
        raise NotImplementedError

    def render(self, file_handle):
        file_handle.writelines(self.html)
