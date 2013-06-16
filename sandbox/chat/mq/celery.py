# Copyright (c) 2013 Appspand, Inc.

from __future__ import absolute_import

from celery import Celery

from chat.settings import base


config = base.parse_options()
celery = Celery(main="chat.mq", broker=config.celery_broker_url,
                #backend=config.celery_result_backend_url,
                include=["mq.tasks"])

# celery.conf.update(
#     CELERY_TASK_RESULT_EXPIRES=3600,
# )

if __name__ == '__main__':
    celery.start()
