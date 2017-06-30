# coding: utf-8
from __future__ import absolute_import

import os

from contrib.utils.file import (add_postfix_to_filename,
                                add_prefix_to_filename,
                                generate_unique_filename,
                                make_path)
from flask import current_app
from PIL import Image
from six import string_types
from wtforms import FileField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import ValidationError
from wtforms.widgets import CheckboxInput

from . import WidgetPrebind
from .widgets import CustomizedList, UploadInput, SelectOptGroup
from ..data.attachment import Attachment


# iter_group() and SelectOptGroupField used from: http://richard.to/programming/project-wonderchicken-part-2.html
def iter_groups(values, data, coerce):
    for value, label in values:
        selected = data is not None and coerce(value) in data
        yield (value, label, selected)


class SelectOptGroupField(SelectField):
    widget = SelectOptGroup(multiple=False)

    def iter_choices(self):
        for value, label in self.choices:
            if type(value) is not tuple:
                yield (value, label, self.coerce(value) == self.data)
            else:
                selected = False
                yield (lambda: iter_groups(value, self.data, self.coerce), label, False)

    def pre_validate(self, form):
        values = []

        if self.data:
            for v, _ in self.choices:
                if type(v) is tuple:
                    values.extend([cv for cv, _ in v])
                else:
                    values.append(v)
            if self.data not in values:
                raise ValidationError(self.gettext(
                    "'%(value)s' is not a valid choice for this field") % dict(value=v))


class RefQuerySelectMultipleField(QuerySelectMultipleField):
    """
    Поле множественного выбора для работы с ValueSet.
    """
    option_widget = CheckboxInput()

    def __init__(self, *args, **kwargs):
        self.widget = WidgetPrebind(
            CustomizedList(prefix_label=False),
            class_='uk-list'
        )
        super(RefQuerySelectMultipleField, self).__init__(*args, **kwargs)

    def labels_list(self):
        selections = [label for value, label, selected in self.iter_choices() if selected]
        result = u', '.join(selections)
        return result


class UploadField(FileField):
    widget = UploadInput()

    def __init__(self, label=None, upload_folder=None, make_preview=True,
                 preview_sizes=list(), **kwargs):
        self.upload_folder = upload_folder
        self.make_preview = make_preview
        self.preview_sizes = [  # preview_sizes if preview_sizes else [
            (1920, 0), (1125, 0), (750, 0)]
        super(UploadField, self).__init__(label, **kwargs)

    def populate_obj(self, obj, name):
        data = {}
        data_folder = full_data_folder = current_app.config.get('PUBLIC_ROOT')

        if self.upload_folder:
            full_data_folder = os.path.join(data_folder, self.upload_folder)

        if self.data:
            filename_path = None

            if isinstance(self.data, string_types):
                if self.data == 'already':  # Изображение уже загружено
                    data = getattr(obj, name)
                    filename_path = data.url
                    data = data.as_json()

            if not isinstance(self.data, string_types):
                # Новое изображение
                path_from_uuid = make_path()
                full_path = os.path.join(*path_from_uuid)

                # Создаём сгенерированные папки
                if not os.path.exists(os.path.join(full_data_folder, full_path)):
                    os.makedirs(os.path.join(full_data_folder, full_path))

                # Генерируем имя файла
                fname = generate_unique_filename(self.data.filename)

                if self.upload_folder:
                    only_path = os.path.join(self.upload_folder, full_path)
                else:
                    only_path = os.path.join(full_path)

                filename_path = os.path.join(only_path, fname)

                data.setdefault('original_filename', self.data.filename)
                data.setdefault('url', filename_path)
                data.setdefault('filename', fname)
                data.setdefault('path', only_path)

                self.data.save(os.path.join(data_folder, filename_path))

            previews = []
            if self.make_preview and filename_path:
                try:
                    height = 200
                    width = 0
                    file_to_preview = os.path.join(data_folder, filename_path)
                    image = Image.open(file_to_preview)
                    preview_filename = add_prefix_to_filename(file_to_preview,
                                                              'preview_')
                    if image.size[0] < image.size[1]:
                        width = int(image.size[1] / image.size[0] * height)
                    else:
                        width = int(image.size[0] / image.size[1] * height)
                    image.thumbnail((width, height), Image.ANTIALIAS)
                    image.save(preview_filename,
                               optimize=True,
                               subsampling=2,
                               quality=80)
                    previews.append(dict(width=200, height=200))
                except Exception as e:
                    current_app.logger.exception(e)
        else:
            # Если уже есть установленные файлы их необходимо удалить
            data = getattr(obj, name, None)
            if isinstance(data, Attachment):
                if data.as_json():
                    if data.url:
                        # Оригинальный файл
                        files = list()
                        files.append(os.path.join(data_folder, data.url))
                        files.append(
                            os.path.join(data_folder, add_prefix_to_filename(
                                data.url, 'preview_'))
                        )

                        for postfix in [750, 1125, 1920]:
                            files.append(os.path.join(data_folder,
                                                      add_postfix_to_filename(
                                                          data.url,
                                                          postfix
                                                      )))

                        for f in files:
                            if os.path.exists(f):
                                os.remove(f)

        setattr(obj, name, data)
