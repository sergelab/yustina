# coding: utf-8
from __future__ import absolute_import

from cgi import escape
from flask_babel import lazy_gettext as __
from wtforms.compat import text_type
from wtforms.widgets import FileInput, ListWidget, Select, TextArea
from wtforms.widgets import html_params, HTMLString


date_widget_params = {'data-uk-datepicker': "{format:'DD.MM.YYYY'}",
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


class CustomizedListWidget(ListWidget):
    """
    Переопределенный виджет для списка с возможностью
    проброса дополнительных параметров в subfield.
    """
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)

        # Для subfield необходимо прокидывать параметр виджета disabled
        disabled = kwargs.get('disabled')
        subfield_kwargs = dict()
        if disabled is not None:
            subfield_kwargs.setdefault('disabled', disabled)

        html = ['<%s %s>' % (self.html_tag, html_params(**kwargs))]
        for subfield in field:
            if self.prefix_label:
                html.append('<li>%s %s</li>' % (subfield.label, subfield(**subfield_kwargs)))
            else:
                html.append('<li>%s %s</li>' % (subfield(**subfield_kwargs), subfield.label))
        html.append('</%s>' % self.html_tag)
        return HTMLString(''.join(html))


class CustomizedList(CustomizedListWidget):
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


class TextileWidget(TextArea):
    def __init__(self, height=350, **kwargs):
        self.height = height

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = list()
        html.append(u'<div data-textile>')
        html.append(u'<div class="uk-grid" style="height:auto;">')
        html.append(u'<div class="uk-width-1-2">')
        html.append(super(TextileWidget, self).__call__(field, **kwargs))
        html.append(u'</div>')
        html.append(u'<div class="uk-width-1-2">')
        html.append(u'<ul class="uk-tab" data-uk-tab="{{connect:\'#{0}_tabs\'}}">'.format(field.id))
        html.append(u'<li class="uk-active"><a href="#">{0}</a></li>'.format(__('Textile preview tab')))
        html.append(u'<li><a href="#">{0}</a></li>'.format(__('Textile help tab')))
        html.append(u'</ul>')
        html.append(u'<ul id="{0}_tabs" class="uk-switcher">'.format(field.id))
        html.append(u'<li style="padding:10px;">')
        html.append(u'<div class="js-textile_preview" style="'
                    u'overflow:auto;height:{0}px;" '
                    u'class="uk-width-1-1"></div>'.format(self.height))
        html.append(u'</li>')
        html.append(u'<li style="padding:10px;">')
        html.append(u'<div class="textile-help">{0}</div>'.format(__('Textile help text')))
        html.append(u'</li>')
        html.append(u'</ul>')
        html.append(u'</div>')
        html.append(u'</div>')
        html.append(u'</div>')
        return HTMLString(''.join(html))


class UploadInput(FileInput):
    """
    Виджет для работы с fileinput.js.
    """
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        class_ = kwargs.get('class_', '')
        class_ = class_ + ' file-uploader' if class_ else 'file-uploader'
        kwargs['class_'] = class_
        return HTMLString('<input %s>' % html_params(
            name=field.name,
            type='file',
            **kwargs
        ))
