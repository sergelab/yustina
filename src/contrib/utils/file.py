# coding: utf-8
from __future__ import absolute_import

import hashlib
import os
import random
import re
import sys
import time
import uuid

from werkzeug.utils import secure_filename


if sys.version_info < (3, ):
    def b(x):
        return x
else:
    import codecs

    def b(x):
        return codecs.latin_1_encode(x)[0]


def generate_unique_filename(original_filename):
    """
    Генерирует уникальное имя файла.
    :param original_filename: Оригинальное имя файла
    :return: Сгенерированное название файла
    """
    md5 = hashlib.md5()
    name, ext = os.path.splitext(original_filename)
    md5.update(b('{0}{1}{2}'.format(
        time.time(),
        random.randrange(1, sys.maxsize),
        uuid.uuid4()
    )))
    return secure_filename('{0}{1}'.format(
        md5.hexdigest(), ext
    ))


def make_path():
    str_len = 32
    uuid_str = str(uuid.uuid4()).replace('-', '')
    if len(uuid_str) != str_len:
        raise Exception('Invalid UUID length. Must be {0}, given {1}.'.format(
            str_len, len(uuid_str)
        ))
    result = re.findall(r'.{1,2}', uuid_str, re.DOTALL)
    return result or []


def add_prefix_to_filename(original_filename, prefix=None):
    """
    Добавляет prefix к названию файла.
    """
    if not prefix:
        return original_filename
    path = os.path.dirname(original_filename)
    fname = os.path.basename(original_filename)
    prefixed_fname = '{0}{1}'.format(prefix, fname)
    return os.path.join(path, prefixed_fname)


def add_postfix_to_filename(original_filename, postfix=None):
    if not postfix:
        return original_filename
    only_path = os.path.dirname(original_filename)
    only_filename = os.path.basename(original_filename)
    f_name, f_ext = os.path.splitext(only_filename)
    postfixed_fname = '{fname}_{postfix}{fext}'.format(
        fname=f_name,
        postfix=postfix,
        fext=f_ext
    )
    return os.path.join(only_path, postfixed_fname)
