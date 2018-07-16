# encoding: utf-8
import os, json, time

from django.conf import settings
from django.core.management import BaseCommand
from datetime import datetime
from webanalysis.models import AccessLog


class Command(BaseCommand):

    def handle(self, *args, **options):
        path = os.path.join(settings.BASE_DIR, 'media', 'notices')

        while True:
            lists = os.listdir(path)
            for filename in lists:
                notice = None
                path_notice = os.path.join(path, filename)
                with open(path_notice, 'rt') as fhandler:
                    notice = json.loads(fhandler.read())
                try:
                    self.parse(notice)
                except BaseException as e:
                    raise e
                
                os.unlink(path_notice)

            time.sleep(5)

    def parse(self,notice):
        file_id = notice['id']
        with open(notice.get('path'),'rt') as fhandler:
            for line in fhandler:
                nodes = line.split()
                log = AccessLog()
                log.file_id = file_id
                log.access_time=datetime.strptime(nodes[3], '[%d/%b/%Y:%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                log.ip = nodes[0]
                log.url = nodes[6]
                log.status_code = nodes[8]
                log.save()
        print('parse over: {0}'.format(notice['path']))
