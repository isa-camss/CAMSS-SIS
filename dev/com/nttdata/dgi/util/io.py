import base64
from datetime import datetime
import enum
import hashlib
import json
import logging
import ntpath
import os
import pickle as pkl
import re
import shutil
import smart_open as so
import pathlib as pl
import unidecode


def url_tail(url: str, sep: str = '/'):
    """
    Returns the tail of a path
    """
    return url.rsplit(sep, 1)[1]

def base64_(file: str) -> str:
    """
    Returns the content of a file as a Base64 string
    """
    with open(file, "rb") as file:
        binary = base64.b64encode(file.read()).decode()
    return binary


def timestamp(file: str) -> str:
    """
    Returns the timestamp of a file
    """
    modified = os.path.getmtime(file)
    return datetime.fromtimestamp(modified).__str__()


class HashAlgorithm(enum.IntEnum):
    md5 = 1
    sha1 = 2
    sha256 = 3


def hash(file, algorithm: HashAlgorithm = HashAlgorithm.md5) -> str:
    """
    Returns the hash of a file
    """
    if algorithm == HashAlgorithm.md5:
        return hashlib.md5(file.encode()).hexdigest()
    elif algorithm == HashAlgorithm.sha1:
        return hashlib.sha1(file.encode()).hexdigest()
    elif algorithm == HashAlgorithm.sha256:
        return hashlib.sha256(file.encode()).hexdigest()


def unpickle(file: str):
    """
    Unpickle a file
    """
    with open(file, 'rb') as handle:
        return pkl.load(handle, fix_imports=True)


def now() -> datetime:
    """
    Returns the current timestamp
    """
    return datetime.now()


def log(message: str, level: str = None, condition: bool = True, logger: logging.Logger = None) -> datetime:
    """
    Logs a message
    :param message: the text to print and log
    :param level: info, warning or error
    :param condition: skips the job if a specified condition is not met
    :param logger: the logger used to print and save the execution events
    """
    if condition:
        _logger = logging.getLogger() if not logger else logger
        if _logger.level == logging.getLevelName('INFO') or level == 'i':
            _logger.info(message)
        elif _logger.level == logging.getLevelName('WARNING') or level == 'w':
            _logger.warning(message)
        elif _logger.level == logging.getLevelName('ERROR') or level == 'e':
            _logger.error(message)
    return now()


def list_dirs(root_dir: str):
    """
    Returns list with the names of the first level directories inside a root path.
    """
    return list(os.walk(root_dir))[1]


def drop_file(path: str):
    """
    Remove a file
    """
    if os.path.isfile(path):
        os.remove(path)


def drop_dir(path: str):
    """
    Remove a dir and sub files/folders
    """
    if os.path.isdir(path):
        shutil.rmtree(path)


def from_json(file: str) -> dict:
    """
    Returns a dict from a json file
    """
    with open(file, 'r') as fp:
        return json.load(fp)


def to_json(dic: dict, file: str):
    """
    Saves a dict to a json file path
    """
    with open(file, 'w') as fp:
        json.dump(dic, fp, indent=4)


def alpha2(lang: str) -> str:
    """
    WARNING: MOVED INTO util.string.py for generalization
    Returns the alpha-2 version of an expanded idb lang, like from 'en-US' into 'en'
    :param lang: idb version of the lang
    :return: alpha-2 version of the lang
    """
    return None if not lang else lang[:2]


def make_file_dirs(file_pathname: str) -> str:
    """
    Given the complete path to a file, creates the directories preceding the name of the file
    :param file_pathname: the name of the file
    :return: the path created, without the name of the file
    """
    dir_, file_ = ntpath.split(file_pathname)
    os.makedirs(dir_, exist_ok=True)
    return dir_ if len(dir_) != 0 else None


def unaccent(text: str) -> str:
    return unidecode.unidecode(text)


def nnl(text: str) -> str:
    """
    Replaces all new lined '\n' with ' '
    :param text: text with new lines
    :return: text without new lines
    """
    return text.replace("\n", " ")


def wc(words: tuple, text: str = None) -> int:
    """
    Counts the occurrences of a word in a file or in a text (both are mutually exclusive)
    :param words: the list of word to count
    :param text: the text where the word occurs
    :return: the number of occurrences
    """
    total = 0
    for word in words:
        total += len(re.findall(word, text))
    return total

def xst_file(path: str) -> bool:
    """
    Checks whether a file or directory exists or not.
    :param path:  the path to the dir or file
    :return: the result of the checking
    """
    return os.path.isdir(path) or os.path.isfile(path)


def file_to_str(path_filename: str, bytes_number: int = 0) -> str:
    """
    Use this to avoid problems with encoding.
    """
    if not xst_file(path_filename):
        return None
    offset = bytes_number if bytes_number != 0 else pl.Path(path_filename).stat().st_size
    with so.open(path_filename, 'rb') as fin:
        return fin.read(offset).decode('utf-8')

def get_file(path_filename: str) -> (str, str):
    name, ext = file_split_name_ext(get_file_name_from_path(path_filename))
    return name, ext


def file_split_name_ext(file_name: str) -> (str, str):
    v = os.path.splitext(file_name)
    return v[0], v[1]


def get_file_name_from_path(path) -> str:
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)