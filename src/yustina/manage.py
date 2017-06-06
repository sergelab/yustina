# coding: utf-8
from __future__ import absolute_import

from .commands.babel import compile_messages, make_messages
from .init import app


app.cli.add_command(make_messages, 'makemessages')
app.cli.add_command(compile_messages, 'compilemessages')
