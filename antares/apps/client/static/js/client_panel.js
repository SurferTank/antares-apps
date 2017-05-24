/**
 * 
 * 
 */
function display_client_panel(client_id, main_branch_id) {
	if (client_id && client_id.length>0) {
        $("#clientPanel").show();
    }
	
    if (antaresClientLinks.user_relations_call) {
        $('#relations_table')
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
                    'url': antaresClientLinks.user_relations_call,
                    'data': {
                        'csrfmiddlewaretoken': $.cookie('csrftoken'),
                        'client_id': client_id,
                    },
                    'method': 'GET',
                    'type': 'json',

                },
                'language': {
                    'emptyTable': gettext('antares.apps.client.templates.emptyMessages.no_relations_set'),
                },
                'fnDrawCallback': function(oSettings) {
                    if (oSettings._iDisplayLength >= oSettings.fnRecordsDisplay()) {
                        $(oSettings.nTableWrapper).find('.dataTables_paginate').hide();
                    } else {
                        $(oSettings.nTableWrapper).find('.dataTables_paginate').show();
                    }
                },
            });
    }
    if (antaresClientLinks.attributes_view_call) {
        $('#client_attributes_table')
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
                    'url': antaresClientLinks.attributes_view_call,
                    'data': {
                        'csrfmiddlewaretoken': $.cookie('csrftoken'),
                        'client_id': client_id,
                    },
                    'method': 'GET',
                    'type': 'json',

                },
                'language': {
                    'emptyTable': gettext('antares.apps.client.templates.emptyMessages.no_attributes_set'),
                },
                'fnDrawCallback': function(oSettings) {
                    if (oSettings._iDisplayLength >= oSettings.fnRecordsDisplay()) {
                        $(oSettings.nTableWrapper).find('.dataTables_paginate').hide();
                    } else {
                        $(oSettings.nTableWrapper).find('.dataTables_paginate').show();
                    }
                },
            });
    }


    if (antaresClientLinks.client_id_call) {
        $('#client_id_table').DataTable({
            'paging': true,
            'processing': true,
            'serverSide': true,
            'info': false,
            'searching': false,
            'bLengthChange': false,
            'iDisplayLength': 15,
            'conditionalPaging': true,
            'ajax': {
                'url': antaresClientLinks.client_id_call,
                'data': {
                    'csrfmiddlewaretoken': $.cookie('csrftoken'),
                    'client_id': client_id,
                },
                'method': 'GET',
                'type': 'json',

            },
            'language': {
                'emptyTable': gettext('antares.apps.client.templates.emptyMessages.no_client_ids_set'),
            },
            'fnDrawCallback': function(oSettings) {
                if (oSettings._iDisplayLength >= oSettings.fnRecordsDisplay()) {
                    $(oSettings.nTableWrapper).find('.dataTables_paginate').hide();
                } else {
                    $(oSettings.nTableWrapper).find('.dataTables_paginate').show();
                }
            },
        });
    }

    if (antaresClientLinks.address_list_call) {
        $('#address_id_table').DataTable({
            'paging': true,
            'processing': true,
            'serverSide': true,
            'info': false,
            'searching': false,
            'bLengthChange': false,
            'iDisplayLength': 15,
            'conditionalPaging': true,
            'ajax': {
                'url': antaresClientLinks.address_list_call,
                'data': {
                    'csrfmiddlewaretoken': $.cookie('csrftoken'),
                    'branch_id': main_branch_id,
                },
                'method': 'GET',
                'type': 'json',

            },
            'language': {
                'emptyTable': gettext('antares.apps.client.templates.emptyMessages.no_addresses_set'),
            },
            'fnDrawCallback': function(oSettings) {
                if (oSettings._iDisplayLength >= oSettings.fnRecordsDisplay()) {
                    $(oSettings.nTableWrapper).find('.dataTables_paginate').hide();
                } else {
                    $(oSettings.nTableWrapper).find('.dataTables_paginate').show();
                }
            },
        });
    }

    if (antaresClientLinks.business_classification_list_call) {
        $('#business_classification_id_table').DataTable({
            'paging': true,
            'processing': true,
            'serverSide': true,
            'info': false,
            'searching': false,
            'bLengthChange': false,
            'iDisplayLength': 15,
            'conditionalPaging': true,
            'ajax': {
                'url': antaresClientLinks.business_classification_list_call,
                'data': {
                    'csrfmiddlewaretoken': $.cookie('csrftoken'),
                    'branch_id': main_branch_id,
                },
                'method': 'GET',
                'type': 'json',

            },
            'language': {
                'emptyTable': gettext('antares.apps.client.templates.emptyMessages.no_business_classification_set'),
            },
            'fnDrawCallback': function(oSettings) {
                if (oSettings._iDisplayLength >= oSettings.fnRecordsDisplay()) {
                    $(oSettings.nTableWrapper).find('.dataTables_paginate').hide();
                } else {
                    $(oSettings.nTableWrapper).find('.dataTables_paginate').show();
                }
            },
        });
    }

    if (antaresClientLinks.email_list_call) {
        $('#email_id_table').DataTable({
            'paging': true,
            'processing': true,
            'serverSide': true,
            'info': false,
            'searching': false,
            'bLengthChange': false,
            'iDisplayLength': 15,
            'conditionalPaging': true,
            'ajax': {
                'url': antaresClientLinks.email_list_call,
                'data': {
                    'csrfmiddlewaretoken': $.cookie('csrftoken'),
                    'branch_id': main_branch_id,
                },
                'method': 'GET',
                'type': 'json',

            },
            'language': {
                'emptyTable': gettext('antares.apps.client.templates.emptyMessages.no_email_set'),
            },
            'fnDrawCallback': function(oSettings) {
                if (oSettings._iDisplayLength >= oSettings.fnRecordsDisplay()) {
                    $(oSettings.nTableWrapper).find('.dataTables_paginate').hide();
                } else {
                    $(oSettings.nTableWrapper).find('.dataTables_paginate').show();
                }
            },
        });
    }

    if (antaresClientLinks.telephone_list_call) {
        $('#telephone_table').DataTable({
            'paging': true,
            'processing': true,
            'serverSide': true,
            'info': false,
            'searching': false,
            'bLengthChange': false,
            'iDisplayLength': 15,
            'conditionalPaging': true,
            'ajax': {
                'url': antaresClientLinks.telephone_list_call,
                'data': {
                    'csrfmiddlewaretoken': $.cookie('csrftoken'),
                    'branch_id': main_branch_id,
                },
                'method': 'GET',
                'type': 'json',

            },
            'language': {
                'emptyTable': gettext('antares.apps.client.templates.emptyMessages.no_telephone_set'),
            },
            'fnDrawCallback': function(oSettings) {
                if (oSettings._iDisplayLength >= oSettings.fnRecordsDisplay()) {
                    $(oSettings.nTableWrapper).find('.dataTables_paginate').hide();
                } else {
                    $(oSettings.nTableWrapper).find('.dataTables_paginate').show();
                }
            },
        });

    }

    if (antaresClientLinks.socialnetwork_list_call) {
        $('#social_network_table').DataTable({
            'paging': true,
            'processing': true,
            'serverSide': true,
            'info': false,
            'searching': false,
            'bLengthChange': false,
            'iDisplayLength': 15,
            'conditionalPaging': true,
            'ajax': {
                'url': antaresClientLinks.socialnetwork_list_call,
                'data': {
                    'csrfmiddlewaretoken': $.cookie('csrftoken'),
                    'branch_id': main_branch_id,
                },
                'method': 'GET',
                'type': 'json',

            },
            'language': {
                'emptyTable': gettext('antares.apps.client.templates.emptyMessages.no_social_networks_set'),
            },
            'fnDrawCallback': function(oSettings) {
                if (oSettings._iDisplayLength >= oSettings.fnRecordsDisplay()) {
                    $(oSettings.nTableWrapper).find('.dataTables_paginate').hide();
                } else {
                    $(oSettings.nTableWrapper).find('.dataTables_paginate').show();
                }
            },
        });
    }

}


