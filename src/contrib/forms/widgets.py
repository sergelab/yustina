# coding: utf-8
from __future__ import absolute_import

from cgi import escape
from flask_babel import lazy_gettext as __
from wtforms.compat import text_type
from wtforms.widgets import ListWidget, Select
from wtforms.widgets import html_params, HTMLString


date_widget_params = {'data-uk-datepicker': "{format:'DD-MM-YYYY'}",
                      'placeholder': __('Date field placeholder')}


class SelectOptGroup(object):
    """
    Виджет для работы с выпадающим списком имеющим группы.
    """
    def __init__(self, multiple=False):
        self.multiple = multiple

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)

        if self.multiple:
            kwargs['multiple'] = True

        html = ['<select %s>' % html_params(name=field.name, **kwargs)]

        for val, label, selected in field.iter_choices():
            if callable(val):
                html.append('<optgroup label="%s">' % escape(text_type(label)))

                for child_val, child_label, child_selected in val():
                    html.append(Select.render_option(child_val, child_label, child_selected))

                html.append('</optgroup>')
            else:
                html.append(Select.render_option(val, label, selected))

        html.append('</select>')
        return HTMLString(''.join(html))


class CustomizedList(ListWidget):
    """
    Переопределяем ListWidget, оборачиваем в контейнер
    """
    def __init__(self, html_tag='ul', prefix_label=True, use_box=True, **kwargs):
        self.use_box = use_box
        super(CustomizedList, self).__init__(html_tag,
                                             prefix_label,
                                             **kwargs)

    def __call__(self, *args, **kwargs):
        html = list()
        if self.use_box:
            html.append('<div class="uk-scrollable-box">')
        html.append(super(CustomizedList, self).__call__(
            *args, **kwargs))
        if self.use_box:
            html.append('</div>')
        return HTMLString(''.join(html))
