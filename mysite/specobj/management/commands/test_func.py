
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

        logger.info('=START==================================get_actual_specs')
        obj = Obj.objects.get(pk=1)
        today = datetime.date.today()
        pprint(get_actual_specs(obj, today))
        logger.info('=END====================================get_actual_specs\n')

        logger.info('=START==================================set_not_actual_specs')
        pprint(set_not_actual_specs(obj, today))
        logger.info('=END====================================set_not_actual_specs\n')

        logger.info('=START==================================set_delobj_not_actual_specs')
        pprint(set_delobj_not_actual_specs())
        logger.info('=END====================================set_delobj_not_actual_specs\n')

        logger.info('=START==================================del_is_delete_obj')
        pprint(del_is_delete_obj())
        logger.info('=END====================================del_is_delete_obj\n')