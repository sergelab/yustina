# coding: utf-8
from __future__ import absolute_import

import click
import gettext
import json
import os

from flask.cli import with_appcontext
from subprocess import call

from ..init import app


@app.cli.command('makemessages')
@click.option('--locale', '-l')
@with_appcontext
def make_messages(locale):
    """ Extract and make messages. """
    script = os.environ['PYBABEL'] if 'PYBABEL' in os.environ else 'pybabel'
    config_file = os.path.relpath(os.path.join(
        app.config.get('PROJECT_DIR'), 'config', 'translate.cfg'))
    translations_dir = os.path.relpath(os.path.join(
        app.config.get('PROJECT_DIR'), 'translations'))
    pot_file = os.path.relpath(os.path.join(translations_dir, 'messages.pot'))

    def __extract__():
        call([script, 'extract', '-F', config_file, '-k' 'lazy_gettext', '-k', '__', '-o', pot_file, '.'])

    def __update__(locale):
        if os.path.exists(os.path.join(translations_dir, locale, 'LC_MESSAGES', 'messages.po')):
            call([script, 'update', '-i', pot_file, '-d', translations_dir, '-l', locale])
        else:
            call([script, 'init', '-i', pot_file, '-d', translations_dir, '-l', locale])

    __extract__()

    if locale is None:
        for locale in app.config.get('LANGUAGES', {}):
            __update__(locale)
    else:
        __update__(locale)


@app.cli.command('compilemessages')
@click.option('--locale', '-l')
@with_appcontext
def compile_messages(locale):
    """ Compile messages. """
    script = os.environ['PYBABEL'] if 'PYBABEL' in os.environ else 'pybabel'
    translations_dir = os.path.relpath(os.path.join(app.config.get('PROJECT_DIR'),
                                                    'translations'))

    def __tojson__(locale):
        try:
            tr = gettext.translation('messages', translations_dir, [locale])
            keys = tr._catalog.keys()
            key = sorted(keys)
            ret = {}
            for k in keys:
                v = tr._catalog[k]
                if type(k) is tuple:
                    if k[0] not in ret:
                        ret[k[0]] = []
                    ret[k[0]].append(v)
                else:
                    ret[k] = v
            name = '{0}.json'.format(locale)
            with open(os.path.join(translations_dir, locale, name), 'w') as f:
                click.echo('updating catalog "{0}"'.format(
                    os.path.join(translations_dir, locale, name)))
                f.write(json.dumps(ret, ensure_ascii=True, indent=app.debug))
                f.close()
        except IOError as e:
            click.echo('I/O error ({0})'.format(e))

    def __compile__(loc):
        call([script, 'compile', '-d', translations_dir, '-l', loc])
        __tojson__(loc)

    if locale is None:
        for locale in app.config.get('LANGUAGES', {}).keys():
            __compile__(locale)
    else:
        __compile__(locale)
