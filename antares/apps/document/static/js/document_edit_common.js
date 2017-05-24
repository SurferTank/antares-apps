/*
 * Copyright (c) 2013-2017, Surfer Inc. and/or its affiliates. All rights reserved.
 * SURFERTANK INC. PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
 * 
 * Initial Release by Leonardo Javier Belen
 *
 */

/**
 * sets up the document view so everything is ready to use
 * @returns null
 */
function setup_document_edit_view() {
	$("#documentSaveDialog")
			.dialog(
					{
						'title' : 'Document Saved',
						'autoOpen' : false,
						'width' : 'auto',
						'height' : 'auto',
						'modal' : true,
						'open' : function(event, ui) {
							$(".ui-dialog-titlebar-close", ui.dialog | ui)
									.hide();
						},
						'buttons' : [
								{
									'text' : gettext("antares.apps.document.document_view.templates.continue_button"),
									'click' : function() {
										location.href = redirectTo;
									}
								}, ]
					});
	
	$("#documentDraftDialog")
			.dialog(
					{
						'title' : 'Document Drafted',
						'autoOpen' : false,
						'width' : 'auto',
						'height' : 'auto',
						'modal' : true,
						'open' : function(event, ui) {
							$(".ui-dialog-titlebar-close", ui.dialog | ui)
									.hide();
						},
						'buttons' : [
								{
									'text' : gettext("antares.apps.document.document_view.templates.continue_button"),
									'click' : function() {
										location.href = redirectTo;
									}
								},
								{
									'text' : gettext("antares.apps.document.document_view.templates.stay_editing_button"),
									'click' : function() {
										$(this).dialog("close");
									}
								}, ]
					});
	
	$("#documentHelpDialog")
			.dialog(
					{
						'title' : 'Help',
						'autoOpen' : false,
						'width' : 'auto',
						'height' : 'auto',
						'modal' : true,
						'open' : function(event, ui) {

						},
						'buttons' : [
								{
									'text' : gettext("antares.apps.document.document_view.templates.cancel_button"),
									'click' : function() {
										$(this).dialog("close");
									}
								}, ]
					});

	if (g_showSubmit == false) {
		$("#documentSaveButton").css("display", "none");
	}
}

/**
 * validates the document based on the local evaluate function
 * 
 * @returns whether it is validated or not.
 */
function validateDocument() {
	if (evaluateDocument(true) == true) {
		if (g_showSubmit == true) {
			$("#documentSaveButton").css("display", "block");
		} else {
			$("#documentSaveButton").css("display", "none");
		}
		return true;
	} else {
		$("#documentSaveButton").css("display", "none");
		return true;
	}
}

/**
 * Submits a document, based on the status. 
 * @param status the document status
 * @returns null
 */
function formSubmission(status) {
	if (status == "SAVE") {
		if (!validateDocument(true)) {
			alert("something is not right here");
		}
	}
	$.ajax({
		type : 'POST',
		url : antaresDocLinks.api_submit_call,
		data : $('#documentEditorForm').serialize(),
		dataType : 'json',
		success : function(data) {
			if (data.redirectTo != null) {
				redirectTo = data.redirectTo;
			}
			if (data.message != null) {
				$('#saveMessage').text(data.message);
			} else {
				if (status == "SAVE") {
					$("#documentSaveDialog").dialog('open');
				} else {
					$("#documentDraftDialog").dialog('open');
				}
			}
		},
		error : function(jqXHR, textStatus, error) {
			alert("something went wrong.");
		}
	});
}

/**
 * 
 * @param field_id
 * @param catalog_id
 * @returns
 */
function create_autocomplete_field(field_id, catalog_id) {
	$("#fields\\[" + field_id + "\\]").autocomplete(
			{
				source : antaresDocLinks.api_autocomplete_call + "?selector="
						+ catalog_id,
				minLength : 2,
				select : function(event, ui) {
					$(this).text = ui.value
				}
			});
}

/**
 * 
 * @param field_id
 * @param catalog_id
 * @returns
 */
function create_select_field(field_id, catalog_id) {
	$("#fields\\[" + field_id + "\\]").select2(
			{
				ajax : {
					'url' : antaresDocLinks.api_select_call + "?selector="
							+ catalog_id,
					'dataType' : 'json',
					'delay' : 250,
					'data' : function(params) {
						return {
							termId : params.term, /* search term */
							catalogId : "test",
							page : params.page
						};
					},
					results : function(data, page) { 
						/*
						 * parse the results into the format expected by Select2
						 * since we are using custom formatting funtions we do
						 * not need to alter the remote JSON data, except to
						 * indicate that infinite scrolling can be used
						 */
						page = page || 1;
						return {
							results : data.items,
							pagination : {
								more : (page * 30) < data.total_count
							}
						};
					},
					cache : true
				},
				escapeMarkup : function(markup) {
					return markup;
				},
				minimumInputLength : 1
			});
}

/**
 * 
 * @param field_id
 * @param value
 * @param validation_result
 * @returns
 */
function validate_number_field_boundaries(field_id, value, validation_result=true) {
	if (!(!isNaN(parseFloat(value)) && isFinite(value))) {
		renderMessage(getFieldDisplayName(field_id)
				+ gettext("antares.apps.document.document_view.templates.negative_validation_title"),
				gettext("antares.apps.document.document_view.templates.negative_validation_the_field") + " '"+ 
				getFieldDisplayName(field_id) + 
				 "' " +gettext("antares.apps.document.document_view.templates.negative_validation_is_not_a_number"), "error");
		$("#fields\\[" + field_id + "\\]").focus();
		return false;
	}
	if (value < 0) {
		renderMessage(getFieldDisplayName(field_id)
				+ gettext("antares.apps.document.document_view.templates.negative_validation_title"),
				gettext("antares.apps.document.document_view.templates.negative_validation_the_field") + " '"+ getFieldDisplayName(field_id)
						 + "' " + gettext("antares.apps.document.document_view.templates.negative_validation_cannot_be_negative"), "error");
		$("#fields\\[" + field_id + "\\]").focus();
		return false;
	}
	if (validation_result == true) {
		return true;
	} else {
		return false;
	}
}