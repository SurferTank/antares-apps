/**
 * Copyright 2013-2017 SurferTank Inc. 
 * Original version by Leonardo Belen<leobelen@gmail.com> 
 */
function display_accounting_panel(client_id, client_name = null, document = null, document_name = null, concept_type_id = null, concept_type_name = null,
    period = null, account_type_id = null, account_type_name = null) {
    console.log("display_accounting_panel called with client_id=" + client_id + " client_name=" + client_name + " document=" 
    + document + " document_name=" + document_name + " concept_type_id=" + concept_type_id + " concept_type_name=" + concept_type_name + 
    " period="  + period + " account_type_id=" + account_type_id + "account_type_name=" + account_type_name);
    if (client_id && client_id.length>0) {
        $("#accountingPanel").show();
    }

    if (client_id && document == null && concept_type_id == null && period == null && account_type_id == null) {
        process_client_level(client_id, client_name);
    } else if (client_id && document == null && concept_type_id != null && period == null && account_type_id == null) {
        process_concept_type_level(client_id, client_name, concept_type_id, concept_type_name);
    } else if (client_id && document == null && concept_type_id !=null && period != null && account_type_id == null) {
        process_period_level(client_id, client_name, concept_type_id, concept_type_name, period);
    } else if (client_id && document == null && concept_type_id!= null && period!= null && account_type_id!= null) {
        process_account_type_level(client_id, client_name, concept_type_id, concept_type_name, period, 
        		account_type_id, account_type_name);
    }else{
    	 console.log("nothing gets processed");
    }


}

