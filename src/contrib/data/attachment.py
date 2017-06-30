# coding: utf-8
from __future__ import absolute_import

import logging
import os
import sys

from contrib.utils.file import add_postfix_to_filename


class ValidationError(Exception):
    def __init__(self, errors, path=None):
        if not isinstance(errors, list):
            errors = [TypeError(errors)]
        msgs = "\n  ".join([str(e).replace("\n", "\n  ") for e in errors])
        message = "{}:\n  {}".format(path or "{root}", msgs)
        super(ValidationError, self).__init__(message)
        self.errors = errors
        self.path = path

    def prefixed(self, path_prefix):
        path = '{0}.{1}'.format(path_prefix, self.path) if self.path is not None else path_prefix
        return self.__class__(self.errors, path)


class AbstractBase(object):
    def __init__(self, jsondict=None):
        self._owner = None

        if jsondict:
            try:
                self.update_with_json(jsondict)
            except ValidationError as e:
                for err in e.errors:
                    logging.warning(err)

    def as_json(self):
        js = {}
        errs = []

        found = set()
        nonoptionals = set()
        for name, jsname, typ, is_list, of_many, not_optional in self.elementProperties():
            if not_optional:
                nonoptionals.add(of_many or jsname)

            err = None
            value = getattr(self, name)
            if value is None:
                continue

            if is_list:
                if not isinstance(value, list):
                    err = TypeError("Expecting property \"{}\" on {} to be list, but is {}"
                                    .format(name, type(self), type(value)))
                elif len(value) > 0:
                    if not self._matches_type(value[0], typ):
                        err = TypeError("Expecting property \"{}\" on {} to be {}, but is {}"
                                        .format(name, type(self), typ, type(value[0])))
                    else:
                        lst = []
                        for v in value:
                            try:
                                lst.append(v.as_json() if hasattr(v, 'as_json') else v)
                            except ValidationError as e:
                                err = e.prefixed(name)
                        found.add(of_many or jsname)
                        js[jsname] = lst
            else:
                if not self._matches_type(value, typ):
                    err = TypeError("Expecting property \"{}\" on {} to be {}, but is {}"
                                    .format(name, type(self), typ, type(value)))
                else:
                    try:
                        found.add(of_many or jsname)
                        js[jsname] = value.as_json() if hasattr(value, 'as_json') else value
                    except ValidationError as e:
                        err = e.prefixed(name)

            if err is not None:
                errs.append(err if isinstance(err, ValidationError) else ValidationError([err], name))

        # any missing non-optionals?
        if len(nonoptionals - found) > 0:
            for nonop in nonoptionals - found:
                errs.append(KeyError("Property \"{}\" on {} is not optional, you must provide a value for it"
                                     .format(nonop, self)))

        if len(errs) > 0:
            raise ValidationError(errs)
        return js

    @classmethod
    def with_json(cls, jsonobj):
        if isinstance(jsonobj, dict):
            return cls._with_json_dict(jsonobj)

        if isinstance(jsonobj, list):
            return [cls._with_json_dict(jsondict) for jsondict in jsonobj]

        raise TypeError("`with_json()` on {} only takes dict or list of dict, but you provided {}"
                        .format(cls, type(jsonobj)))

    @classmethod
    def _with_json_dict(cls, jsondict):
        if not isinstance(jsondict, dict):
            raise TypeError("Can only use `_with_json_dict()` on {} with a dictionary, got {}"
                            .format(type(cls), type(jsondict)))
        return cls(jsondict)

    @classmethod
    def with_json_and_owner(cls, jsonobj, owner):
        instance = cls.with_json(jsonobj)
        if isinstance(instance, list):
            for inst in instance:
                inst._owner = owner
        else:
            instance._owner = owner

        return instance

    def update_with_json(self, jsondict):
        if jsondict is None:
            return
        if not isinstance(jsondict, dict):
            raise ValidationError("Non-dict type {0} fed to `update_with_json` or {1}".format(
                type(jsondict), type(self)
            ))
        errs = []
        found = set([])
        nonoptionals = set()

        for name, jsname, typ, is_list, of_many, not_optional in self.elementProperties():
            if not jsname in jsondict:
                if not_optional:
                    nonoptionals.add(of_many or jsname)
                continue

            err = None
            value = jsondict[jsname]

            if hasattr(typ, 'with_json_and_owner'):
                try:
                    value = typ.with_json_and_owner(value, self)
                except Exception as e:
                    value = None,
                    err = e

            if value is not None:
                testval = value
                if is_list:
                    if not isinstance(value, list):
                        err = TypeError('Wrong type {0} for list property "{1}" or {2}, '
                                        'expecting a list of {3}'.format(
                            type(value), name, type(self), typ
                        ))
                        testval = None
                    else:
                        testval = value[0] if value and len(value) > 0 else None

                if testval is not None and not self._matches_type(testval, typ):
                    err = TypeError('Wrong type {0} for property "{1}" on {2}, '
                                    'expecting {3}'.format(
                        type(testval), name, type(self), typ
                    ))
                else:
                    setattr(self, name, value)
            if err is not None:
                errs.append(err.prefixed(name) if isinstance(err, ValidationError)
                            else ValidationError([err], name))
            found.add(jsname)
            found.add('_' + jsname)
            if of_many is not None:
                found.add(of_many)

    def _matches_type(self, value, typ):
        if value is None:
            return True
        if isinstance(value, type):
            return True
        if int == typ or float == typ:
            return isinstance(value, int) or isinstance(value, float)
        if (sys.version_info < (3, 0)) and (str == typ or unicode == typ):
            return isinstance(value, str) or isinstance(value, unicode)
        return False

    def elementProperties(self):
        return []


class AttachmentThumbnail(AbstractBase):
    def __init__(self, jsondict=None):
        self.width = None
        self.height = None
        super(AttachmentThumbnail, self).__init__(jsondict=jsondict)

    def elementProperties(self):
        js = super(AttachmentThumbnail, self).elementProperties()
        js.extend([
            ('width', 'width', int, False, None, True),
            ('height', 'height', int, False, None, True)
        ])
        return js


class Attachment(AbstractBase):
    def __init__(self, jsondict=None):
        self.original_filename = None
        self.filename = None
        self.title = None
        self.url = None
        self.path = None
        self.thumbnails = None
        super(Attachment, self).__init__(jsondict=jsondict)

    def sized_url(self, width, height):
        if self.thumbnails:
            for preview in self.thumbnails:
                if preview.width == width and preview.height == height:
                    rfname = 'preview_{0}'.format(self.filename)
                    return os.path.join(self.path, rfname)
        return self.url

    def get_sized(self, size):
        if self.filename and self.path:
            return os.path.join(self.path, add_postfix_to_filename(self.filename,
                                                                   size))
        return None

    def preview(self):
        if self.filename and self.path:
            return os.path.join(self.path, 'preview_{0}'.format(self.filename))
        return None

    def original(self):
        if self.url:
            return self.url
        return None

    def elementProperties(self):
        js = super(Attachment, self).elementProperties()
        js.extend([
            ('original_filename', 'original_filename', str, False, None, False),
            ('path', 'path', str, False, None, False),
            ('filename', 'filename', str, False, None, False),
            ('url', 'url', str, False, None, False),
            ('title', 'title', str, False, None, False),
            ('thumbnails', 'thumbnails', AttachmentThumbnail, True, None, False)
        ])
        return js
