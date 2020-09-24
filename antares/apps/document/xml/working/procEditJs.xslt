<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns="http://www.w3.org/1999/xhtml" version="1.0">
	<xsl:output method="text" indent="yes"
		omit-xml-declaration="yes" />
	<xsl:template match="/">
		<!-- a general function to render a message -->
		<xsl:text><![CDATA[/*
 * Copyright (c) 2013-2017, Surfer Inc. and/or its affiliates. All rights reserved.
 * SURFERTANK INC. PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
 * 
 * Initial Release by Leonardo Javier Belen
 *
 * File automatically generated by Antares. Do not change. 
 */
 ]]></xsl:text>
		<xsl:text disable-output-escaping="yes">function getFieldDisplayName(fieldId) {switch(fieldId) {</xsl:text>
		<xsl:for-each select="//field[@type!='label']">
			<xsl:text disable-output-escaping="yes">case "</xsl:text>
			<xsl:value-of select="@id" />
			<xsl:text disable-output-escaping="yes">":</xsl:text>
			<xsl:if test="(@name and @fieldCode)">
				<xsl:text>return "</xsl:text>
				<xsl:value-of select="concat(@fieldCode, ' - ', @name)" />
				<xsl:text disable-output-escaping="yes">";</xsl:text>
			</xsl:if>
			<xsl:if test="(not(@name) and @fieldCode)">
				<xsl:text>return "</xsl:text>
				<xsl:value-of select="concat(@fieldCode, ' - ', @id)" />
				<xsl:text disable-output-escaping="yes">";</xsl:text>
			</xsl:if>
			<xsl:if test="(@name and not(@fieldCode))">
				<xsl:text>return "</xsl:text>
				<xsl:value-of select="@longName" />
				<xsl:text disable-output-escaping="yes">";</xsl:text>
			</xsl:if>
			<xsl:if test="(not(@name) and not(@fieldCode))">
				<xsl:text>return "</xsl:text>
				<xsl:value-of select="@id" />
				<xsl:text disable-output-escaping="yes">";</xsl:text>
			</xsl:if>
			<xsl:text>break;</xsl:text>
		</xsl:for-each>
		<xsl:text disable-output-escaping="yes">default: return</xsl:text>
		<xsl:value-of select="@id" />
		<xsl:text disable-output-escaping="yes">; } }</xsl:text>
		<xsl:text>function evaluateDocument(doValidations) {</xsl:text>
		<xsl:text>validationResult=true;</xsl:text>
		<xsl:for-each
			select="//field[@calculate='false' or not(@calculate)]">
			<!-- field Registration -->
			<xsl:if
				test="(@dataType='integer' or @dataType='float') and not(@calculate)">
				var
				<xsl:value-of select="@id" />
				<xsl:text>=$("#fields\\[</xsl:text>
				<xsl:value-of select="@id" />
				<xsl:text>\\]").val();</xsl:text>
			</xsl:if>
			<xsl:if test="(@dataType='date') and not(@calculate)">
				var
				<xsl:value-of select="@id" />
				<xsl:text>=new Date($("#fields\\[</xsl:text>
				<xsl:value-of select="@id" />
				<xsl:text>\\]").val());</xsl:text>
			</xsl:if>
			<xsl:if
				test="(@dataType='string' or @dataType='text') and not(@calculate)">
				var
				<xsl:value-of select="@id" />
				<xsl:text>=$("#fields\\[</xsl:text>
				<xsl:value-of select="@id" />
				<xsl:text>\\]").val();</xsl:text>
			</xsl:if>
		</xsl:for-each>
		<xsl:for-each select="//field[@calculate]">
			<xsl:sort data-type="number" select="@calculationOrder" />
			<!-- field calculation -->
			<xsl:if
				test="(@dataType='integer' or @dataType='float') and @calculate">
				var
				<xsl:value-of select="@id" />
				<xsl:text>=(</xsl:text>
				<xsl:value-of select="@calculate" />
				<xsl:text>);
                </xsl:text>
			</xsl:if>
		</xsl:for-each>
		<!-- field update -->
		<xsl:for-each select="//field">
			<xsl:if test="@calculate">
				<xsl:choose>
					<xsl:when test="@format='currency'">
						<xsl:text>$("#fields\\[</xsl:text>
						<xsl:value-of select="@id" />
						<xsl:text>\\]").val(</xsl:text>
						<xsl:value-of select="@id" />
						<xsl:text>);</xsl:text>
					</xsl:when>
					<xsl:when test="@format='percent'">
						<xsl:text>$("#fields\\[</xsl:text>
						<xsl:value-of select="@id" />
						<xsl:text>\\]").val(</xsl:text>
						<xsl:value-of select="@id" />
						<xsl:text>);</xsl:text>
					</xsl:when>
					<xsl:otherwise>
						<xsl:text>$("#fields\\[</xsl:text>
						<xsl:value-of select="@id" />
						<xsl:text>\\]").val(</xsl:text>
						<xsl:value-of select="@id" />
						<xsl:text>);</xsl:text>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
			<xsl:if test="(@dataType='string') and @calculate">
				<xsl:text>$("#fields\\[</xsl:text>
				<xsl:value-of select="@id" />
				<xsl:text>\\]").val(</xsl:text>
				<xsl:value-of select="@id" />
				<xsl:text>);</xsl:text>
			</xsl:if>
			<xsl:if test="(@dataType='date') and @calculate">
				<xsl:text>$("#fields\\[</xsl:text>
				<xsl:value-of select="@id" />
				<xsl:text>\\]")).val(</xsl:text>
				<xsl:value-of select="@id" />
				<xsl:text>);</xsl:text>
			</xsl:if>
		</xsl:for-each>
		<!-- -->
		<!-- validation processing -->
		<!--_______________________ -->
		<!-- -->
		<xsl:text>if(doValidations == true){</xsl:text>
		<xsl:for-each select="//field">
			<xsl:if test="@dataType='integer'">

				<!--<xsl:text>if(!(!isNaN(parseFloat(</xsl:text> <xsl:value-of select="@id"/> 
					<xsl:text disable-output-escaping="yes">)) &amp;&amp; isFinite(</xsl:text> 
					<xsl:value-of select="@id"/> <xsl:text>))) { validationResult=false; }</xsl:text> 
					<xsl:if test="//document/@allowNegativeNumbers='false' or not(//document/@allowNegativeNumbers)"> 
					<xsl:if test="not(@calculate)"> <xsl:text>if(</xsl:text> <xsl:value-of select="@id"/> 
					<xsl:text disable-output-escaping="yes">&lt;0){ renderMessage(getFieldDisplayName("</xsl:text> 
					<xsl:value-of select="@id"/> <xsl:text disable-output-escaping="yes">")+ 
					": The number cannot be negative", "The number stated in the field " + getFieldDisplayName("</xsl:text> 
					<xsl:value-of select="@id"/> <xsl:text disable-output-escaping="yes">")+ 
					" cannot be negative", "error"); $(</xsl:text> <xsl:value-of select="@id"/> 
					<xsl:text disable-output-escaping="yes">).focus(); validationResult=false; 
					}</xsl:text> </xsl:if> </xsl:if> -->
				<xsl:text>validationResult = validate_number_field_boundaries("</xsl:text>
				<xsl:value-of select="@id" />
				<xsl:text disable-output-escaping="yes">", </xsl:text>
				<xsl:value-of select="@id" />
				<xsl:text disable-output-escaping="yes">, validationResult);</xsl:text>
			</xsl:if>
			<xsl:if test="@dataType='float'">
				<!-- <xsl:text>if(!(!isNaN(parseFloat(</xsl:text> <xsl:value-of select="@id"/> 
					<xsl:text disable-output-escaping="yes">)) &amp;&amp; isFinite(</xsl:text> 
					<xsl:value-of select="@id"/> <xsl:text disable-output-escaping="yes">))) 
					{ validationResult=false; }</xsl:text> <xsl:if test="//document/@allowNegativeNumbers='false' 
					or not(//document/@allowNegativeNumbers)"> <xsl:if test="not(@calculate)"> 
					<xsl:text>if(</xsl:text> <xsl:value-of select="@id"/> <xsl:text disable-output-escaping="yes">&lt;0){ 
					renderMessage(getFieldDisplayName("</xsl:text> <xsl:value-of select="@id"/> 
					<xsl:text disable-output-escaping="yes">")+ ": The number cannot be negative", 
					"The number stated in the field " + getFieldDisplayName("</xsl:text> <xsl:value-of 
					select="@id"/> <xsl:text disable-output-escaping="yes">")+ " cannot be negative", 
					"error"); $(</xsl:text> <xsl:value-of select="@id"/> <xsl:text disable-output-escaping="yes">).focus(); 
					validationResult=false; }</xsl:text> </xsl:if> </xsl:if> -->
				<xsl:text>validationResult = validate_number_field_boundaries("</xsl:text>
				<xsl:value-of select="@id" />
				<xsl:text disable-output-escaping="yes">", </xsl:text>
				<xsl:value-of select="@id" />
				<xsl:text disable-output-escaping="yes">, validationResult);</xsl:text>
			</xsl:if>
			<!-- user based requeriments -->
			<xsl:if test="@required='true'">
				<xsl:text disable-output-escaping="yes">if(</xsl:text>
				<xsl:value-of select="@id" />
				<xsl:text disable-output-escaping="yes">==null or</xsl:text>
				<xsl:value-of select="@id" />
				<xsl:text disable-output-escaping="yes">==""){</xsl:text>
				<xsl:text disable-output-escaping="yes">renderMessage("Requirement not met",</xsl:text>
				<xsl:value-of select="@requiredMessage" />
				<xsl:text disable-output-escaping="yes">, "error"); validationResult=false; } }</xsl:text>
			</xsl:if>
			<!-- user based validations -->
			<xsl:if test="@validation">
				<xsl:text disable-output-escaping="yes">if(!(</xsl:text>
				<xsl:value-of select="@validation"
					disable-output-escaping="yes" />
				<xsl:text disable-output-escaping="yes">)){</xsl:text>
				<xsl:text disable-output-escaping="yes">renderMessage("Validation not met",</xsl:text>
				<xsl:value-of select="@validationMessage"
					disable-output-escaping="yes" />
				<xsl:text disable-output-escaping="yes">, "error"); validationResult=false; } }</xsl:text>
			</xsl:if>
		</xsl:for-each>
		<!-- end validations -->
		<xsl:text disable-output-escaping="yes">} return validationResult; }</xsl:text>
	</xsl:template>
</xsl:stylesheet>