function process_client_level(client_id) {
	console.log("process_client_level called with client_id=" + client_id);
    if ($.fn.dataTable.isDataTable('#clientAccountingTable')) {
        $('#clientAccountingTable').DataTable().destroy();
    }

    if (antaresAccountingLinks.client_panel_call) {
        $('#clientAccountingTable')
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
                    'url': antaresAccountingLinks.client_panel_call,
                    'data': {
                        'csrfmiddlewaretoken': $.cookie('csrftoken'),
                        'client_id': client_id,
                    },
                    'method': 'GET',
                    'type': 'json',

                },
                'aoColumnDefs': [{
                    'className': 'text-right',
                	'targets': [1, 2, 3, 4],
                }],
                'language': {
                    'emptyTable': gettext('antares.apps.accounting.templates.emptyMessages.emptyAccount'),
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
    $("#clientAccountingPanel").show();
    $("#breadcrumsAccountingPanel").hide();
    $("#conceptTypeAccountingPanel").hide();
    $("#periodAccountingPanel").hide();
    $("#accountTypeAccountingPanel").hide();

}

function process_concept_type_level(client_id, client_name, concept_type_id, concept_type_name) {
	console.log("process_concept_type_level called with client_id=" + client_id + " client_name=" + client_name +  "concept_type_id=");
    if ($.fn.dataTable.isDataTable('#conceptTypeAccountingTable')) {
        $('#conceptTypeAccountingTable').DataTable().destroy();
    }
    if (antaresAccountingLinks.concept_type_call) {
        $('#conceptTypeAccountingTable').DataTable({
            'paging': true,
            'processing': true,
            'serverSide': true,
            'info': false,
            'searching': false,
            'bLengthChange': false,
            'iDisplayLength': 15,
            'conditionalPaging': true,
            'ajax': {
                'url': antaresAccountingLinks.concept_type_call,
                'data': {
                    'csrfmiddlewaretoken': $.cookie('csrftoken'),
                    'client_id': client_id,
                    'concept_type_id': concept_type_id,
                },
                'method': 'GET',
                'type': 'json',

            },
            'aoColumnDefs': [{
                'className': 'text-right',
            	'targets': [1, 2, 3, 4],
            }],
            'language': {
                'emptyTable': gettext('antares.apps.accounting.templates.emptyMessages.emptyAccount')
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
    build_breadcrumbs(client_id, client_name);
    $("#clientAccountingPanel").hide();
    $("#breadcrumsAccountingPanel").show();
    $("#conceptTypeAccountingPanel").show();
    $("#periodAccountingPanel").hide();
    $("#accountTypeAccountingPanel").hide();
}

function process_period_level(client_id, client_name, concept_type_id, concept_type_name, period) {
    console.log("process_period_level called with client_id=" + client_id + " client_name=" + client_name +  " concept_type_id=" + " period =" + period);
    if ($.fn.dataTable.isDataTable('#periodAccountingTable')) {
        $('#periodAccountingTable').DataTable().destroy();
    }
    if (antaresAccountingLinks.period_call) {
        $('#periodAccountingTable').DataTable({
            'paging': true,
            'processing': true,
            'serverSide': true,
            'info': false,
            'searching': false,
            'bLengthChange': false,
            'iDisplayLength': 15,
            'conditionalPaging': true,
            'ajax': {
                'url': antaresAccountingLinks.period_call,
                'data': {
                    'csrfmiddlewaretoken': $.cookie('csrftoken'),
                    'client_id': client_id,
                    'concept_type_id': concept_type_id,
                    'period': period,
                },
                'method': 'GET',
                'type': 'json',

            },
            'aoColumnDefs': [{
                'className': 'text-right',
            	'targets': [1, 2, 3, 4],
            }],
            'language': {
                'emptyTable': gettext('antares.apps.accounting.templates.emptyMessages.emptyAccount')
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
    build_breadcrumbs(client_id, client_name, null, null, concept_type_id, concept_type_name, period);
    $("#clientAccountingPanel").hide();
    $("#breadcrumsAccountingPanel").show();
    $("#conceptTypeAccountingPanel").hide();
    $("#periodAccountingPanel").show();
    $("#accountTypeAccountingPanel").hide();
}

function process_account_type_level(client_id, client_name, concept_type_id, concept_type_name, period, account_type_id, account_type_name) {
    console.log("process_period_level called with client_id=" + client_id + " client_name=" + client_name +  " concept_type_id=" + 
    " period =" + period + " account_type_id=" + account_type_id +  " account_type_name="+account_type_name);
    if ($.fn.dataTable.isDataTable('#accountTypeAccountingTable')) {
        $('#accountTypeAccountingTable').DataTable().destroy();
    }

    if (antaresAccountingLinks.account_type_call) {
        $('#accountTypeAccountingTable').DataTable({
            'paging': true,
            'processing': true,
            'serverSide': true,
            'info': false,
            'searching': false,
            'bLengthChange': false,
            'iDisplayLength': 15,
            'conditionalPaging': true,
            'ajax': {
                'url': antaresAccountingLinks.account_type_call,
                'data': {
                    'csrfmiddlewaretoken': $.cookie('csrftoken'),
                    'client_id': client_id,
                    'concept_type_id': concept_type_id,
                    'period': period,
                    'account_type_id': account_type_id,
                },
                'method': 'GET',
                'type': 'json',

            },
            'aoColumnDefs': [{
                'bSortable': false,
                'aTargets': [1, 2, 3]
            }, 
            {
            	'className': 'text-right',
                'targets': [4, 5, 6, 7],
            }],
            'language': {
                'emptyTable': gettext('antares.apps.accounting.templates.emptyMessages.emptyAccount'), 
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
    build_breadcrumbs(client_id, client_name, null, null, concept_type_id, concept_type_name, period, account_type_id, account_type_name);
    $("#clientAccountingPanel").hide();
    $("#breadcrumsAccountingPanel").show();
    $("#conceptTypeAccountingPanel").hide();
    $("#periodAccountingPanel").hide();
    $("#accountTypeAccountingPanel").show();
}


function build_breadcrumbs(client_id, client_name = null, document = null, document_name = null, concept_type_id = null, concept_type_name = null,
    period = null, account_type_id = null, account_type_name = null) {
    console.log("build_breadcrumbs called with client_id=" + client_id + " client_name=" + client_name + " document=" 
    + document + " document_name=" + document_name + " concept_type_id=" + concept_type_id + " concept_type_name=" + concept_type_name + 
    " period="  + period + " account_type_id=" + account_type_id + " account_type_name=" + account_type_name);
    $("#breadcrumsAccountingPanel").html("");
    var breadcCrumb = "<div>";
    if (client_id && document == null && concept_type_id == null && period == null && account_type_id == null) {
        breadcCrumb += '<a onClick="display_accounting_panel(\'' +
            client_id + '\', \'' + client_name + '\');">' +
            client_name + '</a>';
    } else if (client_id && document == null && concept_type_id && period == null && account_type_id == null) {
        breadcCrumb += '<a onClick="display_accounting_panel(\'' +
            client_id + '\', \'' + client_name + '\');">' +
            client_name + '</a>';
            breadcCrumb += "<span> &gt; </span>";
            breadcCrumb += '<a onClick="display_accounting_panel(\'' +
            client_id + '\', \'' + client_name + '\', null, null, \'' + concept_type_id + '\', \'' + concept_type_name + '\');">' +
            concept_type_name + '</a>';

    } else if (client_id && document == null && concept_type_id!= null && period != null && account_type_id == null) {
        breadcCrumb += '<a onClick="display_accounting_panel(\'' +
            client_id + '\', \'' + client_name + '\');">' +
            client_name + '</a>';
            breadcCrumb += "<span> &gt; </span>";
            breadcCrumb += '<a onClick="display_accounting_panel(\'' +
            client_id + '\', \'' + client_name + '\', null, null, \'' + concept_type_id + '\', \'' + concept_type_name + '\');">' +
            concept_type_name + '</a>';
            breadcCrumb += "<span> &gt; </span>";
            breadcCrumb += '<a onClick="display_accounting_panel(\'' +
            client_id + '\', \'' + client_name + '\', null, null, \'' + concept_type_id + '\', \'' + concept_type_name + '\', ' + period + ');">' +
            period + '</a>';
    } else if (client_id && document == null && concept_type_id!= null && period!= null && account_type_id!= null) {
        breadcCrumb += '<a onClick="display_accounting_panel(\'' +
            client_id + '\', \'' + client_name + '\');">' +
            client_name + '</a>';
            breadcCrumb += "<span> &gt; </span>";
            breadcCrumb += '<a onClick="display_accounting_panel(\'' +
            client_id + '\', \'' + client_name + '\', null, null, \'' + concept_type_id + '\', \'' + concept_type_name + '\');">' +
            concept_type_name + '</a>';
            breadcCrumb += "<span> &gt; </span>";
            breadcCrumb += '<a onClick="display_accounting_panel(\'' +
            client_id + '\', \'' + client_name + '\', null, null, \'' + concept_type_id + '\', \'' + concept_type_name + '\', ' + period + ');">' +
            period + '</a>';
            breadcCrumb += "<span> &gt; </span>";
            breadcCrumb += '<a onClick="display_accounting_panel(\'' +
            client_id + '\', \'' + client_name + '\', null, null, \'' + concept_type_id + '\', \'' +
            concept_type_name + '\', ' + period + ', \'' + account_type_id + '\', \'' + account_type_name + '\');">' +
            account_type_name + '</a>';
            
    }
    breadcCrumb += "</div>";
    $("#breadcrumsAccountingPanel").append( breadcCrumb);
}

function view_accounting_document(document_id) {
	console.log("view_accounting_document called with document_id=" + document_id);
    if (!$('#accountDocumentDialog_' + document_id).length) {
        $('<div id="accountDocumentDialog_' + document_id + '" />').dialog({
            'title': 'Document',
            'autoOpen': false,
            'width': 'auto',
            'height': 'auto',
            'open': function(event, ui) {

            },
            'buttons': {
                'Ok': function() {
                    $(this).dialog("close");
                },
            },
        }).append('<div id="accountDocumentInnerDiv_' + document_id + '"></div>');

        $('#accountDocumentInnerDiv_' + document_id).load(antaresAccountingLinks.document_view.replace("5911F917-A61B-478B-B7F2-89C754D1FAF6", document_id));

    }
    $("#accountDocumentDialog_" + document_id).dialog('open').show();
}

function print_accounting_document(document_id) {
	console.log("print_accounting_document called with document_id=" + document_id);
    if (!$('#accountDocumentDialog_' + document_id).length) {
        $('<div id="accountDocumentDialog_' + document_id + '" />').dialog({
            'title': 'Document',
            'autoOpen': false,
            'width': 'auto',
            'height': 'auto',
            'open': function(event, ui) {

            },
            'buttons': {
                'Ok': function() {
                    $(this).dialog("close");
                },
            },
        }).append('<div id="accountDocumentInnerDiv_' + document_id + '"></div>');

        $('#accountDocumentInnerDiv_' + document_id).load(antaresAccountingLinks.document_view.replace("5911F917-A61B-478B-B7F2-89C754D1FAF6", document_id));

    }
    $("#accountDocumentDialog_" + document_id).dialog('open').show();
}