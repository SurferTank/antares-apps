import logging
import uuid

from django.utils.translation import ugettext as _
from django_datatables_view.base_datatable_view import BaseDatatableView

from antares.apps.core.middleware.request import get_request

from ..constants import ItemStatusType, SocialNetworkItemType
from ..models import SocialNetworkItem, ClientBranch


logger = logging.getLogger(__name__)


class ApiBranchListSocialNetworkView(BaseDatatableView):
    model = SocialNetworkItem
    columns = [
        'social_network_type',
        'item',
        'is_principal',
        'status',
    ]
    order_columns = [
        'social_network_type',
        'item',
        'is_principal',
        'status',
    ]

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 50

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'social_network_type':
            social_network_type = SocialNetworkItemType.to_enum(
                row.social_network_type)
            if social_network_type is not None:
                return social_network_type.get_label()
            else:
                return None
        elif column == 'item':
            if (row.item):
                return row.item
            else:
                return None
        elif column == 'is_principal':
            if (row.is_principal == True):
                return _("True")
            else:
                return _("False")
        elif column == 'status':
            status = ItemStatusType.to_enum(row.status)
            if (status is not None):
                return status.get_label()
            else:
                return None
        else:
            return super(ApiBranchListSocialNetworkView, self).render_column(
                row, column)

    def filter_queryset(self, qs):
        if (self.request.GET.get('branch_id')):
            self.branch = ClientBranch.find_one(
                uuid.UUID(self.request.GET.get('branch_id')))
            if (self.branch is None):
                raise ValueError(
                    _(__name__ + '.exceptions.branch_does_not_exist'))
        else:
            try:
                self.branch = get_request().user.get_on_behalf_client(
                ).get_default_branch()
            except:
                self.branch = None

        qs = qs.filter(client_branch=self.branch)
        return qs
