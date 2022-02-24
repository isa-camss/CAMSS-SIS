import com.nttdata.dgi.util.io as io


class Textifier:
    source_textification_dir: str
    source_textification_file: str
    textification_dir: str
    lang: bool

    def __init__(self, resources_dir: str = None, resource_file: str = None, target_dir: str = None):

        self.source_textification_dir = resources_dir
        self.source_textification_file = resource_file
        self.textification_dir = target_dir
        self.lang = None

    def __call__(self, resources_dir, resource_file, target_dir):
        self.__init__(resources_dir, resource_file, target_dir)
        return self

    def textify_file(self):
        content, lang_ = io.get_content_from_file(self.source_textification_file, self.lang)
        file_name = io.get_file_name_from_path(self.source_textification_file)
        name, extension = io.file_split_name_ext(file_name)
        new_path = io.slash(self.textification_dir) + name + '.txt'
        if not content:
            pass
        else:
            io.to_file(content, new_path)

        return self

    def textify_folder(self):

        for index, path, name, ext in io.get_files(self.source_textification_dir):
            content, lang_ = io.get_content_from_file(path, self.lang)
            new_path = io.slash(self.textification_dir) + name + '.txt'
            if not content:
                pass
            else:
                io.to_file(content, new_path)
        return self
