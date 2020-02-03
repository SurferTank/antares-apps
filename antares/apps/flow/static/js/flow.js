/**
 * Opens the note editor
 * 
 * @param note_id
 * @param note_title
 * @param note_content
 * @returns
 */
function editNote(note_id, note_title, note_content) {
	if (note_id) {
		$("#note_id").val(note_id);
	} else {
		$("#note_id").val("");
	}
	if (note_title) {
		$("#note_title").val(note_title);
	} else {
		$("#note_title").val("");
	}
	if (note_content) {
		$("#note_content").val(note_content);
	} else {
		$("#note_content").val("");
	}
	$("#flow_add_note")
			.dialog(
					{
						'modal' : true,
						'resizable' : false,
						'width' : 'auto',
						'buttons' : [
								{
									'text' : gettext("antares.apps.flow.templates.dashboard.notes.cancel_button"),
									'click' : function() {
										$(this).dialog("close");
									}
								},
								{
									'text' : gettext('antares.apps.flow.templates.dashboard.notes.save_button'),
									'click' : function() {

										saveCaseNote($(this));
									}
								}, ],
					});
}

/**
 * Sets up the inbox for usage
 * 
 * @param status
 * @returns
 */
function display_inbox_page(status) {
	switch (status.toLowerCase()) {
	case "active":
		setup_active_inbox_cases_view(status);
		break;
	case "completed":
		setup_completed_inbox_cases_view(status);
		break;
	case "stats":
		setup_stats_inbox();
		break;
	default:
		setup_new_inbox_cases_view(status);
	}
}

/**
 * 
 * @param status
 * @returns
 */
