<?xml version="1.0" encoding="UTF-8"?>

<!-- Document : procEditTwig.xslt.xsl Created on : November 10, 2015, 2:31 
	AM Author : leobelen Description: Purpose of transformation follows. -->
<xsl:stylesheet
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="xml" encoding="utf-8"
		omit-xml-declaration="yes" indent="yes" />
	<xsl:template match="/">
		<xsl:text disable-output-escaping="yes"><![CDATA[{% extends template %} 
{% load static i18n markdown_deux_tags pipeline %} 

{% block title %}Antares Document{% endblock %}
{% block ng_app_name %}{% endblock ng_app_name %}
{% block bodyId %}Antares Document{% endblock %}
{% block javascript %} 
    {% if is_inner == 'false' %}
        {% javascript 'jquery_ui_js' %}
    {% endif %}
	{% javascript 'document_edit_common_js' %}
    <script type="text/javascript" src="{% get_media_prefix %}{{edit_js_path}}"></script>
{% endblock javascript %} 

{% block stylesheets %}
   {% if is_inner == 'false' %}
		{% stylesheet 'jquery_ui_css' %}
	{% endif %} 
{% endblock stylesheets %} 

{% block content %} ]]></xsl:text>
		<div class="container">
			<div class="row">
				<xsl:for-each select="document/structuredData[@title]">
					<div id="documentTitle" class="col-lg-12">
						<h4>
							<xsl:value-of select="@title" />
						</h4>
					</div>
				</xsl:for-each>
				<div id="documentEditTabs" class="col-lg-12">
					 <nav>
                        <div class="nav nav-tabs" id="nav-tab" role="tablist">
                          <xsl:for-each select="document/structuredData/page">
						  <button  data-bs-toggle="tab"  type="button" role="tab">
						  <xsl:if test="position()=1">
										<xsl:attribute name="class">
                                        <xsl:text
											disable-output-escaping="yes">nav-link</xsl:text>
                                    </xsl:attribute>
									<xsl:attribute name="aria-selected">
                                        <xsl:text
											disable-output-escaping="yes">true</xsl:text>
                                    </xsl:attribute>
									
									</xsl:if>
									<xsl:if test="position()>1">
										<xsl:attribute name="class">
                                        <xsl:text
											disable-output-escaping="yes">nav-link active</xsl:text>
                                    </xsl:attribute>
									<xsl:attribute name="aria-selected">
                                        <xsl:text
											disable-output-escaping="yes">false</xsl:text>
                                    </xsl:attribute>
									
									</xsl:if>
									
						  <xsl:attribute name="data-bs-target">
						   <xsl:value-of
											select="concat('#antaresDocumentPage-',position())" />
						  </xsl:attribute>
