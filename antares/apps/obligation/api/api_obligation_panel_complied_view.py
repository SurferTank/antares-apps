import logging
import uuid

from django.urls import reverse
from django.utils.translation import ugettext as _
from django_datatables_view.base_datatable_view import BaseDatatableView

from antares.apps.client.models import Client
from antares.apps.core.constants import FieldDataType
from antares.apps.core.middleware.request import get_request
from antares.apps.core.models import UserParameter
from antares.apps.flow.models import FlowActivity

from ..constants import ObligationType, ObligationStatusType
from ..models import ObligationVector


logger = logging.getLogger(__name__)


class ApiObligationPanelCompliedView(BaseDatatableView):
    model = ObligationVector
    columns = [
        'type',
        'concept_type',
        'period',
        'due_date',
        'compliance_date',
        'status',
        'actions',
    ]
    order_columns = [
        'id',
        'concept_type.id',
        'period',
        'due_date',
        'compliance_date'
        'status',
        '',
    ]

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 50

    def __init__(self):
        self.date_format_string = UserParameter.find_one( 'CORE_TEMPLATE_DATE_FORMAT',
            FieldDataType.STRING, '%Y-%m-%d')
        self.client = None
        self.activity = None

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'type':
            if ObligationType.to_enum(row.obligation_type) is not None:
                return _(
                    ObligationType.to_enum(row.obligation_type).get_label())
            else:
                return None

        if column == 'concept_type':
            if row.concept_type.concept_type_name:
                return row.concept_type.concept_type_name
            elif row.concept_type.id:
                return str(row.concept_type.id)
            else:
                return None

        if column == 'period':
            if row.period:
                return row.period
            else:
                return None

        if column == 'due_date':
            if row.due_date:
                return row.due_date.strftime(self.date_format_string)
            else:
                return None
        if column == 'compliance_date':
            if row.compliance_date:
                return row.compliance_date.strftime(self.date_format_string)
            else:
                return None
        if column == 'status':
            if ObligationStatusType.to_enum(row.status) is not None:
                return _(ObligationStatusType.to_enum(row.status).get_label())
            else:
                return None
        if column == 'actions':
            if ObligationType.to_enum(
                    row.obligation_type) != ObligationType.INFORM:
                link_string = '<a href="{document_view}?next={obligation_panel}{activity_ref}"><i class="fa fa-eye" ' + \
                    ' aria-hidden="true"></i></a>'
                if (self.activity is None):
                    return link_string.format(
                        document_view=reverse(
                            "antares.apps.document:view_view",
                            kwargs={
                                'document_id': str(row.compliance_document.id)
                            }),
                        obligation_panel=reverse(
                            'antares.apps.obligation:panel_view'),
                        activity_ref='')
                else:
                    return link_string.format(
                        document_view=reverse(
                            "antares.apps.document:view_view",
                            kwargs={
                                'document_id': str(row.compliance_document.id)
                            }),
                        obligation_panel=reverse(
                            'antares.apps.flow:dashboard_view',
                            kwargs={'activity_id': str(self.activity.id)}),
                        activity_ref='&activity_id={activity_id}'.format(
                            activity_id=self.activity.id))
            else:
                return '<a href="#" onClick="alert(\'Not implemented yet\');"><i class="fa fa-eye" aria-hidden="true"></i></a>'
        else:
            return super(ApiObligationPanelCompliedView, self).render_column(
                row, column)

    def filter_queryset(self, qs):
        if (self.request.GET.get('activity_id')):
            self.activity = FlowActivity.find_one(
                uuid.UUID(self.request.GET.get('activity_id')))

        if (self.request.GET.get('client_id')):
            self.client = Client.find_one(
                uuid.UUID(self.request.GET.get('client_id')))
            if (self.client is None):
                raise ValueError(
                    _(__name__ + '.exceptions.client_does_not_exist'))
        else:
            self.client = get_request().user.get_on_behalf_client()

        qs = ObligationVector.find_by_client_and_status(
            self.client, 'Compliant')
        return qs