function display_client_panel_by_branch(index, branch_id) {

    if (antaresClientLinks.address_list_call) {
        $('#address_id_table_' + index).DataTable({
            'paging': true,
            'processing': true,
            'serverSide': true,
            'info': false,
            'searching': false,
            'bLengthChange': false,
            'iDisplayLength': 15,
            'conditionalPaging': true,
            'ajax': {
                'url': antaresClientLinks.address_list_call,
                'data': {
                    'csrfmiddlewaretoken': $.cookie('csrftoken'),
                    'branch_id': branch_id,
                },
                'method': 'GET',
                'type': 'json',

            },
            'language': {
                'emptyTable': gettext('antares.apps.client.templates.emptyMessages.no_addresses_set'),
            },
            'fnDrawCallback': function(oSettings) {
                if (oSettings._iDisplayLength >= oSettings.fnRecordsDisplay()) {
                    $(oSettings.nTableWrapper).find('.dataTables_paginate').hide();
                } else {
                    $(oSettings.nTableWrapper).find('.dataTables_paginate').show();
                }
            },
        });
    }
    if (antaresClientLinks.email_list_call) {
        $('#email_id_table_' + index).DataTable({
            'paging': true,
            'processing': true,
            'serverSide': true,
            'info': false,
            'searching': false,
            'bLengthChange': false,
            'iDisplayLength': 15,
            'conditionalPaging': true,
            'ajax': {
                'url': antaresClientLinks.email_list_call,
                'data': {
                    'csrfmiddlewaretoken': $.cookie('csrftoken'),
                    'branch_id': branch_id,
                },
                'method': 'GET',
                'type': 'json',

            },
            'language': {
                'emptyTable': gettext('antares.apps.client.templates.emptyMessages.no_email_set'),
            },
            'fnDrawCallback': function(oSettings) {
                if (oSettings._iDisplayLength >= oSettings.fnRecordsDisplay()) {
                    $(oSettings.nTableWrapper).find('.dataTables_paginate').hide();
                } else {
                    $(oSettings.nTableWrapper).find('.dataTables_paginate').show();
                }
            },
        });

    }

    if (antaresLink.business_classification_list_call) {
        $('#business_classification_id_table_' + index).DataTable({
            'paging': true,
            'processing': true,
            'serverSide': true,
            'info': false,
            'searching': false,
            'bLengthChange': false,
            'iDisplayLength': 15,
            'conditionalPaging': true,
            'ajax': {
                'url': antaresLink.business_classification_list_call,
                'data': {
                    'csrfmiddlewaretoken': $.cookie('csrftoken'),
                    'branch_id': branch_id,
                },
                'method': 'GET',
                'type': 'json',

            },
            'language': {
                'emptyTable': gettext('antares.apps.client.templates.emptyMessages.no_business_classification_set'),
            },
            'fnDrawCallback': function(oSettings) {
                if (oSettings._iDisplayLength >= oSettings.fnRecordsDisplay()) {
                    $(oSettings.nTableWrapper).find('.dataTables_paginate').hide();
                } else {
                    $(oSettings.nTableWrapper).find('.dataTables_paginate').show();
                }
            },
        });
    }
    if (antaresClientLinks.telephone_list_call) {
        $('#telephone_table_' + index).DataTable({
            'paging': true,
            'processing': true,
            'serverSide': true,
            'info': false,
            'searching': false,
            'bLengthChange': false,
            'iDisplayLength': 15,
            'conditionalPaging': true,
            'ajax': {
                'url': antaresClientLinks.telephone_list_call,
                'data': {
                    'csrfmiddlewaretoken': $.cookie('csrftoken'),
                    'branch_id': branch_id,
                },
                'method': 'GET',
                'type': 'json',

            },
            'language': {
                'emptyTable': gettext('antares.apps.client.templates.emptyMessages.no_telephone_set'),
            },
            'fnDrawCallback': function(oSettings) {
                if (oSettings._iDisplayLength >= oSettings.fnRecordsDisplay()) {
                    $(oSettings.nTableWrapper).find('.dataTables_paginate').hide();
                } else {
                    $(oSettings.nTableWrapper).find('.dataTables_paginate').show();
                }
            },
        });
    }
    if (antaresClientLinks.socialnetwork_list_call) {
        $('#social_network_table_' + index).DataTable({
            'paging': true,
            'processing': true,
            'serverSide': true,
            'info': false,
            'searching': false,
            'bLengthChange': false,
            'iDisplayLength': 15,
            'conditionalPaging': true,
            'ajax': {
                'url': antaresClientLinks.socialnetwork_list_call,
                'data': {
                    'csrfmiddlewaretoken': $.cookie('csrftoken'),
                    'branch_id': branch_id,
                },
                'method': 'GET',
                'type': 'json',

            },
            'language': {
                'emptyTable': gettext('antares.apps.client.templates.emptyMessages.no_social_networks_set'),
            },
            'fnDrawCallback': function(oSettings) {
                if (oSettings._iDisplayLength >= oSettings.fnRecordsDisplay()) {
                    $(oSettings.nTableWrapper).find('.dataTables_paginate').hide();
                } else {
                    $(oSettings.nTableWrapper).find('.dataTables_paginate').show();
                }
            },
        });
    }


}