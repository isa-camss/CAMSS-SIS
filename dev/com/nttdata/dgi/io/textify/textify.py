
import com.nttdata.dgi.util.io as io


class Textify:

    def textify(self, args: dict):
        source_dir = args['source_dir']
        target_dir = args['target_dir']
        lang = args['lang?']

        for index, path, name, ext in io.get_files(source_dir):
            content, lang_ = io.get_content_from_file(path, lang)
            new_path = io.slash(target_dir) + name + '.txt'
            if not content:
                pass
            else:
                io.to_file(content, new_path)

        return self
