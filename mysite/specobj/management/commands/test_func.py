
import logging
import sys

from django.core.management.base import BaseCommand

from ...models import Obj, Spec
from ...utils import *
from pprint import pprint

logger = logging.getLogger('test_func')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))


class Command(BaseCommand):

    def handle(self, *args, **options):

        logger.info('=START==================================get_actual_characteristics')
        obj = Obj.objects.get(pk=1)
        pprint(get_actual_characteristics(obj))
        logger.info('=END====================================get_actual_characteristics\n')

        logger.info('=START==================================get_actual_characteristics_today')
        pprint(get_actual_characteristics_today())
        logger.info('=END====================================get_actual_characteristics_today\n')

        logger.info('=START==================================get_actual_objects_today')
        pprint(get_actual_objects_today())
        logger.info('=END====================================get_actual_objects_today\n')
