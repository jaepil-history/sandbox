# Copyright (c) 2013 Appspand, Inc.

import json

from boto import sqs
from boto.sqs import jsonmessage

from log import logger
import message.controller
from util import timestamp


SQS = sqs.connect_to_region(aws_access_key_id="AKIAIFHFM4CZA26UVV4A",
                            aws_secret_access_key="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",
                            region_name="ap-southeast-1",
                            path="/")

SQS_QUEUE_TO_SNEK = "MSG_FROM_APPSPAND_TO_SNEK"
SQS_QUEUE_FROM_SNEK = "MSG_FROM_SNEK_TO_APPSPAND"

SQS_QUEUE_TO_SNEK = SQS.get_queue(SQS_QUEUE_TO_SNEK)
SQS_QUEUE_FROM_SNEK = SQS.get_queue(SQS_QUEUE_FROM_SNEK)


def push(sender_uid, group_uid, target_uids, message_info):
    push_body = {
        "sender_uid": sender_uid,
        "group_uid": group_uid,
        "target_uids": target_uids,
        "message_info": {
            "message_uid": message_info.uid,
            "sender_uid": message_info.sender_uid,
            "group_uid": message_info.group_uid,
            "message": message_info.message,
            "countdown": message_info.countdown,
            "issued_at": timestamp.get_timestamp(message_info.issued_at),
            "expires_at": timestamp.get_timestamp(message_info.expires_at)
        }
    }
    push_message = jsonmessage.JSONMessage(body=push_body)
    SQS_QUEUE_TO_SNEK.write(push_message)
    logger.access.debug("pushed to snek: %r" % push_body)


def pull():
    result = []
    items = SQS_QUEUE_FROM_SNEK.get_messages(wait_time_seconds=2)
    if items:
        for item in items:
            item_body = item.get_body()
            result.append(item_body)

        SQS_QUEUE_FROM_SNEK.delete_message_batch(items)

    return result
