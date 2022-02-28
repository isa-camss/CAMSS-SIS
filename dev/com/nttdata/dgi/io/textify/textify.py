import com.nttdata.dgi.util.io as io


class Textifier:
    source_textification_dir: str
    source_textification_file: str
    target_textification_file: str
    textification_dir: str

    def __init__(self, resources_dir: str = None,
                 resource_file: str = None,
                 target_file: str = None,
                 target_dir: str = None):

        self.source_textification_dir = resources_dir
        self.source_textification_file = resource_file
        self.target_textification_file = target_file
        self.textification_dir = target_dir

    def textify_file(self, resource_file, target_file):
        self.source_textification_file = resource_file
        self.target_textification_file = target_file
        content = io.get_content_from_file(self.source_textification_file)
        if not content:
            pass
        else:
            io.to_file(content, self.target_textification_file)

        return self

    def textify_folder(self, resources_dir, target_dir):
        self.source_textification_dir = resources_dir
        self.textification_dir = target_dir

        for index, path, name, ext in io.get_files(self.source_textification_dir):
            content = io.get_content_from_file(path)
            new_path = io.slash(self.textification_dir) + name + '.txt'
            if not content:
                pass
            else:
                io.to_file(content, new_path)
        return self