<xsl:attribute name="aria-controls">
						   <xsl:value-of
											select="concat('antaresDocumentPage-',position())" />
						  </xsl:attribute>
						  <xsl:attribute name="id">
						   <xsl:value-of
											select="concat('nav_antaresDocumentPage-',position())" />
						  </xsl:attribute>
						  <xsl:attribute name="aria-controls">
						   <xsl:value-of
											select="concat('navaria_antaresDocumentPage-',position())" />
						  </xsl:attribute>
						  <xsl:value-of select="@title" />
						  </button>
						  </xsl:for-each>
						  </div>
						</nav>
						
					<div class="tab-content">
						<xsl:for-each select="document/structuredData/page">
							<br />
							<div  role="tabpanel">
									<xsl:if test="position()=1">
										<xsl:attribute name="class">
                                        <xsl:text
											disable-output-escaping="yes">tab-pane fade show active</xsl:text>
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
								<xsl:attribute name="aria-labelledby">
                                    <xsl:value-of
											select="concat('nav_antaresDocumentPage-',position())" />
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
                                <xsl:value-of
								select="@colspan" />
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
							<xsl:call-template
								name="list-string-processing" />
						</xsl:when>
						<xsl:when test="@type='input' and @dataType='date'">
							<xsl:call-template name="input-date-processing" />
						</xsl:when>
						<xsl:when test="@type='checkbox' and @dataType='string'">
							<xsl:call-template
								name="checkbox-string-processing" />
						</xsl:when>
						<xsl:when test="@type='radiobox' and @dataType='string'">
							<xsl:call-template
								name="radio-string-processing" />
						</xsl:when>
						<xsl:when test="@type='textarea'">
							<xsl:call-template name="textarea-processing" />
						</xsl:when>
						<xsl:when test="@type='textarea-editor'">
							<xsl:call-template
								name="textarea-editor-processing" />
						</xsl:when>
						<xsl:when
							test="@type='autocomplete' and @dataType='string'">
							<xsl:call-template
								name="autocomplete-string-processing" />
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
                        <xsl:text
						disable-output-escaping="yes">fieldCode_</xsl:text>
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
			<xsl:attribute name="readonly">true</xsl:attribute>
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
                        <xsl:text
						disable-output-escaping="yes">fieldCode_</xsl:text>
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
			<xsl:attribute name="readonly">true</xsl:attribute>
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
                        <xsl:text
						disable-output-escaping="yes">fieldCode_</xsl:text>
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
			<xsl:attribute name="readonly">true</xsl:attribute>
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
                        <xsl:text
						disable-output-escaping="yes">fieldCode_</xsl:text>
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
			<xsl:attribute name="readonly">true</xsl:attribute>
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
                        <xsl:text
						disable-output-escaping="yes">fieldCode_</xsl:text>
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
			<xsl:attribute name="readonly">true</xsl:attribute>
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
                        <xsl:text
						disable-output-escaping="yes">fieldCode_</xsl:text>
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
			<xsl:attribute name="readonly">true</xsl:attribute>
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
                        <xsl:text
						disable-output-escaping="yes">fieldCode_</xsl:text>
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
			<xsl:attribute name="readonly">true</xsl:attribute>
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
                        <xsl:text
						disable-output-escaping="yes">fieldCode_</xsl:text>
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
			<xsl:attribute name="readonly">true</xsl:attribute>
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
                        <xsl:text
						disable-output-escaping="yes">fieldCode_</xsl:text>
                        <xsl:value-of select="@id" />
                    </xsl:attribute>
					<xsl:value-of select="@fieldCode" />
				</span>
				<xsl:call-template
					name="document-processing-inner" />
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
			<xsl:attribute name="readonly">true</xsl:attribute>
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
                        <xsl:text
						disable-output-escaping="yes">fieldCode_</xsl:text>
                        <xsl:value-of select="@id" />
                    </xsl:attribute>
					<xsl:value-of select="@fieldCode" />
				</span>
				<xsl:call-template
					name="list-string-processing-inner" />
			</div>
		</xsl:if>
		<xsl:if test="not(@fieldCode)">
			<xsl:call-template
				name="list-string-processing-inner" />
		</xsl:if>
	</xsl:template>
	<xsl:template name="list-string-processing-inner">
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
			<xsl:attribute name="readonly">true</xsl:attribute>
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
	<xsl:template name="checkbox-string-processing">
		<xsl:if test="@fieldCode">
			<div class="input-group">
				<span class="input-group-addon">
					<xsl:attribute name="id">
                        <xsl:text
						disable-output-escaping="yes">fieldCode_</xsl:text>
                        <xsl:value-of select="@id" />
                    </xsl:attribute>
					<xsl:value-of select="@fieldCode" />
				</span>
				<xsl:call-template
					name="checkbox-string-processing-inner" />
			</div>
		</xsl:if>
		<xsl:if test="not(@fieldCode)">
			<xsl:call-template
				name="checkbox-string-processing-inner" />
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
			<xsl:attribute name="readonly">true</xsl:attribute>
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
                        <xsl:text
						disable-output-escaping="yes">fieldCode_</xsl:text>
                        <xsl:value-of select="@id" />
                    </xsl:attribute>
					<xsl:value-of select="@fieldCode" />
				</span>
				<xsl:call-template
					name="radio-string-processing-inner" />
			</div>
		</xsl:if>
		<xsl:if test="not(@fieldCode)">
			<xsl:call-template
				name="radio-string-processing-inner" />
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
			<xsl:attribute name="readonly">true</xsl:attribute>
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
                        <xsl:text
						disable-output-escaping="yes">fieldCode_</xsl:text>
                        <xsl:value-of select="@id" />
                    </xsl:attribute>
					<xsl:value-of select="@fieldCode" />
				</span>
				<xsl:call-template
					name="textarea-processing-inner" />
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
			<xsl:attribute name="readonly">true</xsl:attribute>
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
                        <xsl:text
						disable-output-escaping="yes">fieldCode_</xsl:text>
                        <xsl:value-of select="@id" />
                    </xsl:attribute>
					<xsl:value-of select="@fieldCode" />
				</span>
				<xsl:call-template
					name="textarea-editor-processing-inner" />
			</div>
		</xsl:if>
		<xsl:if test="not(@fieldCode)">
			<xsl:call-template
				name="textarea-editor-processing-inner" />
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
			<xsl:attribute name="readonly">true</xsl:attribute>
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
                        <xsl:text
						disable-output-escaping="yes">fieldCode_</xsl:text>
                        <xsl:value-of select="@id" />
                    </xsl:attribute>
					<xsl:value-of select="@fieldCode" />
				</span>
				<xsl:call-template
					name="autocomplete-string-processing-inner" />
			</div>
		</xsl:if>
		<xsl:if test="not(@fieldCode)">
			<xsl:call-template
				name="autocomplete-string-processing-inner" />
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
			<xsl:attribute name="readonly">true</xsl:attribute>
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
</xsl:stylesheet>