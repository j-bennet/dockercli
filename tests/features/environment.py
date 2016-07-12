# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import os
import fixture_utils as fixutils
import docker_utils as dutils

DEBUG_ON_ERROR = False


def before_all(context):
    """
    Set env parameters.
    """
    global DEBUG_ON_ERROR
    DEBUG_ON_ERROR = context.config.userdata.getbool('DEBUG_ON_ERROR')

    os.environ['LINES'] = "50"
    os.environ['COLUMNS'] = "120"
    os.environ['PAGER'] = 'cat'

    context.data_dir = fixutils.get_data_dir()
    context.fixture_lines = fixutils.read_fixture_files()
    context.client = dutils.init_docker_client()
    dutils.pull_required_images(context.client)
    context.exit_sent = False


def after_scenario(context, _):
    """
    Cleans up after each test complete.
    """

    if hasattr(context, 'cli') and not context.exit_sent:
        # Terminate the cli nicely.
        context.cli.terminate()


def after_step(_, step):
    if DEBUG_ON_ERROR and step.status == 'failed':
        import ipdb
        ipdb.post_mortem(step.exc_traceback)