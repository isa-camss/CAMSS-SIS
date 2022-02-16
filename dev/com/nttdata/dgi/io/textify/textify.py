
import com.nttdata.dgi.util.io as io


class Textify:

    def textify(args: object) -> object:
        source_dir = args['source-dir']
        target_dir = args['target-dir']
        exclude = args['exclude-ext']
        lang = args['lang?']
        error = True

        for index, path, name, ext in io.get_files(source_dir):
            content, lang_ = io.get_content_from_file(path, lang)
            new_path = io.slash(target_dir) + name + '.txt'
            excluded = ext in exclude
            if not content:
                yield index, path, new_path, lang_, error, name, ext, excluded
            else:
                if not excluded:
                    io.to_file(content, new_path)
                yield index, path, new_path, lang_, not error, name, ext, excluded

        return