function setup_new_inbox_cases_view(status) {
	if ($.fn.dataTable.isDataTable('#createdCasesInboxTable')) {
		$('#createdCasesInboxTable').DataTable().destroy();
	}
	if (antaresFlowLinks.created_inbox_case_view) {
		$('#createdCasesInboxTable')
				.DataTable(
						{
							'paging' : true,
							'processing' : true,
							'serverSide' : true,
							'info' : false,
							'searching' : false,
							'bLengthChange' : false,
							'iDisplayLength' : 25,
							'conditionalPaging' : true,
							'ajax' : {
								'url' : antaresFlowLinks.created_inbox_case_view,
								'data' : {
									'status_type' : status,
									'csrfmiddlewaretoken' : $
											.cookie('csrftoken'),
								},
								'method' : 'GET',
								'type' : 'json',
							},
							'language' : {
								'emptyTable' : gettext('antares.apps.flow.templates.inbox.emptyTable'),
							},
							'fnDrawCallback' : function(oSettings) {
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
	$("#createdCasesInboxPanel").show();
	$("#activeCasesInboxPanel").hide();
	$("#completedCasesInboxPanel").hide();
	$("#statsInboxPanel").hide();
}

/**
 * 
 * @param status
 * @returns
 */
function setup_active_inbox_cases_view(status) {
	if ($.fn.dataTable.isDataTable('#activeCasesInboxTable')) {
		$('#activeCasesInboxTable').DataTable().destroy();
	}
	if (antaresFlowLinks.active_inbox_case_view) {
		$('#activeCasesInboxTable')
				.DataTable(
						{
							'paging' : true,
							'processing' : true,
							'serverSide' : true,
							'info' : false,
							'searching' : false,
							'bLengthChange' : false,
							'iDisplayLength' : 25,
							'conditionalPaging' : true,
							'ajax' : {
								'url' : antaresFlowLinks.active_inbox_case_view,
								'data' : {
									'status_type' : status,
									'csrfmiddlewaretoken' : $
											.cookie('csrftoken'),
								},
								'method' : 'GET',
								'type' : 'json',
							},
							'language' : {
								'emptyTable' : gettext('antares.apps.flow.templates.inbox.emptyTable'),
							},
							'fnDrawCallback' : function(oSettings) {
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
	$("#createdCasesInboxPanel").hide();
	$("#activeCasesInboxPanel").show();
	$("#completedCasesInboxPanel").hide();
	$("#statsInboxPanel").hide();
}

/**
 * 
 * @param status
 * @returns
 */
function setup_completed_inbox_cases_view(status) {
	if ($.fn.dataTable.isDataTable('#completedCasesInboxTable')) {
		$('#completedCasesInboxTable').DataTable().destroy();
	}
	if (antaresFlowLinks.completed_inbox_case_view) {
		$('#completedCasesInboxTable')
				.DataTable(
						{
							'paging' : true,
							'processing' : true,
							'serverSide' : true,
							'info' : false,
							'searching' : false,
							'bLengthChange' : false,
							'iDisplayLength' : 25,
							'conditionalPaging' : true,
							'ajax' : {
								'url' : antaresFlowLinks.completed_inbox_case_view,
								'data' : {
									'status_type' : status,
									'csrfmiddlewaretoken' : $
											.cookie('csrftoken'),
								},
								'method' : 'GET',
								'type' : 'json',
							},
							'language' : {
								'emptyTable' : gettext('antares.apps.flow.templates.inbox.emptyTable'),
							},
							'fnDrawCallback' : function(oSettings) {
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
	$("#createdCasesInboxPanel").hide();
	$("#activeCasesInboxPanel").hide();
	$("#completedCasesInboxPanel").show();
	$("#statsInboxPanel").hide();
}

/**
 * 
 * @param status
 * @returns
 */
function setup_stats(status) {
	
	$("#createdCasesInboxPanel").hide();
	$("#activeCasesInboxPanel").hide();
	$("#completedCasesInboxPanel").hide();
	$("#statsInboxPanel").show();	
}


/**
 * 
 * @param event
 * @param caseId
 * @param propertyId
 * @param value
 * @returns
 */
function leftToolbarUpdateProperty(event, caseId, propertyId, value) {
	event.preventDefault();
	if (antaresFlowLinks.update_property_call) {
		$.ajax({
			'url' : antaresFlowLinks.update_property_call,
			'data' : {
				'case_id' : caseId,
				'property_id' : propertyId,
				'property_value' : value,
				'csrfmiddlewaretoken' : $.cookie('csrftoken'),
			},
			'method' : 'POST',
			'type' : 'json',
			'success' : function(ret) {
				$("#casePropertiesTable").DataTable().ajax.reload(null, true);
			}

		});
	}
}

/**
 * 
 * @param activity_id
 * @returns
 */
function display_workflow_panel(activity_id) {
	$("#activityCaseName").editable();
	var priorities = [];
	$('#casePriority').editable({
		source : priority_type_choices,
		select2 : {
			width : 200,
			placeholder : 'Select Priority',
			allowClear : false
		}
	});
	if (antaresFlowLinks.case_properties_call) {
		$('#casePropertiesTable').DataTable(
				{
					'paging' : true,
					'processing' : true,
					'serverSide' : true,
					'info' : false,
					'searching' : false,
					'bLengthChange' : false,
					'iDisplayLength' : 25,
					'conditionalPaging' : true,
					'ajax' : {
						'url' : antaresFlowLinks.case_properties_call,
						'data' : {
							'activity_id' : activity_id,
							'csrfmiddlewaretoken' : $.cookie('csrftoken')
						},
						'method' : 'GET',
						'type' : 'json',
					},
					'aoColumnDefs' : [ {
						'bSortable' : false,
						'aTargets' : [ 1 ]
					} ],
					'fnDrawCallback' : function(oSettings) {
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
	if (antaresFlowLinks.case_history_call) {
		$('#caseHistoryTable').DataTable(
				{
					'paging' : true,
					'processing' : true,
					'serverSide' : true,
					'info' : false,
					'searching' : false,
					'bLengthChange' : false,
					'iDisplayLength' : 25,
					'conditionalPaging' : true,
					'ajax' : {
						'url' : antaresFlowLinks.case_history_call,
						'data' : {
							'activity_id' : activity_id,
							'csrfmiddlewaretoken' : $.cookie('csrftoken')
						},
						'method' : 'GET',
						'type' : 'json',
					},
					'aoColumnDefs' : [ {
						'bSortable' : false,
						'aTargets' : [ 1, 4, 5, 6 ]
					} ],
					'fnDrawCallback' : function(oSettings) {
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
	if (antaresFlowLinks.case_document_call) {
		$('#caseDraftDocumentsTable').DataTable(
				{
					'paging' : true,
					'processing' : true,
					'serverSide' : true,
					'info' : false,
					'searching' : false,
					'bLengthChange' : false,
					'iDisplayLength' : 25,
					'conditionalPaging' : true,
					'ajax' : {
						'url' : antaresFlowLinks.case_document_call,
						'data' : {
							'activity_id' : activity_id,
							'status_id' : 'drafted',
							'csrfmiddlewaretoken' : $.cookie('csrftoken')
						},
						'method' : 'GET',
						'type' : 'json',
					},
					'aoColumnDefs' : [ {
						'bSortable' : false,
						'aTargets' : [ 6, 7 ]
					} ],
					'fnDrawCallback' : function(oSettings) {
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
	if (antaresFlowLinks.case_notes_call) {
		$('#caseNotesTable').DataTable(
				{
					'paging' : true,
					'processing' : true,
					'serverSide' : true,
					'info' : false,
					'searching' : false,
					'bLengthChange' : false,
					'iDisplayLength' : 10,
					'conditionalPaging' : true,
					'ajax' : {
						'url' : antaresFlowLinks.case_notes_call,
						'data' : {
							'activity_id' : activity_id,
							'csrfmiddlewaretoken' : $.cookie('csrftoken')
						},
						'method' : 'GET',
						'type' : 'json',
					},
					'aoColumnDefs' : [ {
						'bSortable' : false,
						'aTargets' : [ 3 ]
					} ],
					'fnDrawCallback' : function(oSettings) {
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

/**
 * 
 * @param dialog
 * @returns
 */
function saveCaseNote(dialog) {
	if (antaresFlowLinks.case_notes_call) {
		$.ajax({
			'url' : antaresFlowLinks.case_notes_call,
			'data' : {
				'case_id' : '{{activity.flow_case.id}}',
				'title' : $("#note_title").val(),
				'content' : $("#note_content").val(),
				'note_id' : $("#note_id").val(),
				'csrfmiddlewaretoken' : $.cookie('csrftoken'),
			},
			'method' : 'POST',
			'type' : 'json',
			'success' : function(data) {
				$('#caseNotesTable').DataTable().ajax.reload();
				dialog.dialog("close");
			},
		});
	}
}

/**
 * 
 * @param document_id
 * @returns
 */
function viewWorkflowDocument(document_id) {
	if (!$('#flowDocumentDialog_' + document_id).length) {
		$('<div id="flowDocumentDialog_' + document_id + '" />').dialog({
			'title' : 'Document',
			'autoOpen' : false,
			'width' : 'auto',
			'height' : 'auto',
			'open' : function(event, ui) {

			},
			'buttons' : {
				'Cancel' : function() {
					$(this).dialog("close");
				},
			},
		}).append('<div id="flowDocumentInnerDiv_' + document_id + '"></div>');
		var document_address = "{% url 'antares.apps.document:view_view' document_id='5911F917-A61B-478B-B7F2-89C754D1FAF6' %}?is_inner=yes";
		$('#flowDocumentInnerDiv_' + document_id).load(
				antaresFlowLinks.case_document_view_call.replace(
						"5911F917-A61B-478B-B7F2-89C754D1FAF6", document_id));

	}
	$("#flowDocumentDialog_" + document_id).dialog('open').show();
}

/**
 * 
 * @param document_id
 * @returns
 */
function printWorkflowDocument(document_id) {
	alert("Not implemented yet.");
}

/**
 * 
 * @param document_id
 * @returns
 */
function editWorkflowDocument(document_id) {
	if (!$('#flowEditDocumentDialog_' + document_id).length) {
		$('<div id="flowEditDocumentDialog_' + document_id + '" />').dialog({
			'title' : 'Document',
			'autoOpen' : false,
			'width' : 'auto',
			'height' : 'auto',
			'open' : function(event, ui) {

			},
			'buttons' : {
				'Cancel' : function() {
					$(this).dialog("close");
				},
			},
		})
				.append(
						'<div id="flowEditDocumentInnerDiv_' + document_id
								+ '"></div>');

		$('#flowEditDocumentInnerDiv_' + document_id).load(
				antaresFlowLinks.case_document_edit_call.replace(
						"5911F917-A61B-478B-B7F2-89C754D1FAF6", document_id));

	}
	$("#flowEditDocumentDialog_" + document_id).dialog('open').show();
}

/**
 * 
 * @param activity_id
 * @returns
 */
function openForwardWindow(activity_id) {
	var show_message = false;
	$
			.ajax({
				'url' : antaresFlowLinks.case_forward_case_call,
				'data' : {
					'type' : 'forward',
					'activityId' : activity_id,
					'confirmation' : 'false',
					'csrfmiddlewaretoken' : $.cookie('csrftoken'),
				},
				'method' : 'POST',
				'dataType' : 'json',
				'success' : function(ret) {
					if (ret.message) {
						$("#msgPathFound").hide();
						$("#msgPathNotFound").hide();
						$("#msgValidationError").html(ret.message);
						$("#msgValidationError").show();
						openForwardDialog(true);
					} else {
						if (ret.length === 0) {
							$("#msgPathFound").hide();
							$("#msgValidationError").hide();
						} else {
							$("#msgPathNotFound").hide();
							$("#msgValidationError").hide();
							var tbl = $('#fowardActivitiesTable');
							tbl.empty();
							$(document.createElement('tr'))
									.append(
											'<thead><th><b>'
													+ gettext('antares.apps.flow.templates.dashboard.forward.activity')
													+ '</b></th></thead>')
									.appendTo(tbl);

							$.each(ret.activities, function(index, val) {
								var valName;
								if (val != null) {
									valName = val;
								} else {
									valName = index;
								}
								$(document.createElement('tr')).append(
										'<td>' + valName + '</td>').appendTo(
										tbl);
							})
							openForwardDialog(false);
						}
					}
				}
			});

}

/**
 * 
 * @param message
 * @returns
 */
function openForwardDialog(message) {
	if (message == false) {
		$('#forwardDialog')
				.dialog(
						{
							'title' : gettext('antares.apps.flow.templates.dashboard.forward.forwardCaseButton'),
							'autoOpen' : false,
							'width' : 'auto',
							'height' : 'auto',
							'open' : function(event, ui) {

							},
							'buttons' : [
									{
										'text' : gettext('antares.apps.flow.templates.dashboard.forward.cancelButton'),
										'click' : function() {
											$(this).dialog("close");
										},
									},
									{
										'text' : gettext('antares.apps.flow.templates.dashboard.forward.forwardButton'),
										'click' : function() {
											$
													.ajax({
														'url' : antaresFlowLinks.case_forward_case_call,
														'data' : {
															'type' : 'forward',
															'activityId' : activity_id,
															'confirmation' : 'true',
															'csrfmiddlewaretoken' : $
																	.cookie('csrftoken'),
														},
														'method' : 'POST',
														'dataType' : 'json',
														'success' : function(
																ret) {
															window.location.href = antaresFlowLinks.inbox_view;
														},
														'async' : true,
														'error' : function(ret) {
															$(
																	"#msgPathNotFound")
																	.text(
																			"An error has happened. Try again.");
														},
													});
										}
									} ],
						});
	} else {
		$('#forwardDialog')
				.dialog(
						{
							'title' : 'Forward Case',
							'autoOpen' : false,
							'width' : 'auto',
							'height' : 'auto',
							'open' : function(event, ui) {

							},
							'buttons' : [ {
								'text' : gettext('antares.apps.flow.templates.dashboard.forward.cancelButton'),
								'click' : function() {
									$(this).dialog("close");
								},
							} ],
						});
	}
	$("#forwardDialog").dialog('open').show();
}