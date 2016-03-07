<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="utf-8" />
<xsl:template match="/">
<html lang="en">
    <head>
        <!-- <link rel="stylesheet" type="text/css" href="web/css/bootstrap.min.css" /> -->
        <link rel="stylesheet" type="text/css" href="web/css/theme.css" />
    </head>
    <body>
        <xsl:variable name="url" select="/ColorPalette/@url" />

        <h2><xsl:value-of select="/ColorPalette/@name" /></h2>
        <h3><a href="{$url}"><xsl:value-of select="$url" /></a></h3>

        <div class="list-container palette">
            <h3>Palette</h3>
            <ul>
            <xsl:for-each select="/ColorPalette/Palette/Color">
                <xsl:variable name="color" select="./@value" />
                <xsl:variable name="hex" select="./@hex" />
                <xsl:variable name="hsl" select="./@hsl" />
                <xsl:variable name="hsv" select="./@hsv" />
                <xsl:variable name="cmyk" select="./@cmyk" />
                <xsl:variable name="xyz" select="./@xyz" />
                <xsl:variable name="x" select="substring-before($xyz, ',')" />
                <xsl:variable name="y" select="substring-before( substring-after($xyz, ','), ',')" />
                <li>
                    <a href="#{$hex}">
                    <div class="color" style="background-color: rgb({$color});"></div>
                    <div class="color-info">
                        <table>
                            <tr>
                                <td><strong>RGB</strong></td>
                                <td><xsl:value-of select="$color" /></td>
                            </tr>
                            <tr>
                                <td><strong>HEX</strong></td>
                                <td><xsl:value-of select="$hex" /></td>
                            </tr>
                            <tr>
                                <td><strong>HSV</strong></td>
                                <td><xsl:value-of select="$hsv" /></td>
                            </tr>
                            <tr>
                                <td><strong>HSL</strong></td>
                                <td><xsl:value-of select="$hsl" /></td>
                            </tr>
                            <tr>
                                <td><strong>CMYK</strong></td>
                                <td><xsl:value-of select="$cmyk" /></td>
                            </tr>
                            <tr>
                                <td><strong>CIE x</strong></td>
                                <td><xsl:value-of select="$x" /></td>
                            </tr>
                            <tr>
                                <td><strong>CIE y</strong></td>
                                <td><xsl:value-of select="$y" /></td>
                            </tr>
                        </table>
                    </div>
                    </a>
                </li>
            </xsl:for-each>
            </ul>
        </div>
        <div class="page-container swatches">
            <ul class="pages">
            <xsl:for-each select="/ColorPalette/Swatches">
                <xsl:variable name="id" select="./@id" />
                <li id="{$id}" class="page">
                <xsl:for-each select="./Swatch">
                    <xsl:variable name="name" select="./@name" />
                    <h4><xsl:value-of select="$name" /></h4>
                    <div class="list-container">
                        <ul>
                        <xsl:for-each select="./Color">
                            <xsl:variable name="color" select="./@value" />
                            <xsl:variable name="hex" select="./@hex" />
                            <xsl:variable name="hsl" select="./@hsl" />
                            <xsl:variable name="hsv" select="./@hsv" />
                            <li>
                                <div class="color" style="background-color: rgb({$color});"
                                     data-toggle="tooltip" title="RGB: {$color}&#10;HEX: {$hex}&#10;HSV: {$hsv}&#10;HSL: {$hsl}"></div>
                            </li>
                        </xsl:for-each>
                        </ul>
                    </div>
                </xsl:for-each>
                </li>
            </xsl:for-each>
            </ul>
        </div>
        <div class="map map-margin">
            <h3>Hue Saturation Value</h3>
            <canvas width="270" height="297" />
        </div>
        <div class="cromaticity map-margin">
            <h3>CIE 1931 xy</h3>
            <canvas width="270" height="297" />
            <!--img src="../img/CIE1931xy.png" width="250" height="265" /-->
        </div>
        <script type="text/javascript" src="web/js/maps.js"></script>
        <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
        <script type="text/javascript" src="web/js/bootstrap.min.js"></script>
    </body>
</html>
</xsl:template>

</xsl:stylesheet>