import logging

from django.utils import timezone
from django.utils.translation import ugettext as _

from antares.apps.core.constants import FieldDataType
from antares.apps.core.constants import SystemModuleType
from antares.apps.core.models.system_parameter import SystemParameter
from antares.apps.document.types import Document
from antares.apps.message.constants import MessageStatusType
from antares.apps.message.models import MessageStatus
from antares.apps.user.models import User

from ..models import NotificationRecord
from ..models import NotificationRule


logger = logging.getLogger(__name__)


class NotificationManager(object):
    def __init__(self):
        pass

    @classmethod
    def post_document(cls, document: Document) -> None:
        status = MessageStatus.find_or_create_one(
            document=document, module=SystemModuleType.NOTIFICATIONS)
        if MessageStatusType.to_enum(
                status.status) != MessageStatusType.PENDING:
            return
        for rule in NotificationRule.find_by_form_definition(
                document.header.form_definition):
            data_type = document.get_field_data_type(rule.user_code_variable)
            if (data_type and data_type == FieldDataType.UUID):
                notification_user = User.find_one(
                    document.get_field_value(rule.user_code_variable))
                if (notification_user is None):
                    raise ValueError(
                        _(__name__ + ".exceptions.user_not_found"))

            data_type = document.get_field_data_type(rule.date_variable)
            if (data_type and data_type == FieldDataType.DATE):
                notification_date = document.get_field_value(
                    rule.date_variable)
                if (notification_date is None):
                    notification_date = timezone.now()
            else:
                notification_date = timezone.now()

            data_type = document.get_field_data_type(rule.content_variable)
            if (data_type and (data_type == FieldDataType.STRING
                               or data_type == FieldDataType.TEXT)):
                notification_contents = document.get_field_value(
                    rule.content_variable)
                if (notification_contents is None):
                    raise ValueError(
                        _(__name__ + ".exceptions.no_contents_available"))

            if rule.title_variable:
                data_type = document.get_field_data_type(rule.title_variable)
                if (data_type and (data_type == FieldDataType.STRING
                                   or data_type == FieldDataType.TEXT)):
                    notification_title = document.get_field_value(
                        rule.title_variable)
                    if (notification_title is None):
                        raise ValueError(
                            _(__name__ + ".exceptions.no_title_available"))
            else:
                notification_title = _(
                    SystemParameter.find_one(
                        "DEFAULT_NOTIFICATION_TITLE", FieldDataType.STRING,
                        __name__ + ".default.notification_title"))

            if document.get_author() is None:
                raise ValueError(
                    _(__name__ + ".exceptions.the_document_has_no_author"))

            #we have to check that everything is there to post a new record
            notification_record = NotificationRecord()
            notification_record.author = document.get_author()
            notification_record.content = notification_contents
            notification_record.title = notification_title
            notification_record.document = document
            notification_record.post_date = notification_date
            notification_record.save()

        status.set_status(MessageStatusType.PROCESSED)

    @classmethod
    def get_unread_notifications(max_days: int = 7):
        pass
