# coding: utf-8
from __future__ import absolute_import

from wtforms import SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import ValidationError
from wtforms.widgets import CheckboxInput

from . import WidgetPrebind
from .widgets import CustomizedList, SelectOptGroup


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
