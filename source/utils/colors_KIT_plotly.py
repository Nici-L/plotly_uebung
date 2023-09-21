# extension of plotly express color palettes by KIT colors
import plotly.express as px

## rgba values of the colors from the .pptx template

gray_base = 'rgba(217,217,217,1)'
gray_dark10 = 'rgba(195,195,195,1)'
gray_dark25 = 'rgba(163,163,163,1)'
gray_dark50 = 'rgba(109,109,109,1)'
gray_dark75 = 'rgba(54,54,54,1)'
gray_dark90 = 'rgba(22,22,22,1)'

green1_base = 'rgba(0,150,130,1)'
green1_bright80 = 'rgba(183,255,245,1)'
green1_bright60 = 'rgba(111,255,236,1)'
green1_bright40 = 'rgba(39,255,226,1)'
green1_dark25 = 'rgba(0,113,98,1)'
green1_dark50 = 'rgba(0,75,65,1)'

blue2_base = 'rgba(70,100,170,1)'
blue2_bright80 = 'rgba(217,223,239,1)'
blue2_bright60 = 'rgba(179,192,223,1)'
blue2_bright40 = 'rgba(140,161,208,1)'
blue2_dark25 = 'rgba(53,75,127,1)'
blue2_dark50 = 'rgba(35,50,85,1)'

green4_base = 'rgba(76,181,167,1)'
green4_bright80 = 'rgba(219,240,237,1)'
green4_bright60 = 'rgba(183,225,220,1)'
green4_bright40 = 'rgba(148,211,202,1)'
green4_dark25 = 'rgba(56,136,126,1)'
green4_dark50 = 'rgba(38,91,84,1)'

blue5_base = 'rgba(125,146,195,1)'
blue5_bright80 = 'rgba(229,233,243,1)'
blue5_bright60 = 'rgba(203,211,231,1)'
blue5_bright40 = 'rgba(177,190,219,1)'
blue5_dark25 = 'rgba(76,102,164,1)'
blue5_dark50 = 'rgba(51,68,109,1)'

green6_base = 'rgba(127,202,192,1)'
green6_bright80 = 'rgba(229,244,242,1)'
green6_bright60 = 'rgba(204,234,230,1)'
green6_bright40 = 'rgba(178,223,217,1)'
green6_dark25 = 'rgba(72,174,161,1)'
green6_dark50 = 'rgba(48,116,107,1)'

maygreen_base = 'rgba(140,182,60,1)'
maygreen_bright80 = 'rgba(232,242,215,1)'
maygreen_bright60 = 'rgba(210,228,174,1)'
maygreen_bright40 = 'rgba(187,215,134,1)'
maygreen_dark25 = 'rgba(105,136,45,1)'
maygreen_dark50 = 'rgba(70,91,30,1)'

yellow_base = 'rgba(252,229,0,1)'
yellow_bright80 = 'rgba(255,250,203,1)'
yellow_bright60 = 'rgba(255,246,152,1)'
yellow_bright40 = 'rgba(255,241,100,1)'
yellow_dark25 = 'rgba(189,172,0,1)'
yellow_dark50 = 'rgba(126,114,0,1)'

orange_base = 'rgba(223,155,27,1)'
orange_bright80 = 'rgba(249,235,209,1)'
orange_bright60 = 'rgba(244,215,162,1)'
orange_bright40 = 'rgba(238,196,116,1)'
orange_dark25 = 'rgba(167,116,20,1)'
orange_dark50 = 'rgba(111,78,14,1)'

brown_base = 'rgba(167,130,46,1)'
brown_bright80 = 'rgba(242,232,208,1)'
brown_bright60 = 'rgba(229,209,162,1)'
brown_bright40 = 'rgba(217,186,115,1)'
brown_dark25 = 'rgba(125,98,35,1)'
brown_dark50 = 'rgba(83,65,23,1)'

