/**
 * Copyright 2013-2017 SurferTank Inc. 
 * Original version by Leonardo Belen<leobelen@gmail.com> 
 */
function display_latest_documents(client_id) {
    console.log("showing latest documents with client_id=" + client_id);
    if ($.fn.dataTable.isDataTable('#documentLatestTable')) {
        $('#documentLatestTable').DataTable().destroy();
    }

    if (latestDocumentLinks.latest_documents_call) {
        $('#documentLatestTable')
            .DataTable({
                'paging': true,
                'processing': true,
                'serverSide': true,
                'info': false,
                'searching': false,
                'bLengthChange': false,
                'iDisplayLength': 15,
                'conditionalPaging': true,
                'ajax': {
                    'url': latestDocumentLinks.latest_documents_call,
                    'data': {
                        'csrfmiddlewaretoken': $.cookie('csrftoken'),
                        'client_id': client_id,
                    },
                    'method': 'GET',
                    'type': 'json',

                },
                'language': {
                    'emptyTable': gettext('antares.apps.documents.templates.emptyMessages.emptyList'),
                },
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