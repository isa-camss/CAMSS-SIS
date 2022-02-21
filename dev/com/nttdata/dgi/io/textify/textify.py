import com.nttdata.dgi.util.io as io


class Textifier:
    corpus_dir: str
    textification_dir: str
    lang: dict

    def __init__(self, resources_dir: str = None, target_dir: str = None):

        self.corpus_dir = resources_dir
        self.textification_dir = target_dir
        self.lang = None

    def __call__(self, resources_dir, target_dir):
        self.__init__(resources_dir, target_dir)
        return self

    def textify(self):

        for index, path, name, ext in io.get_files(self.corpus_dir):
            content, lang_ = io.get_content_from_file(path, self.lang)
            new_path = io.slash(self.textification_dir) + name + '.txt'
            if not content:
                pass
            else:
                io.to_file(content, new_path)

        return self