red_base = 'rgba(162,34,35,1)'
red_bright80 = 'rgba(244,203,203,1)'
red_bright60 = 'rgba(233,151,152,1)'
red_bright40 = 'rgba(222,99,100,1)'
red_dark25 = 'rgba(122,25,26,1)'
red_dark50 = 'rgba(81,17,18,1)'

purple_base = 'rgba(163,16,124,1)'
purple_bright80 = 'rgba(249,195,235,1)'
purple_bright60 = 'rgba(243,134,214,1)'
purple_bright40 = 'rgba(237,74,194,1)'
purple_dark25 = 'rgba(122,12,93,1)'
purple_dark50 = 'rgba(82,8,62,1)'

cyan_base = 'rgba(35,161,224,1)'
cyan_bright80 = 'rgba(211,236,249,1)'
cyan_bright60 = 'rgba(167,217,243,1)'
cyan_bright40 = 'rgba(123,199,236,1)'
cyan_dark25 = 'rgba(24,122,170,1)'
cyan_dark50 = 'rgba(16,81,114,1)'

white_base = 'rgba(255,255,255,1)'
white_dark5 = 'rgba(242,242,242,1)'
white_dark15 = 'rgba(217,217,217,1)'
white_dark25 = 'rgba(191,191,191,1)'
white_dark35 = 'rgba(166,166,166,1)'
white_dark50 = 'rgba(127,127,127,1)'

black_base = 'rgba(0,0,0,1)'
black_bright5 = 'rgba(13,13,13,1)'
black_bright15 = 'rgba(38,38,38,1)'
black_bright25 = 'rgba(64,64,64,1)'
black_bright35 = 'rgba(89,89,89,1)'
black_bright50 = 'rgba(127,127,127,1)'

## addition to plotly color palettes
px.colors.qualitative.KITgray = (gray_base, gray_dark10, gray_dark25, gray_dark50,
                                      gray_dark75, gray_dark90)
px.colors.qualitative.KITgreen1 = (green1_base, green1_bright80, green1_bright60, green1_bright40,
                                      green1_dark25, green1_dark50)
px.colors.qualitative.KITblue2 = (blue2_base, blue2_bright80, blue2_bright60, blue2_bright40,
                                      blue2_dark25, blue2_dark50)
px.colors.qualitative.KITgreen4 = (green4_base, green4_bright80, green4_bright60, green4_bright40,
                                      green4_dark25, green4_dark50)
px.colors.qualitative.KITblue5 = (blue5_base, blue5_bright80, blue5_bright60, blue5_bright40,
                                      blue5_dark25, blue5_dark50)
px.colors.qualitative.KITgreen6 = (green6_base, green6_bright80, green6_bright60, green6_bright40,
                                      green6_dark25, green6_dark50)
px.colors.qualitative.KITmaygreen = (maygreen_base, maygreen_bright80, maygreen_bright60, maygreen_bright40,
                                      maygreen_dark25, maygreen_dark50)
px.colors.qualitative.KITyellow = (yellow_base, yellow_bright80, yellow_bright60, yellow_bright40,
                                      yellow_dark25, yellow_dark50)
px.colors.qualitative.KITorange = (orange_base, orange_bright80, orange_bright60, orange_bright40,
                                      orange_dark25, orange_dark50)
px.colors.qualitative.KITbrown = (brown_base, brown_bright80, brown_bright60, brown_bright40,
                                      brown_dark25, brown_dark50)
px.colors.qualitative.KITred = (red_base, red_bright80, red_bright60, red_bright40,
                                      red_dark25, red_dark50)
px.colors.qualitative.KITpurple = (purple_base, purple_bright80, purple_bright60, purple_bright40,
                                      purple_dark25, purple_dark50)
px.colors.qualitative.KITcyan = (cyan_base, cyan_bright80, cyan_bright60, cyan_bright40,
                                      cyan_dark25, cyan_dark50)

px.colors.qualitative.KITwhite = (white_base, white_dark5, white_dark15,
                                  white_dark25, white_dark35, white_dark50)

px.colors.qualitative.KITblack = (black_base, black_bright5, black_bright15,
                                  black_bright25, black_bright35, black_bright50)
