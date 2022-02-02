import os
import logging
import hashlib
import pickle as pkl
import shutil
import base64
import json
import enum
from datetime import datetime


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

