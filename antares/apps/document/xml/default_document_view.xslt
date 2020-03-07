<?xml version="1.0" encoding="UTF-8"?>

<!--
    Document   : procEditTwig.xslt.xsl
    Created on : November 10, 2015, 2:31 AM
    Author     : leobelen
    Description:
        Purpose of transformation follows.
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="xml" encoding="utf-8" omit-xml-declaration="yes" indent="yes"/>
    <xsl:template match="/">
        <xsl:text disable-output-escaping="yes"><![CDATA[{% extends template %}
{% load static i18n  %} 

{% block title %}Antares Document{% endblock %}
{% block ng_app_name %}{% endblock ng_app_name %}
{% block bodyId %}Antares Document{% endblock %}
{% block javascript %} 
    {% if is_inner == 'false' %}
        <script type="text/javascript" src="{% static "jquery-ui/jquery-ui.js" %}"></script>
    {% endif %}
{% endblock javascript %} 

{% block stylesheets %}
    {% if is_inner == 'false' %}
        <link rel="stylesheet" href="{% static "jquery-ui/themes/base/jquery-ui.css" %}">
    <link rel="stylesheet" href="{% static "jquery-ui/themes/base/theme.css" %}">
    {% endif %}
{% endblock stylesheets %} 
 
{% block content %} ]]></xsl:text>
<div class="container">
        <form id="documentEditorForm" method="POST">
            <!-- 
                Lets start with the TABBED section....
             
            -->
            <div class="panel">
                <xsl:for-each select="document/structuredData/page">
                    <xsl:for-each select="line">
                        <xsl:sort data-type="number" select="line"/>
                        <xsl:call-template name="line-processing">
                            <xsl:with-param name="line" select="line"/>
                        </xsl:call-template>
                    </xsl:for-each>
                </xsl:for-each>
            </div>
        </form>
        </div>
        <xsl:text>{% endblock %}
        </xsl:text>
    </xsl:template>
    <xsl:template name="line-processing">
        <xsl:param name="line"/>
        <div class="row">
            <xsl:for-each select="field">
                <div>
                    <xsl:choose>
                        <xsl:when test="@colspan>1">
                            <xsl:attribute name="class">
                                <xsl:text>col-lg-</xsl:text>
                                <xsl:value-of select="@colspan"/>
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
                            <xsl:call-template name="label-processing"/>
                        </xsl:when>
                        <xsl:when test="@type='input' and @dataType='integer'">
                            <xsl:call-template name="integer-processing"/>
                        </xsl:when>
                        <xsl:when test="@type='input' and @dataType='float'">
                            <xsl:call-template name="float-processing"/>
                        </xsl:when>
                        <xsl:when test="@type='input' and @dataType='string'">
                            <xsl:call-template name="string-processing"/>
                        </xsl:when>
                        <xsl:when test="@type='list' and @dataType='string'">
                            <xsl:call-template name="list-string-processing"/>
                        </xsl:when>
                        <xsl:when test="@type='date' and @dataType='date'">
                            <xsl:call-template name="date-processing"/>
                        </xsl:when>
                        <xsl:when test="@type='checkbox' and @dataType='string'">
                            <xsl:call-template name="checkbox-string-processing"/>
                        </xsl:when>
                        <xsl:when test="@type='radiobox' and @dataType='string'">
                            <xsl:call-template name="radio-string-processing"/>
                        </xsl:when>
                        <xsl:when test="@type='textarea'">
                            <xsl:call-template name="textarea-processing"/>
                        </xsl:when>
                        <xsl:when test="@type='money'">
                            <xsl:call-template name="money-processing"/>
                        </xsl:when>
                        <xsl:when test="@type='textarea-editor'">
                            <xsl:call-template name="textarea-editor-processing"/>
                        </xsl:when>
                        <xsl:when test="@type='autocomplete' and @dataType='string'">
                            <xsl:call-template name="autocomplete-string-processing"/>
                        </xsl:when>
                        <xsl:when test="@dataType='uuid'">
                            <xsl:call-template name="uuid-processing"/>
                        </xsl:when>
                        <xsl:when test="@dataType='client'">
                            <xsl:call-template name="client-processing"/>
                        </xsl:when>
                        <xsl:when test="@dataType='user'">
                            <xsl:call-template name="user-processing"/>
                        </xsl:when>
                        <xsl:when test="@dataType='document'">
                            <xsl:call-template name="document-processing"/>
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
                    <xsl:attribute name="data-tooltip"/>
                    <xsl:attribute name="title">
                        <xsl:value-of select="@tooltip"/>
                    </xsl:attribute>
                    <xsl:value-of select="text()"/>
                </span>
            </xsl:when>
            <xsl:otherwise>
                <span>
                    <xsl:value-of select="text()"/>
                </span>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="integer-processing">
        <div>
            <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
            <xsl:value-of select="@id"/>
            <xsl:text disable-output-escaping="yes">|default_if_none:''}}</xsl:text>
        </div>
    </xsl:template>
    <xsl:template name="date-processing">
        <div>
            <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
            <xsl:value-of select="@id"/>
            <xsl:text disable-output-escaping="yes">|default_if_none:''}}</xsl:text>
        </div>
    </xsl:template>
    <xsl:template name="float-processing">
        <div>
            <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
            <xsl:value-of select="@id"/>
            <xsl:text disable-output-escaping="yes">|default_if_none:''}}</xsl:text>
        </div>
    </xsl:template>
    <xsl:template name="string-processing">
        <div>
            <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
            <xsl:value-of select="@id"/>
            <xsl:text disable-output-escaping="yes">|default_if_none:''}}</xsl:text>
        </div>
    </xsl:template>
    <xsl:template name="money-processing">
        <div>
            <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
            <xsl:value-of select="@id"/>
            <xsl:text disable-output-escaping="yes">|default_if_none:''}}</xsl:text>
        </div>
    </xsl:template>
    <xsl:template name="user-processing">
        <div>
            <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
            <xsl:value-of select="@id"/>
            <xsl:text disable-output-escaping="yes">|default_if_none:''}}</xsl:text>
        </div>
    </xsl:template>
    <xsl:template name="uuid-processing">
        <div>
            <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
            <xsl:value-of select="@id"/>
            <xsl:text disable-output-escaping="yes">|default_if_none:''}}</xsl:text>
        </div>
    </xsl:template>
    <xsl:template name="client-processing">
        <div>
            <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
            <xsl:value-of select="@id"/>
            <xsl:text disable-output-escaping="yes">|default_if_none:''}}</xsl:text>
        </div>
    </xsl:template>
    <xsl:template name="document-processing">
        <div>
            <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
            <xsl:value-of select="@id"/>
            <xsl:text disable-output-escaping="yes">.header.hrn_code|default_if_none:''}}</xsl:text>
        </div>
    </xsl:template>
    <xsl:template name="list-string-processing">
        <div>
            <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
            <xsl:value-of select="@id"/>
            <xsl:text disable-output-escaping="yes">|default_if_none:''}}</xsl:text>
        </div>
    </xsl:template>
    <xsl:template name="checkbox-string-processing">
        <div>
            <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
            <xsl:value-of select="@id"/>
            <xsl:text disable-output-escaping="yes">|default_if_none:''}}</xsl:text>
        </div>
    </xsl:template>
    <xsl:template name="radio-string-processing">
        <div>
            <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
            <xsl:value-of select="@id"/>
            <xsl:text disable-output-escaping="yes">|default_if_none:''}}</xsl:text>
        </div>
    </xsl:template>
    <xsl:template name="textarea-processing">
        <div>
            <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
            <xsl:value-of select="@id"/>
            <xsl:text disable-output-escaping="yes">|default_if_none:''}}</xsl:text>
        </div>
    </xsl:template>
    <xsl:template name="textarea-editor-processing">
        <div>
            <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
            <xsl:value-of select="@id"/>
            <xsl:text disable-output-escaping="yes">|default_if_none:''}}</xsl:text>
        </div>
    </xsl:template>
    <xsl:template name="autocomplete-string-processing">
        <div>
            <xsl:text disable-output-escaping="yes">{{fields.</xsl:text>
            <xsl:value-of select="@id"/>
            <xsl:text disable-output-escaping="yes">|default_if_none:''}}</xsl:text>
        </div>
    </xsl:template>
</xsl:stylesheet>