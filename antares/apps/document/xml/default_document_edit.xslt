<?xml version="1.0" encoding="UTF-8"?>

<!-- Document : procEditTwig.xslt.xsl Created on : November 10, 2015, 2:31 
	AM Author : leobelen Description: Purpose of transformation follows. -->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	version="1.0">
	<xsl:output method="xml" encoding="utf-8"
		omit-xml-declaration="yes" indent="yes" />
	<xsl:template match="/">
		<xsl:text disable-output-escaping="yes"><![CDATA[{% extends template %} 
{% load staticfiles i18n markdown_deux_tags static %} 

{% block title %}Antares Document{% endblock %}
{% block ng_app_name %}{% endblock ng_app_name %}
{% block bodyId %}Antares Document{% endblock %}
{% block javascript %} 
    {% if is_inner == 'false' %}
        <script type="text/javascript" src="{% static "jquery-ui/jquery-ui.js" %}"></script>
    {% endif %}
    <script type="text/javascript" src="{% static "js/document_edit_common.js" %}"></script>
    <script type="text/javascript" src="{% get_media_prefix %}{{edit_js_path}}"></script>
{% endblock javascript %} 

{% block stylesheets %}
    {% if is_inner == 'false' %}
        <link rel="stylesheet" href="{% static "jquery-ui/themes/base/jquery-ui.css" %}">
    <link rel="stylesheet" href="{% static "jquery-ui/themes/base/theme.css" %}">
    {% endif %} 
    
{% endblock stylesheets %} 

{% block content %} ]]></xsl:text>
		<div class="container">
			<script type="text/javascript">
				<xsl:text disable-output-escaping="yes"><![CDATA[
var redirectTo = "{{ next_place }}"; 
var g_showSubmit = {{showSubmit}} == 1 ? true : false; 
var antaresDocLinks = { 
    api_submit_call: "{% url 'antares.apps.document:api_edit_submit_view' %}", 
    api_autocomplete_call: "{% url 'antares.apps.core:api_autocomplete_options_view' %}", 
    api_select_call: "{% url 'antares.apps.core:api_select_options_view' %}", 
    }; 
$(document).ready(function() { 
    setup_document_edit_view();
    validateDocument();
});

]]></xsl:text>
			</script>
			<form id="documentEditorForm" method="POST">
				<input type="hidden" name="_event" value="" id="_event" />
				<input type="hidden" id="csrfmiddlewaretoken" name="csrfmiddlewaretoken"
					value="{{{{csrf_token}}}}" />
				<input type="hidden" id="_formType" name="_formType" value="{{{{formType}}}}" />
				<input type="hidden" id="headerFields[form_name]" name="headerFields[form_name]">
					<xsl:attribute name="value">
                    <xsl:text disable-output-escaping="yes">{{headerFields.form_name|default_if_none:''}}</xsl:text>
                </xsl:attribute>
				</input>
				<input type="hidden" id="headerFields[form_version]" name="headerFields[form_version]">
					<xsl:attribute name="value">
                    <xsl:text disable-output-escaping="yes">{{headerFields.form_version|default_if_none:''}}</xsl:text>
                </xsl:attribute>
				</input>
				<input type="hidden" id="headerFields[document_version]" name="headerFields[document_version]">
					<xsl:attribute name="value">
                    <xsl:text disable-output-escaping="yes">{{headerFields.document_version|default_if_none:''}}</xsl:text>
                </xsl:attribute>
				</input>
				<input type="hidden" id="headerFields[active_version]" name="headerFields[active_version]">
					<xsl:attribute name="value">
                    <xsl:text disable-output-escaping="yes">{{headerFields.active_version|default_if_none:''}}</xsl:text>
                </xsl:attribute>
				</input>
				<input type="hidden" id="headerFields[document_id]" name="headerFields[document_id]">
					<xsl:attribute name="value">
                    <xsl:text disable-output-escaping="yes">{{headerFields.document_id|default_if_none:''}}</xsl:text>
                </xsl:attribute>
				</input>
				<input type="hidden" id="headerFields[author]" name="headerFields[author]">
					<xsl:attribute name="value">
                    <xsl:text disable-output-escaping="yes">{{headerFields.author.id|default_if_none:''}}</xsl:text>
                </xsl:attribute>
				</input>
				<input type="hidden" id="headerFields[draft_date]" name="headerFields[draft_date]">
					<xsl:attribute name="value">
                    <xsl:text disable-output-escaping="yes">{{headerFields.draft_date|date:'c'|default_if_none:''}}</xsl:text>
                </xsl:attribute>
				</input>
				<input type="hidden" id="headerFields[associated_to]" name="headerFields[associated_to]">
					<xsl:attribute name="value">
                    <xsl:text disable-output-escaping="yes">{{headerFields.associated_to.id|default_if_none:''}}</xsl:text>
                </xsl:attribute>
				</input>
				<input type="hidden" id="headerFields[association_type]" name="headerFields[association_type]">
					<xsl:attribute name="value">
                    <xsl:text disable-output-escaping="yes">{{headerFields.association_type.value|default_if_none:''}}</xsl:text>
                </xsl:attribute>
				</input>
				<input type="hidden" id="headerFields[flow_case]" name="headerFields[flow_case]">
					<xsl:attribute name="value">
                    <xsl:text disable-output-escaping="yes">{{headerFields.flow_case.id|default_if_none:''}}</xsl:text>
                </xsl:attribute>
				</input>
				<input type="hidden" id="headerFields[origin]" name="headerFields[origin]">
					<xsl:attribute name="value">
                    <xsl:text disable-output-escaping="yes">{{headerFields.origin.value|default_if_none:''}}</xsl:text>
                </xsl:attribute>
				</input>
				<input type="hidden" id="headerFields[status]" name="headerFields[status]">
					<xsl:attribute name="value">
                    <xsl:text disable-output-escaping="yes">{{headerFields.status.value|default_if_none:''}}</xsl:text>
                </xsl:attribute>
				</input>
				<input type="hidden" id="headerFields[client]" name="headerFields[client]">
					<xsl:attribute name="value">
                    <xsl:text disable-output-escaping="yes">{{headerFields.client.id|default_if_none:''}}</xsl:text>
                </xsl:attribute>
				</input>
				<input type="hidden" id="headerFields[branch]" name="headerFields[branch]">
					<xsl:attribute name="value">
                    <xsl:text disable-output-escaping="yes">{{headerFields.branch.id|default_if_none:''}}</xsl:text>
                </xsl:attribute>
				</input>
				<input type="hidden" id="headerFields[concept_type]" name="headerFields[concept_type]">
					<xsl:attribute name="value">
                    <xsl:text disable-output-escaping="yes">{{headerFields.concept_type.id|default_if_none:''}}</xsl:text>
                </xsl:attribute>
				</input>
				<input type="hidden" id="headerFields[account_type]" name="headerFields[account_type]">
					<xsl:attribute name="value">
                    <xsl:text disable-output-escaping="yes">{{headerFields.account_type.id|default_if_none:''}}</xsl:text>
                </xsl:attribute>
				</input>
				<input type="hidden" id="headerFields[period]" name="headerFields[period]">
					<xsl:attribute name="value">
                    <xsl:text disable-output-escaping="yes">{{headerFields.period|default_if_none:''}}</xsl:text>
                </xsl:attribute>
				</input>
				<input type="hidden" id="headerFields[default_currency]" name="default_currency">
					<xsl:attribute name="value">
                    	<xsl:text disable-output-escaping="yes">{{headerFields.default_currency|default_if_none:''}}</xsl:text>
                		</xsl:attribute>
				</input>
				<input type="hidden" id="headerFields[account_document]" name="headerFields[account_document]">
					<xsl:attribute name="value">
                    <xsl:text disable-output-escaping="yes">{{headerFields.account_document.id|default_if_none:''}}</xsl:text>
                </xsl:attribute>
				</input>
				<!-- Lets start with the HEADER of the tabbed section section.... -->
				<div class="navbar">
					<ul class="nav nav-pills pull-left">
						<li>
							<a class="btn btn-primary" id="documentValidateButton" onclick="validateDocument();">
								{% trans 'antares.apps.document.edit.buttons.validate' %}</a>
						</li>
						<li>
							<a class="btn btn-primary" href="#"
								onclick="$('#_event').val('DRAFT MODIFICATION'); formSubmission('DRAFT MODIFICATION');"
								id="documentDraftButton">{% trans 'antares.apps.document.edit.buttons.draft' %}</a>
						</li>
						<li>
							<a class="btn btn-primary" href="#"
								onclick="$('#_event').val('SAVE'); formSubmission('SAVE');" id="documentSaveButton">
								{% trans 'antares.apps.document.edit.buttons.save' %}</a>
						</li>
					</ul>
					<xsl:if test="/document/headerElements/helpText">
						<ul class="nav nav-pills pull-right">
							<li>
								<a class="btn btn-primary" onClick="$('#documentHelpDialog').dialog('open');">
									{% trans 'antares.apps.document.edit.buttons.help' %}</a>
							</li>
						</ul>
					</xsl:if>
				</div>
				<div class="row">
					<xsl:for-each select="document/structuredData[@title]">
						<div id="documentTitle" class="col-lg-12">
							<h4>
								<xsl:value-of select="@title" />
							</h4>
						</div>
					</xsl:for-each>
					<div id="documentEditTabs" class="col-lg-12">
						<ul class="nav nav-tabs">
							<xsl:for-each select="document/structuredData/page">
								<li>
									<a>
										<xsl:attribute name="href">
                                        <xsl:value-of
											select="concat('#antaresDocumentPage-',position())" />
                                    </xsl:attribute>
										<xsl:value-of select="@title" />
									</a>
								</li>
							</xsl:for-each>
						</ul>
						<div class="tab-content">
							<xsl:for-each select="document/structuredData/page">
								<br />
								<div>
									<xsl:if test="position()=1">
										<xsl:attribute name="class">
                                        <xsl:text
											disable-output-escaping="yes">tab-pane fade in active</xsl:text>
                                    </xsl:attribute>
									</xsl:if>
									<xsl:if test="position()>1">
										<xsl:attribute name="class">
                                        <xsl:text
											disable-output-escaping="yes">tab-pane fade</xsl:text>
                                    </xsl:attribute>
									</xsl:if>
									<xsl:attribute name="id">
                                    <xsl:value-of
										select="concat('#antaresDocumentPage-', position())" />
                                </xsl:attribute>
									<div class="container">
										<xsl:for-each select="line">
											<xsl:sort data-type="number" select="line" />
											<xsl:call-template name="line-processing">
												<xsl:with-param name="line" select="line" />
											</xsl:call-template>
										</xsl:for-each>
									</div>
								</div>
							</xsl:for-each>
						</div>
					</div>
				</div>
				<div id="documentSaveDialog" style="display:none;">
					<div id="documentSaveDialogContent">{% trans 'antares.apps.document.messages.document_drafted' %}</div>
				</div>
				<div id="documentDraftDialog" style="display:none;">
					<div id="documentDraftDialogContent">{% trans 'antares.apps.document.messages.document_saved' %}</div>
				</div>
				<div id="documentHelpDialog" style="display:none;">
					<div id="documentSaveHelpContent">
						<xsl:text disable-output-escaping="yes">{% markdown trusted %}</xsl:text>
						<xsl:value-of select="/document/headerElements/helpText" />
						<xsl:text disable-output-escaping="yes">{% endmarkdown %}</xsl:text>
					</div>
				</div>
			</form>
		</div>
		<xsl:text>{% endblock %}</xsl:text>
	</xsl:template>
	<xsl:template name="line-processing">
		<xsl:param name="line" />
		<div class="row">
			<xsl:for-each select="field">
				<div>
					<xsl:choose>
						<xsl:when test="@colspan>1">
							<xsl:attribute name="class">
                                <xsl:text>col-lg-</xsl:text>
                                <xsl:value-of select="@colspan" />
                            </xsl:attribute>
						</xsl:when>
						<xsl:otherwise>
							<xsl:attribute name="class">
                                <xsl:text>col-lg-1</xsl:text>
                            </xsl:attribute>
						</xsl:otherwise>
					</xsl:choose>
					<xsl:choose>
						<xsl:when test="@type='label'">
							<xsl:call-template name="label-processing" />
						</xsl:when>
						<xsl:when test="@type='input' and @dataType='integer'">
							<xsl:call-template name="integer-processing" />
						</xsl:when>
						<xsl:when test="@type='input' and @dataType='float'">
							<xsl:call-template name="float-processing" />
						</xsl:when>
						<xsl:when test="@type='input' and @dataType='string'">
							<xsl:call-template name="string-processing" />
						</xsl:when>
						<xsl:when test="@type='list' and @dataType='string'">
							<xsl:call-template name="list-string-processing" />
						</xsl:when>
						<xsl:when test="@type='input' and @dataType='date'">
							<xsl:call-template name="input-date-processing" />
						</xsl:when>
						<xsl:when test="@type='checkbox' and @dataType='string'">
							<xsl:call-template name="checkbox-string-processing" />
						</xsl:when>
						<xsl:when test="@type='radiobox' and @dataType='string'">
							<xsl:call-template name="radio-string-processing" />
						</xsl:when>
						<xsl:when test="@type='textarea'">
							<xsl:call-template name="textarea-processing" />
						</xsl:when>
						<xsl:when test="@type='textarea-editor'">
							<xsl:call-template name="textarea-editor-processing" />
						</xsl:when>
						<xsl:when test="@type='autocomplete' and @dataType='string'">
							<xsl:call-template name="autocomplete-string-processing" />
						</xsl:when>
						<xsl:when test="@type='input' and @dataType='user'">
							<xsl:call-template name="user-processing" />
						</xsl:when>
						<xsl:when test="@type='input' and @dataType='client'">
							<xsl:call-template name="client-processing" />
						</xsl:when>
						<xsl:when test="@type='input' and @dataType='uuid'">
							<xsl:call-template name="uuid-processing" />
						</xsl:when>
						<xsl:when test="@type='input' and @dataType='document'">
							<xsl:call-template name="document-processing" />
						</xsl:when>
						<xsl:when test="@type='input' and @dataType='money'">
							<xsl:call-template name="money-processing" />
						</xsl:when>
					</xsl:choose>
				</div>
			</xsl:for-each>
		</div>
	</xsl:template>
	<xsl:template name="label-processing">
		<xsl:choose>
			<xsl:when test="@tooltip">
				<span aria-haspopup="true" class="has-tip">
					<xsl:attribute name="data-tooltip" />
					<xsl:attribute name="title">
                        <xsl:value-of select="@tooltip" />
                    </xsl:attribute>
					<xsl:value-of select="text()" />
				</span>
			</xsl:when>
			<xsl:otherwise>
				<span>
					<xsl:value-of select="text()" />
				</span>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<!-- -->
	<xsl:template name="integer-processing">
		<xsl:if test="@fieldCode">
			<div class="input-group">
				<span class="input-group-addon">
					<xsl:attribute name="id">
                        <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                        <xsl:value-of select="@id" />
                    </xsl:attribute>
					<xsl:value-of select="@fieldCode" />
				</span>
				<xsl:call-template name="integer-processing-inner" />
			</div>
		</xsl:if>
		<xsl:if test="not(@fieldCode)">
			<xsl:call-template name="integer-processing-inner" />
		</xsl:if>
	</xsl:template>
	<xsl:template name="integer-processing-inner">
		<input>
			<xsl:attribute name="value">
                <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text disable-output-escaping="yes">|default_if_none:'0'}}</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="id">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="name">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
			<xsl:if test="@readonly='yes' or @readonly='true'">
				<xsl:attribute name="readonly">true</xsl:attribute>
			</xsl:if>
			<xsl:attribute name="onblur">
                <xsl:text>evaluateDocument(false);</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="class">
                <xsl:text>form-control</xsl:text>
            </xsl:attribute>
			<xsl:if test="@tooltip">
				<xsl:attribute name="title">
                    <xsl:value-of select="@tooltip" />
                </xsl:attribute>
				<xsl:attribute name="data-toggle">
                    <xsl:value-of select="tooltip" />
                </xsl:attribute>
			</xsl:if>
			<xsl:if test="@fieldCode">
				<xsl:attribute name="aria-describedby">
                    <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                    <xsl:value-of select="@id" />
                </xsl:attribute>
			</xsl:if>
		</input>
	</xsl:template>
	<xsl:template name="input-date-processing">
		<xsl:if test="@fieldCode">
			<div class="input-group">
				<span class="input-group-addon">
					<xsl:attribute name="id">
                        <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                        <xsl:value-of select="@id" />
                    </xsl:attribute>
					<xsl:value-of select="@fieldCode" />
				</span>
				<xsl:call-template name="date-processing-inner" />
			</div>
		</xsl:if>
		<xsl:if test="not(@fieldCode)">
			<xsl:call-template name="date-processing-inner" />
		</xsl:if>
	</xsl:template>
	<xsl:template name="date-processing-inner">
		<input>
			<xsl:attribute name="value">
                <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text disable-output-escaping="yes">|default_if_none:''}}</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="id">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="name">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
			<xsl:if test="@readonly='yes' or @readonly='true'">
				<xsl:attribute name="readonly">true</xsl:attribute>
			</xsl:if>
			<xsl:attribute name="onblur">
                <xsl:text>evaluateDocument(false);</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="class">
                <xsl:text>form-control</xsl:text>
            </xsl:attribute>
			<xsl:if test="@tooltip">
				<xsl:attribute name="title">
                    <xsl:value-of select="@tooltip" />
                </xsl:attribute>
				<xsl:attribute name="data-toggle">
                    <xsl:value-of select="tooltip" />
                </xsl:attribute>
			</xsl:if>
			<xsl:if test="@fieldCode">
				<xsl:attribute name="aria-describedby">
                    <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                    <xsl:value-of select="@id" />
                </xsl:attribute>
			</xsl:if>
		</input>
	</xsl:template>
	<xsl:template name="float-processing">
		<xsl:if test="@fieldCode">
			<div class="input-group">
				<span class="input-group-addon">
					<xsl:attribute name="id">
                        <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                        <xsl:value-of select="@id" />
                    </xsl:attribute>
					<xsl:value-of select="@fieldCode" />
				</span>
				<xsl:call-template name="float-processing-inner" />
			</div>
		</xsl:if>
		<xsl:if test="not(@fieldCode)">
			<xsl:call-template name="float-processing-inner" />
		</xsl:if>
	</xsl:template>
	<xsl:template name="float-processing-inner">
		<input>
			<xsl:attribute name="value">
                <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text disable-output-escaping="yes">|default_if_none:'0'}}</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="id">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="name">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
			<xsl:if test="@readonly='yes' or @readonly='true'">
				<xsl:attribute name="readonly">true</xsl:attribute>
			</xsl:if>
			<xsl:attribute name="onblur">
                <xsl:text>evaluateDocument(false);</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="class">
                <xsl:text>form-control</xsl:text>
            </xsl:attribute>
			<xsl:if test="@tooltip">
				<xsl:attribute name="title">
                    <xsl:value-of select="@tooltip" />
                </xsl:attribute>
				<xsl:attribute name="data-toggle">
                    <xsl:value-of select="tooltip" />
                </xsl:attribute>
			</xsl:if>
			<xsl:if test="@fieldCode">
				<xsl:attribute name="aria-describedby">
                    <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                    <xsl:value-of select="@id" />
                </xsl:attribute>
			</xsl:if>
		</input>
	</xsl:template>
	<xsl:template name="string-processing">
		<xsl:if test="@fieldCode">
			<div class="input-group">
				<span class="input-group-addon">
					<xsl:attribute name="id">
                        <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                        <xsl:value-of select="@id" />
                    </xsl:attribute>
					<xsl:value-of select="@fieldCode" />
				</span>
				<xsl:call-template name="string-processing-inner" />
			</div>
		</xsl:if>
		<xsl:if test="not(@fieldCode)">
			<xsl:call-template name="string-processing-inner" />
		</xsl:if>
	</xsl:template>
	<xsl:template name="string-processing-inner">
		<input>
			<xsl:attribute name="value">
                <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text disable-output-escaping="yes">|default_if_none:''}}</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="id">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="name">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
			<xsl:if test="@readonly='yes' or @readonly='true'">
				<xsl:attribute name="readonly">true</xsl:attribute>
			</xsl:if>
			<xsl:attribute name="onblur">
                <xsl:text>evaluateDocument(false);</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="class">
                <xsl:text>form-control</xsl:text>
            </xsl:attribute>
			<xsl:if test="@tooltip">
				<xsl:attribute name="title">
                    <xsl:value-of select="@tooltip" />
                </xsl:attribute>
				<xsl:attribute name="data-toggle">
                    <xsl:value-of select="tooltip" />
                </xsl:attribute>
			</xsl:if>
			<xsl:if test="@fieldCode">
				<xsl:attribute name="aria-describedby">
                    <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                    <xsl:value-of select="@id" />
                </xsl:attribute>
			</xsl:if>
		</input>
	</xsl:template>
	
	<xsl:template name="money-processing">
		<xsl:if test="@fieldCode">
			<div class="input-group">
				<span class="input-group-addon">
					<xsl:attribute name="id">
                        <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                        <xsl:value-of select="@id" />
                    </xsl:attribute>
					<xsl:value-of select="@fieldCode" />
				</span>
				<xsl:call-template name="money-processing-inner" />
			</div>
		</xsl:if>
		<xsl:if test="not(@fieldCode)">
			<xsl:call-template name="money-processing-inner" />
		</xsl:if>
	</xsl:template>
	<xsl:template name="money-processing-inner">
		<input>
			<xsl:attribute name="value">
                <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text disable-output-escaping="yes">.amount|default_if_none:''}}</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="id">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="name">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
			<xsl:if test="@readonly='yes' or @readonly='true'">
				<xsl:attribute name="readonly">true</xsl:attribute>
			</xsl:if>
			<xsl:attribute name="onblur">
                <xsl:text>evaluateDocument(false);</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="class">
                <xsl:text>form-control</xsl:text>
            </xsl:attribute>
			<xsl:if test="@tooltip">
				<xsl:attribute name="title">
                    <xsl:value-of select="@tooltip" />
                </xsl:attribute>
				<xsl:attribute name="data-toggle">
                    <xsl:value-of select="tooltip" />
                </xsl:attribute>
			</xsl:if>
			<xsl:if test="@fieldCode">
				<xsl:attribute name="aria-describedby">
                    <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                    <xsl:value-of select="@id" />
                </xsl:attribute>
			</xsl:if>
		</input>
	</xsl:template>
	<xsl:template name="user-processing">
		<xsl:if test="@fieldCode">
			<div class="input-group">
				<span class="input-group-addon">
					<xsl:attribute name="id">
                        <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                        <xsl:value-of select="@id" />
                    </xsl:attribute>
					<xsl:value-of select="@fieldCode" />
				</span>
				<xsl:call-template name="user-processing-inner" />
			</div>
		</xsl:if>
		<xsl:if test="not(@fieldCode)">
			<xsl:call-template name="user-processing-inner" />
		</xsl:if>
	</xsl:template>
	<xsl:template name="user-processing-inner">
		<input>
			<xsl:attribute name="type">
                <xsl:text disable-output-escaping="yes">hidden</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="value">
                <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text disable-output-escaping="yes">.id|default_if_none:''}}</xsl:text>
            </xsl:attribute>
            <xsl:attribute name="id">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
            <xsl:attribute name="name">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
		</input>
		<input>
			<xsl:attribute name="value">
                <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text disable-output-escaping="yes">|default_if_none:''}}</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="id">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>_inner_value]</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="name">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>_inner_value]</xsl:text>
            </xsl:attribute>
			<xsl:if test="@readonly='yes' or @readonly='true'">
				<xsl:attribute name="readonly">true</xsl:attribute>
			</xsl:if>
			<xsl:attribute name="onblur">
                <xsl:text>evaluateDocument(false);</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="class">
                <xsl:text>form-control</xsl:text>
            </xsl:attribute>
			<xsl:if test="@tooltip">
				<xsl:attribute name="title">
                    <xsl:value-of select="@tooltip" />
                </xsl:attribute>
				<xsl:attribute name="data-toggle">
                    <xsl:value-of select="tooltip" />
                </xsl:attribute>
			</xsl:if>
			<xsl:if test="@fieldCode">
				<xsl:attribute name="aria-describedby">
                    <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                    <xsl:value-of select="@id" />
                </xsl:attribute>
			</xsl:if>
		</input>
	</xsl:template>
	
	<xsl:template name="client-processing">
		<xsl:if test="@fieldCode">
			<div class="input-group">
				<span class="input-group-addon">
					<xsl:attribute name="id">
                        <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                        <xsl:value-of select="@id" />
                    </xsl:attribute>
					<xsl:value-of select="@fieldCode" />
				</span>
				<xsl:call-template name="client-processing-inner" />
			</div>
		</xsl:if>
		<xsl:if test="not(@fieldCode)">
			<xsl:call-template name="client-processing-inner" />
		</xsl:if>
	</xsl:template>
	<xsl:template name="client-processing-inner">
		<input>
			<xsl:attribute name="type">
                <xsl:text disable-output-escaping="yes">hidden</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="value">
                <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text disable-output-escaping="yes">.id|default_if_none:''}}</xsl:text>
            </xsl:attribute>
            <xsl:attribute name="id">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
            <xsl:attribute name="name">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
		</input>
		<input>
			<xsl:attribute name="value">
                <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text disable-output-escaping="yes">.code|default_if_none:''}}</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="id">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>_inner_value]</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="name">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>_inner_value]</xsl:text>
            </xsl:attribute>
			<xsl:if test="@readonly='yes' or @readonly='true'">
				<xsl:attribute name="readonly">true</xsl:attribute>
			</xsl:if>
			<xsl:attribute name="onblur">
                <xsl:text>evaluateDocument(false);</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="class">
                <xsl:text>form-control</xsl:text>
            </xsl:attribute>
			<xsl:if test="@tooltip">
				<xsl:attribute name="title">
                    <xsl:value-of select="@tooltip" />
                </xsl:attribute>
				<xsl:attribute name="data-toggle">
                    <xsl:value-of select="tooltip" />
                </xsl:attribute>
			</xsl:if>
			<xsl:if test="@fieldCode">
				<xsl:attribute name="aria-describedby">
                    <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                    <xsl:value-of select="@id" />
                </xsl:attribute>
			</xsl:if>
		</input>
	</xsl:template>
	
	<xsl:template name="uuid-processing">
		<xsl:if test="@fieldCode">
			<div class="input-group">
				<span class="input-group-addon">
					<xsl:attribute name="id">
                        <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                        <xsl:value-of select="@id" />
                    </xsl:attribute>
					<xsl:value-of select="@fieldCode" />
				</span>
				<xsl:call-template name="uuid-processing-inner" />
			</div>
		</xsl:if>
		<xsl:if test="not(@fieldCode)">
			<xsl:call-template name="uuid-processing-inner" />
		</xsl:if>
	</xsl:template>
	<xsl:template name="uuid-processing-inner">
		<input>
			<xsl:attribute name="value">
                <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text disable-output-escaping="yes">|default_if_none:''}}</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="id">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="name">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
			<xsl:if test="@readonly='yes' or @readonly='true'">
				<xsl:attribute name="readonly">true</xsl:attribute>
			</xsl:if>
			<xsl:attribute name="onblur">
                <xsl:text>evaluateDocument(false);</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="class">
                <xsl:text>form-control</xsl:text>
            </xsl:attribute>
			<xsl:if test="@tooltip">
				<xsl:attribute name="title">
                    <xsl:value-of select="@tooltip" />
                </xsl:attribute>
				<xsl:attribute name="data-toggle">
                    <xsl:value-of select="tooltip" />
                </xsl:attribute>
			</xsl:if>
			<xsl:if test="@fieldCode">
				<xsl:attribute name="aria-describedby">
                    <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                    <xsl:value-of select="@id" />
                </xsl:attribute>
			</xsl:if>
		</input>
	</xsl:template>
	
	<xsl:template name="document-processing">
		<xsl:if test="@fieldCode">
			<div class="input-group">
				<span class="input-group-addon">
					<xsl:attribute name="id">
                        <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                        <xsl:value-of select="@id" />
                    </xsl:attribute>
					<xsl:value-of select="@fieldCode" />
				</span>
				<xsl:call-template name="document-processing-inner" />
			</div>
		</xsl:if>
		<xsl:if test="not(@fieldCode)">
			<xsl:call-template name="document-processing-inner" />
		</xsl:if>
	</xsl:template>
	<xsl:template name="document-processing-inner">
		<input>
			<xsl:attribute name="type">
                <xsl:text disable-output-escaping="yes">hidden</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="value">
                <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text disable-output-escaping="yes">.id|default_if_none:''}}</xsl:text>
            </xsl:attribute>
            <xsl:attribute name="id">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
            <xsl:attribute name="name">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
		</input>
		<input>
			<xsl:attribute name="value">
                <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text disable-output-escaping="yes">.header.hrn_code|default_if_none:''}}</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="id">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>_inner_value]</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="name">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>_inner_value]</xsl:text>
            </xsl:attribute>
			<xsl:if test="@readonly='yes' or @readonly='true'">
				<xsl:attribute name="readonly">true</xsl:attribute>
			</xsl:if>
			<xsl:attribute name="onblur">
                <xsl:text>evaluateDocument(false);</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="class">
                <xsl:text>form-control</xsl:text>
            </xsl:attribute>
			<xsl:if test="@tooltip">
				<xsl:attribute name="title">
                    <xsl:value-of select="@tooltip" />
                </xsl:attribute>
				<xsl:attribute name="data-toggle">
                    <xsl:value-of select="tooltip" />
                </xsl:attribute>
			</xsl:if>
			<xsl:if test="@fieldCode">
				<xsl:attribute name="aria-describedby">
                    <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                    <xsl:value-of select="@id" />
                </xsl:attribute>
			</xsl:if>
		</input>
	</xsl:template>
	<xsl:template name="list-string-processing">
		<xsl:if test="@fieldCode">
			<div class="input-group">
				<span class="input-group-addon">
					<xsl:attribute name="id">
                        <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                        <xsl:value-of select="@id" />
                    </xsl:attribute>
					<xsl:value-of select="@fieldCode" />
				</span>
				<xsl:call-template name="list-string-processing-inner" />
			</div>
		</xsl:if>
		<xsl:if test="not(@fieldCode)">
			<xsl:call-template name="list-string-processing-inner" />
		</xsl:if>
	</xsl:template>
	<xsl:template name="list-string-processing-inner">
		<input type="hidden">
			<xsl:attribute name="value">
                <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text disable-output-escaping="yes">|default_if_none:''}}</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="id">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="name">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
			<xsl:if test="@readonly='yes' or @readonly='true'">
				<xsl:attribute name="readonly">true</xsl:attribute>
			</xsl:if>
			<xsl:attribute name="onblur">
                <xsl:text>evaluateDocument(false);</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="class">
                <xsl:text>form-control</xsl:text>
            </xsl:attribute>
			<xsl:if test="@tooltip">
				<xsl:attribute name="title">
                    <xsl:value-of select="@tooltip" />
                </xsl:attribute>
				<xsl:attribute name="data-toggle">
                    <xsl:value-of select="tooltip" />
                </xsl:attribute>
			</xsl:if>
			<xsl:if test="@fieldCode">
				<xsl:attribute name="aria-describedby">
                    <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                    <xsl:value-of select="@id" />
                </xsl:attribute>
			</xsl:if>
		</input>
		<script type="text/javascript">
			<xsl:text disable-output-escaping="yes">create_select_field("</xsl:text>
			<xsl:value-of select="@id" />
			<xsl:text disable-output-escaping="yes">", "</xsl:text>
			<xsl:value-of select="@catalogId" />
			<xsl:text disable-output-escaping="yes">");</xsl:text>
		</script>
	</xsl:template>
	<xsl:template name="checkbox-string-processing">
		<xsl:if test="@fieldCode">
			<div class="input-group">
				<span class="input-group-addon">
					<xsl:attribute name="id">
                        <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                        <xsl:value-of select="@id" />
                    </xsl:attribute>
					<xsl:value-of select="@fieldCode" />
				</span>
				<xsl:call-template name="checkbox-string-processing-inner" />
			</div>
		</xsl:if>
		<xsl:if test="not(@fieldCode)">
			<xsl:call-template name="checkbox-string-processing-inner" />
		</xsl:if>
	</xsl:template>
	<xsl:template name="checkbox-string-processing-inner">
		<input>
			<xsl:attribute name="value">
                <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text disable-output-escaping="yes">|default_if_none:''}}</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="id">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="name">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
			<xsl:if test="@readonly='yes' or @readonly='true'">
				<xsl:attribute name="readonly">true</xsl:attribute>
			</xsl:if>
			<xsl:attribute name="onblur">
                <xsl:text>evaluateDocument(false);</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="class">
                <xsl:text>form-control</xsl:text>
            </xsl:attribute>
			<xsl:if test="@tooltip">
				<xsl:attribute name="title">
                    <xsl:value-of select="@tooltip" />
                </xsl:attribute>
				<xsl:attribute name="data-toggle">
                    <xsl:value-of select="tooltip" />
                </xsl:attribute>
			</xsl:if>
			<xsl:if test="@fieldCode">
				<xsl:attribute name="aria-describedby">
                    <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                    <xsl:value-of select="@id" />
                </xsl:attribute>
			</xsl:if>
		</input>
	</xsl:template>
	<xsl:template name="radio-string-processing">
		<xsl:if test="@fieldCode">
			<div class="input-group">
				<span class="input-group-addon">
					<xsl:attribute name="id">
                        <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                        <xsl:value-of select="@id" />
                    </xsl:attribute>
					<xsl:value-of select="@fieldCode" />
				</span>
				<xsl:call-template name="radio-string-processing-inner" />
			</div>
		</xsl:if>
		<xsl:if test="not(@fieldCode)">
			<xsl:call-template name="radio-string-processing-inner" />
		</xsl:if>
	</xsl:template>
	<xsl:template name="radio-string-processing-inner">
		<input>
			<xsl:attribute name="value">
                <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text disable-output-escaping="yes">|default_if_none:''}}</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="id">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="name">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
			<xsl:if test="@readonly='yes' or @readonly='true'">
				<xsl:attribute name="readonly">true</xsl:attribute>
			</xsl:if>
			<xsl:attribute name="onblur">
                <xsl:text>evaluateDocument(false);</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="class">
                <xsl:text>form-control</xsl:text>
            </xsl:attribute>
			<xsl:if test="@tooltip">
				<xsl:attribute name="title">
                    <xsl:value-of select="@tooltip" />
                </xsl:attribute>
				<xsl:attribute name="data-toggle">
                    <xsl:value-of select="tooltip" />
                </xsl:attribute>
			</xsl:if>
			<xsl:if test="@fieldCode">
				<xsl:attribute name="aria-describedby">
                    <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                    <xsl:value-of select="@id" />
                </xsl:attribute>
			</xsl:if>
		</input>
	</xsl:template>
	<xsl:template name="textarea-processing">
		<xsl:if test="@fieldCode">
			<div class="input-group">
				<span class="input-group-addon">
					<xsl:attribute name="id">
                        <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                        <xsl:value-of select="@id" />
                    </xsl:attribute>
					<xsl:value-of select="@fieldCode" />
				</span>
				<xsl:call-template name="textarea-processing-inner" />
			</div>
		</xsl:if>
		<xsl:if test="not(@fieldCode)">
			<xsl:call-template name="textarea-processing-inner" />
		</xsl:if>
	</xsl:template>
	<xsl:template name="textarea-processing-inner">
		<input>
			<xsl:attribute name="value">
                <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text disable-output-escaping="yes">|default_if_none:''}}</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="id">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="name">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
			<xsl:if test="@readonly='yes' or @readonly='true'">
				<xsl:attribute name="readonly">true</xsl:attribute>
			</xsl:if>
			<xsl:attribute name="onblur">
                <xsl:text>evaluateDocument(false);</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="class">
                <xsl:text>form-control</xsl:text>
            </xsl:attribute>
			<xsl:if test="@tooltip">
				<xsl:attribute name="title">
                    <xsl:value-of select="@tooltip" />
                </xsl:attribute>
				<xsl:attribute name="data-toggle">
                    <xsl:value-of select="tooltip" />
                </xsl:attribute>
			</xsl:if>
			<xsl:if test="@fieldCode">
				<xsl:attribute name="aria-describedby">
                    <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                    <xsl:value-of select="@id" />
                </xsl:attribute>
			</xsl:if>
		</input>
	</xsl:template>
	<xsl:template name="textarea-editor-processing">
		<xsl:if test="@fieldCode">
			<div class="input-group">
				<span class="input-group-addon">
					<xsl:attribute name="id">
                        <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                        <xsl:value-of select="@id" />
                    </xsl:attribute>
					<xsl:value-of select="@fieldCode" />
				</span>
				<xsl:call-template name="textarea-editor-processing-inner" />
			</div>
		</xsl:if>
		<xsl:if test="not(@fieldCode)">
			<xsl:call-template name="textarea-editor-processing-inner" />
		</xsl:if>
	</xsl:template>
	<xsl:template name="textarea-editor-processing-inner">
		<input>
			<xsl:attribute name="value">
                <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text disable-output-escaping="yes">|default_if_none:''}}</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="id">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="name">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
			<xsl:if test="@readonly='yes' or @readonly='true'">
				<xsl:attribute name="readonly">true</xsl:attribute>
			</xsl:if>
			<xsl:attribute name="onblur">
                <xsl:text>evaluateDocument(false);</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="class">
                <xsl:text>form-control</xsl:text>
            </xsl:attribute>
			<xsl:if test="@tooltip">
				<xsl:attribute name="title">
                    <xsl:value-of select="@tooltip" />
                </xsl:attribute>
				<xsl:attribute name="data-toggle">
                    <xsl:value-of select="tooltip" />
                </xsl:attribute>
			</xsl:if>
			<xsl:if test="@fieldCode">
				<xsl:attribute name="aria-describedby">
                    <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                    <xsl:value-of select="@id" />
                </xsl:attribute>
			</xsl:if>
		</input>
	</xsl:template>
	<xsl:template name="autocomplete-string-processing">
		<xsl:if test="@fieldCode">
			<div class="input-group">
				<span class="input-group-addon">
					<xsl:attribute name="id">
                        <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                        <xsl:value-of select="@id" />
                    </xsl:attribute>
					<xsl:value-of select="@fieldCode" />
				</span>
				<xsl:call-template name="autocomplete-string-processing-inner" />
			</div>
		</xsl:if>
		<xsl:if test="not(@fieldCode)">
			<xsl:call-template name="autocomplete-string-processing-inner" />
		</xsl:if>
	</xsl:template>
	<xsl:template name="autocomplete-string-processing-inner">
		<input>
			<xsl:attribute name="value">
                <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text disable-output-escaping="yes">|default_if_none:''}}</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="id">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="name">
                <xsl:text>fields[</xsl:text>
                <xsl:value-of select="@id" />
                <xsl:text>]</xsl:text>
            </xsl:attribute>
			<xsl:if test="@readonly='yes' or @readonly='true'">
				<xsl:attribute name="readonly">true</xsl:attribute>
			</xsl:if>
			<xsl:attribute name="onblur">
                <xsl:text>evaluateDocument(false);</xsl:text>
            </xsl:attribute>
			<xsl:attribute name="class">
                <xsl:text>form-control</xsl:text>
            </xsl:attribute>
			<xsl:if test="@tooltip">
				<xsl:attribute name="title">
                    <xsl:value-of select="@tooltip" />
                </xsl:attribute>
				<xsl:attribute name="data-toggle">
                    <xsl:value-of select="tooltip" />
                </xsl:attribute>
			</xsl:if>
			<xsl:if test="@fieldCode">
				<xsl:attribute name="aria-describedby">
                    <xsl:text disable-output-escaping="yes">fieldCode_</xsl:text>
                    <xsl:value-of select="@id" />
                </xsl:attribute>
			</xsl:if>
		</input>
		<script type="text/javascript">
			<xsl:text disable-output-escaping="yes">create_autocomplete_field("</xsl:text>
			<xsl:value-of select="@id" />
			<xsl:text disable-output-escaping="yes">", "</xsl:text>
			<xsl:value-of select="@catalogId" />
			<xsl:text disable-output-escaping="yes">");</xsl:text>
		</script>
	</xsl:template>
</xsl:stylesheet>