/**
 * 
 */

function display_pending_obligations(client_id, display=10)
{
	 if (antaresObligationLinks.obligations_pending_view) {
        $('#pendingObligationsTable')
            .DataTable({
                'paging': true,
                'processing': true,
                'serverSide': true,
                'info': false,
                'searching': false,
                'bLengthChange': false,
                'iDisplayLength': display,
                'conditionalPaging': true,
                'ajax': {
                    'url': antaresObligationLinks.obligations_pending_view,
                    'type': 'GET',
                    'dataType': 'json',
                    'data': {
                        'client_id': client_id,
                        'obligation_type': 'File',
                        'csrfmiddlewaretoken': '{{ csrf_token }}',
                    }
                },
                'language': {
                    'emptyTable': gettext('antares.apps.obligation.templates.emptyMessages.no_pending_obligations_found')
                },
                'aoColumnDefs': [{
                    'bSortable': false,
                    'aTargets': [5 ]
                }],
                'fnDrawCallback': function(oSettings) {
                    if (oSettings._iDisplayLength >= oSettings
                        .fnRecordsDisplay()) {
                        $(oSettings.nTableWrapper).find(
                            '.dataTables_paginate').hide();
                    } else {
                        $(oSettings.nTableWrapper).find(
                            '.dataTables_paginate').show();
                    }
                },
            });
    }
}

function display_completed_obligations(client_id, display=10) {
	 if (antaresObligationLinks.obligations_complied_view) {
        $('#compliedObligationsTable')
            .DataTable({
                'paging': true,
                'processing': true,
                'serverSide': true,
                'info': false,
                'searching': false,
                'bLengthChange': false,
                'iDisplayLength': display,
                'conditionalPaging': true,
                'ajax': {
                    'url': antaresObligationLinks.obligations_complied_view,
                    'type': 'GET',
                    'dataType': 'json',
                    'data': {
                        'client_id': client_id,
                        'obligation_type': 'File',
                        'csrfmiddlewaretoken': '{{ csrf_token }}',
                    }
                },
                'language': {
                    'emptyTable': gettext('antares.apps.obligation.templates.emptyMessages.no_complied_obligations_found')
                },
                'aoColumnDefs': [{
                    'bSortable': false,
                    'aTargets': [1, 5, 6]
                }],
                'fnDrawCallback': function(oSettings) {
                    if (oSettings._iDisplayLength >= oSettings
                        .fnRecordsDisplay()) {
                        $(oSettings.nTableWrapper).find(
                            '.dataTables_paginate').hide();
                    } else {
                        $(oSettings.nTableWrapper).find(
                            '.dataTables_paginate').show();
                    }
                },

            });
    }
}

function display_obligations_panel(client_id) {
    display_pending_obligations(client_id);
    display_completed_obligations(client_id);
}

