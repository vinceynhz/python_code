<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="utf-8" />
<xsl:template match="/">
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="web/css/theme.css" />
    </head>
    <body>
        <xsl:variable name="url" select="/ColorPalette/@url" />

        <h2><xsl:value-of select="/ColorPalette/@name" /></h2>
        <h3><a href="{$url}"><xsl:value-of select="$url" /></a></h3>

        <xsl:for-each select="/ColorPalette/Palette">
        <div class="container">
        <div class="list-container palette">
            <xsl:variable name="name" select="./@name" />
            <xsl:variable name="purl" select="./@url" />
            <h3><xsl:value-of select="$name" /></h3>
            <h4><a href="{$purl}"><xsl:value-of select="$purl" /></a></h4>
            <ul>
            <xsl:for-each select="./Color">
                <xsl:variable name="color" select="./@value" />
                <xsl:variable name="hex" select="./@hex" />
                <xsl:variable name="hsl" select="./@hsl" />
                <xsl:variable name="hsv" select="./@hsv" />
                <xsl:variable name="cmyk" select="./@cmyk" />
                <xsl:variable name="xyz" select="./@xyz" />
                <xsl:variable name="x" select="substring-before($xyz, ',')" />
                <xsl:variable name="y" select="substring-before( substring-after($xyz, ','), ',')" />

                <li>
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
                </li>
            </xsl:for-each>
            </ul>
        </div>
        
        <div class="map">
            <h3>Hue Saturation Value</h3>
            <canvas width="270" height="297" />
        </div>
        <div class="cromaticity">
            <h3>CIE 1931 xy</h3>
            <canvas width="270" height="297" />
            <!--img src="../img/CIE1931xy.png" width="250" height="265" /-->
        </div>
        </div>
        </xsl:for-each>
        <script type="text/javascript" src="web/js/maps.js"></script>
    </body>
</html>
</xsl:template>

</xsl:stylesheet>