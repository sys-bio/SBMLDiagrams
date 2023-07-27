# -*- coding: utf-8 -*-
# This script was written by Jin Xu and available on Github
# https://github.com/SunnyXu/SBMLDiagrams

"""
Created on Mon Aug 23 13:25:34 2021
@author: Jin Xu
"""

import os, sys
from tempfile import TemporaryFile
import simplesbml
import libsbml
import math
import random as _random
import pandas as pd
from SBMLDiagrams import exportSBML
from SBMLDiagrams import editSBML
from SBMLDiagrams import visualizeSBML
from SBMLDiagrams import styleSBML
from SBMLDiagrams import point
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from collections import defaultdict
import json
import numpy as np

#create datafames for NodeData, ReactionData, CompartmentData:
# Column names
netIdx = 0
NETIDX = 'net_idx'
IDX = 'idx'
ID = 'id'
POSITION = 'position'
SIZE = 'size'
FILLCOLOR = 'fill_color'
BORDERCOLOR = 'border_color'
BORDERWIDTH = 'border_width'
COMPIDX = 'comp_idx'
ORIGINALIDX = 'original_idx'
FLOATINGNODE = 'floating_node'
CONCENTRATION = 'concentration'
SHAPEIDX = 'shape_idx'
RXNID = 'rxn_id'
TXTID = 'txt_id'
TXTCONTENT = 'txt_content'
TXTPOSITION = 'txt_position'
TXTSIZE = 'txt_size'
TXTFONTCOLOR = 'txt_font_color'
TXTLINEWIDTH = 'txt_line_width'
TXTFONTSIZE = 'txt_font_size'
TXTFONTFAMILY = 'txt_font_family'
SHAPENAME = 'shape_name'
SHAPETYPE = 'shape_type'
SHAPEINFO = 'shape_info'
SOURCES = 'sources'
TARGETS = 'targets'
RATELAW = 'rate_law'
MODIFIERS = 'modifiers'
LINETHICKNESS = 'line_thickness'
CENTERPOS = 'center_pos'
HANDLES = 'handles'
BEZIER = 'bezier'
ARROWHEADSIZE = 'arrow_head_size'
RXNDASH = "rxn_dash"
RXNREV = "rxn_reversible"
STROKECOLOR = "stroke_color"
TXTANCHOR = 'txt_anchor'
SOURCESLINEENDING = 'sources_lineending'
TARGETSLINEENDING = 'targets_lineending'
MODIFIERSLINEENDING = 'modifiers_lineending'
SRCLINEENDPOS = 'src_lineend_position'
TGTLINEENDPOS = 'tgt_lineend_position'
MODLINEENDPOS = 'mod_lineend_position'
CENTERSIZE = 'center_size'
SRCDASH = 'src_dash'
TGTDASH = 'tgt_dash'
SPECDASH = 'spec_dash'
COLUMN_NAME_df_CompartmentData = [NETIDX, IDX, ID,\
    POSITION, SIZE, FILLCOLOR, BORDERCOLOR, BORDERWIDTH, 
    TXTPOSITION, TXTSIZE, TXTCONTENT, \
    TXTFONTCOLOR, TXTLINEWIDTH, TXTFONTSIZE, TXTANCHOR,\
    SHAPENAME, SHAPETYPE, SHAPEINFO]
COLUMN_NAME_df_NodeData = [NETIDX, COMPIDX, IDX, ORIGINALIDX, ID, FLOATINGNODE,\
    CONCENTRATION, POSITION, SIZE, SHAPEIDX, TXTPOSITION, TXTSIZE, \
    FILLCOLOR, BORDERCOLOR, BORDERWIDTH, TXTFONTCOLOR, TXTLINEWIDTH, TXTFONTSIZE, 
    SHAPENAME, SHAPETYPE, SHAPEINFO, TXTCONTENT, TXTANCHOR, SPECDASH, TXTFONTFAMILY]
COLUMN_NAME_df_ReactionData = [NETIDX, IDX, ID, SOURCES, TARGETS, RATELAW, MODIFIERS, \
    STROKECOLOR, LINETHICKNESS, CENTERPOS, HANDLES, BEZIER, ARROWHEADSIZE, RXNDASH, RXNREV, 
    FILLCOLOR, SOURCESLINEENDING, TARGETSLINEENDING, MODIFIERSLINEENDING, 
    SRCLINEENDPOS, TGTLINEENDPOS, MODLINEENDPOS, CENTERSIZE, SHAPENAME, SHAPETYPE, SHAPEINFO,
    SRCDASH, TGTDASH]
COLUMN_NAME_df_TextData = [TXTCONTENT, TXTPOSITION, TXTSIZE, 
    TXTFONTCOLOR, TXTLINEWIDTH, TXTFONTSIZE, ID, TXTANCHOR]
COLUMN_NAME_df_ShapeData = [SHAPENAME, POSITION, SIZE, FILLCOLOR, BORDERCOLOR, BORDERWIDTH, 
                        SHAPETYPE, SHAPEINFO]
COLUMN_NAME_df_LineEndingData = [ID, POSITION, SIZE, FILLCOLOR, SHAPETYPE, SHAPEINFO, BORDERCOLOR]
COLUMN_NAME_df_ReactionTextData = [RXNID, TXTID, TXTCONTENT, TXTPOSITION, TXTSIZE, 
    TXTFONTCOLOR, TXTLINEWIDTH, TXTFONTSIZE, TXTANCHOR]
# #This is not supported by SBML
# COLUMN_NAME_df_text = [TXTCONTENT, TXTPOSITION, TXTFONTCOLOR, TXTLINEWIDTH, TXTFONTSIZE]

# DIR = os.path.dirname(os.path.abspath(__file__))
# color_xls = pd.ExcelFile(os.path.join(DIR, 'colors.xlsx'))
# df_color = pd.read_excel(color_xls, sheet_name = 'colors')
color_data = {"decimal_rgb": ['[240,248,255]', '[250,235,215]', '[0,255,255]', '[127,255,212]', '[240,255,255]', '[245,245,220]', '[255,228,196]', '[0,0,0]', '[255,235,205]', '[0,0,255]', '[138,43,226]', '[165,42,42]', '[222,184,135]', '[95,158,160]', '[127,255,0]', '[210,105,30]', '[255,127,80]', '[100,149,237]', '[255,248,220]', '[220,20,60]', '[0,255,255]', '[0,0,139]', '[0,139,139]', '[184,134,11]', '[169,169,169]', '[0,100,0]', '[189,183,107]', '[139,0,139]', '[85,107,47]', '[255,140,0]', '[153,50,204]', '[139,0,0]', '[233,150,122]', '[143,188,143]', '[72,61,139]', '[47,79,79]', '[0,206,209]', '[148,0,211]', '[255,20,147]', '[0,191,255]', '[105,105,105]', '[30,144,255]', '[178,34,34]', '[255,250,240]', '[34,139,34]', '[255,0,255]', '[220,220,220]', '[248,248,255]', '[255,215,0]', '[218,165,32]', '[128,128,128]', '[0,128,0]', '[173,255,47]', '[240,255,240]', '[255,105,180]', '[205,92,92]', '[75,0,130]', '[255,255,240]', '[240,230,140]', '[230,230,250]', '[255,240,245]', '[124,252,0]', '[255,250,205]', '[173,216,230]', '[240,128,128]', '[224,255,255]', '[250,250,210]', '[144,238,144]', '[211,211,211]', '[255,182,193]', '[255,160,122]', '[32,178,170]', '[135,206,250]', '[119,136,153]', '[176,196,222]', '[255,255,224]', '[0,255,0]', '[50,205,50]', '[250,240,230]', '[255,0,255]', '[128,0,0]', '[102,205,170]', '[0,0,205]', '[186,85,211]', '[147,112,219]', '[60,179,113]', '[123,104,238]', '[0,250,154]', '[72,209,204]', '[199,21,133]', '[25,25,112]', '[245,255,250]', '[255,228,225]', '[255,228,181]', '[255,222,173]', '[0,0,128]', '[253,245,230]', '[128,128,0]', '[107,142,35]', '[255,165,0]', '[255,69,0]', '[218,112,214]', '[238,232,170]', '[152,251,152]', '[175,238,238]', '[219,112,147]', '[255,239,213]', '[255,218,185]', '[205,133,63]', '[255,192,203]', '[221,160,221]', '[176,224,230]', '[128,0,128]', '[255,0,0]', '[188,143,143]', '[65,105,225]', '[139,69,19]', '[250,128,114]', '[244,164,96]', '[46,139,87]', '[255,245,238]', '[160,82,45]', '[192,192,192]', '[135,206,235]', '[106,90,205]', '[112,128,144]', '[255,250,250]', '[0,255,127]', '[70,130,180]', '[210,180,140]', '[0,128,128]', '[216,191,216]', '[255,99,71]', '[64,224,208]', '[238,130,238]', '[245,222,179]', '[255,255,255]', '[245,245,245]', '[255,255,0]', '[154,205,50]'],\
    "html_name":['AliceBlue', 'AntiqueWhite', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque', 'Black', 'BlanchedAlmond', 'Blue', 'BlueViolet', 'Brown', 'BurlyWood', 'CadetBlue', 'Chartreuse', 'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan', 'DarkBlue', 'DarkCyan', 'DarkGoldenrod', 'DarkGray', 'DarkGreen', 'DarkKhaki', 'DarkMagenta', 'DarkOliveGreen', 'DarkOrange', 'DarkOrchid', 'DarkRed', 'DarkSalmon', 'DarkSeaGreen', 'DarkSlateBlue', 'DarkSlateGray', 'DarkTurquoise', 'DarkViolet', 'DeepPink', 'DeepSkyBlue', 'DimGray', 'DodgerBlue', 'FireBrick', 'FloralWhite', 'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'Goldenrod', 'Gray', 'Green', 'GreenYellow', 'Honeydew', 'HotPink', 'IndianRed', 'Indigo', 'Ivory', 'Khaki', 'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue', 'LightCoral', 'LightCyan', 'LightGoldenrodYellow', 'LightGreen', 'LightGrey', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue', 'LightSlateGray', 'LightSteelBlue', 'LightYellow', 'Lime', 'LimeGreen', 'Linen', 'Magenta', 'Maroon', 'MediumAquamarine', 'MediumBlue', 'MediumOrchid', 'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen', 'MediumTurquoise', 'MediumVioletRed', 'MidnightBlue', 'MintCream', 'MistyRose', 'Moccasin', 'NavajoWhite', 'Navy', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed', 'Orchid', 'PaleGoldenrod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed', 'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple', 'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Salmon', 'SandyBrown', 'SeaGreen', 'Seashell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue', 'SlateGray', 'Snow', 'SpringGreen', 'SteelBlue', 'Tan', 'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White', 'WhiteSmoke', 'Yellow', 'YellowGreen'],\
    "hex_string":['#F0F8FF', '#FAEBD7', '#00FFFF', '#7FFFD4', '#F0FFFF', '#F5F5DC', '#FFE4C4', '#000000', '#FFEBCD', '#0000FF', '#8A2BE2', '#A52A2A', '#DEB887', '#5F9EA0', '#7FFF00', '#D2691E', '#FF7F50', '#6495ED', '#FFF8DC', '#DC143C', '#00FFFF', '#00008B', '#008B8B', '#B8860B', '#A9A9A9', '#006400', '#BDB76B', '#8B008B', '#556B2F', '#FF8C00', '#9932CC', '#8B0000', '#E9967A', '#8FBC8F', '#483D8B', '#2F4F4F', '#00CED1', '#9400D3', '#FF1493', '#00BFFF', '#696969', '#1E90FF', '#B22222', '#FFFAF0', '#228B22', '#FF00FF', '#DCDCDC', '#F8F8FF', '#FFD700', '#DAA520', '#808080', '#008000', '#ADFF2F', '#F0FFF0', '#FF69B4', '#CD5C5C', '#4B0082', '#FFFFF0', '#F0E68C', '#E6E6FA', '#FFF0F5', '#7CFC00', '#FFFACD', '#ADD8E6', '#F08080', '#E0FFFF', '#FAFAD2', '#90EE90', '#D3D3D3', '#FFB6C1', '#FFA07A', '#20B2AA', '#87CEFA', '#778899', '#B0C4DE', '#FFFFE0', '#00FF00', '#32CD32', '#FAF0E6', '#FF00FF', '#800000', '#66CDAA', '#0000CD', '#BA55D3', '#9370DB', '#3CB371', '#7B68EE', '#00FA9A', '#48D1CC', '#C71585', '#191970', '#F5FFFA', '#FFE4E1', '#FFE4B5', '#FFDEAD', '#000080', '#FDF5E6', '#808000', '#6B8E23', '#FFA500', '#FF4500', '#DA70D6', '#EEE8AA', '#98FB98', '#AFEEEE', '#DB7093', '#FFEFD5', '#FFDAB9', '#CD853F', '#FFC0CB', '#DDA0DD', '#B0E0E6', '#800080', '#FF0000', '#BC8F8F', '#4169E1', '#8B4513', '#FA8072', '#F4A460', '#2E8B57', '#FFF5EE', '#A0522D', '#C0C0C0', '#87CEEB', '#6A5ACD', '#708090', '#FFFAFA', '#00FF7F', '#4682B4', '#D2B48C', '#008080', '#D8BFD8', '#FF6347', '#40E0D0', '#EE82EE', '#F5DEB3', '#FFFFFF', '#F5F5F5', '#FFFF00', '#9ACD32']}
df_color = pd.DataFrame(color_data)
df_color["html_name"] = df_color["html_name"].str.lower()

def _rgb_to_color(rgb):
    """
    transfer a list of rgb to a color list with decimal_rgba, html_name and hex_string.

    Args:  
        rgb: list-1*3 or 1*4 matrix for a decimal rgb or rgba.

    Returns:
        color: list-[decimal_rgb, html_name, hex_string].
    
    """
    color = []
    if len(rgb) == 3:
        #decial_rgba:
        rgba = rgb.copy()
        a = 255 # default is fully opaque, the value should be int 255.
        rgba.append(a)
        #hex_string:
        hex_str = '#%02X%02X%02X%02X' % (rgba[0],rgba[1],rgba[2],rgba[3])
        #html_name:
        html_name = ''
        hex_str_search = hex_str[0:-2]
        if hex_str_search in df_color.values:
            index = df_color.index[df_color["hex_string"] == hex_str_search].tolist()[0] #row index 
            html_name = df_color.iloc[index]["html_name"]
        color.append(rgba)
        color.append(html_name)
        color.append(hex_str)
    elif len(rgb) == 4:
        #decial_rgba:
        rgba = rgb.copy()
        #hex_string:
        hex_str = '#%02X%02X%02X%02X' % (rgba[0],rgba[1],rgba[2],rgba[3])
        #html_name:
        html_name = ''
        hex_str_search = hex_str[0:-2]
        if hex_str_search in df_color.values:
            index = df_color.index[df_color["hex_string"] == hex_str_search].tolist()[0] #row index 
            html_name = df_color.iloc[index]["html_name"]
        color.append(rgba)
        color.append(html_name)
        color.append(hex_str)
    else:
        color = [[], '', '']

    return color


#def _SBMLToDF(sbmlStr, reactionLineType = 'bezier', compartmentDefaultSize = [10000-20, 6200-20]):
def _SBMLToDF(sbmlStr, reactionLineType = 'bezier', compartmentDefaultSize = [1000-20, 1000-20]):
    """
    Save the information of an SBML file to a set of dataframe.

    Args:  
        sbmlStr: str-the string of the input sbml file.

        reactionLineType: str-type of the reaction line: 'straight' or 'bezier' (default).

    Returns:
        (df_CompartmentData, df_NodeData, df_ReactionData, df_ArbitraryTextData, df_ArbitraryShapeData): tuple.

        df_CompartmentData: DataFrame-Compartment information.

        df_NodeData: DataFrame-Node information.

        df_ReactionData: DataFrame-Reaction information.

        df_ArbitraryTextData: DataFrame-Arbitrary text information.

        df_ArbitrartyShapeData: DataFrame-Arbitrary shape information.
    
    """

    def hex_to_rgb(value):
        value = value.lstrip('#')
        if len(value) == 6:
            value = value + 'ff'
        return [int(value[i:i+2], 16) for i in (0, 2, 4, 6)]

    df_CompartmentData = pd.DataFrame(columns = COLUMN_NAME_df_CompartmentData)
    df_NodeData = pd.DataFrame(columns = COLUMN_NAME_df_NodeData)
    df_ReactionData = pd.DataFrame(columns = COLUMN_NAME_df_ReactionData)
    df_TextData = pd.DataFrame(columns = COLUMN_NAME_df_TextData)
    df_ShapeData = pd.DataFrame(columns = COLUMN_NAME_df_ShapeData)
    df_LineEndingData = pd.DataFrame(columns = COLUMN_NAME_df_LineEndingData)
    df_ReactionTextData = pd.DataFrame(columns = COLUMN_NAME_df_ReactionTextData)

    comp_id_list = []
    compGlyph_id_list = []
    comp_dimension_list = []
    comp_position_list = []
    comp_text_position_list = []
    comp_text_dimension_list = []
    comp_text_content_list = []
    spec_id_list = []
    specGlyph_id_list = []
    spec_specGlyph_id_list = []
    spec_dimension_list = []
    spec_position_list = []
    spec_text_position_list = []
    spec_text_dimension_list = []
    spec_text_content_list = []
    spec_concentration_list = []
    specRefGlyph_id_list = []
    specGlyph_specRefGlyph_id_list = []
    textGlyph_comp_id_list = []
    textGlyph_spec_id_list = []
    textGlyph_rxn_id_list = []
    rxn_text_position_list = []
    rxn_text_dimension_list = []
    rxn_text_content_list = []
    textGlyph_id_list = []
    text_content_list = []
    text_position_list = []
    text_dimension_list = []
    gen_id_list = []
    gen_position_list = []
    gen_dimension_list = []

    
    #set the default values without render info:
    #comp_fill_color = [158, 169, 255, 200]
    #comp_border_color = [0, 29, 255, 255]
    comp_fill_color = [255, 255, 255, 255]
    comp_border_color = [255, 255, 255, 255]
    comp_border_width = 2.0
    comp_shape_name = ''
    comp_shape_type = ''
    comp_shape_info = []
    spec_fill_color = [255, 204, 153, 200]
    spec_border_color = [255, 108, 9, 255]
    spec_border_width = 2.0
    spec_dash = []
    shapeIdx = 1
    shape_name = ''
    shape_type = ''
    shape_info = []
    reaction_line_color = [91, 176, 253, 255]
    reaction_line_fill = [255, 255, 255, 255]
    reaction_line_width = 3.0
    reaction_arrow_head_size = [reaction_line_width*5, reaction_line_width*4]
    reaction_dash = [] 
    reaction_shape_name = ''
    reaction_shape_type = ''
    reaction_shape_info = []
    text_content = ''
    text_line_color = [0, 0, 0, 255]
    text_line_width = 1.
    text_font_size = 12.
    text_font_family = ""
    [text_anchor, text_vanchor] = ['middle', 'middle']
    gen_fill_color = [255, 255, 255, 255]
    gen_border_color = [0, 0, 0, 255]
    gen_border_width = 2.
    gen_shape_type = ''
    gen_shape_info = []

    comp_render = []
    spec_render = []
    rxn_render = []
    text_render = []
    specRefGlyph_render = []
    gen_render = []
    lineEnding_render = []   

    # def_comp_width = visualizeSBML._getNetworkBottomRightCorner(sbmlStr)[0] + 100.
    # def_comp_height = visualizeSBML._getNetworkBottomRightCorner(sbmlStr)[1] + 100.
    # if visualizeSBML._getNetworkTopLeftCorner(sbmlStr)[0] < 0:
    #     def_comp_width -= visualizeSBML._getNetworkTopLeftCorner()[0]
    # if visualizeSBML._getNetworkTopLeftCorner()[1] < 0:
    #     def_comp_height -= visualizeSBML._getNetworkTopLeftCorner()[1]
    # compartmentDefaultSize = [def_comp_width, def_comp_height]

    mplugin = None
    try: #invalid sbml
        ### from here for layout ###
        document = libsbml.readSBMLFromString(sbmlStr)
        # if document.getNumErrors() != 0:
        #     raise Exception("There are errors in the sbml file.")
        if document.getNumErrors() != 0:
            errMsgRead = document.getErrorLog().toString()
            raise Exception("Errors in SBML Model: ", errMsgRead)
        model_layout = document.getModel()
        try:
            mplugin = model_layout.getPlugin("layout")
        except:
            raise Exception("There is no layout.")  

        if mplugin is not None:
            layout = mplugin.getLayout(0)   
            if layout is not None:
                numCompGlyphs = layout.getNumCompartmentGlyphs()
                numSpecGlyphs = layout.getNumSpeciesGlyphs()
                numReactionGlyphs = layout.getNumReactionGlyphs()
                numTextGlyphs = layout.getNumTextGlyphs()
                numGenGlyphs = layout.getNumGeneralGlyphs()
                for i in range(numCompGlyphs):
                    compGlyph = layout.getCompartmentGlyph(i)
                    temp_id = compGlyph.getCompartmentId()
                    comp_id_list.append(temp_id)
                    compGlyph_id = compGlyph.getId()
                    compGlyph_id_list.append(compGlyph_id)
                    boundingbox = compGlyph.getBoundingBox()
                    height = boundingbox.getHeight()
                    width = boundingbox.getWidth()
                    pos_x = boundingbox.getX()
                    pos_y = boundingbox.getY()
                    comp_dimension_list.append([width,height])
                    comp_position_list.append([pos_x,pos_y])

                    
                    for j in range(numTextGlyphs):
                        textGlyph_temp = layout.getTextGlyph(j)
                        # if textGlyph_temp.isSetOriginOfTextId():
                        #     temp_specGlyph_id = textGlyph_temp.getOriginOfTextId()
                        if textGlyph_temp.isSetGraphicalObjectId():
                            temp_compGlyph_id = textGlyph_temp.getGraphicalObjectId()
                        else:
                            temp_compGlyph_id = ''
                        if temp_compGlyph_id == compGlyph_id:
                            textGlyph = textGlyph_temp
                            text_content = textGlyph.getText()
                            temp_id = textGlyph.getId()
                            textGlyph_comp_id_list.append([compGlyph_id, temp_id])
                            text_boundingbox = textGlyph.getBoundingBox()
                            text_pos_x = text_boundingbox.getX()
                            text_pos_y = text_boundingbox.getY()   
                            text_dim_w = text_boundingbox.getWidth()
                            text_dim_h = text_boundingbox.getHeight()                       
                            comp_text_content_list.append(text_content)
                            comp_text_position_list.append([text_pos_x, text_pos_y])
                            comp_text_dimension_list.append([text_dim_w, text_dim_h])

                #print(comp_text_content_list)
                # if "_compartment_default_" in comp_id_list:
                #     numCompGlyphs -= 1
                #     idx = comp_id_list.index("_compartment_default_")
                #     comp_id_list.remove("_compartment_default_")
                #     del compGlyph_id_list[idx]
                #     del comp_dimension_list[idx]
                #     del comp_position_list[idx] 
                #     del comp_text_content_list[idx]
                #     del comp_text_position_list[idx]
                #     del comp_text_dimension_list[idx]

                reaction_id_list = []
                reactionGlyph_id_list = []
                reaction_rev_list = []
                reaction_center_list = []
                reaction_size_list = []
                kinetics_list = []
                #rct_specGlyph_list = []
                #prd_specGlyph_list = []
                reaction_center_handle_list = []
                rct_specGlyph_handle_list = []
                prd_specGlyph_handle_list = []
                reaction_mod_list = []
                reaction_rct_list = []
                reaction_prd_list = []
                mod_specGlyph_list = []

                
                for i in range(numReactionGlyphs):
                    reactionGlyph = layout.getReactionGlyph(i)
                    reaction_id = reactionGlyph.getReactionId()
                    reactionGlyph_id = reactionGlyph.getId()

                    for j in range(numTextGlyphs):
                        textGlyph_temp = layout.getTextGlyph(j)
                        # if textGlyph_temp.isSetOriginOfTextId():
                        #     temp_specGlyph_id = textGlyph_temp.getOriginOfTextId()
                        if textGlyph_temp.isSetGraphicalObjectId():
                            temp_rxnGlyph_id = textGlyph_temp.getGraphicalObjectId()
                        else:
                            temp_rxnGlyph_id = ''
                        if temp_rxnGlyph_id == reactionGlyph_id:
                            textGlyph = textGlyph_temp
                            text_content = textGlyph.getText()
                            temp_id = textGlyph.getId()
                            textGlyph_rxn_id_list.append([reactionGlyph_id, temp_id])
                            text_boundingbox = textGlyph.getBoundingBox()
                            text_pos_x = text_boundingbox.getX()
                            text_pos_y = text_boundingbox.getY()   
                            text_dim_w = text_boundingbox.getWidth()
                            text_dim_h = text_boundingbox.getHeight()                       
                            rxn_text_content_list.append(text_content)
                            rxn_text_position_list.append([text_pos_x, text_pos_y])
                            rxn_text_dimension_list.append([text_dim_w, text_dim_h])

                    curve = reactionGlyph.getCurve()
                    # listOfCurveSegments = curve.getListOfCurveSegments()
                    # for j in range(len(listOfCurveSegments)):
                    #     center_x = curve.getCurveSegment(j).getStart().getXOffset()
                    #     center_y = curve.getCurveSegment(j).getStart().getYOffset()
                    center_pt = []
                    center_sz = []
                    for segment in curve.getListOfCurveSegments():
                        short_line_start_x = segment.getStart().getXOffset()
                        short_line_start_y = segment.getStart().getYOffset()
                        short_line_end_x   = segment.getEnd().getXOffset()
                        short_line_end_y   = segment.getEnd().getYOffset() 
                        short_line_start = [short_line_start_x, short_line_start_y]
                        short_line_end   = [short_line_end_x, short_line_end_y]
                        if short_line_start == short_line_end: #the centroid is a dot
                            center_pt = short_line_start
                        else: #the centroid is a short line
                            center_pt = [.5*(short_line_start_x+short_line_end_x),.5*(short_line_start_y+short_line_end_y)]

                    try:
                        rxn_boundingbox = reactionGlyph.getBoundingBox()
                        width = rxn_boundingbox.getWidth()
                        height = rxn_boundingbox.getHeight()
                        pos_x = rxn_boundingbox.getX()
                        pos_y = rxn_boundingbox.getY()
                        if center_pt == []:
                            if pos_x == 0 and pos_y == 0 and width == 0 and height == 0: #LinearChain.xml
                                center_pt = []
                                #if the boundingbox can not give the info for the center point,
                                #look for the common point of the start and end points
                                start_end_pt = []
                                for j in range(numSpecRefGlyphs):     
                                    specRefGlyph = reactionGlyph.getSpeciesReferenceGlyph(j)   
                                    curve = specRefGlyph.getCurve()                                  
                                    for segment in curve.getListOfCurveSegments():
                                        line_start_x = segment.getStart().getXOffset()
                                        line_start_y = segment.getStart().getYOffset()
                                        line_end_x = segment.getEnd().getXOffset()
                                        line_end_y = segment.getEnd().getYOffset()
                                        line_start_pt =  [line_start_x, line_start_y]
                                        line_end_pt = [line_end_x, line_end_y]
                                        if line_start_pt in start_end_pt:
                                            center_pt = line_start_pt
                                        if line_end_pt in start_end_pt:
                                            center_pt = line_end_pt
                                        else:
                                            start_end_pt.append(line_start_pt)
                                            start_end_pt.append(line_end_pt)
                            else:
                                center_pt = [pos_x+.5*width, pos_y+.5*height]
                        center_sz = [width, height]
                    except:
                        pass

                    reaction_center_list.append(center_pt)
                    reaction_size_list.append(center_sz)

                    reaction_id_list.append(reaction_id)
                    reactionGlyph_id_list.append(reactionGlyph_id)
                    reaction = model_layout.getReaction(reaction_id)
                    rev = reaction.getReversible()
                    reaction_rev_list.append(rev)
                    try:
                        kinetics = reaction.getKineticLaw().getFormula()
                    except:
                        #if reaction.getKineticLaw() == None, or there is no kinetics info
                        kinetics = ""
                    kinetics_list.append(kinetics)
                    
                    temp_mod_list = []
                    for j in range(len(reaction.getListOfModifiers())):
                        modSpecRef = reaction.getModifier(j)
                        temp_mod_list.append(modSpecRef.getSpecies())
                    reaction_mod_list.append(temp_mod_list)       
                    
                    temp_rct_list = []
                    for j in range(len(reaction.getListOfReactants())):
                        rctSpecRef = reaction.getReactant(j)
                        temp_rct_list.append(rctSpecRef.getSpecies())
                    reaction_rct_list.append(temp_rct_list)

                    temp_prd_list = []
                    for j in range(len(reaction.getListOfProducts())):
                        prdSpecRef = reaction.getProduct(j)
                        temp_prd_list.append(prdSpecRef.getSpecies())
                    reaction_prd_list.append(temp_prd_list)

                    numSpecRefGlyphs = reactionGlyph.getNumSpeciesReferenceGlyphs()

                    #rct_specGlyph_temp_list = []
                    #prd_specGlyph_temp_list = []
                    rct_specGlyph_handles_temp_list = []
                    prd_specGlyph_handles_temp_list = [] 
                    mod_specGlyph_temp_list = []
                    
                    center_handle = []
                    for j in range(numSpecRefGlyphs):
                        specRefGlyph = reactionGlyph.getSpeciesReferenceGlyph(j)
                        specRefGlyph_id = specRefGlyph.getId()                   
                        specRefGlyph_id_list.append(specRefGlyph_id)
                        curve = specRefGlyph.getCurve()
                        spec_handle = []  
                        num_curve = curve.getNumCurveSegments()
                        line_start_list = []
                        line_end_list = []                           
                        for segment in curve.getListOfCurveSegments():                    
                            line_start_x = segment.getStart().getXOffset()
                            line_start_y = segment.getStart().getYOffset()
                            line_end_x = segment.getEnd().getXOffset()
                            line_end_y = segment.getEnd().getYOffset()
                            line_start_list.append([line_start_x, line_start_y])
                            line_end_list.append([line_end_x, line_end_y])

                        try:
                            line_start_pt =  [line_start_list[0][0], line_start_list[0][1]]
                            line_end_pt = [line_end_list[num_curve-1][0], line_end_list[num_curve-1][1]]
                        except:
                            line_start_pt = []
                            line_end_pt = []

                        
                        modifier_lineend_pos = []
                        spec_lineend_pos = []

                        try:
                            dist_start_center = math.sqrt((line_start_pt[0]-center_pt[0])*(line_start_pt[0]-center_pt[0])+(line_start_pt[1]-center_pt[1])*(line_start_pt[1]-center_pt[1]))
                            dist_end_center = math.sqrt((line_end_pt[0]-center_pt[0])*(line_end_pt[0]-center_pt[0])+(line_end_pt[1]-center_pt[1])*(line_end_pt[1]-center_pt[1]))
                            #if math.sqrt(line_start_pt, center_pt) <= math.dist(line_end_pt, center_pt):
                            if dist_start_center <= dist_end_center:
                                #line starts from center
                                spec_lineend_pos = line_end_pt
                                modifier_lineend_pos = line_start_pt
                                
                                if num_curve == 1:
                                    try: #bezier
                                        center_handle_candidate = [segment.getBasePoint1().getXOffset(), 
                                                        segment.getBasePoint1().getYOffset()]                                
                                        spec_handle = [segment.getBasePoint2().getXOffset(),
                                                    segment.getBasePoint2().getYOffset()] 
                                    except: #straight
                                        spec_handle = [.5*(center_pt[0]+line_end_pt[0]),
                                        .5*(center_pt[1]+line_end_pt[1])]
                                        center_handle_candidate = center_pt
                                        #spec_handle = center_pt         
                                else:  
                                    try: #bezier
                                        center_handle_candidate = []  
                                        flag_bezier = 0  
                                        for segment in curve.getListOfCurveSegments():
                                            if segment.getTypeCode() == 102:
                                                flag_bezier = 1
                                        for segment in curve.getListOfCurveSegments():
                                            if flag_bezier == 1: 
                                                #102 CubicBezier #107LineSegment
                                                if segment.getTypeCode() == 102:
                                                    spec_handle = [segment.getBasePoint1().getXOffset(), 
                                                                segment.getBasePoint1().getYOffset()]                                
                                                    center_handle_candidate = center_pt
                                            else:
                                                spec_handle = [.5*(center_pt[0]+line_start_pt[0]),
                                                .5*(center_pt[1]+line_start_pt[1])]
                                                center_handle_candidate = center_pt
                                                #spec_handle = center_pt
                                    except: #straight
                                        spec_handle = [.5*(center_pt[0]+line_end_pt[0]),
                                        .5*(center_pt[1]+line_end_pt[1])]
                                        center_handle_candidate = center_pt
                                        #spec_handle = center_pt 
                            else:
                                #line starts from species
                                spec_lineend_pos = line_start_pt
                                modifier_lineend_pos = line_end_pt
                                
                                if num_curve == 1:
                                    try: #bezier
                                        spec_handle = [segment.getBasePoint1().getXOffset(), 
                                                            segment.getBasePoint1().getYOffset()]                                
                                        center_handle_candidate = [segment.getBasePoint2().getXOffset(),
                                                        segment.getBasePoint2().getYOffset()]
                                    except: #straight
                                        spec_handle = [.5*(center_pt[0]+line_start_pt[0]),
                                        .5*(center_pt[1]+line_start_pt[1])]
                                        center_handle_candidate = center_pt
                                        #spec_handle = center_pt
                                else:
                                    try: #bezier
                                        center_handle_candidate = [] 
                                        flag_bezier = 0  
                                        for segment in curve.getListOfCurveSegments():
                                            if segment.getTypeCode() == 102:
                                                flag_bezier = 1
                                        for segment in curve.getListOfCurveSegments():
                                            if flag_bezier == 1: 
                                                #102 CubicBezier #107LineSegment
                                                if segment.getTypeCode() == 102:
                                                    spec_handle = [segment.getBasePoint1().getXOffset(), 
                                                                segment.getBasePoint1().getYOffset()]                                
                                                    center_handle_candidate = center_pt
                                            else:
                                                spec_handle = [.5*(center_pt[0]+line_start_pt[0]),
                                                .5*(center_pt[1]+line_start_pt[1])]
                                                center_handle_candidate = center_pt
                                                #spec_handle = center_pt
                                    except: #straight
                                        spec_handle = [.5*(center_pt[0]+line_start_pt[0]),
                                        .5*(center_pt[1]+line_start_pt[1])]
                                        center_handle_candidate = center_pt
                                        #spec_handle = center_pt

                        except:
                            center_handle_candidate = []
                            spec_handle = []

                        role = specRefGlyph.getRoleString()
                        specGlyph_id = specRefGlyph.getSpeciesGlyphId()
                        specGlyph_specRefGlyph_id_list.append([specGlyph_id, specRefGlyph_id])
                        specGlyph = layout.getSpeciesGlyph(specGlyph_id)
                        
                        for k in range(numTextGlyphs):
                            textGlyph_temp = layout.getTextGlyph(k)
                            # if textGlyph_temp.isSetOriginOfTextId():
                            #     temp_specGlyph_id = textGlyph_temp.getOriginOfTextId()
                            if textGlyph_temp.isSetGraphicalObjectId():
                                temp_specGlyph_id = textGlyph_temp.getGraphicalObjectId()
                            else:
                                temp_specGlyph_id = ''
                            if temp_specGlyph_id == specGlyph_id:
                                textGlyph = textGlyph_temp
                                text_content = textGlyph.getText()
                                temp_id = textGlyph.getId()
                                textGlyph_spec_id_list.append([specGlyph_id, temp_id])

                        spec_id = specGlyph.getSpeciesId()
                        spec = model_layout.getSpecies(spec_id)
                        try:
                            concentration = spec.getInitialConcentration()
                        except:
                            concentration = 1.
                        spec_boundingbox = specGlyph.getBoundingBox()
                        width = spec_boundingbox.getWidth()
                        height = spec_boundingbox.getHeight()
                        pos_x = spec_boundingbox.getX()
                        pos_y = spec_boundingbox.getY()
                                          
                        #try:
                        text_boundingbox = textGlyph.getBoundingBox()
                        text_pos_x = text_boundingbox.getX()
                        text_pos_y = text_boundingbox.getY()   
                        text_dim_w = text_boundingbox.getWidth()
                        text_dim_h = text_boundingbox.getHeight()
                        # except:
                        #     text_pos_x = pos_x
                        #     text_pos_y = pos_y   
                        #     text_dim_w = width
                        #     text_dim_h = height

                        # if text_content == 'Mt-DNA repair':
                        #     print("node:", [pos_x, pos_y])
                        #     print("text:", [text_pos_x, text_pos_y])


                        if specGlyph_id not in specGlyph_id_list:
                            spec_id_list.append(spec_id)
                            specGlyph_id_list.append(specGlyph_id)
                            spec_specGlyph_id_list.append([spec_id,specGlyph_id])
                            spec_dimension_list.append([width,height])
                            spec_position_list.append([pos_x,pos_y])
                            if text_content == '':
                                text_content = spec_id
                            spec_text_content_list.append(text_content)
                            spec_text_position_list.append([text_pos_x, text_pos_y])
                            spec_text_dimension_list.append([text_dim_w, text_dim_h])
                            spec_concentration_list.append(concentration)

                        # if center_handle == []:
                        #     center_handle.append(center_handle_candidate)

                        # #some "role" assigned wrongly
                        # for k in range(len(spec_specGlyph_id_list)):
                        #     if specGlyph_id == spec_specGlyph_id_list[k][1]:
                        #         if spec_specGlyph_id_list[k][0] in temp_rct_list:
                        #             role = "substrate"
                        # for k in range(len(spec_specGlyph_id_list)):
                        #     if specGlyph_id == spec_specGlyph_id_list[k][1]:
                        #         if spec_specGlyph_id_list[k][0] in temp_prd_list:
                        #             role = "product"
                        # for k in range(len(spec_specGlyph_id_list)):
                        #     if specGlyph_id == spec_specGlyph_id_list[k][1]:
                        #         if spec_specGlyph_id_list[k][0] in temp_mod_list:
                        #             role = "modifier"

                        if role == "substrate" or role == "sidesubstrate": #it is a rct
                            #rct_specGlyph_temp_list.append(specGlyph_id)
                            #the center handle is supposed to be from the reactant
                            if center_handle == []:
                                center_handle.append(center_handle_candidate)
                            rct_specGlyph_handles_temp_list.append([specGlyph_id,spec_handle,specRefGlyph_id,spec_lineend_pos])
                        elif role == "product" or role == "sideproduct": #it is a prd
                            #prd_specGlyph_temp_list.append(specGlyph_id)
                            prd_specGlyph_handles_temp_list.append([specGlyph_id,spec_handle,specRefGlyph_id,spec_lineend_pos])
                        elif role == "modifier" or role == 'activator' or role == "inhibitor": #it is a modifier
                            mod_specGlyph_temp_list.append([specGlyph_id,specRefGlyph_id,modifier_lineend_pos])
                    #rct_specGlyph_list.append(rct_specGlyph_temp_list)
                    #prd_specGlyph_list.append(prd_specGlyph_temp_list)
                    
            
                    try:
                        reaction_center_handle_list.append(center_handle[0])
                    except:
                        #raise Exception("Can not find center handle information to process.")
                        reaction_center_handle_list.append([])

                    rct_specGlyph_handle_list.append(rct_specGlyph_handles_temp_list)
                    prd_specGlyph_handle_list.append(prd_specGlyph_handles_temp_list) 
                    mod_specGlyph_list.append(mod_specGlyph_temp_list)

                #print(reaction_center_handle_list)
                #print(rct_specGlyph_handle_list)
                #print(prd_specGlyph_handle_list)
                #print(mod_specGlyph_list)
                # print(specRefGlyph_id_list)
                # print(specGlyph_specRefGlyph_id_list)
                #print(rct_specGlyph_handle_list)

                #orphan nodes
                for i in range(numSpecGlyphs):
                    specGlyph = layout.getSpeciesGlyph(i)
                    specGlyph_id = specGlyph.getId()
                    if specGlyph_id not in specGlyph_id_list:
                        specGlyph_id_list.append(specGlyph_id)
                        spec_id = specGlyph.getSpeciesId()
                        spec_id_list.append(spec_id)
                        spec_specGlyph_id_list.append([spec_id,specGlyph_id])
                        boundingbox = specGlyph.getBoundingBox()
                        height = boundingbox.getHeight()
                        width = boundingbox.getWidth()
                        pos_x = boundingbox.getX()
                        pos_y = boundingbox.getY()
                        spec_dimension_list.append([width,height])
                        spec_position_list.append([pos_x,pos_y])
                        for k in range(numTextGlyphs):
                            textGlyph_temp = layout.getTextGlyph(k)
                            if textGlyph_temp != None:
                                # if textGlyph_temp.isSetOriginOfTextId():
                                #     temp_specGlyph_id = textGlyph_temp.getOriginOfTextId()
                                if textGlyph_temp.isSetGraphicalObjectId():
                                    temp_specGlyph_id = textGlyph_temp.getGraphicalObjectId()
                                else:
                                    temp_specGlyph_id = ''
                                if temp_specGlyph_id == specGlyph_id:
                                    textGlyph = textGlyph_temp
                                    text_content = textGlyph.getText()
                                    temp_id = textGlyph.getId()
                                    textGlyph_spec_id_list.append([specGlyph_id, temp_id])

                        try:
                            text_boundingbox = textGlyph.getBoundingBox()
                            text_pos_x = text_boundingbox.getX()
                            text_pos_y = text_boundingbox.getY()   
                            text_dim_w = text_boundingbox.getWidth()
                            text_dim_h = text_boundingbox.getHeight()
                        except:
                            text_pos_x = pos_x
                            text_pos_y = pos_y   
                            text_dim_w = width
                            text_dim_h = height
                        spec_text_position_list.append([text_pos_x, text_pos_y])
                        spec_text_dimension_list.append([text_dim_w, text_dim_h])
                        if text_content == '':
                            text_content = spec_id
                        spec_text_content_list.append(text_content)
                        try:
                            concentration = spec.getInitialConcentration()
                        except:
                            concentration = 1.
                        spec_concentration_list.append(concentration)

                #print(reaction_mod_list) #species_id_list
                #print(mod_specGlyph_list) #species_reference_id_list
                #print(spec_specGlyph_id_list)

                #arbitrary text
                for i in range(numTextGlyphs):
                    textGlyph = layout.getTextGlyph(i)
                    #if not textGlyph.isSetOriginOfTextId() and not textGlyph.isSetGraphicalObjectId():
                    if not textGlyph.isSetGraphicalObjectId():
                        #if there is no original text id set
                        temp_id = textGlyph.getId()
                        text_content = textGlyph.getText()
                        textGlyph_id_list.append(temp_id)
                        text_content_list.append(text_content)
                        try:
                            text_boundingbox = textGlyph.getBoundingBox()
                            text_pos_x = text_boundingbox.getX()
                            text_pos_y = text_boundingbox.getY()   
                            text_dim_w = text_boundingbox.getWidth()
                            text_dim_h = text_boundingbox.getHeight()
                            text_position_list.append([text_pos_x,text_pos_y])
                            text_dimension_list.append([text_dim_w,text_dim_h])
                        except:
                            text_position_list.append([])
                            text_dimension_list.append([])
                    
                #arbitrary shape
                for i in range(numGenGlyphs):
                    genGlyph = layout.getGeneralGlyph(i)
                    temp_id = genGlyph.getId()
                    gen_id_list.append(temp_id)
                    try:
                        shape_boundingbox = genGlyph.getBoundingBox()
                        shape_pos_x = shape_boundingbox.getX()
                        shape_pos_y = shape_boundingbox.getY()   
                        shape_dim_w = shape_boundingbox.getWidth()
                        shape_dim_h = shape_boundingbox.getHeight()
                        gen_position_list.append([shape_pos_x,shape_pos_y])
                        gen_dimension_list.append([shape_dim_w,shape_dim_h])
                    except:
                        gen_position_list.append([])
                        gen_dimension_list.append([])

                #local render
                rPlugin = layout.getPlugin("render")
                if (rPlugin != None and rPlugin.getNumLocalRenderInformationObjects() > 0):
                    info = rPlugin.getRenderInformation(0)
                    color_list = []
                    gradient_list = []
                    #comp_render = []
                    #spec_render = []
                    #rxn_render = []
                    #text_render = []
                    #lineEnding_render = []
                    #gen_render = []
                    #specRefGlyph_render = []
                    arrowHeadSize = reaction_arrow_head_size #default if there is no lineEnding
                    id_arrowHeadSize = []

                    for  j in range(0, info.getNumColorDefinitions()):
                        color = info.getColorDefinition(j)
                        color_list.append([color.getId(),color.createValueString()])

                    
                    for j in range(0, info.getNumLineEndings()):
                        lineEnding = info.getLineEnding(j)
                        group = lineEnding.getGroup()
                        temp_id = lineEnding.getId()
                        boundingbox = lineEnding.getBoundingBox()
                        width = boundingbox.getWidth()
                        height= boundingbox.getHeight()
                        pos_x = boundingbox.getX()
                        pos_y = boundingbox.getY()
                        temp_pos = [pos_x,pos_y]
                        temp_size = [width, height]
                        id_arrowHeadSize.append([temp_id,temp_size])
                        lineEnding_fill_color = []
                        for k in range(len(color_list)):
                            if color_list[k][0] == group.getFill():
                                lineEnding_fill_color = hex_to_rgb(color_list[k][1])
                        lineEnding_border_color = []
                        for k in range(len(color_list)):
                            if color_list[k][0] == group.getStroke():
                                lineEnding_border_color = hex_to_rgb(color_list[k][1])
                                
                        shape_type=[]
                        shapeInfo=[]
                        for k in range(group.getNumElements()):
                            element = group.getElement(k)
                            temp_shape_type = element.getElementName()
                            shape_type.append(temp_shape_type)
                        
                            if temp_shape_type == 'ellipse':
                                center_x = (element.getCX().getRelativeValue())
                                center_y = (element.getCY().getRelativeValue())
                                radius_x = (element.getRX().getRelativeValue())
                                radius_y = (element.getRY().getRelativeValue())
                                if all(v == 0 for v in [radius_x, radius_y]):
                                    radius_x = element.getRX().getAbsoluteValue()
                                    radius_y = element.getRY().getAbsoluteValue()
                                    radius_x = 100*(radius_x)/width
                                    radius_y = 100*(radius_y)/height                     
                                shapeInfo.append([[center_x,center_y],[radius_x,radius_y]])

                            if temp_shape_type == 'polygon':
                                NumRenderPoints = element.getListOfElements().getNumRenderPoints()
                                temp_shapeInfo = []
                                for k in range(NumRenderPoints):
                                    point_x = float(element.getListOfElements().get(k).getX().getCoordinate().strip('%'))
                                    point_y = float(element.getListOfElements().get(k).getY().getCoordinate().strip('%'))         
                                    temp_shapeInfo.append([point_x,point_y])
                                shapeInfo.append(temp_shapeInfo)
                            
                            if temp_shape_type == 'rectangle':
                                width = element.getWidth().getRelativeValue()
                                height = element.getHeight().getRelativeValue()
                                shapeInfo.append([width, height])
                        # print(temp_id)
                        # print(shape_type)
                        # print(shapeInfo)
                            
                        lineEnding_render.append([temp_id, temp_pos, temp_size, 
                        lineEnding_fill_color, shape_type, shapeInfo, lineEnding_border_color])
                    
                    for j in range(len(lineEnding_render)):
                        temp_id = lineEnding_render[j][0]
                        temp_pos = lineEnding_render[j][1]
                        temp_size = lineEnding_render[j][2]
                        lineEnding_fill_color = lineEnding_render[j][3]
                        shape_type = lineEnding_render[j][4]
                        shapeInfo = lineEnding_render[j][5]
                        lineEnding_border_color = lineEnding_render[j][6]
                        LineEndingData_row_dct = {k:[] for k in COLUMN_NAME_df_LineEndingData}
                        LineEndingData_row_dct[ID].append(temp_id)
                        LineEndingData_row_dct[POSITION].append(temp_pos)
                        LineEndingData_row_dct[SIZE].append(temp_size)
                        LineEndingData_row_dct[FILLCOLOR].append(lineEnding_fill_color)
                        LineEndingData_row_dct[SHAPETYPE].append(shape_type)
                        LineEndingData_row_dct[SHAPEINFO].append(shapeInfo)
                        LineEndingData_row_dct[BORDERCOLOR].append(lineEnding_border_color)
                        #print(LineEndingData_row_dct)
                        #print(df_LineEndingData)
                        if len(df_LineEndingData) == 0:
                            df_LineEndingData = pd.DataFrame(LineEndingData_row_dct)
                        else:
                            df_LineEndingData = pd.concat([df_LineEndingData,\
                                pd.DataFrame(LineEndingData_row_dct)], ignore_index=True)

                    for j in range(0, info.getNumGradientDefinitions()):
                        gradient = info.getGradientDefinition(j)
                        grad_type = gradient.getElementName()
                        if grad_type == "linearGradient":
                            id = gradient.getId()
                            grad_start = [gradient.getXPoint1().getRelativeValue(),gradient.getYPoint1().getRelativeValue()]
                            grad_end = [gradient.getXPoint2().getRelativeValue(),gradient.getYPoint2().getRelativeValue()]
                            grad_info = [grad_start,grad_end]
                        elif grad_type == "radialGradient":
                            id = gradient.getId()
                            grad_center = [gradient.getCenterX().getRelativeValue(),gradient.getCenterY().getRelativeValue()]
                            grad_radius = [gradient.getRadius().getRelativeValue()]
                            grad_info = [grad_center,grad_radius]
                        stop_info = []
                        for k in range(0,gradient.getNumGradientStops()):
                            stop = gradient.getGradientStop(k)
                            offset = stop.getOffset().getRelativeValue()
                            stop_color_name = stop.getStopColor()
                            stop_color = spec_fill_color
                            for kk in range(len(color_list)):
                                if color_list[kk][0] == stop_color_name:
                                    stop_color = hex_to_rgb(color_list[kk][1])
                            stop_info.append([offset,stop_color])
                        gradient_list.append([id,grad_type, grad_info,stop_info])

                    for j in range (0, info.getNumStyles()):
                        style = info.getStyle(j)
                        group = style.getGroup()
                        typeList = style.createTypeString()
                        idList = style.createIdString()
                        roleList = style.createRoleString()

                        if typeList == '': 
                            #if the typeList is not defined, self define it based on idList
                            #which is the layout id instead of id
                            if idList in compGlyph_id_list:
                                typeList = 'COMPARTMENTGLYPH'
                            elif idList in specGlyph_id_list:
                                typeList = 'SPECIESGLYPH'
                            elif idList in reactionGlyph_id_list:
                                typeList = 'REACTIONGLYPH'
                            elif idList in textGlyph_id_list:
                                typeList = 'TEXTGLYPH'
                            elif any(idList in sublist for sublist in textGlyph_comp_id_list):
                                typeList = 'TEXTGLYPH'
                            elif any(idList in sublist for sublist in textGlyph_spec_id_list):
                                typeList = 'TEXTGLYPH'
                            elif any(idList in sublist for sublist in textGlyph_rxn_id_list):
                                typeList = 'TEXTGLYPH'
                            elif idList in specRefGlyph_id_list:
                                typeList = 'SPECIESREFERENCEGLYPH'
                            # else:
                            #     print(idList)
                            # elif idList == "":
                            #     print(roleList)

                        if 'COMPARTMENTGLYPH' in typeList:
                            #change layout id to id for later to build the list of render
                            render_comp_id = idList
                            for k in range(len(compGlyph_id_list)):    
                                if compGlyph_id_list[k] == idList:
                                    render_comp_id = comp_id_list[k]  
                            if idList == 'CompG__compartment_default_':
                                render_comp_id = '_compartment_default_'                            

                            fill_color = group.getFill()
                            if fill_color.lower() in df_color.values:
                                index = df_color.index[df_color["html_name"] == fill_color.lower()].tolist()[0] #row index 
                                rgb_pre = df_color.iloc[index]["decimal_rgb"]
                                rgb_pre = rgb_pre[1:-1].split(",")
                                rgb = [int(x) for x in rgb_pre]
                                comp_fill_color = rgb                 
                            else:
                                try:
                                    comp_fill_color = hex_to_rgb(fill_color)                          
                                except:
                                    for k in range(len(color_list)):
                                        if color_list[k][0] == fill_color:
                                            comp_fill_color = hex_to_rgb(color_list[k][1])

                            border_color = group.getStroke()
                            if border_color.lower() in df_color.values:
                                index = df_color.index[df_color["html_name"] == border_color.lower()].tolist()[0] #row index 
                                rgb_pre = df_color.iloc[index]["decimal_rgb"]
                                rgb_pre = rgb_pre[1:-1].split(",")
                                rgb = [int(x) for x in rgb_pre]
                                comp_border_color = rgb 
                            else:
                                try:
                                    comp_border_color = hex_to_rgb(border_color)
                                except:
                                    for k in range(len(color_list)):
                                        if color_list[k][0] == border_color:
                                            comp_border_color = hex_to_rgb(color_list[k][1])
        
                            comp_border_width = group.getStrokeWidth()

                            shape_type = ""
                            #print(group.getNumElements())# There is only one element
                            #for element in group.getListOfElements():
                            element = group.getElement(0)
                            shape_name = ""
                            shapeInfo = []
                            if element != None:
                                shape_type = element.getElementName()
                                if shape_type == "rectangle":
                                    shape_name = "rectangle"
                                    radius_x = element.getRX().getRelativeValue()
                                    radius_y = element.getRY().getRelativeValue()
                                    shapeInfo.append([radius_x, radius_y])
                            comp_render.append([render_comp_id,comp_fill_color,comp_border_color,comp_border_width, 
                            shape_name, shape_type, shapeInfo])
                        
                        elif 'SPECIESGLYPH' in typeList:
                            #change layout id to id for later to build the list of render
                            render_spec_id = idList

                            for k in range(len(spec_specGlyph_id_list)):    
                                if spec_specGlyph_id_list[k][1] == idList:
                                    render_spec_id = spec_specGlyph_id_list[k][0] 
                                    spec_dimension = spec_dimension_list[k]

                            fill_color = group.getFill()
                            if fill_color.lower() in df_color.values:
                                index = df_color.index[df_color["html_name"] == fill_color.lower()].tolist()[0] #row index 
                                rgb_pre = df_color.iloc[index]["decimal_rgb"]
                                rgb_pre = rgb_pre[1:-1].split(",")
                                rgb = [int(x) for x in rgb_pre]
                                spec_fill_color = rgb  
                            else:
                                try:#some spec fill color is defined as hex string directly
                                    spec_fill_color = hex_to_rgb(fill_color)
                                except:
                                    for k in range(len(color_list)):
                                        if color_list[k][0] == fill_color:
                                            spec_fill_color = hex_to_rgb(color_list[k][1])

                            border_color = group.getStroke()
                            if border_color.lower() in df_color.values:
                                index = df_color.index[df_color["html_name"] == border_color.lower()].tolist()[0] #row index 
                                rgb_pre = df_color.iloc[index]["decimal_rgb"]
                                rgb_pre = rgb_pre[1:-1].split(",")
                                rgb = [int(x) for x in rgb_pre]
                                spec_border_color = rgb 
                            else:
                                try:
                                    spec_border_color = hex_to_rgb(border_color)
                                except:
                                    for k in range(len(color_list)):
                                        if color_list[k][0] == border_color:
                                            spec_border_color = hex_to_rgb(color_list[k][1])

                            spec_dash = []
                            if group.isSetDashArray():
                                spec_num_dash = group.getNumDashes()
                                for num in range(spec_num_dash):
                                    spec_dash.append(group.getDashByIndex(num))
                                
                            for k in range(len(gradient_list)):
                                if gradient_list[k][0] == group.getFill():
                                    spec_fill_color = gradient_list[k][1:]
                            spec_border_width = group.getStrokeWidth()
                            # if spec_border_width <= 0:
                            #     spec_border_width = 0
                            #     spec_border_color = spec_fill_color
                            #name_list = []
                            shape_type = ''
                            #print(group.getNumElements())# There is only one element
                            #for element in group.getListOfElements():
                            element = group.getElement(0)
                            shapeIdx = 0
                            shape_name = "text_only"
                            shapeInfo = []
                            if element != None:
                                shape_type = element.getElementName()
                                if shape_type == "rectangle":
                                    shapeIdx = 1
                                    shape_name = "rectangle"
                                    radius_x = element.getRX().getRelativeValue()
                                    radius_y = element.getRY().getRelativeValue()
                                    shapeInfo.append([radius_x, radius_y])
                                elif shape_type == "ellipse": #ellipse
                                    shapeIdx = 2
                                    shape_name = "ellipse"
                                    # center_x = element.getCX().getRelativeValue()
                                    # center_y = element.getCY().getRelativeValue()
                                    # radius_x = element.getRX().getRelativeValue()
                                    # radius_y = element.getRY().getRelativeValue()
                                    # shapeInfo.append([[center_x,center_y],[radius_x,radius_y]])
                                elif shape_type == "polygon":
                                    NumRenderpoints = element.getListOfElements().getNumRenderPoints()
                                    for num in range(NumRenderpoints):
                                        point_x = element.getListOfElements().get(num).getX().getRelativeValue()
                                        point_y = element.getListOfElements().get(num).getY().getRelativeValue()
                                        shapeInfo.append([point_x,point_y])
                                    if all(v == [0.,0.] for v in shapeInfo):
                                        shapeInfo = []
                                        spec_width = spec_dimension[0]
                                        spec_hight = spec_dimension[1]
                                        for num in range(NumRenderpoints):
                                            point_x = element.getListOfElements().get(num).getX().getAbsoluteValue()
                                            point_y = element.getListOfElements().get(num).getY().getAbsoluteValue()
                                            shapeInfo.append([100.*point_x/spec_width,
                                            100.*point_y/spec_hight])
                                    
                                    if NumRenderpoints == 6: #hexagon:
                                        shapeIdx = 3
                                        shape_name = "hexagon"
                                    elif NumRenderpoints == 2: #line
                                        shapeIdx = 4
                                        shape_name = "line"
                                    elif NumRenderpoints == 3: #triangle
                                        shapeIdx = 5
                                        shape_name = "triangle"
                                        #triangle_vertex = [[25.0, 7.0],[100.0, 50.0],[25.0, 86.0]]
                                        upTriangle_vertex = [[50,0],[100,80.6],[0,80.6]]
                                        downTriangle_vertex = [[0,19.4],[100,19.5],[50.,100.]]
                                        leftTriangle_vertex = [[80.6,0],[80.6,100],[0,50]]
                                        rightTriangle_vertex = [[19.4,0],[100.,50],[19.4,100]]
                                        if all(item in shapeInfo for item in upTriangle_vertex):
                                            shapeIdx = 6
                                            shape_name = "upTriangle"
                                        if all(item in shapeInfo for item in downTriangle_vertex):
                                            shapeIdx = 7
                                            shape_name = "downTriangle"
                                        if all(item in shapeInfo for item in leftTriangle_vertex):
                                            shapeIdx = 8
                                            shape_name = "leftTriangle"
                                        if all(item in shapeInfo for item in rightTriangle_vertex):
                                            shapeIdx = 9
                                            shape_name = "rightTriangle"

                            spec_render.append([render_spec_id,spec_fill_color,spec_border_color,spec_border_width,
                            shapeIdx, shape_name, shape_type, shapeInfo, spec_dash])
                            #print(spec_render)

                        elif 'REACTIONGLYPH' in typeList:
                            #change layout id to id for later to build the list of render
                            render_rxn_id = idList
                            for k in range(len(reactionGlyph_id_list)):    
                                if reactionGlyph_id_list[k] == idList:
                                    render_rxn_id = reaction_id_list[k] 
                            if group.isSetEndHead():
                                temp_id = group.getEndHead() 
                            reaction_dash = []
                            if group.isSetDashArray():
                                reaction_num_dash = group.getNumDashes()
                                for num in range(reaction_num_dash):
                                    reaction_dash.append(group.getDashByIndex(num))

                            #print("reaction:", reaction_dash)
                            for k in range(len(id_arrowHeadSize)):
                                if temp_id == id_arrowHeadSize[k][0]:
                                    arrowHeadSize = id_arrowHeadSize[k][1]

                            fill_color = group.getFill()
                            if fill_color.lower() in df_color.values:
                                index = df_color.index[df_color["html_name"] == fill_color.lower()].tolist()[0] #row index 
                                rgb_pre = df_color.iloc[index]["decimal_rgb"]
                                rgb_pre = rgb_pre[1:-1].split(",")
                                rgb = [int(x) for x in rgb_pre]
                                reaction_line_fill = rgb 
                            try:
                                reaction_line_fill = hex_to_rgb(fill_color)
                            except:
                                for k in range(len(color_list)):
                                    if color_list[k][0] == fill_color:
                                        reaction_line_fill = hex_to_rgb(color_list[k][1])

                            stroke_color = group.getStroke()
                            if stroke_color.lower() in df_color.values:
                                index = df_color.index[df_color["html_name"] == stroke_color.lower()].tolist()[0] #row index 
                                rgb_pre = df_color.iloc[index]["decimal_rgb"]
                                rgb_pre = rgb_pre[1:-1].split(",")
                                rgb = [int(x) for x in rgb_pre]
                                reaction_line_color = rgb 
                            else:
                                try:
                                    reaction_line_color = hex_to_rgb(stroke_color)
                                except:
                                    for k in range(len(color_list)):
                                        if color_list[k][0] == stroke_color:
                                            reaction_line_color = hex_to_rgb(color_list[k][1])
                            
                            reaction_line_width = group.getStrokeWidth()

                            shape_type = ""
                            shape_name = ""
                            shapeInfo = []
                            element = group.getElement(0)
                            if element != None:
                                shape_type = element.getElementName()
                                if shape_type == "rectangle":
                                    shape_name = "rectangle"
                                elif shape_type == "ellipse": #ellipse
                                    shape_name = "ellipse"

                            rxn_render.append([render_rxn_id, reaction_line_color, reaction_line_width, 
                            arrowHeadSize, reaction_dash, reaction_line_fill, shape_name, shape_type, shape_info])
                        
                        elif 'TEXTGLYPH' in typeList:
                            render_text_id = idList
                            for k in range(len(textGlyph_comp_id_list)):    
                                if textGlyph_comp_id_list[k][1] == idList:
                                    render_text_id = textGlyph_comp_id_list[k][0] 
                            for k in range(len(textGlyph_spec_id_list)):    
                                if textGlyph_spec_id_list[k][1] == idList:
                                    render_text_id = textGlyph_spec_id_list[k][0]
                            for k in range(len(textGlyph_rxn_id_list)):    
                                if textGlyph_rxn_id_list[k][1] == idList:
                                    render_text_id = textGlyph_rxn_id_list[k][0]

                            text_color = group.getStroke()
                            if text_color.lower() in df_color.values:
                                index = df_color.index[df_color["html_name"] == text_color.lower()].tolist()[0] #row index 
                                rgb_pre = df_color.iloc[index]["decimal_rgb"]
                                rgb_pre = rgb_pre[1:-1].split(",")
                                rgb = [int(x) for x in rgb_pre]
                                text_line_color = rgb   
                            else:  
                                try:
                                    text_line_color = hex_to_rgb(text_color)
                                except:
                                    for k in range(len(color_list)):
                                        if color_list[k][0] == text_color:
                                            text_line_color = hex_to_rgb(color_list[k][1])

                            
                            text_line_width = group.getStrokeWidth()
                            if group.isSetTextAnchor():
                                text_anchor = group.getTextAnchorAsString()
                            if group.isSetVTextAnchor():
                                text_vanchor = group.getVTextAnchorAsString()
                            if math.isnan(text_line_width):
                                text_line_width = 1.
                            text_font_size = float(group.getFontSize().getCoordinate())
                            if math.isnan(text_font_size):
                                text_font_size = 12.
                            text_font_family = group.getFontFamily()

                            text_render.append([render_text_id,text_line_color,text_line_width,
							text_font_size, [text_anchor, text_vanchor], idList, text_font_family])
                            #print(text_render)
                        elif 'GENERALGLYPH' in typeList:
                            render_gen_id = idList
                            fill_color = group.getFill()
                            if fill_color.lower() in df_color.values:
                                index = df_color.index[df_color["html_name"] == fill_color.lower()].tolist()[0] #row index 
                                rgb_pre = df_color.iloc[index]["decimal_rgb"]
                                rgb_pre = rgb_pre[1:-1].split(",")
                                rgb = [int(x) for x in rgb_pre]
                                gen_fill_color = rgb 
                            else:
                                try:
                                    gen_fill_color = hex_to_rgb(fill_color)
                                except:
                                    for k in range(len(color_list)):
                                        if color_list[k][0] == fill_color:
                                            gen_fill_color = hex_to_rgb(color_list[k][1])

                            border_color = group.getStroke()
                            if border_color.lower() in df_color.values:
                                index = df_color.index[df_color["html_name"] == border_color.lower()].tolist()[0] #row index 
                                rgb_pre = df_color.iloc[index]["decimal_rgb"]
                                rgb_pre = rgb_pre[1:-1].split(",")
                                rgb = [int(x) for x in rgb_pre]
                                gen_border_color = rgb  
                            else:
                                try:
                                    gen_border_color = hex_to_rgb(border_color)
                                except:
                                    for k in range(len(color_list)):
                                        if color_list[k][0] == border_color:
                                            gen_border_color = hex_to_rgb(color_list[k][1])
                 
                            gen_border_width = group.getStrokeWidth()
                            gen_shape_type = ''
                            gen_shape_info = []
                            element = group.getElement(0)
                            if element != None:
                                gen_shape_type = element.getElementName()
                                if gen_shape_type == "polygon":
                                    NumRenderpoints = element.getListOfElements().getNumRenderPoints()
                                    for num in range(NumRenderpoints):
                                        point_x = element.getListOfElements().get(num).getX().getRelativeValue()
                                        point_y = element.getListOfElements().get(num).getY().getRelativeValue()
                                        gen_shape_info.append([point_x,point_y]) 

                            gen_render.append([render_gen_id, gen_fill_color, gen_border_color,
                            gen_border_width, gen_shape_type, gen_shape_info])

                        elif 'SPECIESREFERENCEGLYPH' in typeList:
                            render_specRefGlyph_id = idList
                            # for k in range(len(specGlyph_specRefGlyph_id_list)):    
                            #     if specGlyph_specRefGlyph_id_list[k][1] == idList:
                            #         render_specRefGlyph_id = specGlyph_specRefGlyph_id_list[k][0] 
                            endHead = group.getEndHead()

                            reaction_dash = []
                            if group.isSetDashArray():
                                reaction_num_dash = group.getNumDashes()
                                for num in range(reaction_num_dash):
                                    reaction_dash.append(group.getDashByIndex(num))

                            specRefGlyph_render.append([render_specRefGlyph_id, endHead, reaction_dash])

            #print(specRefGlyph_render)
            
            #global render 
            try: 
                grPlugin = mplugin.getListOfLayouts().getPlugin("render")
            except:
                pass

            if (grPlugin != None and grPlugin.getNumGlobalRenderInformationObjects() > 0):
                info = grPlugin.getRenderInformation(0)
                color_list = []
                gradient_list = []
                #comp_render = []
                #spec_render = []
                #rxn_render = []
                #text_render = []
                #lineEnding_render = []
                #gen_render = []
                #specRefGlyph_render = []
                arrowHeadSize = reaction_arrow_head_size #default if there is no lineEnding
                id_arrowHeadSize = []

                for  j in range(0, info.getNumColorDefinitions()):
                    color = info.getColorDefinition(j)
                    color_list.append([color.getId(),color.createValueString()])

                
                for j in range(0, info.getNumLineEndings()):
                    lineEnding = info.getLineEnding(j)
                    group = lineEnding.getGroup()
                    temp_id = lineEnding.getId()
                    boundingbox = lineEnding.getBoundingBox()
                    width = boundingbox.getWidth()
                    height= boundingbox.getHeight()
                    pos_x = boundingbox.getX()
                    pos_y = boundingbox.getY()
                    temp_pos = [pos_x,pos_y]
                    temp_size = [width, height]
                    id_arrowHeadSize.append([temp_id,temp_size])
                    lineEnding_fill_color = []
                    for k in range(len(color_list)):
                        if color_list[k][0] == group.getFill():
                            lineEnding_fill_color = hex_to_rgb(color_list[k][1])
                    lineEnding_border_color = []
                    for k in range(len(color_list)):
                        if color_list[k][0] == group.getStroke():
                            lineEnding_border_color = hex_to_rgb(color_list[k][1])
                            
                    shape_type=[]
                    shapeInfo=[]
                    for k in range(group.getNumElements()):
                        element = group.getElement(k)
                        temp_shape_type = element.getElementName()
                        shape_type.append(temp_shape_type)
                    
                        if temp_shape_type == 'ellipse':
                            center_x = (element.getCX().getRelativeValue())
                            center_y = (element.getCY().getRelativeValue())
                            radius_x = (element.getRX().getRelativeValue())
                            radius_y = (element.getRY().getRelativeValue())
                            if all(v == 0 for v in [radius_x, radius_y]):
                                radius_x = element.getRX().getAbsoluteValue()
                                radius_y = element.getRY().getAbsoluteValue()
                                radius_x = 100*(radius_x)/width
                                radius_y = 100*(radius_y)/height                     
                            shapeInfo.append([[center_x,center_y],[radius_x,radius_y]])

                        if temp_shape_type == 'polygon':
                            NumRenderPoints = element.getListOfElements().getNumRenderPoints()
                            temp_shapeInfo = []
                            for k in range(NumRenderPoints):
                                point_x = float(element.getListOfElements().get(k).getX().getCoordinate().strip('%'))
                                point_y = float(element.getListOfElements().get(k).getY().getCoordinate().strip('%'))         
                                temp_shapeInfo.append([point_x,point_y])
                            shapeInfo.append(temp_shapeInfo)

                        if temp_shape_type == 'rectangle':
                            width = element.getWidth().getRelativeValue()
                            height = element.getHeight().getRelativeValue()
                            shapeInfo.append([width, height])
                    # print(temp_id)
                    # print(shape_type)
                    # print(shapeInfo)
                        
                    lineEnding_render.append([temp_id, temp_pos, temp_size, 
                    lineEnding_fill_color, shape_type, shapeInfo, lineEnding_border_color])
                
                for j in range(len(lineEnding_render)):
                    temp_id = lineEnding_render[j][0]
                    temp_pos = lineEnding_render[j][1]
                    temp_size = lineEnding_render[j][2]
                    lineEnding_fill_color = lineEnding_render[j][3]
                    shape_type = lineEnding_render[j][4]
                    shapeInfo = lineEnding_render[j][5]
                    lineEnding_border_color = lineEnding_render[j][6]
                    LineEndingData_row_dct = {k:[] for k in COLUMN_NAME_df_LineEndingData}
                    LineEndingData_row_dct[ID].append(temp_id)
                    LineEndingData_row_dct[POSITION].append(temp_pos)
                    LineEndingData_row_dct[SIZE].append(temp_size)
                    LineEndingData_row_dct[FILLCOLOR].append(lineEnding_fill_color)
                    LineEndingData_row_dct[SHAPETYPE].append(shape_type)
                    LineEndingData_row_dct[SHAPEINFO].append(shapeInfo)
                    LineEndingData_row_dct[BORDERCOLOR].append(lineEnding_border_color)
                    #print(LineEndingData_row_dct)
                    #print(df_LineEndingData)
                    if len(df_LineEndingData) == 0:
                        df_LineEndingData = pd.DataFrame(LineEndingData_row_dct)
                    else:
                        df_LineEndingData = pd.concat([df_LineEndingData,\
                            pd.DataFrame(LineEndingData_row_dct)], ignore_index=True)

                for j in range(0, info.getNumGradientDefinitions()):
                    gradient = info.getGradientDefinition(j)
                    grad_type = gradient.getElementName()
                    if grad_type == "linearGradient":
                        id = gradient.getId()
                        grad_start = [gradient.getXPoint1().getRelativeValue(),gradient.getYPoint1().getRelativeValue()]
                        grad_end = [gradient.getXPoint2().getRelativeValue(),gradient.getYPoint2().getRelativeValue()]
                        grad_info = [grad_start,grad_end]
                    elif grad_type == "radialGradient":
                        id = gradient.getId()
                        grad_center = [gradient.getCenterX().getRelativeValue(),gradient.getCenterY().getRelativeValue()]
                        grad_radius = [gradient.getRadius().getRelativeValue()]
                        grad_info = [grad_center,grad_radius]
                    stop_info = []
                    for k in range(0,gradient.getNumGradientStops()):
                        stop = gradient.getGradientStop(k)
                        offset = stop.getOffset().getRelativeValue()
                        stop_color_name = stop.getStopColor()
                        stop_color = spec_fill_color
                        for kk in range(len(color_list)):
                            if color_list[kk][0] == stop_color_name:
                                stop_color = hex_to_rgb(color_list[kk][1])
                        stop_info.append([offset,stop_color])
                    gradient_list.append([id,grad_type, grad_info,stop_info])

                for j in range (0, info.getNumStyles()):
                    style = info.getStyle(j)
                    group = style.getGroup()
                    typeList = style.createTypeString()
                    roleList = style.createRoleString()
                    idList = ""

                    if roleList == "modifier" or roleList == "product": 
                        typeList = 'SPECIESREFERENCEGLYPH'

                    if 'COMPARTMENTGLYPH' in typeList:
                        render_comp_id = idList

                        fill_color = group.getFill()
                        if fill_color.lower() in df_color.values:
                            index = df_color.index[df_color["html_name"] == fill_color.lower()].tolist()[0] #row index 
                            rgb_pre = df_color.iloc[index]["decimal_rgb"]
                            rgb_pre = rgb_pre[1:-1].split(",")
                            rgb = [int(x) for x in rgb_pre]
                            comp_fill_color = rgb                 
                        else:
                            try:
                                comp_fill_color = hex_to_rgb(fill_color)                          
                            except:
                                for k in range(len(color_list)):
                                    if color_list[k][0] == fill_color:
                                        comp_fill_color = hex_to_rgb(color_list[k][1])

                        border_color = group.getStroke()
                        if border_color.lower() in df_color.values:
                            index = df_color.index[df_color["html_name"] == border_color.lower()].tolist()[0] #row index 
                            rgb_pre = df_color.iloc[index]["decimal_rgb"]
                            rgb_pre = rgb_pre[1:-1].split(",")
                            rgb = [int(x) for x in rgb_pre]
                            comp_border_color = rgb 
                        else:
                            try:
                                comp_border_color = hex_to_rgb(border_color)
                            except:
                                for k in range(len(color_list)):
                                    if color_list[k][0] == border_color:
                                        comp_border_color = hex_to_rgb(color_list[k][1])
    
    
                        comp_border_width = group.getStrokeWidth()

                        shape_type = ""
                        #print(group.getNumElements())# There is only one element
                        #for element in group.getListOfElements():
                        element = group.getElement(0)
                        shape_name = ""
                        shapeInfo = []
                        if element != None:
                            shape_type = element.getElementName()
                            if shape_type == "rectangle":
                                shape_name = "rectangle"
                                radius_x = element.getRX().getRelativeValue()
                                radius_y = element.getRY().getRelativeValue()
                                shapeInfo.append([radius_x, radius_y])
                        comp_render.append([render_comp_id,comp_fill_color,comp_border_color,comp_border_width, 
                        shape_name, shape_type, shapeInfo])
       
                    elif 'SPECIESGLYPH' in typeList:
                        render_spec_id = idList
                        fill_color = group.getFill()
                        if fill_color.lower() in df_color.values:
                            index = df_color.index[df_color["html_name"] == fill_color.lower()].tolist()[0] #row index 
                            rgb_pre = df_color.iloc[index]["decimal_rgb"]
                            rgb_pre = rgb_pre[1:-1].split(",")
                            rgb = [int(x) for x in rgb_pre]
                            spec_fill_color = rgb  
                        else:
                            try:#some spec fill color is defined as hex string directly
                                spec_fill_color = hex_to_rgb(fill_color)
                            except:
                                for k in range(len(color_list)):
                                    if color_list[k][0] == fill_color:
                                        spec_fill_color = hex_to_rgb(color_list[k][1])

                        border_color = group.getStroke()
                        if border_color.lower() in df_color.values:
                            index = df_color.index[df_color["html_name"] == border_color.lower()].tolist()[0] #row index 
                            rgb_pre = df_color.iloc[index]["decimal_rgb"]
                            rgb_pre = rgb_pre[1:-1].split(",")
                            rgb = [int(x) for x in rgb_pre]
                            spec_border_color = rgb 
                        else:
                            try:
                                spec_border_color = hex_to_rgb(border_color)
                            except:
                                for k in range(len(color_list)):
                                    if color_list[k][0] == border_color:
                                        spec_border_color = hex_to_rgb(color_list[k][1])
                    
                        spec_dash = []
                        if group.isSetDashArray():
                            spec_num_dash = group.getNumDashes()
                            for num in range(spec_num_dash):
                                spec_dash.append(group.getDashByIndex(num))                          
                        
                        for k in range(len(gradient_list)):
                            if gradient_list[k][0] == group.getFill():
                                spec_fill_color = gradient_list[k][1:]
                        spec_border_width = group.getStrokeWidth()
                        # if spec_border_width <= 0:
                        #     spec_border_width = 0
                        #     spec_border_color = spec_fill_color
                        #name_list = []
                        shape_type = ''
                        #print(group.getNumElements())# There is only one element
                        #for element in group.getListOfElements():
                        element = group.getElement(0)
                        shapeIdx = 0
                        shape_name = "text_only"
                        shapeInfo = []
                        if element != None:
                            shape_type = element.getElementName()
                            if shape_type == "rectangle":
                                shapeIdx = 1
                                shape_name = "rectangle"
                                radius_x = element.getRX().getRelativeValue()
                                radius_y = element.getRY().getRelativeValue()
                                shapeInfo.append([radius_x, radius_y])
                            elif shape_type == "ellipse": #ellipse
                                shapeIdx = 2
                                shape_name = "ellipse"
                                # center_x = element.getCX().getRelativeValue()
                                # center_y = element.getCY().getRelativeValue()
                                # radius_x = element.getRX().getRelativeValue()
                                # radius_y = element.getRY().getRelativeValue()
                                # shapeInfo.append([[center_x,center_y],[radius_x,radius_y]])
                            elif shape_type == "polygon":
                                NumRenderpoints = element.getListOfElements().getNumRenderPoints()
                                for num in range(NumRenderpoints):
                                    point_x = element.getListOfElements().get(num).getX().getRelativeValue()
                                    point_y = element.getListOfElements().get(num).getY().getRelativeValue()
                                    shapeInfo.append([point_x,point_y])
                                if all(v == [0.,0.] for v in shapeInfo):
                                    shapeInfo = []
                                    spec_width = spec_dimension[0]
                                    spec_hight = spec_dimension[1]
                                    for num in range(NumRenderpoints):
                                        point_x = element.getListOfElements().get(num).getX().getAbsoluteValue()
                                        point_y = element.getListOfElements().get(num).getY().getAbsoluteValue()
                                        shapeInfo.append([100.*point_x/spec_width,
                                        100.*point_y/spec_hight])
                                
                                if NumRenderpoints == 6: #hexagon:
                                    shapeIdx = 3
                                    shape_name = "hexagon"
                                elif NumRenderpoints == 2: #line
                                    shapeIdx = 4
                                    shape_name = "line"
                                elif NumRenderpoints == 3: #triangle
                                    shapeIdx = 5
                                    shape_name = "triangle"
                                    #triangle_vertex = [[25.0, 7.0],[100.0, 50.0],[25.0, 86.0]]
                                    upTriangle_vertex = [[50,0],[100,80.6],[0,80.6]]
                                    downTriangle_vertex = [[0,19.4],[100,19.5],[50.,100.]]
                                    leftTriangle_vertex = [[80.6,0],[80.6,100],[0,50]]
                                    rightTriangle_vertex = [[19.4,0],[100.,50],[19.4,100]]
                                    if all(item in shapeInfo for item in upTriangle_vertex):
                                        shapeIdx = 6
                                        shape_name = "upTriangle"
                                    if all(item in shapeInfo for item in downTriangle_vertex):
                                        shapeIdx = 7
                                        shape_name = "downTriangle"
                                    if all(item in shapeInfo for item in leftTriangle_vertex):
                                        shapeIdx = 8
                                        shape_name = "leftTriangle"
                                    if all(item in shapeInfo for item in rightTriangle_vertex):
                                        shapeIdx = 9
                                        shape_name = "rightTriangle"

                        spec_render.append([render_spec_id,spec_fill_color,spec_border_color,spec_border_width,
                        shapeIdx, shape_name, shape_type, shapeInfo, spec_dash])
                        #print(spec_render)

                    elif 'REACTIONGLYPH' in typeList:
                        render_rxn_id = idList
            
                        reaction_dash = []
                        if group.isSetDashArray():
                            reaction_num_dash = group.getNumDashes()
                            for num in range(reaction_num_dash):
                                reaction_dash.append(group.getDashByIndex(num))
                
                        fill_color = group.getFill()
                        if fill_color.lower() in df_color.values:
                            index = df_color.index[df_color["html_name"] == fill_color.lower()].tolist()[0] #row index 
                            rgb_pre = df_color.iloc[index]["decimal_rgb"]
                            rgb_pre = rgb_pre[1:-1].split(",")
                            rgb = [int(x) for x in rgb_pre]
                            reaction_line_fill = rgb 
                        try:
                            reaction_line_fill = hex_to_rgb(fill_color)
                        except:
                            for k in range(len(color_list)):
                                if color_list[k][0] == fill_color:
                                    reaction_line_fill = hex_to_rgb(color_list[k][1])

                        stroke_color = group.getStroke()
                        if stroke_color.lower() in df_color.values:
                            index = df_color.index[df_color["html_name"] == stroke_color.lower()].tolist()[0] #row index 
                            rgb_pre = df_color.iloc[index]["decimal_rgb"]
                            rgb_pre = rgb_pre[1:-1].split(",")
                            rgb = [int(x) for x in rgb_pre]
                            reaction_line_color = rgb 
                        else:
                            try:
                                reaction_line_color = hex_to_rgb(stroke_color)
                            except:
                                for k in range(len(color_list)):
                                    if color_list[k][0] == stroke_color:
                                        reaction_line_color = hex_to_rgb(color_list[k][1])
                        reaction_line_width = group.getStrokeWidth()
                        shape_type = ""
                        shape_name = ""
                        shapeInfo = []
                        element = group.getElement(0)
                        if element != None:
                            shape_type = element.getElementName()
                            if shape_type == "rectangle":
                                shape_name = "rectangle"
                            elif shape_type == "ellipse": #ellipse
                                shape_name = "ellipse"

                        rxn_render.append([render_rxn_id, reaction_line_color, reaction_line_width, 
                        arrowHeadSize, reaction_dash, reaction_line_fill, shape_name, shape_type, shape_info])

                    elif 'TEXTGLYPH' in typeList:
                        render_text_id = idList
           
                        text_color = group.getStroke()
                        if text_color.lower() in df_color.values:
                            index = df_color.index[df_color["html_name"] == text_color.lower()].tolist()[0] #row index 
                            rgb_pre = df_color.iloc[index]["decimal_rgb"]
                            rgb_pre = rgb_pre[1:-1].split(",")
                            rgb = [int(x) for x in rgb_pre]
                            text_line_color = rgb   
                        else:  
                            try:
                                text_line_color = hex_to_rgb(text_color)
                            except:
                                for k in range(len(color_list)):
                                    if color_list[k][0] == text_color:
                                        text_line_color = hex_to_rgb(color_list[k][1])

                        text_line_width = group.getStrokeWidth()
                        if group.isSetTextAnchor():
                            text_anchor = group.getTextAnchorAsString()
                        if group.isSetVTextAnchor():
                            text_vanchor = group.getVTextAnchorAsString()
                        if math.isnan(text_line_width):
                            text_line_width = 1.
                        text_font_size = float(group.getFontSize().getCoordinate())
                        if math.isnan(text_font_size):
                            text_font_size = 12.
                        text_font_family = group.getFontFamily()
                        text_render.append([render_text_id,text_line_color,text_line_width,
                        text_font_size, [text_anchor, text_vanchor], idList, text_font_family])
                        #print(render_text_id)
                    elif 'GENERALGLYPH' in typeList:
                        render_gen_id = idList

                        fill_color = group.getFill()
                        if fill_color.lower() in df_color.values:
                            index = df_color.index[df_color["html_name"] == fill_color.lower()].tolist()[0] #row index 
                            rgb_pre = df_color.iloc[index]["decimal_rgb"]
                            rgb_pre = rgb_pre[1:-1].split(",")
                            rgb = [int(x) for x in rgb_pre]
                            gen_fill_color = rgb 
                        else:
                            try:
                                gen_fill_color = hex_to_rgb(fill_color)
                            except:
                                for k in range(len(color_list)):
                                    if color_list[k][0] == fill_color:
                                        gen_fill_color = hex_to_rgb(color_list[k][1])

                        border_color = group.getStroke()
                        if border_color.lower() in df_color.values:
                            index = df_color.index[df_color["html_name"] == border_color.lower()].tolist()[0] #row index 
                            rgb_pre = df_color.iloc[index]["decimal_rgb"]
                            rgb_pre = rgb_pre[1:-1].split(",")
                            rgb = [int(x) for x in rgb_pre]
                            gen_border_color = rgb  
                        else:
                            try:
                                gen_border_color = hex_to_rgb(border_color)
                            except:
                                for k in range(len(color_list)):
                                    if color_list[k][0] == border_color:
                                        gen_border_color = hex_to_rgb(color_list[k][1])
                
                        gen_border_width = group.getStrokeWidth()
                        gen_shape_type = ''
                        gen_shape_info = []
                        element = group.getElement(0)
                        if element != None:
                            gen_shape_type = element.getElementName()
                            if gen_shape_type == "polygon":
                                NumRenderpoints = element.getListOfElements().getNumRenderPoints()
                                for num in range(NumRenderpoints):
                                    point_x = element.getListOfElements().get(num).getX().getRelativeValue()
                                    point_y = element.getListOfElements().get(num).getY().getRelativeValue()
                                    gen_shape_info.append([point_x,point_y]) 

                        gen_render.append([render_gen_id, gen_fill_color, gen_border_color,
                        gen_border_width, gen_shape_type, gen_shape_info])

                    elif 'SPECIESREFERENCEGLYPH' in typeList: 
                        #render_specRefGlyph_id = idList               
                        endHead = group.getEndHead()
                        reaction_dash = []
                        if endHead != "none":
                            for m in range(numReactionGlyphs):
                                if roleList == "modifier":
                                    for n in range(len(mod_specGlyph_list[m])):
                                        idList = mod_specGlyph_list[m][n][1]
                                        specRefGlyph_render.append([idList, endHead, reaction_dash])
                                
                                if roleList == "product":
                                    for n in range(len(prd_specGlyph_handle_list[m])):
                                        idList = prd_specGlyph_handle_list[m][n][2]
                                        if not any(idList in sublist for sublist in specRefGlyph_render):
                                            specRefGlyph_render.append([idList, endHead, reaction_dash])
   
                            
        #print(comp_render)
        #print(spec_render)
        #print(rxn_render)
        #print(text_render)
        #print(gen_render)
        #print(specRefGlyph_render)
        #print(lineEnding_render)

        model = simplesbml.loadSBMLStr(sbmlStr)
        numFloatingNodes  = model.getNumFloatingSpecies()
        FloatingNodes_ids = model.getListOfFloatingSpecies()
        numBoundaryNodes  = model.getNumBoundarySpecies()
        BoundaryNodes_ids = model.getListOfBoundarySpecies()
        numNodes = numFloatingNodes + numBoundaryNodes
        numRxns   = model.getNumReactions()
        Rxns_ids  = model.getListOfReactionIds()
        numComps  = model.getNumCompartments()
        Comps_ids = model.getListOfCompartmentIds()
        # if "_compartment_default_" in Comps_ids:
        #     numComps -= 1
        #     Comps_ids.remove("_compartment_default_")
        comp_idx_id_list = []
        #Is this the same as comp_node_list?
        numNodes = numFloatingNodes + numBoundaryNodes
        comp_node_list = [0]*numComps #Note: numComps is different from numCompGlyphs
        for i in range(numComps):
            comp_node_list[i] = []

        #if there is layout info:
        if len(spec_id_list) != 0 or len(textGlyph_id_list) != 0 or len(gen_id_list) != 0:
            # comp_specs_in_list = []
            # for i in range(numComps):
            #     comp_node_list[i] = []
            # for i in range(numComps):#only consider the compartment with species in
            #     for j in range(numFloatingNodes):
            #         comp_id = model.getCompartmentIdSpeciesIsIn(FloatingNodes_ids[j])
            #         if comp_id not in comp_specs_in_list:
            #             comp_specs_in_list.append(comp_id)
            #     for j in range(numBoundaryNodes):
            #         comp_id = model.getCompartmentIdSpeciesIsIn(BoundaryNodes_ids[j])
            #         if comp_id not in comp_specs_in_list:
            #             comp_specs_in_list.append(comp_id)
            for i in range(numComps):
                temp_id = Comps_ids[i]
                comp_idx_id_list.append([i,temp_id])
                vol= model.getCompartmentVolume(i)
                if math.isnan(vol):
                    vol = 1.
                position = [10.,10.]
                dimension = compartmentDefaultSize
                comp_fill_color = [255, 255, 255, 255]
                comp_border_color = [255, 255, 255, 255]
                comp_border_width = 2.0
                text_content = ''
                text_position = [0.,0.]
                text_dimension = [0.,0.]
                #if len(comp_id_list) != 0 and temp_id != "_compartment_default_" and (temp_id in comp_specs_in_list):
                if len(comp_id_list) != 0:
                #if mplugin is not None:
                    if temp_id == "_compartment_default_":
                        position = [10., 10.]
                        dimension = compartmentDefaultSize
                        #comp_border_color = [255, 255, 255, 255]
                        #comp_fill_color = [255, 255, 255, 255]

                    for j in range(len(comp_id_list)):
                        if comp_id_list[j] == temp_id:
                            dimension = comp_dimension_list[j]
                            position = comp_position_list[j]
                    for j in range(len(comp_text_content_list)):
                        if comp_id_list[j] == temp_id:
                            text_content = comp_text_content_list[j]
                            text_position = comp_text_position_list[j]
                            text_dimension = comp_text_dimension_list[j]
                    for j in range(len(comp_render)):
                        if temp_id == comp_render[j][0]:
                            comp_fill_color = comp_render[j][1]
                            comp_border_color = comp_render[j][2]
                            comp_border_width = comp_render[j][3]
                            comp_shape_name = comp_render[j][4]
                            comp_shape_type = comp_render[j][5]
                            comp_shape_info = comp_render[j][6]

                    if len(comp_render) == 1:
                        if comp_render[0][0] == '': #global render
                            comp_fill_color = comp_render[0][1]
                            comp_border_color = comp_render[0][2]
                            comp_border_width = comp_render[0][3]
                            comp_shape_name = comp_render[j][4]
                            comp_shape_type = comp_render[j][5]
                            comp_shape_info = comp_render[j][6]
                    for j in range(len(comp_id_list)):    
                        if comp_id_list[j] == temp_id:
                            tempGlyph_id = compGlyph_id_list[j]                         
                            for k in range(len(text_render)):
                                if tempGlyph_id == text_render[k][0]:
                                    text_line_color = text_render[k][1]
                                    text_line_width = text_render[k][2]
                                    text_font_size = text_render[k][3]
                                    [text_anchor, text_vanchor] = text_render[k][4]
                                    text_font_family = text_render[k][6]
                            if len(text_render) == 1:
                                if text_render[0][0] == '':#global render
                                    text_line_color = text_render[0][1]
                                    text_line_width = text_render[0][2]
                                    text_font_size = text_render[0][3]
                                    [text_anchor, text_vanchor] = text_render[0][4]
                                    text_font_family = text_render[0][6]

                else:# no layout info about compartment,
                        # then the whole size of the canvas is the compartment size
                        # modify the compartment size using the max_rec function above
                        # random assigned network:
                        # dimension = [800,800]
                        # position = [40,40]
                        # the whole size of the compartment: 4000*2500
                        position = [10.,10.]
                        dimension = compartmentDefaultSize
                        text_content = ''
                        text_position = [0., 0.]
                        text_dimension = [0, 0.]
                        comp_shape_name = ''
                        comp_shape_type = ''
                        comp_shape_info = []
                        #If there is no render info about the compartments given from sbml,
                        #they will be set as white. 
                        #comp_fill_color = [255, 255, 255, 255]
                        #comp_border_color = [255, 255, 255, 255]
                

                CompartmentData_row_dct = {k:[] for k in COLUMN_NAME_df_CompartmentData}
                CompartmentData_row_dct[NETIDX].append(netIdx)
                CompartmentData_row_dct[IDX].append(i)
                CompartmentData_row_dct[ID].append(temp_id)
                #CompartmentData_row_dct[VOLUMNE].append(vol)
                CompartmentData_row_dct[POSITION].append(position)
                CompartmentData_row_dct[SIZE].append(dimension)
                CompartmentData_row_dct[BORDERCOLOR].append(comp_border_color)
                CompartmentData_row_dct[FILLCOLOR].append(comp_fill_color)
                CompartmentData_row_dct[BORDERWIDTH].append(comp_border_width)
                CompartmentData_row_dct[TXTPOSITION].append(text_position)
                CompartmentData_row_dct[TXTSIZE].append(text_dimension)
                CompartmentData_row_dct[TXTCONTENT].append(text_content)
                CompartmentData_row_dct[TXTFONTCOLOR].append(text_line_color)
                CompartmentData_row_dct[TXTLINEWIDTH].append(text_line_width)
                CompartmentData_row_dct[TXTFONTSIZE].append(text_font_size)
                CompartmentData_row_dct[TXTANCHOR].append([text_anchor, text_vanchor])
                CompartmentData_row_dct[SHAPENAME].append(comp_shape_name)
                CompartmentData_row_dct[SHAPETYPE].append(comp_shape_type)
                CompartmentData_row_dct[SHAPEINFO].append(comp_shape_info)
                # for j in range(len(COLUMN_NAME_df_CompartmentData)):
                #     try: 
                #         CompartmentData_row_dct[COLUMN_NAME_df_CompartmentData[j]] = CompartmentData_row_dct[COLUMN_NAME_df_CompartmentData[j]][0]
                #     except:
                #         CompartmentData_row_dct[COLUMN_NAME_df_CompartmentData[j]] = ''
                # df_CompartmentData = df_CompartmentData.append(CompartmentData_row_dct, ignore_index=True)
                if len(df_CompartmentData) == 0:
                    df_CompartmentData = pd.DataFrame(CompartmentData_row_dct)
                else:
                    df_CompartmentData = pd.concat([df_CompartmentData,\
                        pd.DataFrame(CompartmentData_row_dct)], ignore_index=True)

            numSpec_in_reaction = len(spec_specGlyph_id_list)

            id_list = []
            node_idx_specGlyphid_list = []
            # orphan nodes have been considered, so numSpec_in_reaction should equals to numSpecGlyphs
            # if numSpecGlyphs > numSpec_in_reaction:
            #     print("Orphan nodes are removed.")
            for i in range (numSpec_in_reaction):
                temp_id = spec_specGlyph_id_list[i][0]
                temp_concentration = spec_concentration_list[i]
                tempGlyph_id = spec_specGlyph_id_list[i][1]
                dimension = spec_dimension_list[i]
                position = spec_position_list[i]
                text_position = spec_text_position_list[i]
                text_dimension = spec_text_dimension_list[i]
                text_content = spec_text_content_list[i]
                comp_id = model.getCompartmentIdSpeciesIsIn(temp_id)
                #print(comp_id)
                temp_comp_idx = -1
                for j in range(len(comp_idx_id_list)):
                    if comp_idx_id_list[j][1] == comp_id:
                        temp_comp_idx = comp_idx_id_list[j][0]
                for j in range(numFloatingNodes):
                    if temp_id == FloatingNodes_ids[j]:
                        if temp_id not in id_list:
                            #spec_render
                            flag_local = 0
                            for k in range(len(spec_render)):
                                if temp_id == spec_render[k][0]:
                                    spec_fill_color = spec_render[k][1]
                                    spec_border_color = spec_render[k][2]
                                    spec_border_width = spec_render[k][3]
                                    shapeIdx = spec_render[k][4]
                                    shape_name = spec_render[k][5]
                                    shape_type = spec_render[k][6]
                                    shape_info = spec_render[k][7]
                                    spec_dash = spec_render[k][8]
                                    flag_local = 1
                            if flag_local == 0 and len(spec_render) != 1:
                                for k in range(len(spec_render)):
                                    if spec_render[k][0] == '': #global render but not for all
                                        spec_fill_color = spec_render[k][1]
                                        spec_border_color = spec_render[k][2]
                                        spec_border_width = spec_render[k][3]
                                        shapeIdx = spec_render[k][4]
                                        shape_name = spec_render[k][5]
                                        shape_type = spec_render[k][6]
                                        shape_info = spec_render[k][7]
                                        spec_dash = spec_render[k][8]
                            if len(spec_render) == 1:
                                if spec_render[0][0] == '': #global render
                                    spec_fill_color = spec_render[0][1]
                                    spec_border_color = spec_render[0][2]
                                    spec_border_width = spec_render[0][3]
                                    shapeIdx = spec_render[0][4]
                                    shape_name = spec_render[0][5]
                                    shape_type = spec_render[0][6]
                                    shape_info = spec_render[0][7]
                                    spec_dash = spec_render[k][8]
                            for k in range(len(text_render)):
                                if tempGlyph_id == text_render[k][0]:
                                    text_line_color = text_render[k][1]
                                    text_line_width = text_render[k][2]
                                    text_font_size = text_render[k][3]
                                    [text_anchor, text_vanchor] = text_render[k][4]
                                    text_font_family = text_render[k][6]
                            if len(text_render) == 1:
                                if text_render[0][0] == '':#global render
                                    text_line_color = text_render[0][1]
                                    text_line_width = text_render[0][2]
                                    text_font_size = text_render[0][3]
                                    [text_anchor, text_vanchor] = text_render[0][4]
                                    text_font_family = text_render[0][6]
                            id_list.append(temp_id)
                            node_idx_specGlyphid_list.append([i,tempGlyph_id])
                            
                            NodeData_row_dct = {k:[] for k in COLUMN_NAME_df_NodeData}
                            NodeData_row_dct[NETIDX].append(netIdx)
                            NodeData_row_dct[COMPIDX].append(temp_comp_idx)
                            NodeData_row_dct[IDX].append(i)
                            NodeData_row_dct[ORIGINALIDX].append(-1)
                            NodeData_row_dct[ID].append(temp_id)
                            NodeData_row_dct[FLOATINGNODE].append('TRUE')
                            NodeData_row_dct[CONCENTRATION].append(temp_concentration)
                            NodeData_row_dct[POSITION].append(position)
                            NodeData_row_dct[SIZE].append(dimension)
                            NodeData_row_dct[SHAPEIDX].append(shapeIdx)
                            NodeData_row_dct[TXTPOSITION].append(text_position)
                            NodeData_row_dct[TXTSIZE].append(text_dimension)
                            NodeData_row_dct[FILLCOLOR].append(spec_fill_color)
                            NodeData_row_dct[BORDERCOLOR].append(spec_border_color)
                            NodeData_row_dct[BORDERWIDTH].append(spec_border_width)
                            NodeData_row_dct[TXTFONTCOLOR].append(text_line_color)
                            NodeData_row_dct[TXTLINEWIDTH].append(text_line_width)
                            NodeData_row_dct[TXTFONTSIZE].append(text_font_size)
                            NodeData_row_dct[SHAPENAME].append(shape_name)
                            NodeData_row_dct[SHAPETYPE].append(shape_type)
                            NodeData_row_dct[SHAPEINFO].append(shape_info)
                            NodeData_row_dct[TXTCONTENT].append(text_content)
                            NodeData_row_dct[TXTANCHOR].append([text_anchor, text_vanchor])
                            NodeData_row_dct[SPECDASH].append(spec_dash)
                            NodeData_row_dct[TXTFONTFAMILY].append(text_font_family)
                            # for j in range(len(COLUMN_NAME_df_NodeData)):
                            #     try: 
                            #         NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = NodeData_row_dct[COLUMN_NAME_df_NodeData[j]][0]
                            #     except:
                            #         NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = ''
                            # df_NodeData = df_NodeData.append(NodeData_row_dct, ignore_index=True)
                            if len(df_NodeData) == 0:
                                df_NodeData = pd.DataFrame(NodeData_row_dct)
                            else:
                                df_NodeData = pd.concat([df_NodeData,\
                                    pd.DataFrame(NodeData_row_dct)], ignore_index=True)
                    
                        else:
                            original_idx = id_list.index(temp_id)
                            #spec_render
                            flag_local = 0
                            for k in range(len(spec_render)):
                                if temp_id == spec_render[k][0]:
                                    spec_fill_color = spec_render[k][1]
                                    spec_border_color = spec_render[k][2]
                                    spec_border_width = spec_render[k][3]
                                    shapeIdx = spec_render[k][4]
                                    shape_name = spec_render[k][5]
                                    shape_type = spec_render[k][6]
                                    shape_info = spec_render[k][7]
                                    spec_dash = spec_render[k][8]
                                    flag_local = 1
                            if flag_local == 0 and len(spec_render) != 1:
                                for k in range(len(spec_render)):
                                    if spec_render[k][0] == '': #global render but not for all
                                        spec_fill_color = spec_render[k][1]
                                        spec_border_color = spec_render[k][2]
                                        spec_border_width = spec_render[k][3]
                                        shapeIdx = spec_render[k][4]
                                        shape_name = spec_render[k][5]
                                        shape_type = spec_render[k][6]
                                        shape_info = spec_render[k][7]
                                        spec_dash = spec_render[k][8]
                            if len(spec_render) == 1:
                                if spec_render[0][0] == '': #global render
                                    spec_fill_color = spec_render[0][1]
                                    spec_border_color = spec_render[0][2]
                                    spec_border_width = spec_render[0][3]
                                    shapeIdx = spec_render[0][4]
                                    shape_name = spec_render[0][5]
                                    shape_type = spec_render[0][6]
                                    shape_info = spec_render[0][7]
                                    spec_dash = spec_render[k][8]
                            for k in range(len(text_render)):
                                if tempGlyph_id == text_render[k][0]:
                                    text_line_color = text_render[k][1]
                                    text_line_width = text_render[k][2]
                                    text_font_size = text_render[k][3]
                                    [text_anchor, text_vanchor] = text_render[k][4]
                                    text_font_family = text_render[k][6]
                            if len(text_render) == 1:
                                if text_render[0][0] == '':#global render
                                    text_line_color = text_render[0][1]
                                    text_line_width = text_render[0][2]
                                    text_font_size = text_render[0][3]
                                    [text_anchor, text_vanchor] = text_render[0][4]
                                    text_font_family = text_render[0][6]
                            node_idx_specGlyphid_list.append([i,tempGlyph_id])

                            NodeData_row_dct = {k:[] for k in COLUMN_NAME_df_NodeData}
                            NodeData_row_dct[NETIDX].append(netIdx)
                            NodeData_row_dct[COMPIDX].append(temp_comp_idx)
                            NodeData_row_dct[IDX].append(i)
                            NodeData_row_dct[ORIGINALIDX].append(original_idx)
                            NodeData_row_dct[ID].append(temp_id)
                            NodeData_row_dct[FLOATINGNODE].append('TRUE')
                            NodeData_row_dct[CONCENTRATION].append(temp_concentration)
                            NodeData_row_dct[POSITION].append(position)
                            NodeData_row_dct[SIZE].append(dimension)
                            NodeData_row_dct[SHAPEIDX].append(shapeIdx)
                            NodeData_row_dct[TXTPOSITION].append(text_position)
                            NodeData_row_dct[TXTSIZE].append(text_dimension)
                            NodeData_row_dct[FILLCOLOR].append(spec_fill_color)
                            NodeData_row_dct[BORDERCOLOR].append(spec_border_color)
                            NodeData_row_dct[BORDERWIDTH].append(spec_border_width)
                            NodeData_row_dct[TXTFONTCOLOR].append(text_line_color)
                            NodeData_row_dct[TXTLINEWIDTH].append(text_line_width)
                            NodeData_row_dct[TXTFONTSIZE].append(text_font_size)
                            NodeData_row_dct[SHAPENAME].append(shape_name)
                            NodeData_row_dct[SHAPETYPE].append(shape_type)
                            NodeData_row_dct[SHAPEINFO].append(shape_info)
                            NodeData_row_dct[TXTCONTENT].append(text_content)
                            NodeData_row_dct[TXTANCHOR].append([text_anchor, text_vanchor])
                            NodeData_row_dct[SPECDASH].append(spec_dash)
                            NodeData_row_dct[TXTFONTFAMILY].append(text_font_family)
                            # for j in range(len(COLUMN_NAME_df_NodeData)):
                            #     try: 
                            #         NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = NodeData_row_dct[COLUMN_NAME_df_NodeData[j]][0]
                            #     except:
                            #         NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = ''
                            # df_NodeData = df_NodeData.append(NodeData_row_dct, ignore_index=True)
                            if len(df_NodeData) == 0:
                                df_NodeData = pd.DataFrame(NodeData_row_dct)
                            else:
                                df_NodeData = pd.concat([df_NodeData,\
                                    pd.DataFrame(NodeData_row_dct)], ignore_index=True)
                for j in range(numBoundaryNodes):
                    if temp_id == BoundaryNodes_ids[j]:
                        if temp_id not in id_list:
                            #spec_render
                            flag_local = 0
                            for k in range(len(spec_render)):
                                if temp_id == spec_render[k][0]:
                                    spec_fill_color = spec_render[k][1]
                                    spec_border_color = spec_render[k][2]
                                    spec_border_width = spec_render[k][3]
                                    shapeIdx = spec_render[k][4]
                                    shape_name = spec_render[k][5]
                                    shape_type = spec_render[k][6]
                                    shape_info = spec_render[k][7]
                                    spec_dash = spec_render[k][8]
                                    flag_local = 1
                            if flag_local == 0 and len(spec_render) != 1:
                                for k in range(len(spec_render)):
                                    if spec_render[k][0] == '': #global render but not for all
                                        spec_fill_color = spec_render[k][1]
                                        spec_border_color = spec_render[k][2]
                                        spec_border_width = spec_render[k][3]
                                        shapeIdx = spec_render[k][4]
                                        shape_name = spec_render[k][5]
                                        shape_type = spec_render[k][6]
                                        shape_info = spec_render[k][7]
                                        spec_dash = spec_render[k][8]
                            if len(spec_render) == 1:
                                if spec_render[0][0] == '': #global render
                                    spec_fill_color = spec_render[0][1]
                                    spec_border_color = spec_render[0][2]
                                    spec_border_width = spec_render[0][3]
                                    shapeIdx = spec_render[0][4]
                                    shape_name = spec_render[0][5]
                                    shape_type = spec_render[0][6]
                                    shape_info = spec_render[0][7]
                                    spec_dash = spec_render[k][8]
                            for k in range(len(text_render)):
                                if tempGlyph_id == text_render[k][0]:
                                    text_line_color = text_render[k][1]
                                    text_line_width = text_render[k][2]  
                                    text_font_size = text_render[k][3] 
                                    [text_anchor, text_vanchor] = text_render[k][4] 
                                    text_font_family = text_render[k][6]
                            if len(text_render) == 1:
                                if text_render[0][0] == '':#global render
                                    text_line_color = text_render[0][1]
                                    text_line_width = text_render[0][2]
                                    text_font_size = text_render[0][3]
                                    [text_anchor, text_vanchor] = text_render[0][4] 
                                    text_font_family = text_render[0][6]   
                            id_list.append(temp_id)
                            node_idx_specGlyphid_list.append([i,tempGlyph_id])

                            NodeData_row_dct = {k:[] for k in COLUMN_NAME_df_NodeData}
                            NodeData_row_dct[NETIDX].append(netIdx)
                            NodeData_row_dct[COMPIDX].append(temp_comp_idx)
                            NodeData_row_dct[IDX].append(i)
                            NodeData_row_dct[ORIGINALIDX].append(-1)
                            NodeData_row_dct[ID].append(temp_id)
                            NodeData_row_dct[FLOATINGNODE].append('FALSE')
                            NodeData_row_dct[CONCENTRATION].append(temp_concentration)
                            NodeData_row_dct[POSITION].append(position)
                            NodeData_row_dct[SIZE].append(dimension)
                            NodeData_row_dct[SHAPEIDX].append(shapeIdx)
                            NodeData_row_dct[TXTPOSITION].append(text_position)
                            NodeData_row_dct[TXTSIZE].append(text_dimension)
                            NodeData_row_dct[FILLCOLOR].append(spec_fill_color)
                            NodeData_row_dct[BORDERCOLOR].append(spec_border_color)
                            NodeData_row_dct[BORDERWIDTH].append(spec_border_width)
                            NodeData_row_dct[TXTFONTCOLOR].append(text_line_color)
                            NodeData_row_dct[TXTLINEWIDTH].append(text_line_width)
                            NodeData_row_dct[TXTFONTSIZE].append(text_font_size)
                            NodeData_row_dct[SHAPENAME].append(shape_name)
                            NodeData_row_dct[SHAPETYPE].append(shape_type)
                            NodeData_row_dct[SHAPEINFO].append(shape_info)
                            NodeData_row_dct[TXTCONTENT].append(text_content)
                            NodeData_row_dct[TXTANCHOR].append([text_anchor, text_vanchor])
                            NodeData_row_dct[SPECDASH].append(spec_dash)
                            NodeData_row_dct[TXTFONTFAMILY].append(text_font_family)
                            # for j in range(len(COLUMN_NAME_df_NodeData)):
                            #     try: 
                            #         NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = NodeData_row_dct[COLUMN_NAME_df_NodeData[j]][0]
                            #     except:
                            #         NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = ''
                            # df_NodeData = df_NodeData.append(NodeData_row_dct, ignore_index=True)
                            if len(df_NodeData) == 0:
                                df_NodeData = pd.DataFrame(NodeData_row_dct)
                            else:
                                df_NodeData = pd.concat([df_NodeData,\
                                    pd.DataFrame(NodeData_row_dct)], ignore_index=True)
                        else:
                            #spec_render
                            flag_local = 0
                            for k in range(len(spec_render)):
                                if temp_id == spec_render[k][0]:
                                    spec_fill_color = spec_render[k][1]
                                    spec_border_color = spec_render[k][2]
                                    spec_border_width = spec_render[k][3]
                                    shapeIdx = spec_render[k][4]
                                    shape_name = spec_render[k][5]
                                    shape_type = spec_render[k][6]
                                    shape_info = spec_render[k][7]
                                    spec_dash = spec_render[k][8]
                                    flag_local = 1
                            if flag_local == 0 and len(spec_render) != 1:
                                for k in range(len(spec_render)):
                                    if spec_render[k][0] == '': #global render but not for all
                                        spec_fill_color = spec_render[k][1]
                                        spec_border_color = spec_render[k][2]
                                        spec_border_width = spec_render[k][3]
                                        shapeIdx = spec_render[k][4]
                                        shape_name = spec_render[k][5]
                                        shape_type = spec_render[k][6]
                                        shape_info = spec_render[k][7]
                                        spec_dash = spec_render[k][8]
                            if len(spec_render) == 1:
                                if spec_render[0][0] == '': #global render
                                    spec_fill_color = spec_render[0][1]
                                    spec_border_color = spec_render[0][2]
                                    spec_border_width = spec_render[0][3]
                                    shapeIdx = spec_render[0][4]
                                    shape_name = spec_render[0][5]
                                    shape_type = spec_render[0][6]
                                    shape_info = spec_render[0][7]
                                    spec_dash = spec_render[k][8]
                            for k in range(len(text_render)):
                                if tempGlyph_id == text_render[k][0]:
                                    text_line_color = text_render[k][1]
                                    text_line_width = text_render[k][2] 
                                    text_font_size = text_render[k][3]
                                    [text_anchor, text_vanchor] = text_render[k][4]
                                    text_font_family = text_render[k][6]
                            if len(text_render) == 1:
                                if text_render[0][0] == '':#global render
                                    text_line_color = text_render[0][1]
                                    text_line_width = text_render[0][2]
                                    text_font_size = text_render[0][3]
                                    [text_anchor, text_vanchor] = text_render[0][4]
                                    text_font_family = text_render[0][6]

                            node_idx_specGlyphid_list.append([i,tempGlyph_id])

                            NodeData_row_dct = {k:[] for k in COLUMN_NAME_df_NodeData}
                            NodeData_row_dct[NETIDX].append(netIdx)
                            NodeData_row_dct[COMPIDX].append(temp_comp_idx)
                            NodeData_row_dct[IDX].append(i)
                            NodeData_row_dct[ORIGINALIDX].append(original_idx)
                            NodeData_row_dct[ID].append(temp_id)
                            NodeData_row_dct[FLOATINGNODE].append('FALSE')
                            NodeData_row_dct[CONCENTRATION].append(temp_concentration)
                            NodeData_row_dct[POSITION].append(position)
                            NodeData_row_dct[SIZE].append(dimension)
                            NodeData_row_dct[SHAPEIDX].append(shapeIdx)
                            NodeData_row_dct[TXTPOSITION].append(text_position)
                            NodeData_row_dct[TXTSIZE].append(text_dimension)
                            NodeData_row_dct[FILLCOLOR].append(spec_fill_color)
                            NodeData_row_dct[BORDERCOLOR].append(spec_border_color)
                            NodeData_row_dct[BORDERWIDTH].append(spec_border_width)
                            NodeData_row_dct[TXTFONTCOLOR].append(text_line_color)
                            NodeData_row_dct[TXTLINEWIDTH].append(text_line_width)
                            NodeData_row_dct[TXTFONTSIZE].append(text_font_size)
                            NodeData_row_dct[SHAPENAME].append(shape_name)
                            NodeData_row_dct[SHAPETYPE].append(shape_type)
                            NodeData_row_dct[SHAPEINFO].append(shape_info)
                            NodeData_row_dct[TXTCONTENT].append(text_content)
                            NodeData_row_dct[TXTANCHOR].append([text_anchor, text_vanchor])
                            NodeData_row_dct[SPECDASH].append(spec_dash)
                            NodeData_row_dct[TXTFONTFAMILY].append(text_font_family)
                            # for j in range(len(COLUMN_NAME_df_NodeData)):
                            #     try: 
                            #         NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = NodeData_row_dct[COLUMN_NAME_df_NodeData[j]][0]
                            #     except:
                            #         NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = ''
                            # df_NodeData = df_NodeData.append(NodeData_row_dct, ignore_index=True)
                            if len(df_NodeData) == 0:
                                df_NodeData = pd.DataFrame(NodeData_row_dct)
                            else:
                                df_NodeData = pd.concat([df_NodeData,\
                                    pd.DataFrame(NodeData_row_dct)], ignore_index=True)
            
            for i in range (numReactionGlyphs):
                src_idx_list = []
                src_position = []
                src_dimension = []
                src_endhead = []
                src_dash = []
                src_lineend_pos = []
                dst_idx_list = [] 
                dst_position = []
                dst_dimension = []
                dst_endhead = []
                dst_dash = []
                dst_lineend_pos = []
                mod_idx_list = []
                mod_position = []
                mod_dimension = []
                mod_endhead = []
                mod_lineend_pos = []
                src_handle = []
                dst_handle = []
                temp_id = reaction_id_list[i]
                rxn_rev = reaction_rev_list[i]
                kinetics = kinetics_list[i]
                # rct_num = max(len(rct_specGlyph_handle_list[i]),len(reaction_rct_list[i]))
                # prd_num = max(len(prd_specGlyph_handle_list[i]),len(reaction_prd_list[i]))
                # mod_num = max(len(mod_specGlyph_list[i]),len(reaction_mod_list[i]))
                rct_num = len(rct_specGlyph_handle_list[i])
                prd_num = len(prd_specGlyph_handle_list[i])
                mod_num = len(mod_specGlyph_list[i])

                #print(rct_num, prd_num, mod_num)

                # for j in range(rct_num):
                #     temp_specGlyph_id = rct_specGlyph_list[i][j]
                #     for k in range(numSpec_in_reaction):
                #         if temp_specGlyph_id == specGlyph_id_list[k]:
                #             src_position.append(spec_position_list[k])
                #             src_dimension.append(spec_dimension_list[k])

                # for j in range(prd_num):
                #     temp_specGlyph_id = prd_specGlyph_list[i][j]
                #     for k in range(numSpec_in_reaction):
                #         if temp_specGlyph_id == specGlyph_id_list[k]:
                #             dst_position.append(spec_position_list[k])
                #             dst_dimension.append(spec_dimension_list[k])

                if rct_num != 0 or prd_num != 0:
                    for j in range(rct_num):
                        temp_specGlyph_id = rct_specGlyph_handle_list[i][j][0]
                        temp_specRefGlyph_id = rct_specGlyph_handle_list[i][j][2]
                        for k in range(len(node_idx_specGlyphid_list)):
                            if temp_specGlyph_id == node_idx_specGlyphid_list[k][1]:
                                src_idx_list.append(node_idx_specGlyphid_list[k][0])
                        for k in range(numSpec_in_reaction):
                            if temp_specGlyph_id == specGlyph_id_list[k]:
                                src_position.append(spec_position_list[k])
                                src_dimension.append(spec_dimension_list[k])
                        for k in range(len(specRefGlyph_render)):
                            if temp_specRefGlyph_id == specRefGlyph_render[k][0]:
                                src_endhead.append(specRefGlyph_render[k][1])
                        for k in range(len(specRefGlyph_render)):
                            if temp_specRefGlyph_id == specRefGlyph_render[k][0]:
                                src_dash = specRefGlyph_render[k][2]

                        src_handle.append(rct_specGlyph_handle_list[i][j][1])
                        src_lineend_pos.append(rct_specGlyph_handle_list[i][j][3])
                    src_idx_list_corr = []
                    [src_idx_list_corr.append(x) for x in src_idx_list if x not in src_idx_list_corr]

                    for j in range(prd_num):
                        temp_specGlyph_id = prd_specGlyph_handle_list[i][j][0]
                        temp_specRefGlyph_id = prd_specGlyph_handle_list[i][j][2]
                        for k in range(len(node_idx_specGlyphid_list)):
                            if temp_specGlyph_id == node_idx_specGlyphid_list[k][1]:
                                dst_idx_list.append(node_idx_specGlyphid_list[k][0])
                        for k in range(numSpec_in_reaction):
                            if temp_specGlyph_id == specGlyph_id_list[k]:
                                dst_position.append(spec_position_list[k])
                                dst_dimension.append(spec_dimension_list[k])
                        for k in range(len(specRefGlyph_render)):
                            if temp_specRefGlyph_id == specRefGlyph_render[k][0]:
                                dst_endhead.append(specRefGlyph_render[k][1])
                        for k in range(len(specRefGlyph_render)):
                            if temp_specRefGlyph_id == specRefGlyph_render[k][0]:
                                dst_dash = specRefGlyph_render[k][2]

                        dst_handle.append(prd_specGlyph_handle_list[i][j][1])
                        dst_lineend_pos.append(prd_specGlyph_handle_list[i][j][3])

                    dst_idx_list_corr = []
                    [dst_idx_list_corr.append(x) for x in dst_idx_list if x not in dst_idx_list_corr]

                    #print(mod_specGlyph_list)
                    for j in range(mod_num):
                        #if len(mod_specGlyph_list[i]) != 0:
                        if len(mod_specGlyph_list[i]) == mod_num:
                            #all the modifiers are defined as role in the SpecRefGlyph
                            temp_specGlyph_id = mod_specGlyph_list[i][j][0]
                            temp_specRefGlyph_id = mod_specGlyph_list[i][j][1]
                            mod_lineend_pos.append(mod_specGlyph_list[i][j][2])
                            for k in range(len(node_idx_specGlyphid_list)):
                                if temp_specGlyph_id == node_idx_specGlyphid_list[k][1]:
                                    mod_idx_list.append(node_idx_specGlyphid_list[k][0])
                            for k in range(numSpec_in_reaction):
                                if temp_specGlyph_id == specGlyph_id_list[k]:
                                    mod_position.append(spec_position_list[k])
                                    mod_dimension.append(spec_dimension_list[k])
                            for k in range(len(specRefGlyph_render)):
                                if temp_specRefGlyph_id == specRefGlyph_render[k][0]:
                                    mod_endhead.append(specRefGlyph_render[k][1])
                        else:
                            for k in range(len(spec_specGlyph_id_list)):
                                if reaction_mod_list[i][j] == spec_specGlyph_id_list[k][0]:
                                    temp_specGlyph_id = spec_specGlyph_id_list[k][1]
                            for k in range(len(node_idx_specGlyphid_list)):
                                if temp_specGlyph_id == node_idx_specGlyphid_list[k][1]:
                                    mod_idx_list.append(node_idx_specGlyphid_list[k][0])
                            for k in range(numSpec_in_reaction):
                                if temp_specGlyph_id == specGlyph_id_list[k]:
                                    mod_position.append(spec_position_list[k])
                                    mod_dimension.append(spec_dimension_list[k])
                            for k in range(len(specRefGlyph_render)):
                                if temp_specRefGlyph_id == specRefGlyph_render[k][0]:
                                    mod_endhead.append(specRefGlyph_render[k][1])

                else:
                    src_idx_list = []
                    dst_idx_list = []
                    mod_idx_list = []
                    rct_num = model.getNumReactants(i)
                    prd_num = model.getNumProducts(i)
                    mod_num = model.getNumModifiers(temp_id)
             
                    for j in range(rct_num):
                        rct_id = model.getReactant(temp_id,j)
                        for k in range(len(spec_specGlyph_id_list)):
                            if spec_specGlyph_id_list[k][0] == rct_id:
                                tempGlyph_id = spec_specGlyph_id_list[k][1]
                        for k in range(len(node_idx_specGlyphid_list)):
                            if node_idx_specGlyphid_list[k][1] == tempGlyph_id:
                                src_idx_list.append(node_idx_specGlyphid_list[k][0])
                    src_idx_list_corr = []
                    [src_idx_list_corr.append(x) for x in src_idx_list if x not in src_idx_list_corr]

                    for j in range(prd_num):
                        prd_id = model.getProduct(temp_id,j)
                        for k in range(len(spec_specGlyph_id_list)):
                            if spec_specGlyph_id_list[k][0] == prd_id:
                                tempGlyph_id = spec_specGlyph_id_list[k][1]
                        for k in range(len(node_idx_specGlyphid_list)):
                            if node_idx_specGlyphid_list[k][1] == tempGlyph_id:
                                dst_idx_list.append(node_idx_specGlyphid_list[k][0]) 
                    dst_idx_list_corr = []
                    [dst_idx_list_corr.append(x) for x in dst_idx_list if x not in dst_idx_list_corr]

                    modifiers = model.getListOfModifiers(temp_id)
                    for j in range(mod_num):
                        mod_id = modifiers[j]
                        for k in range(len(spec_specGlyph_id_list)):
                            if spec_specGlyph_id_list[k][0] == mod_id:
                                tempGlyph_id = spec_specGlyph_id_list[k][1]
                        for k in range(len(node_idx_specGlyphid_list)):
                            if node_idx_specGlyphid_list[k][1] == tempGlyph_id:
                                mod_idx_list.append(node_idx_specGlyphid_list[k][0])

                for j in range(len(rxn_render)):
                    if temp_id == rxn_render[j][0]:
                        reaction_line_color = rxn_render[j][1]
                        reaction_line_width = rxn_render[j][2]
                        reaction_arrow_head_size = rxn_render[j][3]
                        reaction_dash = rxn_render[j][4]
                        reaction_line_fill = rxn_render[j][5]
                        reaction_shape_name = rxn_render[j][6]
                        reaction_shape_type = rxn_render[j][7]
                        reaction_shape_info = rxn_render[j][8]
                if len(rxn_render) == 1:
                    if rxn_render[0][0] == '':#global render
                        reaction_line_color = rxn_render[0][1]
                        reaction_line_width = rxn_render[0][2]
                        reaction_arrow_head_size = rxn_render[0][3]
                        reaction_dash = rxn_render[0][4]
                        reaction_line_fill = rxn_render[0][5]
                        reaction_shape_name = rxn_render[j][6]
                        reaction_shape_type = rxn_render[j][7]
                        reaction_shape_info = rxn_render[j][8]
            
                # try:
                #     if reaction_dash == [] and src_dash != []:
                #         reaction_dash = src_dash
                # except:
                #     if reaction_dash == [] and dst_dash != []:
                #         reaction_dash = dst_dash

                for j in range(len(reaction_id_list)):    
                    if reaction_id_list[j] == temp_id:
                        tempGlyph_id = reactionGlyph_id_list[j]  
                        for m in range(len(textGlyph_rxn_id_list)):
                            if textGlyph_rxn_id_list[m][0] == tempGlyph_id: #reactionGlyph_id
                                textGlyph_id = textGlyph_rxn_id_list[m][1]
                                text_content = rxn_text_content_list[m]
                                text_position = rxn_text_position_list[m]
                                text_dimension = rxn_text_dimension_list[m]

                                for k in range(len(text_render)):
                                    if textGlyph_id == text_render[k][5]:
                                        text_line_color = text_render[k][1]
                                        text_line_width = text_render[k][2]
                                        text_font_size = text_render[k][3]
                                        [text_anchor, text_vanchor] = text_render[k][4]
                                        text_font_family = text_render[k][6]
                                if len(text_render) == 1:
                                    if text_render[0][0] == '':#global render
                                        text_line_color = text_render[0][1]
                                        text_line_width = text_render[0][2]
                                        text_font_size = text_render[0][3]
                                        [text_anchor, text_vanchor] = text_render[0][4]
                                        text_font_family = text_render[0][6]

                                ReactionTextData_row_dct = {k:[] for k in COLUMN_NAME_df_ReactionTextData}
                                ReactionTextData_row_dct[RXNID].append(temp_id)
                                ReactionTextData_row_dct[TXTID].append(textGlyph_id)
                                ReactionTextData_row_dct[TXTCONTENT].append(text_content)
                                ReactionTextData_row_dct[TXTPOSITION].append(text_position)
                                ReactionTextData_row_dct[TXTSIZE].append(text_dimension)
                                ReactionTextData_row_dct[TXTFONTCOLOR].append(text_line_color)
                                ReactionTextData_row_dct[TXTLINEWIDTH].append(text_line_width)
                                ReactionTextData_row_dct[TXTFONTSIZE].append(text_font_size)
                                ReactionTextData_row_dct[TXTANCHOR].append([text_anchor, text_vanchor])
                                if len(df_ReactionTextData) == 0:
                                    df_ReactionTextData = pd.DataFrame(ReactionTextData_row_dct)
                                else:
                                    df_ReactionTextData = pd.concat([df_ReactionTextData,\
                                        pd.DataFrame(ReactionTextData_row_dct)], ignore_index=True)
       
                try: 
                    center_size = [0.,0.]
                    center_position = reaction_center_list[i]
                    center_size = reaction_size_list[i]
                    center_handle = reaction_center_handle_list[i]
                    if center_handle != []:
                        handles = [center_handle]
                    else:
                        handles = [center_position]
                    handles.extend(src_handle)
                    handles.extend(dst_handle) 
                    #print("process:", handles) 
                    ReactionData_row_dct = {k:[] for k in COLUMN_NAME_df_ReactionData}
                    ReactionData_row_dct[NETIDX].append(netIdx)
                    ReactionData_row_dct[IDX].append(i)
                    ReactionData_row_dct[ID].append(temp_id)
                    ReactionData_row_dct[SOURCES].append(src_idx_list_corr)
                    ReactionData_row_dct[TARGETS].append(dst_idx_list_corr)
                    ReactionData_row_dct[RATELAW].append(kinetics)
                    ReactionData_row_dct[MODIFIERS].append(mod_idx_list)
                    ReactionData_row_dct[STROKECOLOR].append(reaction_line_color)
                    ReactionData_row_dct[LINETHICKNESS].append(reaction_line_width)
                    ReactionData_row_dct[CENTERPOS].append(center_position)
                    ReactionData_row_dct[HANDLES].append(handles)
                    if reactionLineType == 'bezier':
                        ReactionData_row_dct[BEZIER].append('TRUE')
                    else:
                        ReactionData_row_dct[BEZIER].append('FALSE')
                    ReactionData_row_dct[ARROWHEADSIZE].append(reaction_arrow_head_size)
                    ReactionData_row_dct[RXNDASH].append(reaction_dash)
                    ReactionData_row_dct[RXNREV].append(rxn_rev)
                    ReactionData_row_dct[FILLCOLOR].append(reaction_line_fill)
                    if src_endhead == []:
                        src_endhead = ["_line_ending_default_NONE_" + temp_id]
                        #default src endhead 
                        if ('_line_ending_default_NONE_' + temp_id) not in df_LineEndingData[ID].values:        
                            LineEndingData_row_dct = {k:[] for k in COLUMN_NAME_df_LineEndingData}
                            LineEndingData_row_dct[ID].append('_line_ending_default_NONE_' + temp_id)
                            LineEndingData_row_dct[POSITION].append([0.,0.])
                            LineEndingData_row_dct[SIZE].append([0.,0.])
                            LineEndingData_row_dct[FILLCOLOR].append(reaction_line_color)
                            LineEndingData_row_dct[SHAPETYPE].append([])
                            LineEndingData_row_dct[SHAPEINFO].append([])
                            LineEndingData_row_dct[BORDERCOLOR].append(reaction_line_color)
                            if len(df_LineEndingData) == 0:
                                df_LineEndingData = pd.DataFrame(LineEndingData_row_dct)
                            else:
                                df_LineEndingData = pd.concat([df_LineEndingData,\
                                    pd.DataFrame(LineEndingData_row_dct)], ignore_index=True)

                    ReactionData_row_dct[SOURCESLINEENDING].append(src_endhead)
                    if dst_endhead == []:
                        dst_endhead = ['line_ending_' + temp_id]
                        #default dst endhead
                        if ('line_ending_' + temp_id) not in df_LineEndingData[ID].values: 
                            LineEndingData_row_dct = {k:[] for k in COLUMN_NAME_df_LineEndingData}
                            LineEndingData_row_dct[ID].append('line_ending_' + temp_id)
                            LineEndingData_row_dct[POSITION].append([-reaction_arrow_head_size[0], -0.5*reaction_arrow_head_size[1]])
                            LineEndingData_row_dct[SIZE].append(reaction_arrow_head_size)
                            LineEndingData_row_dct[FILLCOLOR].append(reaction_line_color)
                            LineEndingData_row_dct[SHAPETYPE].append(['polygon'])
                            LineEndingData_row_dct[SHAPEINFO].append([[[0,0], [100,50], [0,100], [0,0]]])
                            LineEndingData_row_dct[BORDERCOLOR].append(reaction_line_color)
                            if len(df_LineEndingData) == 0:
                                df_LineEndingData = pd.DataFrame(LineEndingData_row_dct)
                            else:
                                df_LineEndingData = pd.concat([df_LineEndingData,\
                                    pd.DataFrame(LineEndingData_row_dct)], ignore_index=True)

                    ReactionData_row_dct[TARGETSLINEENDING].append(dst_endhead)
                    if mod_endhead != [] and len(mod_endhead) < len(mod_idx_list):
                        for j in range(len(mod_idx_list)-len(mod_endhead)):
                            mod_endhead.append(mod_endhead[0])
                    if mod_endhead == [] and len(mod_idx_list) != 0:
                        for j in range(len(mod_idx_list)):
                            mod_endhead.append('line_ending_modifier_'+temp_id+"_"+str(mod_idx_list[j]))
                        #default modifier endhead
                        for j in range(len(mod_idx_list)):
                            if ('line_ending_modifier_' + temp_id + '_' + str(mod_idx_list[j])) not in df_LineEndingData[ID].values: 
                                LineEndingData_row_dct = {k:[] for k in COLUMN_NAME_df_LineEndingData}
                                LineEndingData_row_dct[ID].append('line_ending_modifier_' + temp_id + '_' + str(mod_idx_list[j]))
                                LineEndingData_row_dct[POSITION].append([-1.*reaction_line_width, 0.])
                                LineEndingData_row_dct[SIZE].append([2*reaction_line_width, 2*reaction_line_width])
                                LineEndingData_row_dct[FILLCOLOR].append(reaction_line_color)
                                LineEndingData_row_dct[SHAPETYPE].append(['ellipse'])
                                LineEndingData_row_dct[SHAPEINFO].append([[[0.0, 0.0], [100.0, 100.0]]])
                                LineEndingData_row_dct[BORDERCOLOR].append(reaction_line_color)

                                if len(df_LineEndingData) == 0:
                                    df_LineEndingData = pd.DataFrame(LineEndingData_row_dct)
                                else:
                                    df_LineEndingData = pd.concat([df_LineEndingData,\
                                        pd.DataFrame(LineEndingData_row_dct)], ignore_index=True)
           
                    ReactionData_row_dct[MODIFIERSLINEENDING].append(mod_endhead)
                    ReactionData_row_dct[SRCLINEENDPOS].append(src_lineend_pos)
                    ReactionData_row_dct[TGTLINEENDPOS].append(dst_lineend_pos)
                    ReactionData_row_dct[MODLINEENDPOS].append(mod_lineend_pos)
                    ReactionData_row_dct[CENTERSIZE].append(center_size)
                    ReactionData_row_dct[SHAPENAME].append(reaction_shape_name)
                    ReactionData_row_dct[SHAPETYPE].append(reaction_shape_type)
                    ReactionData_row_dct[SHAPEINFO].append(reaction_shape_info)
                    ReactionData_row_dct[SRCDASH].append(src_dash)
                    ReactionData_row_dct[TGTDASH].append(dst_dash)
                    # for j in range(len(COLUMN_NAME_df_ReactionData)):
                    #     try: 
                    #         ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]] = ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]][0]
                    #     except:
                    #         ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]] = ''
                    # df_ReactionData = df_ReactionData.append(ReactionData_row_dct, ignore_index=True)
                    if len(df_ReactionData) == 0:
                        df_ReactionData = pd.DataFrame(ReactionData_row_dct)
                    else:
                        df_ReactionData = pd.concat([df_ReactionData,\
                            pd.DataFrame(ReactionData_row_dct)], ignore_index=True)

                except:
                    center_x = 0.
                    center_y = 0.
                    center_size = [0.,0.]

                    for j in range(rct_num):
                        center_x += src_position[j][0]+.5*src_dimension[j][0]
                        center_y += src_position[j][1]+.5*src_dimension[j][1]
                    for j in range(prd_num):
                        center_x += dst_position[j][0]+.5*dst_dimension[j][0]
                        center_y += dst_position[j][1]+.5*dst_dimension[j][1]
                    center_x = center_x/(rct_num + prd_num) 
                    center_y = center_y/(rct_num + prd_num)
                    center_position = [center_x, center_y]
                    handles = [center_position]
                    for j in range(rct_num):
                        src_handle_x = .5*(center_position[0] + src_position[j][0] + .5*src_dimension[j][0])
                        src_handle_y = .5*(center_position[1] + src_position[j][1] + .5*src_dimension[j][1])
                        handles.append([src_handle_x,src_handle_y])
                    for j in range(prd_num):
                        dst_handle_x = .5*(center_position[0] + dst_position[j][0] + .5*dst_dimension[j][0])
                        dst_handle_y = .5*(center_position[1] + dst_position[j][1] + .5*dst_dimension[j][1])
                        handles.append([dst_handle_x,dst_handle_y])

                    ReactionData_row_dct = {k:[] for k in COLUMN_NAME_df_ReactionData}
                    ReactionData_row_dct[NETIDX].append(netIdx)
                    ReactionData_row_dct[IDX].append(i)
                    ReactionData_row_dct[ID].append(temp_id)
                    ReactionData_row_dct[SOURCES].append(src_idx_list_corr)
                    ReactionData_row_dct[TARGETS].append(dst_idx_list_corr)
                    ReactionData_row_dct[RATELAW].append(kinetics)
                    ReactionData_row_dct[MODIFIERS].append(mod_idx_list)
                    ReactionData_row_dct[STROKECOLOR].append(reaction_line_color)
                    ReactionData_row_dct[LINETHICKNESS].append(reaction_line_width)
                    ReactionData_row_dct[CENTERPOS].append(center_position)
                    ReactionData_row_dct[HANDLES].append(handles)
                    if reactionLineType == 'bezier':
                        ReactionData_row_dct[BEZIER].append('TRUE')
                    else:
                        ReactionData_row_dct[BEZIER].append('FALSE')
                    ReactionData_row_dct[ARROWHEADSIZE].append(reaction_arrow_head_size)
                    ReactionData_row_dct[RXNDASH].append(reaction_dash)
                    ReactionData_row_dct[RXNREV].append(rxn_rev)
                    ReactionData_row_dct[FILLCOLOR].append(reaction_line_fill)
                    if src_endhead == []:
                        src_endhead = ["_line_ending_default_NONE_" + temp_id]
                        #default src endhead 
                        if ('_line_ending_default_NONE_' + temp_id) not in df_LineEndingData[ID].values:        
                            LineEndingData_row_dct = {k:[] for k in COLUMN_NAME_df_LineEndingData}
                            LineEndingData_row_dct[ID].append('_line_ending_default_NONE_' + temp_id)
                            LineEndingData_row_dct[POSITION].append([0.,0.])
                            LineEndingData_row_dct[SIZE].append([0.,0.])
                            LineEndingData_row_dct[FILLCOLOR].append(reaction_line_color)
                            LineEndingData_row_dct[SHAPETYPE].append([])
                            LineEndingData_row_dct[SHAPEINFO].append([])
                            LineEndingData_row_dct[BORDERCOLOR].append(reaction_line_color)
                            if len(df_LineEndingData) == 0:
                                df_LineEndingData = pd.DataFrame(LineEndingData_row_dct)
                            else:
                                df_LineEndingData = pd.concat([df_LineEndingData,\
                                    pd.DataFrame(LineEndingData_row_dct)], ignore_index=True)

                    ReactionData_row_dct[SOURCESLINEENDING].append(src_endhead)
                    if dst_endhead == []:
                        dst_endhead = ['line_ending_' + temp_id]
                        #default dst endhead
                        if ('line_ending_' + temp_id) not in df_LineEndingData[ID].values: 
                            LineEndingData_row_dct = {k:[] for k in COLUMN_NAME_df_LineEndingData}
                            LineEndingData_row_dct[ID].append('line_ending_' + temp_id)
                            LineEndingData_row_dct[POSITION].append([-reaction_arrow_head_size[0], -0.5*reaction_arrow_head_size[1]])
                            LineEndingData_row_dct[SIZE].append(reaction_arrow_head_size)
                            LineEndingData_row_dct[FILLCOLOR].append(reaction_line_color)
                            LineEndingData_row_dct[SHAPETYPE].append(['polygon'])
                            LineEndingData_row_dct[SHAPEINFO].append([[[0,0], [100,50], [0,100], [0,0]]])
                            LineEndingData_row_dct[BORDERCOLOR].append(reaction_line_color)
                            if len(df_LineEndingData) == 0:
                                df_LineEndingData = pd.DataFrame(LineEndingData_row_dct)
                            else:
                                df_LineEndingData = pd.concat([df_LineEndingData,\
                                    pd.DataFrame(LineEndingData_row_dct)], ignore_index=True)

                    ReactionData_row_dct[TARGETSLINEENDING].append(dst_endhead)
                    if mod_endhead != [] and len(mod_endhead) < len(mod_idx_list):
                        for j in range(len(mod_idx_list)-len(mod_endhead)):
                            mod_endhead.append(mod_endhead[0])
                    if mod_endhead == [] and len(mod_idx_list) != 0:
                        for j in range(len(mod_idx_list)):
                            mod_endhead.append('line_ending_modifier_'+temp_id+"_"+str(mod_idx_list[j]))
                        #default modifier endhead
                        for j in range(len(mod_idx_list)):
                            if ('line_ending_modifier_' + temp_id + '_' + str(mod_idx_list[j])) not in df_LineEndingData[ID].values: 
                                LineEndingData_row_dct = {k:[] for k in COLUMN_NAME_df_LineEndingData}
                                LineEndingData_row_dct[ID].append('line_ending_modifier_' + temp_id + '_' + str(mod_idx_list[j]))
                                LineEndingData_row_dct[POSITION].append([-1.*reaction_line_width, 0.])
                                LineEndingData_row_dct[SIZE].append([2.*reaction_line_width, 2.*reaction_line_width])
                                LineEndingData_row_dct[FILLCOLOR].append(reaction_line_color)
                                LineEndingData_row_dct[SHAPETYPE].append(['ellipse'])
                                LineEndingData_row_dct[SHAPEINFO].append([[[0.0, 0.0], [100.0, 100.0]]])
                                LineEndingData_row_dct[BORDERCOLOR].append(reaction_line_color)

                                if len(df_LineEndingData) == 0:
                                    df_LineEndingData = pd.DataFrame(LineEndingData_row_dct)
                                else:
                                    df_LineEndingData = pd.concat([df_LineEndingData,\
                                        pd.DataFrame(LineEndingData_row_dct)], ignore_index=True)

                    ReactionData_row_dct[MODIFIERSLINEENDING].append(mod_endhead)
                    ReactionData_row_dct[SRCLINEENDPOS].append(src_lineend_pos)
                    ReactionData_row_dct[TGTLINEENDPOS].append(dst_lineend_pos)
                    ReactionData_row_dct[MODLINEENDPOS].append(mod_lineend_pos)
                    ReactionData_row_dct[CENTERSIZE].append(center_size)
                    ReactionData_row_dct[SHAPENAME].append(reaction_shape_name)
                    ReactionData_row_dct[SHAPETYPE].append(reaction_shape_type)
                    ReactionData_row_dct[SHAPEINFO].append(reaction_shape_info)
                    ReactionData_row_dct[SRCDASH].append(src_dash)
                    ReactionData_row_dct[TGTDASH].append(dst_dash)
                    # for j in range(len(COLUMN_NAME_df_ReactionData)):
                    #     try: 
                    #         ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]] = ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]][0]
                    #     except:
                    #         ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]] = ''
                    # df_ReactionData = df_ReactionData.append(ReactionData_row_dct, ignore_index=True)
                    if len(df_ReactionData) == 0:
                        df_ReactionData = pd.DataFrame(ReactionData_row_dct)
                    else:
                        df_ReactionData = pd.concat([df_ReactionData,\
                            pd.DataFrame(ReactionData_row_dct)], ignore_index=True)


            #arbitrary text
            for i in range(len(textGlyph_id_list)):
                textGlyph = layout.getTextGlyph(textGlyph_id_list[i])
                #if not textGlyph.isSetOriginOfTextId() and not textGlyph.isSetGraphicalObjectId():
                textGlyph_id = textGlyph_id_list[i]
                text_content = text_content_list[i]
                position = text_position_list[i]
                dimension = text_dimension_list[i]
                for k in range(len(text_render)):
                    if textGlyph_id == text_render[k][0]:
                        text_line_color = text_render[k][1]
                        text_line_width = text_render[k][2]
                        text_font_size = text_render[k][3]
                        [text_anchor, text_vanchor] = text_render[k][4]
                        text_font_family = text_render[k][6]
                if len(text_render) == 1:
                    if text_render[0][0] == '':#global render
                        text_line_color = text_render[0][1]
                        text_line_width = text_render[0][2]
                        text_font_size = text_render[0][3]
                        [text_anchor, text_vanchor] = text_render[0][4]
                        text_font_family = text_render[0][6]
                TextData_row_dct = {k:[] for k in COLUMN_NAME_df_TextData}
                TextData_row_dct[TXTCONTENT].append(text_content)
                TextData_row_dct[TXTPOSITION].append(position)
                TextData_row_dct[TXTSIZE].append(dimension)
                TextData_row_dct[TXTFONTCOLOR].append(text_line_color)
                TextData_row_dct[TXTLINEWIDTH].append(text_line_width)
                TextData_row_dct[TXTFONTSIZE].append(text_font_size)
                TextData_row_dct[ID].append(textGlyph_id)
                TextData_row_dct[TXTANCHOR].append([text_anchor, text_vanchor])
                

                if len(df_TextData) == 0:
                    df_TextData = pd.DataFrame(TextData_row_dct)
                else:
                    df_TextData = pd.concat([df_TextData,\
                        pd.DataFrame(TextData_row_dct)], ignore_index=True)

            #arbitrary shape
            for i in range(len(gen_id_list)):
                genGlyph = layout.getGeneralGlyph(gen_id_list[i])
                genGlyph_id = gen_id_list[i]
                position = gen_position_list[i]
                dimension = gen_dimension_list[i]
                for k in range(len(gen_render)):
                    if genGlyph_id == gen_render[k][0]:
                        shape_fill_color = gen_render[k][1]
                        shape_border_color = gen_render[k][2]
                        shape_border_width = gen_render[k][3]
                        shape_type = gen_render[k][4]
                        shape_info = gen_render[k][5]
                ShapeData_row_dct = {k:[] for k in COLUMN_NAME_df_ShapeData}
                ShapeData_row_dct[SHAPENAME].append(genGlyph_id)
                ShapeData_row_dct[POSITION].append(position)
                ShapeData_row_dct[SIZE].append(dimension)
                ShapeData_row_dct[FILLCOLOR].append(shape_fill_color)
                ShapeData_row_dct[BORDERCOLOR].append(shape_border_color)
                ShapeData_row_dct[BORDERWIDTH].append(shape_border_width)
                ShapeData_row_dct[SHAPETYPE].append(shape_type)
                ShapeData_row_dct[SHAPEINFO].append(shape_info)

                if len(df_ShapeData) == 0:
                    df_ShapeData = pd.DataFrame(ShapeData_row_dct)
                else:
                    df_ShapeData = pd.concat([df_ShapeData,\
                        pd.DataFrame(ShapeData_row_dct)], ignore_index=True)
    
        
        else: # there is no layout information, assign position randomly and size as default
            comp_id_list = Comps_ids
            nodeIdx_temp = 0 #to track the node index

            for i in range(numComps):
                temp_id = Comps_ids[i]
                comp_idx_id_list.append([i,temp_id])
                vol= model.getCompartmentVolume(i)
                if math.isnan(vol):
                    vol = 1.
                dimension = compartmentDefaultSize
                position = [10.,10.]
                comp_border_color = [255, 255, 255, 255]
                comp_fill_color = [255, 255, 255, 255]
                text_content = ''
                text_position = [0.,0.]
                text_dimension = [0.,0.]
                comp_shape_name = ''
                comp_shape_type = ''
                comp_shape_info = []

                CompartmentData_row_dct = {k:[] for k in COLUMN_NAME_df_CompartmentData}
                CompartmentData_row_dct[NETIDX].append(netIdx)
                CompartmentData_row_dct[IDX].append(i)
                CompartmentData_row_dct[ID].append(temp_id)
                #CompartmentData_row_dct[VOLUMNE].append(vol)
                CompartmentData_row_dct[POSITION].append(position)
                CompartmentData_row_dct[SIZE].append(dimension)
                CompartmentData_row_dct[BORDERCOLOR].append(comp_border_color)
                CompartmentData_row_dct[FILLCOLOR].append(comp_fill_color)
                CompartmentData_row_dct[BORDERWIDTH].append(comp_border_width)
                CompartmentData_row_dct[TXTPOSITION].append(text_position)
                CompartmentData_row_dct[TXTSIZE].append(text_dimension)
                CompartmentData_row_dct[TXTCONTENT].append(text_content)
                CompartmentData_row_dct[TXTFONTCOLOR].append(text_line_color)
                CompartmentData_row_dct[TXTLINEWIDTH].append(text_line_width)
                CompartmentData_row_dct[TXTFONTSIZE].append(text_font_size)
                CompartmentData_row_dct[TXTANCHOR].append([text_anchor, text_vanchor])
                CompartmentData_row_dct[SHAPENAME].append(comp_shape_name)
                CompartmentData_row_dct[SHAPETYPE].append(comp_shape_type)
                CompartmentData_row_dct[SHAPEINFO].append(comp_shape_info)
                # for j in range(len(COLUMN_NAME_df_CompartmentData)):
                #     try: 
                #         CompartmentData_row_dct[COLUMN_NAME_df_CompartmentData[j]] = CompartmentData_row_dct[COLUMN_NAME_df_CompartmentData[j]][0]
                #     except:
                #         CompartmentData_row_dct[COLUMN_NAME_df_CompartmentData[j]] = ''
                # df_CompartmentData = df_CompartmentData.append(CompartmentData_row_dct, ignore_index=True)
                if len(df_CompartmentData) == 0:
                    df_CompartmentData = pd.DataFrame(CompartmentData_row_dct)
                else:
                    df_CompartmentData = pd.concat([df_CompartmentData,\
                        pd.DataFrame(CompartmentData_row_dct)], ignore_index=True)

            spec_id_list = [] 
            spec_dimension_list = []
            spec_position_list = []
            node_idx_specid_list = []
            for i in range (numFloatingNodes):
                temp_id = FloatingNodes_ids[i]
                try:
                    temp_concentration = model.getSpeciesInitialConcentration(temp_id)
                except:
                    temp_concentration = 1.0
                dimension = [60,40]
                position = [40 + math.trunc (_random.random()*800), 40 + math.trunc (_random.random()*800)]
                spec_id_list.append(temp_id)
                spec_dimension_list.append(dimension)
                spec_position_list.append(position)
                node_idx_specid_list.append([i,temp_id])
            for i in range (numBoundaryNodes):
                temp_id = BoundaryNodes_ids[i]
                try:
                    temp_concentration = model.getSpeciesInitialConcentration(temp_id)
                except:
                    temp_concentration = 1.0
                dimension = [60,40]
                position = [40 + math.trunc (_random.random()*800), 40 + math.trunc (_random.random()*800)]
                spec_id_list.append(temp_id)
                spec_dimension_list.append(dimension)
                spec_position_list.append(position)
                node_idx_specid_list.append([i+numFloatingNodes,temp_id])
            #print(node_idx_specid_list)

            for i in range (numFloatingNodes):
                temp_id = FloatingNodes_ids[i]
                text_content = temp_id
                comp_id = model.getCompartmentIdSpeciesIsIn(temp_id)
                temp_comp_idx = -1
                for j in range(len(comp_idx_id_list)):
                    if comp_idx_id_list[j][1] == comp_id:
                        temp_comp_idx = comp_idx_id_list[j][0]
                for k in range(numNodes):
                    if spec_id_list[k] == temp_id:
                        position = spec_position_list[k]
                        dimension = spec_dimension_list[k]

                NodeData_row_dct = {k:[] for k in COLUMN_NAME_df_NodeData}
                NodeData_row_dct[NETIDX].append(netIdx)
                NodeData_row_dct[COMPIDX].append(temp_comp_idx)
                NodeData_row_dct[IDX].append(i)
                NodeData_row_dct[ORIGINALIDX].append(-1)
                NodeData_row_dct[ID].append(temp_id)
                NodeData_row_dct[FLOATINGNODE].append('TRUE')
                NodeData_row_dct[CONCENTRATION].append(temp_concentration)
                NodeData_row_dct[POSITION].append(position)
                NodeData_row_dct[SIZE].append(dimension)
                NodeData_row_dct[SHAPEIDX].append(shapeIdx)
                NodeData_row_dct[TXTPOSITION].append(position)
                NodeData_row_dct[TXTSIZE].append(dimension)
                NodeData_row_dct[FILLCOLOR].append(spec_fill_color)
                NodeData_row_dct[BORDERCOLOR].append(spec_border_color)
                NodeData_row_dct[BORDERWIDTH].append(spec_border_width)
                NodeData_row_dct[TXTFONTCOLOR].append(text_line_color)
                NodeData_row_dct[TXTLINEWIDTH].append(text_line_width)
                NodeData_row_dct[TXTFONTSIZE].append(text_font_size)
                NodeData_row_dct[SHAPENAME].append(shape_name)
                NodeData_row_dct[SHAPETYPE].append(shape_type)
                NodeData_row_dct[SHAPEINFO].append(shape_info)
                NodeData_row_dct[TXTCONTENT].append(text_content)
                NodeData_row_dct[TXTANCHOR].append([text_anchor, text_vanchor])
                NodeData_row_dct[SPECDASH].append(spec_dash)
                NodeData_row_dct[TXTFONTFAMILY].append(text_font_family)
                # for j in range(len(COLUMN_NAME_df_NodeData)):
                #     try: 
                #         NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = NodeData_row_dct[COLUMN_NAME_df_NodeData[j]][0]
                #     except:
                #         NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = ''
                # df_NodeData = df_NodeData.append(NodeData_row_dct, ignore_index=True)
                
                if len(df_NodeData) == 0:
                    df_NodeData = pd.DataFrame(NodeData_row_dct)
                else:
                    df_NodeData = pd.concat([df_NodeData,\
                        pd.DataFrame(NodeData_row_dct)], ignore_index=True)
            for i in range (numBoundaryNodes):
                temp_id = BoundaryNodes_ids[i]
                text_content = temp_id
                comp_id = model.getCompartmentIdSpeciesIsIn(temp_id)
                temp_comp_idx = -1
                for j in range(len(comp_idx_id_list)):
                    if comp_idx_id_list[j][1] == comp_id:
                        temp_comp_idx = comp_idx_id_list[j][0]
                for k in range(numNodes):
                    if spec_id_list[k] == temp_id:
                        position = spec_position_list[k]
                        dimension = spec_dimension_list[k]

                
                NodeData_row_dct = {k:[] for k in COLUMN_NAME_df_NodeData}
                NodeData_row_dct[NETIDX].append(netIdx)
                NodeData_row_dct[COMPIDX].append(temp_comp_idx)
                NodeData_row_dct[IDX].append(numFloatingNodes + i)
                NodeData_row_dct[ORIGINALIDX].append(-1)
                NodeData_row_dct[ID].append(temp_id)
                NodeData_row_dct[FLOATINGNODE].append('FALSE')
                NodeData_row_dct[CONCENTRATION].append(temp_concentration)
                NodeData_row_dct[POSITION].append(position)
                NodeData_row_dct[SIZE].append(dimension)
                NodeData_row_dct[SHAPEIDX].append(shapeIdx)
                NodeData_row_dct[TXTPOSITION].append(position)
                NodeData_row_dct[TXTSIZE].append(dimension)
                NodeData_row_dct[FILLCOLOR].append(spec_fill_color)
                NodeData_row_dct[BORDERCOLOR].append(spec_border_color)
                NodeData_row_dct[BORDERWIDTH].append(spec_border_width)
                NodeData_row_dct[TXTFONTCOLOR].append(text_line_color)
                NodeData_row_dct[TXTLINEWIDTH].append(text_line_width)
                NodeData_row_dct[TXTFONTSIZE].append(text_font_size)
                NodeData_row_dct[SHAPENAME].append(shape_name)
                NodeData_row_dct[SHAPETYPE].append(shape_type)
                NodeData_row_dct[SHAPEINFO].append(shape_info)
                NodeData_row_dct[TXTCONTENT].append(text_content)
                NodeData_row_dct[TXTANCHOR].append([text_anchor, text_vanchor])
                NodeData_row_dct[SPECDASH].append(spec_dash)
                NodeData_row_dct[TXTFONTFAMILY].append(text_font_family)
                # for j in range(len(COLUMN_NAME_df_NodeData)):
                #     try: 
                #         NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = NodeData_row_dct[COLUMN_NAME_df_NodeData[j]][0]
                #     except:
                #         NodeData_row_dct[COLUMN_NAME_df_NodeData[j]] = ''
                # df_NodeData = df_NodeData.append(NodeData_row_dct, ignore_index=True)
                if len(df_NodeData) == 0:
                    df_NodeData = pd.DataFrame(NodeData_row_dct)
                else:
                    df_NodeData = pd.concat([df_NodeData,\
                        pd.DataFrame(NodeData_row_dct)], ignore_index=True)
    
            for i in range (numRxns):
                src_idx_list = []
                dst_idx_list = []
                mod_idx_list = []
                src_position = []
                dst_position = []
                mod_position = []
                src_dimension = []
                dst_dimension = []
                mod_dimension = []
                src_endhead = []
                dst_endhead = []
                mod_endhead = []
                src_lineend_pos = []
                dst_lineend_pos = []
                mod_lineend_pos = []
                src_dash = []
                dst_dash = []
                temp_id = Rxns_ids[i]
                reaction = model_layout.getReaction(temp_id)
                rxn_rev = reaction.getReversible()
                try: 
                    kinetics = model.getRateLaw(i)
                except:
                    kinetics = ""
                rct_num = model.getNumReactants(i)
                prd_num = model.getNumProducts(i)
                mod_num = model.getNumModifiers(temp_id)
                for j in range(rct_num):
                    rct_id = model.getReactant(temp_id,j)
                    for k in range(len(node_idx_specid_list)):
                        if node_idx_specid_list[k][1] == rct_id:
                            src_idx_list.append(node_idx_specid_list[k][0])
                    for k in range(numNodes):
                        if spec_id_list[k] == rct_id:
                            src_position.append(spec_position_list[k])
                            src_dimension.append(spec_dimension_list[k])
                src_idx_list_corr = []
                [src_idx_list_corr.append(x) for x in src_idx_list if x not in src_idx_list_corr]

                for j in range(prd_num):
                    prd_id = model.getProduct(temp_id,j)
                    for k in range(len(node_idx_specid_list)):
                        if node_idx_specid_list[k][1] == prd_id:
                            dst_idx_list.append(node_idx_specid_list[k][0])
                    for k in range(numNodes):
                        if spec_id_list[k] == prd_id:
                            dst_position.append(spec_position_list[k])
                            dst_dimension.append(spec_dimension_list[k])  
                dst_idx_list_corr = []
                [dst_idx_list_corr.append(x) for x in dst_idx_list if x not in dst_idx_list_corr]

                modifiers = model.getListOfModifiers(temp_id)
                for j in range(mod_num):
                    mod_id = modifiers[j]
                    for k in range(len(node_idx_specid_list)):
                        if node_idx_specid_list[k][1] == mod_id:
                            mod_idx_list.append(node_idx_specid_list[k][0])
                    for k in range(numNodes):
                        if spec_id_list[k] == mod_id:
                            mod_position.append(spec_position_list[k])
                            mod_dimension.append(spec_dimension_list[k])
                
                center_x = 0.
                center_y = 0.
                center_size = [0.,0.]

                for j in range(rct_num):
                    center_x += src_position[j][0]+.5*src_dimension[j][0]
                    center_y += src_position[j][1]+.5*src_dimension[j][1]
                for j in range(prd_num):
                    center_x += dst_position[j][0]+.5*dst_dimension[j][0]
                    center_y += dst_position[j][1]+.5*dst_dimension[j][1]
                center_x = center_x/(rct_num + prd_num) 
                center_y = center_y/(rct_num + prd_num)
                center_position = [center_x, center_y]
                handles = [center_position]
                for j in range(rct_num):
                    src_handle_x = .5*(center_position[0] + src_position[j][0] + .5*src_dimension[j][0])
                    src_handle_y = .5*(center_position[1] + src_position[j][1] + .5*src_dimension[j][1])
                    handles.append([src_handle_x,src_handle_y])
                for j in range(prd_num):
                    dst_handle_x = .5*(center_position[0] + dst_position[j][0] + .5*dst_dimension[j][0])
                    dst_handle_y = .5*(center_position[1] + dst_position[j][1] + .5*dst_dimension[j][1])
                    handles.append([dst_handle_x,dst_handle_y])
                
                ReactionData_row_dct = {k:[] for k in COLUMN_NAME_df_ReactionData}
                ReactionData_row_dct[NETIDX].append(netIdx)
                ReactionData_row_dct[IDX].append(i)
                ReactionData_row_dct[ID].append(temp_id)
                ReactionData_row_dct[SOURCES].append(src_idx_list_corr)
                ReactionData_row_dct[TARGETS].append(dst_idx_list_corr)
                ReactionData_row_dct[RATELAW].append(kinetics)
                ReactionData_row_dct[MODIFIERS].append(mod_idx_list)
                ReactionData_row_dct[STROKECOLOR].append(reaction_line_color)
                ReactionData_row_dct[LINETHICKNESS].append(reaction_line_width)
                ReactionData_row_dct[CENTERPOS].append(center_position)
                ReactionData_row_dct[HANDLES].append(handles)
                if reactionLineType == 'bezier':
                    ReactionData_row_dct[BEZIER].append('TRUE')
                else:
                    ReactionData_row_dct[BEZIER].append('FALSE')
                ReactionData_row_dct[ARROWHEADSIZE].append(reaction_arrow_head_size)
                ReactionData_row_dct[RXNDASH].append(reaction_dash)
                ReactionData_row_dct[RXNREV].append(rxn_rev)
                ReactionData_row_dct[FILLCOLOR].append(reaction_line_fill)
                if src_endhead == []:
                    src_endhead = ["_line_ending_default_NONE_" + temp_id]
                    #default src endhead 
                    if ('_line_ending_default_NONE_' + temp_id) not in df_LineEndingData[ID].values:        
                        LineEndingData_row_dct = {k:[] for k in COLUMN_NAME_df_LineEndingData}
                        LineEndingData_row_dct[ID].append('_line_ending_default_NONE_' + temp_id)
                        LineEndingData_row_dct[POSITION].append([0.,0.])
                        LineEndingData_row_dct[SIZE].append([0.,0.])
                        LineEndingData_row_dct[FILLCOLOR].append(reaction_line_color)
                        LineEndingData_row_dct[SHAPETYPE].append([])
                        LineEndingData_row_dct[SHAPEINFO].append([])
                        LineEndingData_row_dct[BORDERCOLOR].append(reaction_line_color)
                        if len(df_LineEndingData) == 0:
                            df_LineEndingData = pd.DataFrame(LineEndingData_row_dct)
                        else:
                            df_LineEndingData = pd.concat([df_LineEndingData,\
                                pd.DataFrame(LineEndingData_row_dct)], ignore_index=True)

                ReactionData_row_dct[SOURCESLINEENDING].append(src_endhead)
                if dst_endhead == []:
                    dst_endhead = ['line_ending_' + temp_id]
                    #default dst endhead
                    if ('line_ending_' + temp_id) not in df_LineEndingData[ID].values: 
                        LineEndingData_row_dct = {k:[] for k in COLUMN_NAME_df_LineEndingData}
                        LineEndingData_row_dct[ID].append('line_ending_' + temp_id)
                        LineEndingData_row_dct[POSITION].append([-reaction_arrow_head_size[0], -0.5*reaction_arrow_head_size[1]])
                        LineEndingData_row_dct[SIZE].append(reaction_arrow_head_size)
                        LineEndingData_row_dct[FILLCOLOR].append(reaction_line_color)
                        LineEndingData_row_dct[SHAPETYPE].append(['polygon'])
                        LineEndingData_row_dct[SHAPEINFO].append([[[0,0], [100,50], [0,100], [0,0]]])
                        LineEndingData_row_dct[BORDERCOLOR].append(reaction_line_color)
                        if len(df_LineEndingData) == 0:
                            df_LineEndingData = pd.DataFrame(LineEndingData_row_dct)
                        else:
                            df_LineEndingData = pd.concat([df_LineEndingData,\
                                pd.DataFrame(LineEndingData_row_dct)], ignore_index=True)

                ReactionData_row_dct[TARGETSLINEENDING].append(dst_endhead)
                if mod_endhead == [] and len(mod_idx_list) != 0:
                    for j in range(len(mod_idx_list)):
                        mod_endhead.append('line_ending_modifier_'+temp_id+"_"+str(mod_idx_list[j]))
                    #default modifier endhead
                    for j in range(len(mod_idx_list)):
                        if ('line_ending_modifier_' + temp_id + '_' + str(mod_idx_list[j])) not in df_LineEndingData[ID].values: 
                            LineEndingData_row_dct = {k:[] for k in COLUMN_NAME_df_LineEndingData}
                            LineEndingData_row_dct[ID].append('line_ending_modifier_' + temp_id + '_' + str(mod_idx_list[j]))
                            LineEndingData_row_dct[POSITION].append([-1.*reaction_line_width, 0.])
                            LineEndingData_row_dct[SIZE].append([2.*reaction_line_width, 2.*reaction_line_width])
                            LineEndingData_row_dct[FILLCOLOR].append(reaction_line_color)
                            LineEndingData_row_dct[SHAPETYPE].append(['ellipse'])
                            LineEndingData_row_dct[SHAPEINFO].append([[[0.0, 0.0], [100.0, 100.0]]])
                            LineEndingData_row_dct[BORDERCOLOR].append(reaction_line_color)
                            if len(df_LineEndingData) == 0:
                                df_LineEndingData = pd.DataFrame(LineEndingData_row_dct)
                            else:
                                df_LineEndingData = pd.concat([df_LineEndingData,\
                                    pd.DataFrame(LineEndingData_row_dct)], ignore_index=True)

                ReactionData_row_dct[MODIFIERSLINEENDING].append(mod_endhead)
                ReactionData_row_dct[SRCLINEENDPOS].append(src_lineend_pos)
                ReactionData_row_dct[TGTLINEENDPOS].append(dst_lineend_pos)
                ReactionData_row_dct[MODLINEENDPOS].append(mod_lineend_pos)
                ReactionData_row_dct[CENTERSIZE].append(center_size)
                ReactionData_row_dct[SHAPENAME].append(reaction_shape_name)
                ReactionData_row_dct[SHAPETYPE].append(reaction_shape_type)
                ReactionData_row_dct[SHAPEINFO].append(reaction_shape_info)
                ReactionData_row_dct[SRCDASH].append(src_dash)
                ReactionData_row_dct[TGTDASH].append(dst_dash)
                # for j in range(len(COLUMN_NAME_df_ReactionData)):
                #     try: 
                #         ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]] = ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]][0]
                #     except:
                #         ReactionData_row_dct[COLUMN_NAME_df_ReactionData[j]] = ''
                # df_ReactionData = df_ReactionData.append(ReactionData_row_dct, ignore_index=True)
                if len(df_ReactionData) == 0:
                    df_ReactionData = pd.DataFrame(ReactionData_row_dct)
                else:
                    df_ReactionData = pd.concat([df_ReactionData,\
                        pd.DataFrame(ReactionData_row_dct)], ignore_index=True)


        #return (df_CompartmentData, df_NodeData, df_ReactionData, df_TextData) 
        return (df_CompartmentData, df_NodeData, df_ReactionData, df_TextData, df_ShapeData, 
        df_LineEndingData, df_ReactionTextData) 

    except:
       raise ValueError('Invalid SBML!')

    # except Exception as e:
    #     raise Exception (e)  


class load:
    """
    Load SBML string for further processing, i.e. read, edit, visualize the SBML string or
    export it as an updated SBML string.

    Args: 
        sbmlstr: str-the SBML string.

    """

    def __init__(self, sbmlstr):

        # self.sbmlstr = sbmlstr
        # self.df = _SBMLToDF(self.sbmlstr)
        # self.color_style = styleSBML.Style()
        # self.df_text = pd.DataFrame(columns = COLUMN_NAME_df_text)
        # if self.df == None:
        #    sys.exit("There is no valid information to process.")

        if os.path.isfile(sbmlstr):
            with open(sbmlstr) as f:
                self.sbmlstr = f.read()
        else:  
            self.sbmlstr = sbmlstr

        try:
          if not self.sbmlstr.startswith('<?xml'):
              raise Exception (sbmlstr + ' is not a valid sbml model')

          self.df = _SBMLToDF(self.sbmlstr)
          self.color_style = styleSBML.Style()    
          #self.df_text = pd.DataFrame(columns = COLUMN_NAME_df_text)
        except Exception as err:
            raise Exception (err)


    def getCompartmentPosition(self, id):
        """
        Get the position of a compartment with given compartment id.

        Args: 
            id: str-the id of the compartment.

        Returns:
            position: a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the compartment.  

        Examples: 
            p = sd.getCompartmentPosition('compartment_id')

            print ('x = ', p.x, 'y = ', p.y)         

        """

        p = visualizeSBML._getCompartmentPosition(self.df, id)
        num_alias = len(p)
        position_list = []
        for alias in range(num_alias):
            position = point.Point (p[alias][0], p[alias][1])
            position_list.append(position)
        if len(position_list) == 1:
            position = position_list[0]
        else:
            raise Exception("This is not a valid id.")
        return position

    def getCompartmentSize(self, id):
        """
        Get the size of a compartment with given compartment id.

        Args: 
            id: str-the id of the compartment.

        Returns:
            size: a Point object with attributes x and y representing
            the width and height of the compartment.

        Examples: 
            p = sd.getCompartmentSize('compartment_id')
            
            print ('Width = ', p.x, 'Height = ', p.y)

        """

        p = visualizeSBML._getCompartmentSize (self.df, id)
        num_alias = len(p)
        size_list = []
        for alias in range(num_alias):
            size = point.Point (p[alias][0], p[alias][1])
            size_list.append(size)
        if len(size_list) == 1:
            size = size_list[0]
        else:
            raise Exception("This is not a valid id.")
        return size

    def getCompartmentFillColor(self, id):
        """
        Get the fill color for a compartment with given compartment id.

        Args: 
            id: str-the id of the compartment.

        Returns:
            fill_color: list-[rgba 1*4 matrix, html_name str (if any, otherwise ''), 
            hex str (8 digits)].
        """
        idx_list = self.df[0].index[self.df[0]["id"] == id].tolist() #row index
        fill_color_list =[] 
        for i in range(len(idx_list)):
            rgb = self.df[0].iloc[idx_list[i]]["fill_color"]
            color = _rgb_to_color(rgb)
            fill_color_list.append(color)
        
        if len(fill_color_list) == 1:
            fill_color = fill_color_list[0]
        else:
            raise Exception("This is not a valid id.")
        return fill_color

    def getCompartmentBorderColor(self, id):
        """
        Get the border color of a compartment with a given compartment id.

        Args: 
            id: str-the id of the compartment.

        Returns:
            border_color: list-[rgba 1*4 matrix, html_name str (if any, otherwise ''), 
            hex str (8 digits)].

        """
        idx_list = self.df[0].index[self.df[0]["id"] == id].tolist()
        border_color_list =[] 
        for i in range(len(idx_list)):
            rgb = self.df[0].iloc[idx_list[i]]["border_color"]
            color = _rgb_to_color(rgb)
            border_color_list.append(color)

        if len(border_color_list) == 1:
            border_color = border_color_list[0]
        else:
            raise Exception("This is not a valid id.")
        return border_color

    def getCompartmentBorderWidth(self, id):
        """
        Get the border width of a compartment with a given compartment id.

        Args: 
            id: str-the id of the compartment.

        Returns:
            border_width: float-compartment border line width.

        """
        
        idx_list = self.df[0].index[self.df[0]["id"] == id].tolist()
        border_width_list =[] 
        for i in range(len(idx_list)):
            border_width_list.append(self.df[0].iloc[idx_list[i]]["border_width"])

        if len(border_width_list) == 1:
            border_width = border_width_list[0]
        else:
            raise Exception("This is not a valid id.")
        return border_width


    def getCompartmentTextPosition(self, id):
        """
        Get the text position of a compartment with given compartment id.

        Args: 
            id: str-the id of the compartment.

        Returns:
            position: a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the compartment.  

        Examples: 
            p = sd.getCompartmentTextPosition('compartment_id')

            print ('x = ', p.x, 'y = ', p.y)         

        """

        p = visualizeSBML._getCompartmentTextPosition(self.df, id)
        num_alias = len(p)
        position_list = []
        for alias in range(num_alias):
            position = point.Point (p[alias][0], p[alias][1])
            position_list.append(position)
        if len(position_list) == 1:
            position = position_list[0]
        else:
            raise Exception("This is not a valid id.")
        return position

    def getCompartmentTextSize(self, id):
        """
        Get the text size of a compartment with given compartment id.

        Args: 
            id: str-the id of the compartment.

        Returns:
            size: a Point object with attributes x and y representing
            the width and height of the compartment.

        Examples: 
            p = sd.getCompartmentTextSize('compartment_id')
            
            print ('Width = ', p.x, 'Height = ', p.y)

        """

        p = visualizeSBML._getCompartmentTextSize (self.df, id)
        num_alias = len(p)
        size_list = []
        for alias in range(num_alias):
            size = point.Point (p[alias][0], p[alias][1])
            size_list.append(size)
        if len(size_list) == 1:
            size = size_list[0]
        else:
            raise Exception("This is not a valid id.")
        return size

    def getCompartmentTextContent(self, id):
        """
        Get the text content of a compartment with a given compartment id.

        Args: 
            id: str-the id of the compartment.

        Returns:
            txt_content: str-the content of the compartment text.
        """

        idx_list = self.df[0].index[self.df[0]["id"] == id].tolist()
        txt_content_list =[] 
        for i in range(len(idx_list)):
            content = self.df[0].iloc[idx_list[i]]["txt_content"]
            txt_content_list.append(content)
        if len(txt_content_list) == 1:
            txt_content =  txt_content_list[0]
        else:
            raise Exception("This is not a valid id.")
        
        return txt_content

    def getCompartmentTextFontColor(self, id):
        """
        Get the text font color of a compartment with a given compartment id.

        Args: 
            id: str-the id of the compartment.

        Returns:
            txt_font_color: list-[rgba 1*4 matrix, html_name str (if any, otherwise ''), 
            hex str (8 digits)].

        """

        idx_list = self.df[0].index[self.df[0]["id"] == id].tolist()
        txt_font_color_list =[] 
        for i in range(len(idx_list)):
            rgb = self.df[0].iloc[idx_list[i]]["txt_font_color"]
            color = _rgb_to_color(rgb)
            txt_font_color_list.append(color)
        if len(txt_font_color_list) == 1:
            txt_font_color = txt_font_color_list[0]
        else:
            raise Exception("This is not a valid id.")

        return txt_font_color

    def getCompartmentTextLineWidth(self, id):
        """
        Get the text line width of a compartment with a given compartment id.

        Args: 
            id: int-the id of the compartment.

        Returns:
            txt_line_width: float-compartment text line width.

        """
        idx_list = self.df[0].index[self.df[0]["id"] == id].tolist()
        txt_line_width_list =[] 
        for i in range(len(idx_list)):
            txt_line_width_list.append(self.df[0].iloc[idx_list[i]]["txt_line_width"])
        if len(txt_line_width_list) == 1:
            txt_line_width =  txt_line_width_list[0]
        else:
            raise Exception("This is not a valid id.")

        return txt_line_width

    def getCompartmentTextFontSize(self, id):
        """
        Get the text font size of a compartment with a given compartment id.

        Args: 
            id: str-the id of the compartment.

        Returns:
            txt_font_size: float.

        """
        idx_list = self.df[0].index[self.df[0]["id"] == id].tolist()
        txt_font_size_list =[] 
        for i in range(len(idx_list)):
            txt_font_size_list.append(float(self.df[0].iloc[idx_list[i]]["txt_font_size"]))
        if len(txt_font_size_list) == 1:
            txt_font_size =  txt_font_size_list[0]
        else:
            raise Exception("This is not a valid id.")
            
        return txt_font_size

    def getCompartmentTextAnchor(self, id):
        """
        Get the horizontal anchor of a compartment text with a given compartment id.

        Args: 
            id: str-the id of the compartment.

        Returns:
            txt_anchor: str-the horizantal anchor of the compartment text, which can be "start",
            "middle" and "end".
        """

        idx_list = self.df[0].index[self.df[0]["id"] == id].tolist()
        txt_anchor_list =[] 
        for i in range(len(idx_list)):
            anchor = self.df[0].iloc[idx_list[i]]["txt_anchor"][0]
            txt_anchor_list.append(anchor)
        if len(txt_anchor_list) == 1:
            txt_anchor =  txt_anchor_list[0]
        else:
            raise Exception("This is not a valid id.")

        return txt_anchor

    def getCompartmentTextVAnchor(self, id):
        """
        Get the vertical anchor of a compartment text with a given compartment id.

        Args: 
            id: str-the id of the compartment.

        Returns:
            txt_anchor: str-the vertical anchor of the compartment text, which can be "top", 
            "middle", "baseline" and "bottom".
        """

        idx_list = self.df[0].index[self.df[0]["id"] == id].tolist()
        txt_anchor_list =[] 
        for i in range(len(idx_list)):
            anchor = self.df[0].iloc[idx_list[i]]["txt_anchor"][1]
            txt_anchor_list.append(anchor)
        if len(txt_anchor_list) == 1:
            txt_vanchor =  txt_anchor_list[0]
        else:
            raise Exception("This is not a valid id.")

        return txt_vanchor

    def getNodeAliasNum(self, id):
        """
        Get the number of alias nodes with a given node id.

        Args: 
            id: str-the id of the node.

        Returns:
            num_alias: int-the number of alias nodes with the given node id.            

        """

        p = visualizeSBML._getNodePosition(self.df, id)
        num_alias = len(p)
        return num_alias

    def isFloatingNode(self, id, alias = 0):
        """
        Returns True if the given node is a floating node.

        Args: 
            id: str-the id of the node.
            
            alias: int-alias node index: 0 to number of alias nodes -1.

        Returns:
            floating_node: bool-floating node (True) or not (False).

        """
        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        floating_node_list =[] 
        if len(idx_list) == 0:
            raise Exception("This is not a valid id.")
        for i in range(len(idx_list)):
            floating_node_list.append(bool(self.df[1].iloc[idx_list[i]]["floating_node"]))
        if alias < len(idx_list) and alias >= 0:
            floating_node = floating_node_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")
        return floating_node


    def getNodePosition(self, id, alias = 0):
        """
        Get the position of a node with a given node id.

        Args: 
            id: str-the id of the node.
            
            alias: int-alias node index: 0 to number of alias nodes -1.

        Returns:
            position: a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the node.

        Examples: 
            p = sd.getNodePosition('ATP')
            
            print('x = ', p.x, 'y = ', p.y)            

        """

        p = visualizeSBML._getNodePosition(self.df, id)
        num_alias = len(p)
        position_list = []
        for i in range(num_alias):
            position = point.Point (p[i][0], p[i][1])
            position_list.append(position)
        if len(position_list) == 0:
            raise Exception("This is not a valid id.")
        if alias < len(position_list) and alias >= 0:
            position = position_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")
        
        return position


    def getNodeCenter(self, id, alias = 0):
        """
        Get the center point of a node with a given node id.

        Args: 
            id: str-the id of the node.
            
            alias: int-alias node index: 0 to number of alias nodes -1.

        Returns:
            position-a Point object with x and y coordinates of the center of the node.
           
        Examples:
            p = sd.getNodeCenter('ATP')
                
            print(p.x, p.y)

        """   
        if not (id in self.getNodeIdList()):
            raise Exception("No such node found in model: " + id)
            
        p = visualizeSBML._getNodePosition(self.df, id) 
        size = visualizeSBML._getNodeSize(self.df, id)
        num_alias = len(p)
        position_list = []
        for i in range(num_alias):
            cx = p[i][0] + size[i][0]/2
            cy = p[i][1] + size[i][1]/2
            position = point.Point(cx, cy) 
            position_list.append(position)
        if len(position_list) == 0:
            raise Exception("This is not a valid id.")
        if alias < len(position_list) and alias >= 0:
            position = position_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")
        
        return position
        

    def getNodeSize(self, id, alias = 0):
        """
        Get the size of a node with a given node id.

        Args: 
            id: str-the id of the node.
            
            alias: int-alias node index: 0 to number of alias nodes -1.

        Returns:
            size: a Point object with attributes x and y representing
            the width and height of the node.

        Examples: 
            p = sd.getNodeSize('ATP')
            
            print ('Width = ', p.x, 'Height = ', p.y)

        """

        p = visualizeSBML._getNodeSize (self.df, id)
        num_alias = len(p)
        size_list = []
        for i in range(num_alias):
            size = point.Point (p[i][0], p[i][1])
            size_list.append(size)
        if len(size_list) == 0:
            raise Exception("This is not a valid id.")
        if alias < len(size_list) and alias >= 0:
            size =  size_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias nodes.")
        
        return size

    def getNodeShape(self, id, alias = 0):
        """
        Get the shape index and the shape of a node with a given node id.

        Args: 
            id: str-the id of the node.
            
            alias: int-alias node index: 0 to number of alias nodes -1.

        Returns:
            shape: tuple (shape_name, vertex_positions)
            
            shape_name: str-the name of the node shape.

            vertex_positions: list-the vertex positions if any. 

        """

        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        vertex = []
        shape_list =[] 
        for i in range(len(idx_list)):
            shape_name = self.df[1].iloc[idx_list[i]]["shape_name"]
            shape_type = self.df[1].iloc[idx_list[i]]["shape_type"]
            shape_info = self.df[1].iloc[idx_list[i]]["shape_info"]
            node_position = self.df[1].iloc[idx_list[i]]["position"]
            node_size = self.df[1].iloc[idx_list[i]]["size"]
            if shape_type == "rectangle":
                vertex = [node_position,[node_position[0]+node_size[0],node_position[1]],
                [node_position[0]+node_size[0],node_position[1]+node_size[1]],
                [node_position[0],node_position[1]+node_size[1]]]
            elif shape_type == "polygon":
                for j in range(len(shape_info)):
                    vertex_x = node_position[0]+node_size[0]*shape_info[j][0]/100.
                    vertex_y = node_position[1]+node_size[1]*shape_info[j][1]/100.
                    vertex.append([vertex_x,vertex_y])         

            shape_list.append((shape_name, vertex))
        if len(shape_list) == 0:
            raise Exception("This is not a valid id.")
        if alias < len(shape_list) and alias >= 0:
            shape =  shape_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")
        return shape


    def getNodeTextPosition(self, id, alias = 0):
        """
        Get the text position of a node with a given node id.

        Args: 
            id: str-the id of node.
            
            alias: int-alias node index: 0 to number of alias nodes -1.

        Returns:
            txt_position: a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the node text.

        Examples: 
            p = sd.getNodeTextPosition('ATP')

            print ('x = ', p.x, 'y = ', p.y)            

        """

        p = visualizeSBML._getNodeTextPosition(self.df, id)
        num_alias = len(p)
        txt_position_list = []
        for i in range(num_alias):
            txt_position = point.Point (p[i][0], p[i][1])
            txt_position_list.append(txt_position)
        if len(txt_position_list) == 0:
            raise Exception("This is not a valid id.")
        if alias < len(txt_position_list) and alias >= 0:
            txt_position =  txt_position_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")

        return txt_position

        
    def getNodeTextSize(self, id, alias = 0):
        """
        Get the text size of a node with a given node id.

        Args: 
            id: str-the id of the node.

            alias: int-alias node index: 0 to number of alias nodes -1.

        Returns:
            size: a Point object with attributes x and y representing
            the width and height of the node text.

        Examples:
            p = sd.getNodeTextSize('ATP')

            print ('Width = ', p.x, 'Height = ', p.y)          

        """

        p = visualizeSBML._getNodeTextSize(self.df, id)
        num_alias = len(p)
        txt_size_list = []
        for i in range(num_alias):
            txt_size = point.Point (p[i][0], p[i][1])
            txt_size_list.append(txt_size)
        if len(txt_size_list) == 0:
            raise Exception("This is not a valid id.")
        if alias < len(txt_size_list) and alias >= 0:
            txt_size =  txt_size_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")

        return txt_size


    def getNodeFillColor(self, id, alias = 0):
        """
        Get the fill color of a node with a given node id.

        Args: 
            id: str-the id of the node.

            alias: int-alias node index: 0 to number of alias nodes -1.

        Returns:
            fill_color: list-[rgba 1*4 matrix, html_name str (if any, otherwise ''), 
            hex str (8 digits)]; 
            
            or list-[str-gradient_type, list-gradient_info, list-stop_info],
            where gradient_type can be 'linearGradient' or 'radialGradient', while gradient_info
            and stop_info refers to setNodeFillLinearGradient() and setNodeFillRadialGradient.

        """

        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        fill_color_list =[] 
        for i in range(len(idx_list)):
            rgb = self.df[1].iloc[idx_list[i]]["fill_color"]
            if type(rgb[0]) == str:
                color = rgb
            else:
                color = _rgb_to_color(rgb)
            fill_color_list.append(color)
        if len(fill_color_list) == 0:
            raise Exception("This is not a valid id.")
        if alias < len(fill_color_list) and alias >= 0:
            fill_color = fill_color_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")
        return fill_color


    def getNodeBorderColor(self, id, alias = 0):
        """
        Get the border color of a node with a given node id.

        Args: 
            id: str-the id of the node.
            
            alias: int-alias node index: 0 to number of alias nodes -1.

        Returns:
            border_color: list-[rgba 1*4 matrix, html_name str (if any, otherwise ''), 
            hex str (8 digits)].

        """

        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        border_color_list =[] 
        for i in range(len(idx_list)):
            rgb = self.df[1].iloc[idx_list[i]]["border_color"]
            color = _rgb_to_color(rgb)
            border_color_list.append(color)
        if len(border_color_list) == 0:
            raise Exception("This is not a valid id.")
        if alias < len(border_color_list) and alias >= 0:
            border_color =  border_color_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")

        return border_color


    def getNodeBorderWidth(self, id, alias = 0):
        """
        Get the border width of a node with a given node id.

        Args: 
            id: str-the id of the node.
            
            alias: int-alias node index: 0 to number of alias nodes -1.

        Returns:
            border_width: float-node border line width.

        """
        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        border_width_list =[] 
        for i in range(len(idx_list)):
            border_width_list.append(self.df[1].iloc[idx_list[i]]["border_width"])
        if len(border_width_list) == 0:
            raise Exception("This is not a valid id.")
        if alias < len(border_width_list) and alias >= 0:
            border_width =  border_width_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")

        return border_width

    def getNodeTextContent(self, id, alias = 0):
        """
        Get the text content of a node with a given node id.

        Args: 
            id: str-the id of the node.

            alias: int-alias node index: 0 to number of alias nodes -1.

        Returns:
            txt_content: str-the content of the node text.
        """

        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        txt_content_list =[] 
        for i in range(len(idx_list)):
            content = self.df[1].iloc[idx_list[i]]["txt_content"]
            txt_content_list.append(content)
        if len(txt_content_list) == 0:
            raise Exception("This is not a valid id.")

        if alias < len(txt_content_list) and alias >= 0:
            txt_content =  txt_content_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")
        return txt_content

    def getNodeTextFontColor(self, id, alias = 0):
        """
        Get the text font color of a node with a given node id.

        Args: 
            id: str-the id of the node.

            alias: int-alias node index: 0 to number of alias nodes -1.

        Returns:
            txt_font_color: list-[rgba 1*4 matrix, html_name str (if any, otherwise ''), 
            hex str (8 digits)].

        """

        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        txt_font_color_list =[] 
        for i in range(len(idx_list)):
            rgb = self.df[1].iloc[idx_list[i]]["txt_font_color"]
            color = _rgb_to_color(rgb)
            txt_font_color_list.append(color)
        if len(txt_font_color_list) == 0:
            raise Exception("This is not a valid id.")

        if alias < len(txt_font_color_list) and alias >= 0:
            txt_font_color =  txt_font_color_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")
        return txt_font_color

    def getNodeTextLineWidth(self, id, alias = 0):
        """
        Get the text line width of a node with a given node id.

        Args: 
            id: int-the id of the node.

            alias: int-alias node index: 0 to number of alias nodes -1.

        Returns:
            txt_line_width: float-node text line width.

        """
        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        txt_line_width_list =[] 
        for i in range(len(idx_list)):
            txt_line_width_list.append(self.df[1].iloc[idx_list[i]]["txt_line_width"])
        if len(txt_line_width_list) == 0:
            raise Exception("This is not a valid id.")
        if alias < len(txt_line_width_list) and alias >= 0:
            txt_line_width =  txt_line_width_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")

        return txt_line_width

    def getNodeTextFontSize(self, id, alias = 0):
        """
        Get the text font size of a node with a given node id.

        Args: 
            id: str-the id of the node.

            alias: int-alias node index: 0 to number of alias nodes -1.

        Returns:
            txt_font_size: float.

        """
        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        txt_font_size_list =[] 
        for i in range(len(idx_list)):
            txt_font_size_list.append(float(self.df[1].iloc[idx_list[i]]["txt_font_size"]))
        if len(txt_font_size_list) == 0:
            raise Exception("This is not a valid id.")
        if alias < len(txt_font_size_list) and alias >= 0:
            txt_font_size =  txt_font_size_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")

        return txt_font_size

    def getNodeTextAnchor(self, id, alias = 0):
        """
        Get the horizontal anchor of a node text with a given node id.

        Args: 
            id: str-the id of the node.

            alias: int-alias node index: 0 to number of alias nodes -1.

        Returns:
            txt_anchor: str-the horizantal anchor of the node text, which can be "start",
            "middle" and "end".
        """

        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        txt_anchor_list =[] 
        for i in range(len(idx_list)):
            anchor = self.df[1].iloc[idx_list[i]]["txt_anchor"][0]
            txt_anchor_list.append(anchor)
        if len(txt_anchor_list) == 0:
            raise Exception("This is not a valid id.")

        if alias < len(txt_anchor_list) and alias >= 0:
            txt_anchor =  txt_anchor_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")
        return txt_anchor

    def getNodeTextVAnchor(self, id, alias = 0):
        """
        Get the vertical anchor of a node text with a given node id.

        Args: 
            id: str-the id of the node.

            alias: int-alias node index: 0 to number of alias nodes -1.

        Returns:
            txt_anchor: str-the vertical anchor of the node text, which can be "top", 
            "middle", "baseline" and "bottom".
        """

        idx_list = self.df[1].index[self.df[1]["id"] == id].tolist()
        txt_anchor_list =[] 
        for i in range(len(idx_list)):
            anchor = self.df[1].iloc[idx_list[i]]["txt_anchor"][1]
            txt_anchor_list.append(anchor)
        if len(txt_anchor_list) == 0:
            raise Exception("This is not a valid id.")

        if alias < len(txt_anchor_list) and alias >= 0:
            txt_vanchor =  txt_anchor_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias.")
        return txt_vanchor

    def getReactionCenterPosition(self, id):
        """
        Get the center position of a reaction with a given reaction id.

        Args: 
            id: str-the id of the reaction.

        Returns:
            center_position: a Point object with attributes x and y representing
            the x/y position of the current center of the reaction. 

        Examples: 
            p = sd.getReactionCenterPosition('reaction_id')

            print ('x = ', p.x, 'y = ', p.y)          

        """

        p = visualizeSBML._getReactionCenterPosition(self.df, id)
        num = len(p)
        center_position_list = []
        for i in range(num):
            center_position = point.Point (p[i][0], p[i][1])
            center_position_list.append(center_position)
        if len(center_position_list) == 1:
            center_position = center_position_list[0]
        else:
            raise Exception("This is not a valid id.")

        return center_position

    def getReactionBezierHandles(self, id):
        """
        Get the bezier handle positions of a reaction with a given reaction id.

        Args: 
            id: str-the id of the reaction.

        Returns:
            handle_positions: list-position of the handles: 
            [center handle, reactant handles, product handles].

            position: a Point object with attributes x and y representing the x/y position.          

        """

        p = visualizeSBML._getReactionBezierHandles(self.df, id)
        num = len(p)
        handle_position_list = []
        for j in range(num):
            handle_position = []
            for i in range(len(p[j])):
                handle_position.append(point.Point(p[j][i][0], p[j][i][1]))
            handle_position_list.append(handle_position)

        if len(handle_position_list) == 1:
            handle_position = handle_position_list[0]
        else:
            raise Exception("This is not a valid id.")

        return handle_position

    def getReactionFillColor(self, id):
        """
        Get the fill color of a reaction with with a given reaction id.

        Args: 
            id: str-the id of the reaction.

        Returns:
            fill_color: list-[rgba 1*4 matrix, html_name str (if any, otherwise ''), 
            hex str (8 digits)].

        """
        idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
        fill_color_list =[] 
        for i in range(len(idx_list)):
            rgb = self.df[2].iloc[idx_list[i]]["stroke_color"]
            color = _rgb_to_color(rgb)
            fill_color_list.append(color)
        
        if len(fill_color_list) == 1:
            fill_color = fill_color_list[0]
        else:
            raise Exception("This is not a valid id.")
        
        return fill_color

    def getReactionLineThickness(self, id):
        """
        Get the line thickness of a reaction with a given reaction id.

        Args: 
            id: str-the id of the reaction.

        Returns:
            line_thickness: float-reaction border line width.

        """
        idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
        line_thickness_list =[] 
        for i in range(len(idx_list)):
            line_thickness_list.append(self.df[2].iloc[idx_list[i]]["line_thickness"])

        if len(line_thickness_list) == 1:
            line_thickness = line_thickness_list[0]
        else:
            raise Exception("This is not a valid id.")

        return line_thickness

    def getReactionDashStyle(self, id):
        """
        Get the dash information with a given reaction id.

        Args: 
            id: str-the id of the reaction.

        Returns:
            dash: list - [] means solid; 
            [a,b] means drawing a a-point line and following a b-point gap and etc;
            [a,b,c,d] means drawing a a-point line and following a b-point gap, and then
            drawing a c-point line followed by a d-point gap.

        """
        idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
        dash_list =[] 
        for i in range(len(idx_list)):
            dash_list.append((self.df[2].iloc[idx_list[i]]["rxn_dash"]))
        if len(dash_list) == 1:
            dash = dash_list[0]
        else:
            raise Exception("This is not a valid id.")
        
        return dash

    def _isBezierReactionType(self, id):
        """
        Judge whether it is a bezier reaction curve with a given reaction id.

        Args: 
            id: str-the id of the reaction.

        Returns:
            bezier: bool-bezier reaction (True) or not (False)

        """
        idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
        bezier_list =[] 
        for i in range(len(idx_list)):
            bezier_list.append(bool(self.df[2].iloc[idx_list[i]]["bezier"]))
        
        if len(bezier_list) == 1:
            bezier = bezier_list[0]
        else:
            raise Exception("This is not a valid id.")

        return bezier

    def _getReactionArrowHeadPosition(self, id):
        """
        Get the arrow head position of reactions with a given reaction id.

        Args: 
            id: str-the id of the reaction.

        Returns:
            arrow_head_position: a Point object with attributes x and y representing
            the x/y position of the relative position of the arrow head as an line ending.

        Examples: 
            p = sd.getReactionArrowHeadPosition('reaction_id')
            
            print('x = ', p.x, 'y = ', p.y)

        """
        line_ending_id = []
        arrow_head_position_pre = []
        idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
        for i in range(len(idx_list)):
            line_ending_id.append(self.df[2].iloc[idx_list[i]]["targets_lineending"][0]) 
        if len(line_ending_id) == 1:
            idx_lineending = self.df[5].index[self.df[5]["id"] == line_ending_id[0]].tolist()
            if len(idx_lineending) == 1:
                arrow_head_position_pre.append(self.df[5].iloc[idx_lineending[0]]["position"])
                if len(arrow_head_position_pre) == 1:
                    arrow_head_position = point.Point(arrow_head_position_pre[0][0],arrow_head_position_pre[0][1])
                else:
                    raise Exception("There is no arrow head position information.")
            else:
                raise Exception("There is no arrow head information.")
        else:
            raise Exception("This is not a valid id.")

        return arrow_head_position

    #This is the old version of arrow head size without defining lineending
    # def getReactionArrowHeadSize(self, id):
    #     """
    #     Get the arrow head size of reactions with a given reaction id.

    #     Args: 
    #         id: str-the id of the reaction.

    #     Returns:
    #         arrow_head_size: a Point object with attributes x and y representing
    #         the width and height of the arrow head.

    #     Examples: 
    #         p = sd.getReactionArrowHeadSize('reaction_id')
            
    #         print ('Width = ', p.x, 'Height = ', p.y)

    #     """
    #     arrow_head_size_pre = []
    #     idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
    #     for i in range(len(idx_list)):
    #         arrow_head_size_pre.append(self.df[2].iloc[idx_list[i]]["arrow_head_size"]) 
    #     arrow_head_size_list =[]
    #     for i in range(len(arrow_head_size_pre)):
    #         arrow_head_size_list.append(point.Point(arrow_head_size_pre[i][0],arrow_head_size_pre[i][1]))
    #     if len(arrow_head_size_list) == 1:
    #         arrow_head_size = arrow_head_size_list[0]
    #     else:
    #         raise Exception("This is not a valid id.")

    #     return arrow_head_size

    def getReactionArrowHeadSize(self, id):
        """
        Get the arrow head size of reactions with a given reaction id.

        Args: 
            id: str-the id of the reaction.

        Returns:
            arrow_head_size: a Point object with attributes x and y representing
            the width and height of the arrow head.

        Examples: 
            p = sd.getReactionArrowHeadSize('reaction_id')
            
            print ('Width = ', p.x, 'Height = ', p.y)

        """
        line_ending_id = []
        arrow_head_size_pre = []
        idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
        for i in range(len(idx_list)):
            line_ending_id.append(self.df[2].iloc[idx_list[i]]["targets_lineending"][0]) 
        if len(line_ending_id) == 1:
            idx_lineending = self.df[5].index[self.df[5]["id"] == line_ending_id[0]].tolist()
            if len(idx_lineending) == 1:
                arrow_head_size_pre.append(self.df[5].iloc[idx_lineending[0]]["size"])
                if len(arrow_head_size_pre) == 1:
                    arrow_head_size = point.Point(arrow_head_size_pre[0][0],arrow_head_size_pre[0][1])
                else:
                    raise Exception("There is no arrow head size information.")
            else:
                raise Exception("There is no arrow head information.")
        else:
            raise Exception("This is not a valid id.")

        return arrow_head_size


    def getReactionArrowHeadFillColor(self, id):
        """

        Get the fill color of the reaction arrow head with a given reaction id.

        Args: 
            id: str-the id of the reaction.

        Returns:
            fill_color: list-[rgba 1*4 matrix, html_name str (if any, otherwise ''), 
            hex str (8 digits)]

        """
        line_ending_id = []
        arrow_head_fill_pre = []
        idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
        for i in range(len(idx_list)):
            line_ending_id.append(self.df[2].iloc[idx_list[i]]["targets_lineending"][0]) 
        if len(line_ending_id) == 1:
            idx_lineending = self.df[5].index[self.df[5]["id"] == line_ending_id[0]].tolist()
            if len(idx_lineending) == 1:
                arrow_head_fill_pre.append(self.df[5].iloc[idx_lineending[0]]["fill_color"])
                if len(arrow_head_fill_pre) == 1:
                    fill_color = _rgb_to_color(arrow_head_fill_pre[0])
                else:
                    raise Exception("There is no arrow head size information.")
            else:
                raise Exception("There is no arrow head information.")
        else:
            raise Exception("This is not a valid id.")

        return fill_color

    def getReactionArrowHeadShape(self, id):
        """

        Get the shape of the reaction arrow head with a given reaction id.

        Args: 
            id: str-the id of the reaction.

        Returns:
            shape: tuple (shape_type_list, shape_info_list)
            
            shape_type_list: list of str-the name of the arrow head shape.

            shape_info_list: list-the shape information corresponding to the list of 
            shape_type_list.

        """
        line_ending_id = []
        shape_type = []
        shape_info = []
        idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
        for i in range(len(idx_list)):
            line_ending_id.append(self.df[2].iloc[idx_list[i]]["targets_lineending"][0]) 
        if len(line_ending_id) == 1:
            idx_lineending = self.df[5].index[self.df[5]["id"] == line_ending_id[0]].tolist()
            if len(idx_lineending) == 1:
                shape_type = self.df[5].iloc[idx_lineending[0]]["shape_type"]
                shape_info = self.df[5].iloc[idx_lineending[0]]["shape_info"]
                if len(shape_type) >= 1:
                    shape = (shape_type, shape_info)
                else:
                    raise Exception("There is no arrow head size information.")
            else:
                raise Exception("There is no arrow head information.")
        else:
            raise Exception("This is not a valid id.")

        return shape

    def getReactionModifierNum(self, id):
        """
        Get the number of modifiers of reactions with a given reaction id.

        Args: 
            id: str-the id of the reaction.

        Returns:
            modifier_num: int-number of modifiers.

        """
        idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
        for i in range(len(idx_list)):
            line_ending_id = self.df[2].iloc[idx_list[i]]["modifiers_lineending"]
        if len(line_ending_id) != 0:
            modifier_num = len(line_ending_id)
        else:
            raise Exception("This is not a valid id.")

        return modifier_num

    def _getReactionModifierHeadPosition(self, id, mod_idx = 0):
        """
        Get the modifier head position of reactions with a given reaction id.

        Args: 
            id: str-the id of the reaction.

            mod_idx: int-the index of the modifier: 0 to number of modifiers -1.

        Returns:
            head_position: a Point object with attributes x and y representing
            the x/y position of the relative position of the modifier head as an line ending.

        Examples: 
            p = sd.getReactionModifierHeadPosition('reaction_id')
            
            print('x = ', p.x, 'y = ', p.y)

        """
        line_ending_id = []
        head_position_pre = []
        idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
        mod_num = self.getReactionModifierNum(id)
        if type(mod_idx) == int and mod_idx >= 0 and mod_idx < mod_num:
            for i in range(len(idx_list)):
                line_ending_id.append(self.df[2].iloc[idx_list[i]]["modifiers_lineending"][mod_idx]) 
            if len(line_ending_id) == 1:
                idx_lineending = self.df[5].index[self.df[5]["id"] == line_ending_id[0]].tolist()
                if len(idx_lineending) == 1:
                    head_position_pre.append(self.df[5].iloc[idx_lineending[0]]["position"])
                    if len(head_position_pre) == 1:
                        head_position = point.Point(head_position_pre[0][0],head_position_pre[0][1])
                    else:
                        raise Exception("There is no modifier head position information.")
                else:
                    raise Exception("There is no modifier head information.")
            else:
                raise Exception("This is not a valid id.")
        else:
            raise Exception("This is not a valid modifier index.")

        return head_position

    def getReactionModifierHeadSize(self, id, mod_idx = 0):
        """
        Get the modifier head size of reactions with a given reaction id.

        Args: 
            id: str-the id of the reaction.

            mod_idx: int-index of the modifier: 0 to number of modifiers -1.

        Returns:
            head_size: a Point object with attributes x and y representing
            the width and height of the modifier head.

        Examples: 
            p = sd.getReactionModifierHeadSize('reaction_id')
            
            print ('Width = ', p.x, 'Height = ', p.y)

        """
        line_ending_id = []
        head_size_pre = []
        idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
        mod_num = self.getReactionModifierNum(id)
        if type(mod_idx) == int and mod_idx >= 0 and mod_idx < mod_num:
            for i in range(len(idx_list)):
                line_ending_id.append(self.df[2].iloc[idx_list[i]]["modifiers_lineending"][mod_idx]) 
            if len(line_ending_id) == 1:
                idx_lineending = self.df[5].index[self.df[5]["id"] == line_ending_id[0]].tolist()
                if len(idx_lineending) == 1:
                    head_size_pre.append(self.df[5].iloc[idx_lineending[0]]["size"])
                    if len(head_size_pre) == 1:
                        head_size = point.Point(head_size_pre[0][0],head_size_pre[0][1])
                    else:
                        raise Exception("There is no modifier head size information.")
                else:
                    raise Exception("There is no modifier head information.")
            else:
                raise Exception("This is not a valid id.")
        else:
            raise Exception("This is not a valid modifier index.")

        return head_size

    def getReactionModifierHeadFillColor(self, id, mod_idx = 0):
        """

        Get the fill color of the reaction modifier head with a given reaction id.

        Args: 
            id: str-the id of the reaction.

            mod_idx: int-index of the modifier: 0 to number of modifiers -1.

        Returns:
            fill_color: list-[rgba 1*4 matrix, html_name str (if any, otherwise ''), 
            hex str (8 digits)]

        """
        line_ending_id = []
        head_fill_pre = []
        idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
        mod_num = self.getReactionModifierNum(id)
        if type(mod_idx) == int and mod_idx >= 0 and mod_idx < mod_num:
            for i in range(len(idx_list)):
                line_ending_id.append(self.df[2].iloc[idx_list[i]]["modifiers_lineending"][mod_idx]) 
            if len(line_ending_id) == 1:
                idx_lineending = self.df[5].index[self.df[5]["id"] == line_ending_id[0]].tolist()
                if len(idx_lineending) == 1:
                    head_fill_pre.append(self.df[5].iloc[idx_lineending[0]]["fill_color"])
                    if len(head_fill_pre) == 1:
                        fill_color = _rgb_to_color(head_fill_pre[0])
                    else:
                        raise Exception("There is no modifier head size information.")
                else:
                    raise Exception("There is no modifier head information.")
            else:
                raise Exception("This is not a valid id.")
        else:
            raise Exception("This is not a valid modifier index.")

        return fill_color

    def getReactionModifierHeadShape(self, id, mod_idx = 0):
        """

        Get the shape of the reaction modifier head with a given reaction id.

        Args: 
            id: str-the id of the reaction.
     
            mod_idx: int-index of the modifier: 0 to number of modifiers -1.

        Returns:
            shape: tuple (shape_type_list, shape_info_list)
            
            shape_type_list: list of str-the name of the modifier head shape.

            shape_info_list: list-the shape information corresponding to the list of 
            shape_type_list.

        """
        line_ending_id = []
        shape_type = []
        shape_info = []
        idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
        mod_num = self.getReactionModifierNum(id)
        if type(mod_idx) == int and mod_idx >= 0 and mod_idx < mod_num:
            for i in range(len(idx_list)):
                line_ending_id.append(self.df[2].iloc[idx_list[i]]["modifiers_lineending"][mod_idx]) 
            if len(line_ending_id) == 1:
                idx_lineending = self.df[5].index[self.df[5]["id"] == line_ending_id[0]].tolist()
                if len(idx_lineending) == 1:
                    shape_type = self.df[5].iloc[idx_lineending[0]]["shape_type"]
                    shape_info = self.df[5].iloc[idx_lineending[0]]["shape_info"]
                    if len(shape_type) >= 1:
                        shape = (shape_type, shape_info)
                    else:
                        raise Exception("There is no modifier head size information.")
                else:
                    raise Exception("There is no modifier head information.")
            else:
                raise Exception("This is not a valid id.")
        else:
            raise Exception("This is not a valid modifier index.")

        return shape

    def setCompartmentPosition(self, id, position):
        """
        Set the x,y coordinates of the compartment position.

        Args:  
            id: str-compartment id.

            position: list or point.Point()
                
            list-
            [position_x, position_y], the coordinate represents the top-left hand corner of 
            the compartment.

            point.Point()-
            a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the compartment.

        """
        self.df = editSBML._setCompartmentPosition(self.df, id, position)
        #return self.df
    
    def setCompartmentSize(self, id, size):
        """
        Set the compartment size.

        Args:  
            df: DataFrame-initial information.

            id: str-compartment id.

            size: list or point.Point()
                
            list-
            1*2 matrix-size of the compartment [width, height].

            point.Point()-
            a Point object with attributes x and y representing the width and height of 
            the compartment.

        """
        self.df = editSBML._setCompartmentSize(self.df, id, size)
        #return self.df

    def setCompartmentFillColor(self, id, fill_color, opacity = 1.):
        """
        Set the compartment fill color.

        Args:  
            id: str-compartment id.

            fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

        """
        self.df = editSBML._setCompartmentFillColor(self.df, id, fill_color, opacity)
        #return self.df

    def setCompartmentBorderColor(self, id, border_color, opacity = 1.):       
        """
        Set the compartment border color.

        Args:  
            id: str-compartment id.

            border_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

        """
        self.df = editSBML._setCompartmentBorderColor(self.df, id, border_color, opacity)
        #return self.df

    def setCompartmentBorderWidth(self, id, border_width):
        """
        Set the compartment border width.

        Args:  
            id: str-compartment id.

            border_width: float-compartment border line width.

        """
        self.df = editSBML._setCompartmentBorderWidth(self.df, id, border_width)
        #return self.df

    def setCompartmentTextPosition(self, id, position):
        """
        Set the x,y coordinates of the compartment text position.

        Args:  
            id: str-compartment id.

            position: list or point.Point()
                
            list-
            [position_x, position_y], the coordinate represents the top-left hand corner of 
            the compartment.

            point.Point()-
            a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the compartment.

        """
        self.df = editSBML._setCompartmentTextPosition(self.df, id, position)
        #return self.df
    
    def setCompartmentTextSize(self, id, size):
        """
        Set the compartment text size.

        Args:  
            df: DataFrame-initial information.

            id: str-compartment id.

            size: list or point.Point()
                
            list-
            1*2 matrix-size of the compartment [width, height].

            point.Point()-
            a Point object with attributes x and y representing the width and height of 
            the compartment.

        """
        self.df = editSBML._setCompartmentTextSize(self.df, id, size)
        #return self.df
    
    def setCompartmentTextContent(self, id, txt_content):
        """
        Set the compartment text content for a compartment of given id.

        Args:  
            id: str-compartment id.

            txt_content: str-compartment text content.

        Examples:
            la.setCompartmentTextContent ('compartment4', 'C4')
        """
        self.df = editSBML._setCompartmentTextContent(self.df, id, txt_content)
        #return self.df

    def setCompartmentTextFontColor(self, id, txt_font_color, opacity = 1.):
        """
        Set the compartment text font color for a compartment of given id.

        Args:  
            id: str-compartment id.

            txt_font_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

        Examples:
            la.setCompartmentTextFontColor ('commpartment1', 'CornflowerBlue')
        """
        self.df = editSBML._setCompartmentTextFontColor(self.df, id, txt_font_color, opacity)
        #return self.df

    def setCompartmentTextLineWidth(self, id, txt_line_width):
        """
        Set the compartment text line width for a compartment of given id.

        Args:  
            id: str-compartment id.

            txt_line_width: float-compartment text line width.

        """
        self.df = editSBML._setCompartmentTextLineWidth(self.df, id, txt_line_width)
        #return self.df

    def setCompartmentTextFontSize(self, id, txt_font_size):
        """
        Set the compartment text font size for a compartment of given id.

        Args:  
            id: str-compartment id.

            txt_font_size: float-compartment text font size, the units for size are assumed to be in points.
            
        """
        self.df = editSBML._setCompartmentTextFontSize(self.df, id, txt_font_size)
        #return self.df

    def setCompartmentTextAnchor(self, id, txt_anchor):
        """
        Set the horizontal anchor for a compartment text of given id.

        Args:  
            id: str-compartment id.

            txt_anchor: str-compartment text horizontal anchor, which can be "start",
            "middle" and "end".
            
        """
        self.df = editSBML._setCompartmentTextAnchor(self.df, id, txt_anchor)
        #return self.df

    def setCompartmentTextVAnchor(self, id, txt_vanchor):
        """
        Set the vertical anchor for a compartment text of given id.

        Args:  
            id: str-compartment id.

            txt_vanchor: str-compartment text vertical anchor, which can be which can be "top", 
            "middle", "baseline" and "bottom".
            
        """
        self.df = editSBML._setCompartmentTextVAnchor(self.df, id, txt_vanchor)
        #return self.df



    def setFloatingBoundaryNode(self, id, floating_node, alias = 0):
        """
        Set a node to be floating node (True) or boundary node (False).

        Args:  
            id: str-node id.

            floating_node: bool-floating node (True) or not (False).

            alias: int-alias node index: 0 to number of alias node -1.
        
        """
        self.df = editSBML._setFloatingBoundaryNode(self.df, id, floating_node, alias=alias)
        #return self.df

    def setNodePosition(self, id, position, alias = 0):
        """
        Set the x,y coordinates of the node position.

        Args:  
            id: str-node id.

            position: list or point.Point()
                
            list-
            [position_x, position_y], the coordinate represents the top-left hand corner of the node.

            point.Point()-
            a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the node.

            alias: int-alias node index: 0 to number of alias nodes -1.

        """
        self.df = editSBML._setNodePosition(self.df, id, position, alias=alias)
        #return self.df

    def setNodeAndTextPosition(self, id, position, alias = 0):
        """
        Set the x,y coordinates of the node position and node text position if they are consistent.
        Please only use this function if you want to design the node position and node text 
        position to be the same, otherwise use setNodePosition() and setNodeTextPosition() 
        separately to set the position of the node and the node text.

        Args:  
            id: str-node id.

            position: list or point.Point()
                
            list-
            [position_x, position_y], the coordinate represents the top-left hand corner of the 
            node and the node text.

            point.Point()-
            a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the node and the node text.

            alias: int-alias node index: 0 to number of alias nodes -1.

        """
        self.df = editSBML._setNodePosition(self.df, id, position, alias=alias)
        self.df = editSBML._setNodeTextPosition(self.df, id, position, alias=alias)
        #return self.df

    def setNodeSize(self, id, size, alias = 0):
        """
        Set the node size.

        Args:  
            id: str-node id.

            size: list or point.Point()
                
            list-
            1*2 matrix-size of the node [width, height].

            point.Point()-
            a Point object with attributes x and y representing the width and height of 
            the node.

            alias: int-alias node index: 0 to number of alias nodes -1.

        """
        self.df = editSBML._setNodeSize(self.df, id, size, alias=alias)
        #return self.df

    def setNodeAndTextSize(self, id, size, alias = 0):
        """
        Set the node and node text size if there are consistent.

        Args:  
            id: str-node id.

            size: list or point.Point()
                
            list-
            1*2 matrix-size of the node and text [width, height].

            point.Point()-
            a Point object with attributes x and y representing the width and height of 
            the node and node text.

            alias: int-alias node index: 0 to number of alias nodes -1.

        """
        self.df = editSBML._setNodeSize(self.df, id, size, alias=alias)
        self.df = editSBML._setNodeTextSize(self.df, id, size, alias=alias)
        #return self.df

    def setNodeShape(self, id, shape, alias = 0):
        """
        Set the node shape by shape index or name string.

        Args:  
            id: str-node id.

            shape: int or str
            int-0:text_only, 1:rectangle, 2:ellipse, 3:hexagon, 4:line, or 5:triangle;
            6:upTriangle, 7:downTriangle, 8:leftTriangle, 9: rightTriangle.
                
            str-"text_only", "rectangle", "ellipse", "hexagon", "line", or "triangle";
            "upTriangle", "downTriangle", "leftTriangle", "rightTriangle".

            alias: int-alias node index: 0 to number of alias nodes -1.
            
        """
        self.df = editSBML._setNodeShape(self.df, id, shape, alias=alias)
        #return self.df

    def setNodeArbitraryPolygonShape(self, id, shape_name, shape_info, alias = 0):
        """
        Set an arbitrary polygon shape to a node by shape name and shape info.

        Args:  
            id: str-node id.

            shape_name: str-name of the arbitrary polygon shape.

            shape_info: list-[[x1,y1],[x2,y2],[x3,y3],etc], where x,y are floating numbers from 0 to 100.
            x represents the percentage of width, and y represents the percentage of height.

            alias: int-alias node index: 0 to number of alias nodes -1.
            
        """
        self.df = editSBML._setNodeArbitraryPolygonShape(self.df, id, shape_name, shape_info, alias=alias)
        #return self.df

    # def _setNodeArbitraryEllipseShape(self, id, shape_name, shape_info):
    #     """
    #     Set an arbitrary ellipse shape to a node by shape name and shape info.

    #     Args:  
    #         id: str-node id.

    #         shape_name: str-name of the arbitrary ellipse shape.

    #         shape_info: list-[[[x1,y1],[r1,r2]]], where x,y,r are floating numbers from 0 to 100.
    #     """
    #     self.df = editSBML._setNodeArbitraryEllipseShape(self.df, id, shape_name, shape_info)
    #     return self.df

    def setNodeTextPosition(self, id, txt_position, alias = 0):
        """
        Set the x,y coordinates of the node text position.

        Args:  
            id: str-node id.

            txt_position: list or point.Point()
                
            list-
            [txt_position_x, txt_position_y], the coordinate represents the top-left hand 
            corner of the node text.

            point.Point()-
            a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the node text.

            alias: int-alias node index: 0 to number of alias nodes -1.

        """
        self.df = editSBML._setNodeTextPosition(self.df, id, txt_position, alias=alias)
        #return self.df

    def moveNodeTextPosition(self, id, rel_position, alias = 0):
        """
        Move the x,y coordinates of the node text position relative to its original position.

        Args:  
            id: str-node id.

            rel_position: list or point.Point()
                
            list-
            [rel_position_x, rel_position_y], the relative coordinates moving away from the 
            original node text position.

            point.Point()-
            a Point object with attributes x and y representing the relative coordinates moving 
            away from the original node text position.

            alias: int-alias node index: 0 to number of alias nodes -1.

        """
        original_position = visualizeSBML._getNodeTextPosition(self.df, id)[alias]
        if type(rel_position) != list and type(rel_position) != type(point.Point()):
            raise Exception("Please enter a valid rel_position type.")
        if type(rel_position) == type(point.Point()):
            rel_position = [rel_position.x, rel_position.y]
        update_position = [original_position[0] + rel_position[0], 
                            original_position[1] + rel_position[1]]
        self.df = editSBML._setNodeTextPosition(self.df, id, update_position, alias=alias)
        #return self.df

    def setNodeTextPositionCenter(self, id, alias = 0):
        """
        Set the node text position to the center of the node.

        Args:  
            id: str-node id.

            alias: int-alias node index: 0 to number of alias nodes -1.

        """
        self.df = editSBML._setNodeTextPositionCenter(self.df, id, alias=alias)
        #return self.df

    def setNodeTextPositionLeftCenter(self, id, alias = 0):
        """
        Set the node text position to the left center of the node.

        Args:  
            id: str-node id.

            alias: int-alias node index: 0 to number of alias nodes -1.

        """
        self.df = editSBML._setNodeTextPositionLeftCenter(self.df, id, alias=alias)
        #return self.df

    def setNodeTextPositionRightCenter(self, id, alias = 0):
        """
        Set the node text position to the right center of the node.

        Args:  
            id: str-node id.

            alias: int- alias node index: 0 to number of alias nodes -1.

        """
        self.df = editSBML._setNodeTextPositionRightCenter(self.df, id, alias=alias)
        #return self.df

    def setNodeTextPositionUpperCenter(self, id, alias = 0):
        """
        Set the node text position to the upper center of the node.

        Args:  
            id: str-node id.

            alias: int-alias node index: 0 to number of alias nodes -1.

        """
        self.df = editSBML._setNodeTextPositionUpperCenter(self.df, id, alias=alias)
        #return self.df

    def setNodeTextPositionLowerCenter(self, id, alias = 0):
        """
        Set the node text position to the lower center of the node.

        Args:  
            id: str-node id.

            alias: int-alias node index: 0 to number of alias nodes -1.

        """
        self.df = editSBML._setNodeTextPositionLowerCenter(self.df, id, alias=alias)
        #return self.df

    def setNodeTextPositionUpperLeft(self, id, alias = 0):
        """
        Set the node text position to the upper left of the node.

        Args:  
            id: str-node id.

            alias: int-alias node index: 0 to number of alias nodes -1.

        """
        self.df = editSBML._setNodeTextPositionUpperLeft(self.df, id, alias=alias)
        #return self.df
    
    def setNodeTextPositionUpperRight(self, id, alias = 0):
        """
        Set the node text position to the upper right of the node.

        Args:  
            id: str-node id.

            alias: int-alias node index: 0 to number of alias nodes -1.

        """
        self.df = editSBML._setNodeTextPositionUpperRight(self.df, id, alias=alias)
        #return self.df

    def setNodeTextPositionLowerLeft(self, id, alias = 0):
        """
        Set the node text position to the lower left of the node.

        Args:  
            id: str-node id.

            alias: int-alias node index: 0 to number of alias nodes -1.

        """
        self.df = editSBML._setNodeTextPositionLowerLeft(self.df, id, alias=alias)
        #return self.df

    def setNodeTextPositionLowerRight(self, id, alias = 0):
        """
        Set the node text position to the lower right of the node.

        Args:  
            id: str-node id.

            alias: int-alias node index: 0 to number of alias nodes -1.

        """
        self.df = editSBML._setNodeTextPositionLowerRight(self.df, id, alias=alias)
        #return self.df

    def setNodeTextSize(self, id, txt_size, alias = 0):
        """
        Set the node text size with given node id.

        Args:  
            id: str-node id.

            txt_size: list or point.Point()
                
            list-
            1*2 matrix-size of the node text [width, height].

            point.Point()-
            a Point object with attributes x and y representing the width and height of 
            bounding box that enclosed the node text. The text font size wil be adjusted to fill
            the given bounding box. 

            alias: int-alias node index: 0 to number of alias nodes -1.

        """
        self.df = editSBML._setNodeTextSize(self.df, id, txt_size, alias=alias)
        #return self.df
 
    def setNodeFillColor(self, id, fill_color, opacity = 1., alias = 0):
        """
        Set the node fill color with given node id.

        Args:  
            id: str-node id.

            fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

            alias: int-alias node index: 0 to number of alias nodes -1.

        """
        self.df = editSBML._setNodeFillColor(self.df, id, fill_color, opacity, alias=alias)
        #return self.df

    def setNodeFillLinearGradient(self, id, gradient_info, stop_info, alias = 0):
        """
        Set the node fill linear gradient with given node id.

        Args:  
            id: str-node id.

            gradient_info: list - [[x1,y1],[x2,y2]], where x,y are floating numbers from 0 to 100.
            x represents the percentage of width, and y represents the percentage of height.

            stop_info: 
            list - [[x1,[r1,g1,b1,a1]],[x2,[r2,g2,b2,a2]],etc],
            where x is floating number from 0 to 100.

            or list - [[x1, html_name_str, opacity], [x2, html_name_str, opacity], etc], 
            where opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

            alias: int-alias node index: 0 to number of alias nodes -1.

        Examples:
            setNodeFillLinearGradient("ADH1", [[0.0, 50.], [100.0, 50.0]], [[0.0, [255, 255, 255, 255]], [100.0, [192, 192, 192, 255]]])

            setNodeFillLinearGradient("ADH1", [[0.0, 50.], [100.0, 50.0]], [[0.0, "red", 1.0], [100.0, "blue", 1.0]])
        """
        self.df = editSBML._setNodeFillLinearGradient(self.df, id, gradient_info, stop_info, alias=alias)
        #return self.df

    def setNodeFillRadialGradient(self, id, gradient_info, stop_info, alias = 0):
        """
        Set the node fill radial gradient.

        Args:  
            id: str-node id.

            gradient_info: list - [[x1,y1],[r]], where x,y,r are floating numbers from 0 to 100.
            x represents the center with percentage of width and height; r represents the radius.

            stop_info:
            list - [[x1,[r1,g1,b1,a1]],[x2,[r2,g2,b2,a2]],etc], where x is floating number from 0 to 100.
            
            or list - [[x1, html_name_str, opacity], [x2, html_name_str, opacity], etc], where opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

            alias: int-alias node index: 0 to number of alias nodes -1.

        Examples:
            df.setNodeFillRadialGradient("Species_1", [[50.0, 50.0], [50.]], [[0.0, [255, 255, 255, 255]], [100.0, [0, 0, 0, 255]]])
    
            df.setNodeFillRadialGradient("Species_1", [[50.0, 50.0], [50.]], [[0.0, "red", 1.0], [100.0, "blue", 1.0]])

        """
        self.df = editSBML._setNodeFillRadialGradient(self.df, id, gradient_info, stop_info, alias=alias)
        #return self.df

    def setNodeBorderColor(self, id, border_color, opacity = 1., alias = 0):
        """
        Set the node border color of a node with a given id.

        Args:  
            id: str-node id.

            border_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

            alias: int-alias node index: 0 to number of alias nodes -1.

        Examples:
            la.setNodeBorderColor ('node1', 'CornflowerBlue')
        """
        self.df = editSBML._setNodeBorderColor(self.df, id, border_color, opacity, alias=alias)

    def setNodeBorderWidth(self, id, border_width, alias = 0):
        """
        Set the node border width for a node of given id.

        Args:  
            id: str-node id.

            border_width: float-node border line width.

            alias: int-alias node index: 0 to number of alias nodes -1.

        Examples:
            la.setNodeBorderWidth ('node4', 3)
        """
        self.df = editSBML._setNodeBorderWidth(self.df, id, border_width, alias=alias)
        #return self.df

    def setNodeTextContent(self, id, txt_content, alias = 0):
        """
        Set the node text content for a node of given id.

        Args:  
            id: str-node id.

            txt_content: str-node text content.

            alias: int-alias node index: 0 to number of alias nodes -1.

        Examples:
            la.setNodeTextContent ('node4', 'N4')
        """
        self.df = editSBML._setNodeTextContent(self.df, id, txt_content, alias=alias)
        #return self.df

    def setNodeTextFontColor(self, id, txt_font_color, opacity = 1., alias = 0):
        """
        Set the node text font color for a node of given id.

        Args:  
            id: str-node id.

            txt_font_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

            alias: int-alias node index: 0 to number of alias nodes -1.
        
        Examples:
            la.setNodeTextFontColor ('node1', 'CornflowerBlue')
        """
        self.df = editSBML._setNodeTextFontColor(self.df, id, txt_font_color, opacity, alias=alias)
        #return self.df

    def setNodeTextLineWidth(self, id, txt_line_width, alias = 0):
        """
        Set the node text line width for a node of given id.

        Args:  
            id: str-node id.

            txt_line_width: float-node text line width.

            alias: int-alias node index: 0 to number of alias nodes -1.
        
        """
        self.df = editSBML._setNodeTextLineWidth(self.df, id, txt_line_width, alias=alias)
        #return self.df

    def setNodeTextFontSize(self, id, txt_font_size, alias = 0):
        """
        Set the node text font size for a node of given id.

        Args:  
            id: str-node id.

            txt_font_size: float-node text font size, the units for size are assumed to be in points.
            
            alias: int-alias node index: 0 to number of alias nodes -1.
        
        """
        self.df = editSBML._setNodeTextFontSize(self.df, id, txt_font_size, alias=alias)
        #return self.df

    def setNodeTextAnchor(self, id, txt_anchor, alias = 0):
        """
        Set the horizontal anchor for a node text of given id.

        Args:  
            id: str-node id.

            txt_anchor: str-node text horizontal anchor, which can be "start",
            "middle" and "end".
            
            alias: int-alias node index: 0 to number of alias nodes -1.
        
        """
        self.df = editSBML._setNodeTextAnchor(self.df, id, txt_anchor, alias=alias)
        #return self.df

    def setNodeTextVAnchor(self, id, txt_vanchor, alias = 0):
        """
        Set the vertical anchor for a node text of given id.

        Args:  
            id: str-node id.

            txt_vanchor: str-node text vertical anchor, which can be which can be "top", 
            "middle", "baseline" and "bottom".
            
            alias: int-alias node index: 0 to number of alias nodes -1.
        
        """
        self.df = editSBML._setNodeTextVAnchor(self.df, id, txt_vanchor, alias=alias)
        #return self.df

    def setReactionToStraightLine(self, id):
        """
        For a reaction of given id, use straight lines to represent the reaction. 
        The default reaction line style is to use Bezier curves.

        Args:  
            id: str-reaction id.
      
        """
        # center_x = 0.
        # center_y = 0.

        idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
        if len(idx_list) == 0:
            raise Exception("This is not a valid id.")
        rct_list = []
        prd_list = []
        rct_list.append(self.df[2].iloc[idx_list[0]]["sources"])
        prd_list.append(self.df[2].iloc[idx_list[0]]["targets"])

        rct_num = len(rct_list[0])
        prd_num = len(prd_list[0])

        rct_id_list = []
        prd_id_list = []
        for i in range(rct_num):
            temp_idx = self.df[1].index[self.df[1]["idx"] == rct_list[0][i]].tolist()[0]
            rct_id_list.append(self.df[1].iloc[temp_idx]["id"])
        for i in range(prd_num):
            temp_idx = self.df[1].index[self.df[1]["idx"] == prd_list[0][i]].tolist()[0]
            prd_id_list.append(self.df[1].iloc[temp_idx]["id"])

        src_position = []
        src_dimension = []
        dst_position = []
        dst_dimension = []
        for i in range(rct_num):
            temp_idx = self.df[1].index[self.df[1]["id"] == rct_id_list[i]].tolist()[0]
            src_position.append(self.df[1].iloc[temp_idx]["position"])
            src_dimension.append(self.df[1].iloc[temp_idx]["size"])
        for i in range(prd_num):
            temp_idx = self.df[1].index[self.df[1]["id"] == prd_id_list[i]].tolist()[0]
            dst_position.append(self.df[1].iloc[temp_idx]["position"])
            dst_dimension.append(self.df[1].iloc[temp_idx]["size"])
  
        # for j in range(rct_num):
        #     center_x += src_position[j][0]+.5*src_dimension[j][0]
        #     center_y += src_position[j][1]+.5*src_dimension[j][1]
        # for j in range(prd_num):
        #     center_x += dst_position[j][0]+.5*dst_dimension[j][0]
        #     center_y += dst_position[j][1]+.5*dst_dimension[j][1]
        # center_x = center_x/(rct_num + prd_num) 
        # center_y = center_y/(rct_num + prd_num)
        center_position_pt = visualizeSBML._getReactionCenterPosition(self.df, id)
        center_position = [center_position_pt[0][0], center_position_pt[0][1]]
        #center_position = [center_x, center_y]
        handles = [center_position]
        for j in range(rct_num):
            src_handle_x = .5*(center_position[0] + src_position[j][0] + .5*src_dimension[j][0])
            src_handle_y = .5*(center_position[1] + src_position[j][1] + .5*src_dimension[j][1])
            handles.append([src_handle_x,src_handle_y])
        for j in range(prd_num):
            dst_handle_x = .5*(center_position[0] + dst_position[j][0] + .5*dst_dimension[j][0])
            dst_handle_y = .5*(center_position[1] + dst_position[j][1] + .5*dst_dimension[j][1])
            handles.append([dst_handle_x,dst_handle_y])
        # print('rct:', src_position, src_dimension)
        # print('prd:', dst_position, dst_dimension)
        # print("center:", center_position)
        # print("handle:", handles)
        self.df = editSBML._setReactionCenterPosition(self.df, id, center_position)        
        self.df = editSBML._setReactionBezierHandles(self.df, id, handles)
 

    def setReactionCenterPosition(self, id, position):
        """
        Set the reaction center position for a reaction with a given reaction id.

        Args:  
            id: str-reaction id.
            
            position: list or point.Point()
                
            list-
            1*2 matrix-[position_x, position_y].

            point.Point()-
            a Point object with attributes x and y representing the x/y position.

        """
        self.df = editSBML._setReactionCenterPosition(self.df, id, position)
    

    def setReactionBezierHandles(self, id, position):
        """
        Set the reaction bezier handle positions for a given reaction.

        Args:  
            id: str-reaction id.
            
            position: list-position of the handles: [center handle, reactant handle1, ..., product handle1, ...].
                            
            center handle/reactant handle1/product handle1: list or point.Point()
                
            list-
            [position_x, position_y], the coordinate represents the top-left hand 
            corner of the node.

            point.Point()-
            a Point object with attributes x and y representing the x/y position.

        Examples:
            setReactionBezierHandles ('J1', [point.Point(550,150),point.Point(530,155),point.Point(600,120)])
            
            setReactionBezierHandles("J3", [[550,150],[530,155],[600,120]])
        """
        self.df = editSBML._setReactionBezierHandles(self.df, id, position)
        #return self.df

    def setReactionDefaultCenterAndHandlePositions(self, id):
        """
        Set detault center and handle positions. The default center is the centroid of the reaction,
        and the default handle positions are middle points of nodes (species) and the centroid.

        Args:  
            id: str-reaction id.
            
        """
        
        center_x = 0.
        center_y = 0.

        idx_list = self.df[2].index[self.df[2]["id"] == id].tolist()
        if len(idx_list) == 0:
            raise Exception("This is not a valid id.")
        rct_list = []
        prd_list = []
        rct_list.append(self.df[2].iloc[idx_list[0]]["sources"])
        prd_list.append(self.df[2].iloc[idx_list[0]]["targets"])

        rct_num = len(rct_list[0])
        prd_num = len(prd_list[0])

        rct_id_list = []
        prd_id_list = []
        for i in range(rct_num):
            temp_idx = self.df[1].index[self.df[1]["idx"] == rct_list[0][i]].tolist()[0]
            rct_id_list.append(self.df[1].iloc[temp_idx]["id"])
        for i in range(prd_num):
            temp_idx = self.df[1].index[self.df[1]["idx"] == prd_list[0][i]].tolist()[0]
            prd_id_list.append(self.df[1].iloc[temp_idx]["id"])

        src_position = []
        src_dimension = []
        dst_position = []
        dst_dimension = []
        for i in range(rct_num):
            temp_idx = self.df[1].index[self.df[1]["id"] == rct_id_list[i]].tolist()[0]
            src_position.append(self.df[1].iloc[temp_idx]["position"])
            src_dimension.append(self.df[1].iloc[temp_idx]["size"])
        for i in range(prd_num):
            temp_idx = self.df[1].index[self.df[1]["id"] == prd_id_list[i]].tolist()[0]
            dst_position.append(self.df[1].iloc[temp_idx]["position"])
            dst_dimension.append(self.df[1].iloc[temp_idx]["size"])
  
        for j in range(rct_num):
            center_x += src_position[j][0]+.5*src_dimension[j][0]
            center_y += src_position[j][1]+.5*src_dimension[j][1]
        for j in range(prd_num):
            center_x += dst_position[j][0]+.5*dst_dimension[j][0]
            center_y += dst_position[j][1]+.5*dst_dimension[j][1]
        center_x = center_x/(rct_num + prd_num) 
        center_y = center_y/(rct_num + prd_num)
        center_position = [center_x, center_y]
        handles = [center_position]
        for j in range(rct_num):
            src_handle_x = .5*(center_position[0] + src_position[j][0] + .5*src_dimension[j][0])
            src_handle_y = .5*(center_position[1] + src_position[j][1] + .5*src_dimension[j][1])
            handles.append([src_handle_x,src_handle_y])
        for j in range(prd_num):
            dst_handle_x = .5*(center_position[0] + dst_position[j][0] + .5*dst_dimension[j][0])
            dst_handle_y = .5*(center_position[1] + dst_position[j][1] + .5*dst_dimension[j][1])
            handles.append([dst_handle_x,dst_handle_y])
        # print('rct:', src_position, src_dimension)
        # print('prd:', dst_position, dst_dimension)
        # print("center:", center_position)
        # print("handle:", handles)
        self.df = editSBML._setReactionCenterPosition(self.df, id, center_position)        
        self.df = editSBML._setReactionBezierHandles(self.df, id, handles)

        #return self.df

    def setReactionFillColor(self, id, fill_color, opacity = 1.):
        """
        Set the reaction fill color.

        Args:  
            id: str-reaction id.

            fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

        Examples:
            setReactionFillColor ('J1', "BurlyWood")
        
        """
        self.df = editSBML._setReactionFillColor(self.df, id, fill_color, opacity)
        #return self.df


    def setReactionLineThickness(self, id, line_thickness):
        """
        Set the reaction line thickness.

        Args:  
            id: str-reaction id.

            line_thickness: float-reaction border line width.
        
        """
        self.df = editSBML._setReactionLineThickness(self.df, id, line_thickness)
        #return self.df

    def setReactionDashStyle(self, id, dash = []):
        """
        Set the reaction dash information with a certain reaction id.

        Args:  
            id: str-reaction id.

            dash: list-[] means solid; 
            [a,b] means drawing a a-point line and following a b-point gap and etc;
            [a,b,c,d] means drawing a a-point line and following a b-point gap, and then 
            drawing a c-point line followed by a d-point gap.

        Examples:
            To produce a dash such as - - - -, use setReactionDashStyle ('J1', [5,5,5,5]).
        
        """
        self.df = editSBML._setReactionDashStyle(self.df, id, dash)
        #return self.df

    def _setBezierReactionType(self, id, bezier = True):
        """
        Set the reaction type to use a Bezier curve depending on the Bezier flag. 

        Args:  
            id: str-reaction id.

            bezier: bool-bezier reaction (True as default) or not (False as straightline).
        
        """
        self.df = editSBML._setBezierReactionType(self.df, id, bezier)
        #return self.df

    def _setReactionArrowHeadPosition(self, id, position):

        """
        Set the reaction arrow head position with a certain reaction id.

        Args: 
            id: str-reaction id. 

            position: list or point.Point()
                
            list-
            [position_x, position_y], the coordinate represents the relative position of the 
            arrow head as an line ending.

            point.Point()-
            a Point object with attributes x and y representing
            the x/y position of the relative position of the arrow head as an line ending.

        Examples:
            setReactionArrowHeadPosition("r_0", [-12., -6.])
        
        """
        self.df = editSBML._setReactionArrowHeadPosition(self.df, id, position)
    
    # def setReactionArrowHeadSize(self, id, size):
    # #def setReactionArrowHeadSize(self, size):
    #     """
    #     Set the reaction arrow head size with a certain reaction id.

    #     Args:  
    #         size: list or point.Point()
                
    #         list-
    #         1*2 matrix-size of the arrow head [width, height].

    #         point.Point()-
    #         a Point object with attributes x and y representing the width and height of 
    #         the arrow head.

    #     Examples:
    #         setReactionArrowHeadSize("r_0", [50., 50.])
        
    #     """
    #     self.df = editSBML._setReactionArrowHeadSize(self.df, id, size)

    def setReactionArrowHeadSize(self, id, size):

        """
        Set the reaction arrow head size with a certain reaction id.

        Args: 
            id: str-reaction id. 

            size: list or point.Point()
                
            list-
            1*2 matrix-size of the arrow head [width, height].

            point.Point()-
            a Point object with attributes x and y representing the width and height of 
            the arrow head.

        Examples:
            setReactionArrowHeadSize("r_0", [12., 12.])
        
        """
        self.df = editSBML._setReactionArrowHeadSize(self.df, id, size)
    
    
    def setReactionArrowHeadFillColor(self, id, fill_color, opacity = 1.):

        """
        Set the reaction arrow head fill color with a certain reaction id.

        Args: 
            id: str-reaction id. 

            fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

        Examples:
            setReactionArrowHeadFillColor ('J1', "BurlyWood")
        
        """
        self.df = editSBML._setReactionArrowHeadFillColor(self.df, id, fill_color, opacity)
        #return self.df
        
    def setReactionArrowHeadShape(self, id, shape_type_list, shape_info_list):
        """
        Set shape(s) to a reaction arrow head by the shape info.

        Args:  
            id: str-node id.

            shape_type_list: list-list of shape_type.

            shape_type: str-polygon, ellipse, rectangle.

            shape_info_list: list-list of shape_info.

            shape_info: list-

            if polygon:
            [[x1,y1],[x2,y2],[x3,y3],etc], where x,y are floating numbers from 0 to 100.
            x represents the percentage of width, and y represents the percentage of height.
            
            if ellipse:
            [[cx, cy], [rx, ry]], where each number is a floating number from 0 to 100.
            c represent the center of the ellipse, and r represents its radii.
            
            if rectangle:
            []
            
        """
        self.df = editSBML._setReactionArrowHeadShape(self.df, id, shape_type_list, shape_info_list)
        #return self.df

    # def addText(self, txt_str, txt_position, txt_font_color = [0, 0, 0], opacity = 1., 
    #     txt_line_width = 1., txt_font_size = 12.):
    #     """
    #     Add arbitrary text onto canvas.

    #     Args:  
    #         txt_str: str-the text content.

    #         txt_position: list-[position_x, position_y], the coordinate represents the top-left hand 
    #         corner of the node text.

    #         txt_font_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

    #         opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

    #         txt_line_width: float-node text line width.

    #         txt_font_size: float-node text font size.
            
    #     """
    #     self.df_text = editSBML._addText(self.df_text, txt_str=txt_str, txt_position=txt_position, 
    #     txt_font_color=txt_font_color, opacity=opacity, txt_line_width=txt_line_width, 
    #     txt_font_size=txt_font_size) 
        
    #     return self.df_text


    # def removeText(self, txt_str):
    #     """
    #     Remove the arbitrary text from canvas.

    #     Args:  
    #         txt_str: str-the text content.
            
    #     """
    #     self.df_text = editSBML._removeText(self.df_text, txt_str=txt_str) 
        
    #     return self.df_text

    def _setReactionModifierHeadPosition(self, id, position, mod_idx = 0):

        """
        Set the reaction modifier head position with a certain reaction id.

        Args: 
            id: str-reaction id. 

            position: list or point.Point()
                
            list-
            [position_x, position_y], the coordinate represents the relative position of the 
            modifier head as an line ending.

            point.Point()-
            a Point object with attributes x and y representing
            the x/y position of the relative position of the modifier head as an line ending.

            mod_idx: int-the index of the modifier: 0 to number of modifiers -1.

        Examples:
            setReactionModifierHeadPosition("r_0", [-12., -6.])
        
        """
        mod_num = self.getReactionModifierNum(id)
        if type(mod_idx) == int and mod_idx >= 0 and mod_idx < mod_num:
            pass
        else:
            raise Exception("This is not a valid modifier index.")
        self.df = editSBML._setReactionModifierHeadPosition(self.df, id, position, mod_idx = mod_idx)
    
    def setReactionModifierHeadSize(self, id, size, mod_idx = 0):

        """
        Set the reaction modifier head size with a certain reaction id.

        Args: 
            id: str-reaction id. 

            size: list or point.Point()
                
            list-
            1*2 matrix-size of the modifier head [width, height].

            point.Point()-
            a Point object with attributes x and y representing the width and height of 
            the modifier head.

            mod_idx: int-the index of the modifier: 0 to number of modifiers -1.

        Examples:
            setReactionModifierHeadSize("r_0", [12., 12.])
        
        """
        mod_num = self.getReactionModifierNum(id)
        if type(mod_idx) == int and mod_idx >= 0 and mod_idx < mod_num:
            pass
        else:
            raise Exception("This is not a valid modifier index.")
        self.df = editSBML._setReactionModifierHeadSize(self.df, id, size, mod_idx = mod_idx)

    def setReactionModifierHeadFillColor(self, id, fill_color, opacity = 1., mod_idx = 0):

        """
        Set the reaction modifier head fill color with a certain reaction id.

        Args: 
            id: str-reaction id. 

            fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).
            
            mod_idx: int-the index of the modifier: 0 to number of modifiers -1.

        Examples:
            setReactionModifierHeadFillColor ('J1', "BurlyWood")
        
        """
        mod_num = self.getReactionModifierNum(id)
        if type(mod_idx) == int and mod_idx >= 0 and mod_idx < mod_num:
            pass
        else:
            raise Exception("This is not a valid modifier index.")
        self.df = editSBML._setReactionModifierHeadFillColor(self.df, id, fill_color, 
        opacity, mod_idx = mod_idx)
        #return self.df

    def setReactionModifierHeadShape(self, id, shape_type_list, shape_info_list, mod_idx = 0):
        """
        Set shape(s) to a reaction modifier head by the shape info.

        Args:  
            id: str-node id.

            shape_type_list: list-list of shape_type.

            shape_type: str-polygon, ellipse, rectangle.

            shape_info_list: list-list of shape_info.

            shape_info: list-

            if polygon:
            [[x1,y1],[x2,y2],[x3,y3],etc], where x,y are floating numbers from 0 to 100.
            x represents the percentage of width, and y represents the percentage of height.
            
            if ellipse:
            [[cx, cy], [rx, ry]], where each number is a floating number from 0 to 100.
            c represent the center of the ellipse, and r represents its radii.

            if rectangle:
            []

            mod_idx: int-the index of the modifier: 0 to number of modifiers -1.
            
        """
        mod_num = self.getReactionModifierNum(id)
        if type(mod_idx) == int and mod_idx >= 0 and mod_idx < mod_num:
            pass
        else:
            raise Exception("This is not a valid modifier index.")
        self.df = editSBML._setReactionModifierHeadShape(self.df, id, shape_type_list, 
        shape_info_list, mod_idx = mod_idx)
        #return self.df

    def getTextContent(self, txt_id):
        """
        Get the arbitrary text content with the text id.

        Args: 
            txt_id: str-the text id.

        Returns:
            txt_content: str-text content.
        
        """
        idx_list = self.df[3].index[self.df[3]["id"] == txt_id].tolist()
        txt_content_list =[]
        for i in range(len(idx_list)):
            txt_content_list.append(self.df[3].iloc[idx_list[i]]["txt_content"])

        if len(txt_content_list) == 1:
            txt_content = txt_content_list[0]
        else:
            raise Exception("This is not a valid id.")
        return txt_content

    def getTextPosition(self, txt_id):
        """
        Get the arbitrary text position with its id.

        Args: 
            txt_id: str-the id of the text.

        Returns: 
            position: a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the text.

        Examples: 
            p = sd.getTextPosition('text_id')
            
            print ('x = ', p.x, 'y = ', p.y)            

        """

        p = visualizeSBML._getTextPosition(self.df, txt_id)
        num_alias = len(p)
        position_list = []
        for alias in range(num_alias):
            position = point.Point (p[alias][0], p[alias][1])
            position_list.append(position)
        if len(position_list) == 1:
            position = position_list[0]
        else:
            raise Exception("This is not a valid id.")

        return position

    def getTextSize(self, txt_id):
        """
        Get the arbitrary text size with its text id.

        Args: 
            txt_id: str-the text id.

        Returns:
            txt_size: a Point object with attributes x and y representing
            the width and height of the text.

        Examples: 
            p = sd.getTextSize('text_id')

            print ('Width = ', p.x, 'Height = ', p.y)

        """

        p = visualizeSBML._getTextSize (self.df, txt_id)
        num_alias = len(p)
        txt_size_list = []
        for alias in range(num_alias):
            txt_size = point.Point (p[alias][0], p[alias][1])
            txt_size_list.append(txt_size)
        if len(txt_size_list) == 1:
            txt_size = txt_size_list[0]
        else:
            raise Exception("This is not a valid id.")
        return txt_size

    def getTextFontColor(self, txt_id):
        """
        Get the arbitrary text font color with its text id.

        Args: 
            txt_id: str-the text id.

        Returns:
            txt_font_color: list-[rgba 1*4 matrix, html_name str (if any, otherwise ''), 
            hex str (8 digits)].
        """

        idx_list = self.df[3].index[self.df[3]["id"] == txt_id].tolist()
        txt_font_color_list =[] 
        for i in range(len(idx_list)):
            rgb = self.df[3].iloc[idx_list[i]]["txt_font_color"]
            color = _rgb_to_color(rgb)
            txt_font_color_list.append(color)
        if len(txt_font_color_list) == 1:
            txt_font_color = txt_font_color_list[0]
        else:
            raise Exception("This is not a valid id.")

        return txt_font_color

    def getTextLineWidth(self, txt_id):
        """
        Get the arbitrary text line width with the text id.

        Args: 
            txt_id: str-the text id.

        Returns:
            txt_line_width: float-node text line width.
        
        """
        idx_list = self.df[3].index[self.df[3]["id"] == txt_id].tolist()
        txt_line_width_list =[] 
        for i in range(len(idx_list)):
            txt_line_width_list.append(self.df[3].iloc[idx_list[i]]["txt_line_width"])
        if len(txt_line_width_list) == 1:
            txt_line_width = txt_line_width_list[0]
        else:
            raise Exception("This is not a valid id.")

        return txt_line_width

    def getTextFontSize(self, txt_id):
        """
        Get the arbitrary text font size with the text id.

        Args: 
            txt_id: str-the text id.

        Returns:
            txt_font_size: float-text font size.
        
        """
        idx_list = self.df[3].index[self.df[3]["id"] == txt_id].tolist()
        txt_font_size_list =[]
        for i in range(len(idx_list)):
            txt_font_size_list.append(float(self.df[3].iloc[idx_list[i]]["txt_font_size"]))

        if len(txt_font_size_list) == 1:
            txt_font_size = txt_font_size_list[0]
        else:
            raise Exception("This is not a valid id.")
        return txt_font_size


    def setTextContent(self, txt_id, txt_content):
        """
        Set the arbitrary text content.

        Args:  
            txt_id: str-the text id.

            txt_content: str-the text content.
        
        """
        self.df = editSBML._setTextContent(self.df, txt_id, txt_content)
        #return self.df

    def setTextPosition(self, txt_id, txt_position):
        """
        Set the x,y coordinates of the arbitrary text position.

        Args:  
            txt_id: str-the text id.

            txt_position: list or point.Point()
                
            list-
            [txt_position_x, txt_position_y], the coordinate represents the top-left hand corner of 
            the node text.

            point.Point()-
            a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the text.

        """
        self.df = editSBML._setTextPosition(self.df, txt_id, txt_position)
        #return self.df

    def setTextSize(self, txt_id, txt_size):
        """
        Set the arbitrary text size.

        Args:  
            txt_id: str-the text id.

            txt_size: list or point.Point()
                
            list-
            1*2 matrix-size of the text [width, height].

            point.Point()-
            a Point object with attributes x and y representing the width and height of 
            the text.
        
        """
        self.df = editSBML._setTextSize(self.df, txt_id, txt_size)
        #return self.df

    def setTextFontColor(self, txt_id, txt_font_color, opacity = 1.):
        """
        Set the arbitrary text font color.

        Args:  
            txt_id: str-the text id.

            txt_font_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).
        
        """
        self.df = editSBML._setTextFontColor(self.df, txt_id, txt_font_color, opacity)
        #return self.df

    def setTextLineWidth(self, txt_id, txt_line_width):
        """
        Set the arbitrary text line width.

        Args:  
            txt_id: str-the text id.

            txt_line_width: float-node text line width.
        
        """
        self.df = editSBML._setTextLineWidth(self.df, txt_id, txt_line_width)
        #return self.df

    def setTextFontSize(self, txt_id, txt_font_size):
        """
        Set the arbitrary text font size.

        Args:  
            txt_id: str-the text id.

            txt_font_size: float-text font size.
        
        """
        self.df = editSBML._setTextFontSize(self.df, txt_id, txt_font_size)
        #return self.df

    def addText(self, txt_id, txt_content, txt_position, txt_size, txt_font_color = [0, 0, 0], opacity = 1., 
        txt_line_width = 1., txt_font_size = 12.):
        """
        Add arbitrary text onto canvas.

        Args: 
            txt_id: str-the text id.

            txt_content: str-the text content.

            txt_position: list or point.Point()
                
            list-
            [position_x, position_y], the coordinate represents the top-left hand corner of 
            the text.

            point.Point()-
            a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the text.

            txt_size: list or point.Point()
                
            list-
            1*2 matrix-size of the text [width, height].

            point.Point()-
            a Point object with attributes x and y representing the width and height of 
            the text.

            txt_font_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

            txt_line_width: float-text line width.

            txt_font_size: float-text font size.
            
        """
        self.df = editSBML._addText(self.df, txt_id=txt_id, txt_content=txt_content, txt_position=txt_position,
        txt_size = txt_size, txt_font_color=txt_font_color, opacity=opacity, txt_line_width=txt_line_width, 
        txt_font_size=txt_font_size) 
        
        #return self.df

    def removeText(self, txt_id):
        """
        Remove the arbitrary text from canvas.

        Args:  
            txt_id: str-the text id.
        """
        self.df = editSBML._removeText(self.df, txt_id = txt_id) 
        
        #return self.df

    def addRectangle(self, shape_name, position, size, fill_color = [255,255,255], fill_opacity = 1., 
        border_color = [0,0,0], border_opacity = 1., border_width = 2.):
        """
        Add a rectangle onto canvas.

        Args:  
            shape_name: str-the name of the rectangle.

            position: list or point.Point()
                
            list-
            [position_x, position_y], the coordinate represents the top-left hand corner of 
            the rectangle.

            point.Point()-
            a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the rectangle.

            size: list or point.Point()
                
            list-
            1*2 matrix-size of the rectangle [width, height].

            point.Point()-
            a Point object with attributes x and y representing the width and height of 
            the rectangle.

            fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            fill_opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

            border_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            border_opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

            border_width: float-node text line width.
            
        """
        self.df = editSBML._addRectangle(self.df, shape_name, position, size, fill_color=fill_color, 
        fill_opacity=fill_opacity, border_color=border_color, border_opacity = border_opacity,
        border_width=border_width) 
        
        #return self.df

    def addEllipse(self, shape_name, position, size, fill_color = [255,255,255], fill_opacity = 1., 
        border_color = [0,0,0], border_opacity = 1., border_width = 2.):
        """
        Add an ellipse onto canvas.

        Args:  
            shape_name: str-the name of the ellipse.

            position: list or point.Point()
                
            list-
            [position_x, position_y], the coordinate represents the top-left hand corner of 
            the ellipse.

            point.Point()-
            a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the ellipse.

            size: list or point.Point()
                
            list-
            1*2 matrix-size of the ellipse [width, height].

            point.Point()-
            a Point object with attributes x and y representing the width and height of 
            the ellipse.

            fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            fill_opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

            border_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            border_opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

            border_width: float-node text line width.
            
        """
        self.df = editSBML._addEllipse(self.df, shape_name, position, size, fill_color=fill_color, 
        fill_opacity=fill_opacity, border_color=border_color, border_opacity = border_opacity,
        border_width=border_width) 
        
        #return self.df

    def addPolygon(self, shape_name, shape_info, position, size, fill_color = [255,255,255], 
        fill_opacity = 1., border_color = [0,0,0], border_opacity = 1., border_width = 2.):
        """
        Add an ellipse onto canvas.

        Args:  
            shape_name: str-the name of the polygon.

            shape_info: list-[[x1,y1],[x2,y2],[x3,y3],etc], where x,y are floating numbers from 0 to 100.
            x represents the percentage of width, and y represents the percentage of height.

            position: list or point.Point()
                
            list-
            [position_x, position_y], the coordinate represents the top-left hand corner of 
            the Polygon.

            point.Point()-
            a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the polygon.

            size: list or point.Point()
                
            list-
            1*2 matrix-size of the polygon [width, height].

            point.Point()-
            a Point object with attributes x and y representing the width and height of 
            the Polygon.

            fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            fill_opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

            border_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

            border_opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

            border_width: float-node text line width.
            
        """
        self.df = editSBML._addPolygon(self.df, shape_name, shape_info, position, size, fill_color=fill_color, 
        fill_opacity=fill_opacity, border_color=border_color, border_opacity = border_opacity, 
        border_width=border_width) 
        
        #return self.df

    def removeShape(self, shape_name_str):
        """
        Remove the arbitrary shape from canvas.

        Args:  
            shape_name_str: str-the shape name.
        
        """
        self.df = editSBML._removeShape(self.df, shape_name_str = shape_name_str) 
        
        #return self.df


    def getShapePosition(self, shape_name_str):
        """
        Get the arbitrary shape position with its shape name.

        Args: 
            shape_name_str: str-the shape name of the arbitrary shape.

        Returns:
            position: a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the shape.

        Examples: 
            p = sd.getShapePosition('shape_name')

            print ('x = ', p.x, 'y = ', p.y)

        """

        p = visualizeSBML._getShapePosition(self.df, shape_name_str)
        num_alias = len(p)
        position_list = []
        for alias in range(num_alias):
            position = point.Point (p[alias][0], p[alias][1])
            position_list.append(position)
        if len(position_list) == 1:
            position = position_list[0]
        else:
            raise Exception("This is not a valid id.")
        return position

    def getShapeSize(self, shape_name_str):
        """
        Get the arbitrary shape size with its shape name.

        Args: 
            shape_name_str: str-the shape name.

        Returns:
            shape_size: a Point object with attributes x and y representing
            the width and height of the shape.

        Examples: 
            p = sd.getShapeSize('shape_name')

            print ('Width = ', p.x, 'Height = ', p.y)
        
        """

        p = visualizeSBML._getShapeSize (self.df, shape_name_str)
        num_alias = len(p)
        shape_size_list = []
        for alias in range(num_alias):
            shape_size = point.Point (p[alias][0], p[alias][1])
            shape_size_list.append(shape_size)
        if len(shape_size_list) == 1:
            shape_size = shape_size_list[0]
        else:
            raise Exception("This is not a valid id.")
        return shape_size


    def export(self):
        """
        This method returns the current model as an SBML string.

        Returns:
            SBMLStr_layout_render: str-the string of the output sbml file. 
        
        """
        sbml = exportSBML._DFToSBML(self.df, self.sbmlstr)
        return sbml

    def setColorStyle(self, style):
        """
        Set the color style.

        Args:
            style: can be either the "default" string or a new color class
        
        """
        if style == "default":
            self.color_style = styleSBML.Style(style_name="default")
        else:
            self.color_style = style
        #self.lineEnding_fill_color = self.color_style.getReactionLineColor()

    def getColorStyle(self):
        """
        Returns an object representing the current color style.

        Returns: 
            The current color style.
        
        Examples:
            la.getColorStyle().getStyleName()
        """
        return self.color_style

    def getColorStyleJson(self, filename = None):
        """
        Get the current color style in json format and save to a json file if need be.

        Returns:
            The current color style. in json format
        
        """
        if filename:
            out_file = open(filename, "w")
            json.dump(self.color_style.__dict__, out_file, indent=6)
        return json.dumps(self.color_style.__dict__)

    #def autolayout(self, layout="spring", scale=200., k=1., iterations=100, graphvizProgram = "dot"):
    def autolayout(self, layout="spring", scale=200., k=1., iterations=100):

        """
        Autolayout the node positions using networkX library.

        layout: str-the layout name from networkX, which can be one of the following:

            spring (default): positioning nodes using Fruchterman-Reingold force-directed algorithm;
        
            spectral: positioning the nodes using the eigenvectors of the graph Laplacian;

            random: positioning nodes randomly;
        
            circular: positioning nodes on a circle;

        scale (applies to "spring", "spectral", "circular"): float-Scale factor for positions. 
        The nodes are positioned in a box of size scale in each dim centered at center.
        
        k (applies to "spring"): float-Optimal distance between nodes. 
        Increase this value to move nodes farther apart.

        iterations (applies to "spring"): int-maximum number of iterations to use during the calculation.            

        """

        #warnings:
        if type(float(scale)) is not float or scale <= 0:
            raise Exception("Not valid scale")

        if type(float(k)) is not float or k <= 0:
            raise Exception("Not valid k")

        if type(iterations) is not int or iterations <= 0:
            raise Exception("Not valid iterations")

        if not self.hasLayout():
            sbmlStr = self.export()
            v_info = visualizeSBML._draw(sbmlStr,showImage=False,newStyle=self.color_style)
            edges = v_info.edges
            model = simplesbml.loadSBMLStr(sbmlStr)

            graph = nx.Graph()
            g = defaultdict(list)
            nodes = model.getListOfAllSpecies()
            reaction_ids = model.getListOfReactionIds()

            width, height = self.color_style.getImageSize()
            if scale == None:
                scale = max(width, height) // 2
            center = [width // 2, height // 2]

            # # Jessie:
            # for node in nodes:
            #     graph.add_node(node)
            # for edge in edges:
            #     src = edge[0]
            #     dests = edge[1:]
            #     for dest in dests:
            #         graph.add_edge(src, dest)
            #         g[src].append(dest)

            for node in nodes:
                graph.add_node(node)

            for rxn in reaction_ids:
                graph.add_node(rxn) #represent the reaction centroid as a node
                num_rct = model.getNumReactants(rxn)
                num_prd = model.getNumProducts(rxn)
                for i in range(num_rct):
                    rct = model.getReactant(rxn, i)
                    graph.add_edge(rct, rxn)
                for i in range(num_prd):
                    prd = model.getProduct(rxn, i)
                    graph.add_edge(rxn, prd)


            pos = defaultdict(list)

            if layout == "spring":
                pos = nx.spring_layout(graph, scale=scale, center=center, k=k, iterations=iterations)
            elif layout == "spectral":
                pos = nx.spectral_layout(graph, scale=scale, center=center)
            elif layout == "random":
                pos = nx.random_layout(graph, center=center)
            elif layout == "circular":
                pos = nx.circular_layout(graph, scale=scale, center=center)              
            # elif layout == "graphviz":
            #     pos = graphviz_layout(graph, prog = graphvizProgram)

            else:
                raise Exception("no such layout")

            for n, p in pos.items():
                if layout == "random":
                    p *= scale
                if type(p) is tuple:
                    p = list(p)
                else:
                    p = p.tolist()
                try:#node position
                    self.setNodeAndTextPosition(n, p)
                except:#reaction centroid position
                    self.setReactionCenterPosition(n, p)

            center_list = []
            handles_list = []
            line_width_list = []
            for id in reaction_ids:
                self.setReactionDefaultCenterAndHandlePositions(id)
                center_position = self.getReactionCenterPosition(id)
                handles = self.getReactionBezierHandles(id)
                center_list.append([center_position.x, center_position.y])
                handles_list_pre = []
                for i in range(len(handles)):
                    handles_list_pre.append([handles[i].x, handles[i].y])
                handles_list.append(handles_list_pre)
                line_width_list.append(self.getReactionLineThickness(id))
            
            # #overlap of centroids from different reactions
            # overlap_center_idx_list = []
            # for i in range(len(center_list)):
            #     for j in [x for x in range(len(center_list)) if x != i]:
            #         if [(center_list[i][0]-center_list[j][0])**2+(center_list[i][1]-center_list[j][1])**2]<=2*line_width_list[i]**2:
            #             if [i,j] not in overlap_center_idx_list and [j,i] not in overlap_center_idx_list:
            #                 overlap_center_idx_list.append([i,j])
            
            # for i in range(len(overlap_center_idx_list)):
            #     idx = overlap_center_idx_list[i][0]
            #     idx2 = overlap_center_idx_list[i][1]
            #     id = reaction_ids[idx]
            #     id2 = reaction_ids[idx2]
            #     center_position = center_list[idx]
            #     center_position2 = center_list[idx2]
            #     handle_rct1 = handles_list[idx][1]
            #     handle_rct1_2 = handles_list[idx2][1]
            #     handles = handles_list[idx]
            #     handles2 = handles_list[idx2]
            #     line_width = line_width_list[idx]
            #     radius = math.dist(center_position, handle_rct1)
            #     if radius != 0:
            #         theta = line_width/radius
            #         x = center_position[0] + theta*center_position[1]
            #         y = center_position[1] - theta*center_position[0]
            #         center_position_update = [x, y]
            #         handles_update = [center_position_update] + handles[1:]
            #         self.setReactionCenterPosition(id, center_position_update)
            #         self.setReactionBezierHandles(id, handles_update)
            #         radius2 = math.dist(center_position2, handle_rct1_2)
            #         if radius2 !=0 :
            #             theta2 = line_width/radius2
            #             x2 = center_position2[0] - theta2*center_position2[1]
            #             y2 = center_position2[1] + theta2*center_position2[0]
            #             center_position_2_update = [x2, y2]
            #             handles_update2 = [center_position_2_update] + handles2[1:]
            #             self.setReactionCenterPosition(id2, center_position_2_update)
            #             self.setReactionBezierHandles(id2, handles_update2)
            #overlap of handles from one reaction
            # for k in range(len(handles_list)):
            #     overlap_handles_idx_list = []
            #     for i in range(len(handles_list[k])):
            #         for j in [x for x in range(len(handles_list[k])) if x != i]:
            #             if [(handles_list[k][i][0]-handles_list[k][j][0])**2+(handles_list[k][i][1]-handles_list[k][j][1])**2]<=2*line_width_list[k]**2:
            #                 if [i,j] not in overlap_handles_idx_list and [j,i] not in overlap_handles_idx_list:
            #                     overlap_handles_idx_list.append([i,j])
            #     for i in range(len(overlap_handles_idx_list)):
            #         idx = overlap_handles_idx_list[i][0]
            #         idx2 = overlap_handles_idx_list[i][1]
            #         center_position = center_list[k]
            #         handle = handles_list[k][idx]
            #         handle2 = handles_list[k][idx2]
            #         id = reaction_ids[k]
            #         line_width = line_width_list[k]
            #         #print(center_position, handle, handle2, id, line_width)
            #         radius = math.dist(center_position, handle)
            #         if radius != 0:
            #             theta = line_width/radius
            #             x = handle[0] + theta*handle[1]
            #             y = handle[1] - theta*handle[0]
            #             handle_update = [x, y]
            #             radius2 = math.dist(center_position, handle2)   
            #             if radius2 != 0:
            #                 theta2 = line_width/radius
            #                 x2 = handle2[0] - theta2*handle2[1]
            #                 y2 = handle2[1] + theta2*handle2[0]
            #                 handle2_update = [x2, y2]
            #                 handles_update = handles_list[k]
            #                 handles_update[idx] = handle_update
            #                 handles_update[idx2] = handle2_update
            #                 self.setReactionBezierHandles(id, handles_update)

    def centroidOverLap(self):
        sbmlStr = self.export()
        model = simplesbml.loadSBMLStr(sbmlStr)
        reaction_ids = model.getListOfReactionIds()
        center_list = []
        handles_list = []
        line_width_list = []
        for id in reaction_ids:
            self.setReactionDefaultCenterAndHandlePositions(id)
            center_position = self.getReactionCenterPosition(id)
            handles = self.getReactionBezierHandles(id)
            center_list.append([center_position.x, center_position.y])
            handles_list_pre = []
            for i in range(len(handles)):
                handles_list_pre.append([handles[i].x, handles[i].y])
            handles_list.append(handles_list_pre)
            line_width_list.append(self.getReactionLineThickness(id))
        
        #overlap of centroids from different reactions
        overlap_center_idx_list = []
        for i in range(len(center_list)):
            for j in [x for x in range(len(center_list)) if x != i]:
                if [(center_list[i][0]-center_list[j][0])**2+(center_list[i][1]-center_list[j][1])**2]<=2*line_width_list[i]**2:
                    if [i,j] not in overlap_center_idx_list and [j,i] not in overlap_center_idx_list:
                        overlap_center_idx_list.append([i,j])
        
        for i in range(len(overlap_center_idx_list)):
            idx = overlap_center_idx_list[i][0]
            idx2 = overlap_center_idx_list[i][1]
            id = reaction_ids[idx]
            id2 = reaction_ids[idx2]
            center_position = center_list[idx]
            center_position2 = center_list[idx2]
            handle_rct1 = handles_list[idx][1]
            handle_rct1_2 = handles_list[idx2][1]
            handles = handles_list[idx]
            handles2 = handles_list[idx2]
            line_width = line_width_list[idx]
            radius = math.dist(center_position, handle_rct1)
            if radius != 0:
                theta = line_width/radius
                x = center_position[0] + theta*center_position[1]
                y = center_position[1] - theta*center_position[0]
                center_position_update = [x, y]
                handles_update = [center_position_update] + handles[1:]
                self.setReactionCenterPosition(id, center_position_update)
                self.setReactionBezierHandles(id, handles_update)
                radius2 = math.dist(center_position2, handle_rct1_2)
                if radius2 !=0 :
                    theta2 = line_width/radius2
                    x2 = center_position2[0] - theta2*center_position2[1]
                    y2 = center_position2[1] + theta2*center_position2[0]
                    center_position_2_update = [x2, y2]
                    handles_update2 = [center_position_2_update] + handles2[1:]
                    self.setReactionCenterPosition(id2, center_position_2_update)
                    self.setReactionBezierHandles(id2, handles_update2)

    def HandleOverLap(self):
        sbmlStr = self.export()
        model = simplesbml.loadSBMLStr(sbmlStr)
        reaction_ids = model.getListOfReactionIds()
        center_list = []
        handles_list = []
        line_width_list = []
        for id in reaction_ids:
            self.setReactionDefaultCenterAndHandlePositions(id)
            center_position = self.getReactionCenterPosition(id)
            handles = self.getReactionBezierHandles(id)
            center_list.append([center_position.x, center_position.y])
            handles_list_pre = []
            for i in range(len(handles)):
                handles_list_pre.append([handles[i].x, handles[i].y])
            handles_list.append(handles_list_pre)
            line_width_list.append(self.getReactionLineThickness(id))

        #overlap of handles from one reaction
        for k in range(len(handles_list)):
            overlap_handles_idx_list = []
            for i in range(len(handles_list[k])):
                for j in [x for x in range(len(handles_list[k])) if x != i]:
                    if [(handles_list[k][i][0]-handles_list[k][j][0])**2+(handles_list[k][i][1]-handles_list[k][j][1])**2]<=2*line_width_list[k]**2:
                        if [i,j] not in overlap_handles_idx_list and [j,i] not in overlap_handles_idx_list:
                            overlap_handles_idx_list.append([i,j])
            for i in range(len(overlap_handles_idx_list)):
                idx = overlap_handles_idx_list[i][0]
                idx2 = overlap_handles_idx_list[i][1]
                center_position = center_list[k]
                handle = handles_list[k][idx]
                handle2 = handles_list[k][idx2]
                id = reaction_ids[k]
                line_width = line_width_list[k]
                #print(center_position, handle, handle2, id, line_width)
                radius = math.dist(center_position, handle)
                if radius != 0:
                    theta = line_width/radius
                    x = handle[0] + theta*handle[1]
                    y = handle[1] - theta*handle[0]
                    handle_update = [x, y]
                    radius2 = math.dist(center_position, handle2)   
                    if radius2 != 0:
                        theta2 = line_width/radius
                        x2 = handle2[0] - theta2*handle2[1]
                        y2 = handle2[1] + theta2*handle2[0]
                        handle2_update = [x2, y2]
                        handles_update = handles_list[k]
                        handles_update[idx] = handle_update
                        handles_update[idx2] = handle2_update
                        self.setReactionBezierHandles(id, handles_update)


    def draw(self, setImageSize = [], scale = 1., output_fileName = '', 
        reactionLineType = 'bezier', showBezierHandles = False, 
        showReactionIds = False, showReversible = False, longText = 'auto-font'):

        """
        Draw to a PNG/JPG/PDF file.

        Args: 
            setImageSize: list-[] (default: default output size), or set by the users with a list
            containing two elements indicating the size of the image [width, height].

            scale: float-determines the figure output size = scale * default output size.
            Increasing the scale will make the resolution higher.

            output_fileName: str-filename: '' (default: will not save the file), 
            or eg 'fileName.png'. Allowable extensions include '.png', '.jpg', or '.pdf'.

            reactionLineType: str-type of the reaction line: 'straight' or 'bezier' (default).
            If there is no layout information from the SBML file, all reaction lines will look like
            straight lines even when using 'bezier' curves.

            showBezierHandles: bool-show the Bezier handles (True) or not (False as default).

            showReactionIds: bool-show the reaction ids (True) or not (False as default).

            showReversible: bool-show whether the reaction is reversible (True) or not (False as default).

            longText: str-'auto-font'(default) will automatically decrease the font size to fit the 
            current dimensions of the node; or 'ellipsis' will show '....' if the text is too long to fit the node.

        Examples: 
            sd.draw()

            sd.draw(output_fileName = 'output.pdf')

            sd.draw(setImageSize = [1000, 1000], output_fileName = 'output.png')

            sd.draw(scale = 2., output_fileName = 'output.jpg')

            sd.draw(output_fileName = 'output.png', reactionLineType = 'straight', longText = 'ellipsis')

            sd.draw(output_fileName = 'output.png', reactionLineType = 'bezier', showBezierHandles = True, showReactionIds = True, showReversible = True)

        """

        sbmlStr = self.export()
        visualizeSBML._draw(sbmlStr,  setImageSize = setImageSize, 
        scale = scale, output_fileName = output_fileName, 
        reactionLineType = reactionLineType, showBezierHandles = showBezierHandles, 
        showReactionIds = showReactionIds, showReversible = showReversible, longText = longText,
        newStyle = self.color_style)
        #df_text = self.df_text)

    def getNetworkTopLeftCorner(self):
        """
        Returns the top left-hand corner of the network from the SBML string.

        Returns:   
            position: a Point object with attributes x and y representing
            the x/y position of the top-left hand corner of the network.
        
        Examples:
            p = sd.getNetworkTopLeftConer()
                
            print(p.x, p.y)

        """ 
        sbmlStr = self.export()
        position  = visualizeSBML._getNetworkTopLeftCorner(sbmlStr)
        position = point.Point(position[0],position[1])
        return position

    def getNetworkBottomRightCorner(self):
        """
        Returns the bottom right-hand corner of the network from the SBML string.

        Returns:
            position: a Point object with attributes x and y representing
            the x/y position of the bottom-right hand corner of the network.

        Examples:
            p = sd.getNetworkBottomRightConer()
                
            print(p.x, p.y)
    
        """
        sbmlStr = self.export()
        position  = visualizeSBML._getNetworkBottomRightCorner(sbmlStr)
        position = point.Point(position[0],position[1])
        return position
    
    def getNetworkSize(self):
        """
        Returns the size of the network.

        Returns:
            size: a Point object with attributes x and y representing
            the width and height of the network.
        
        Examples: 
            p = sd.getNetworkSize()
            
            print ('Width = ', p.x, 'Height = ', p.y)

        """ 
        sbmlStr = self.export()
        size  = visualizeSBML._getNetworkSize(sbmlStr)
        size = point.Point(size[0],size[1])
        return size

    def getCompartmentIdList(self):
        """
        Returns the list of compartment ids.

        Returns:
            id_list-list of ids.
            
            id-str-compartment id.
        
        """ 

        id_list = self.df[0]["id"].tolist()
        return id_list

    def getNodeIdList(self):
        """
        Returns the list of node ids.

        Returns:
            id_list-list of ids.
            
            id-str-node id.
        
        """ 

        id_list = self.df[1]["id"].tolist()
        return id_list

    def getReactionIdList(self):
        """
        Returns the list of reaction ids.

        Returns:
            id_list-list of ids.
            
            id-str-reaction id.
        
        """ 

        id_list = self.df[2]["id"].tolist()
        return id_list

    def getTextIdList(self):
        """
        Returns a list of text id.

        Returns:
            txt_id_list-list of txt_id.
            
            txt_id-str-arbitrary text id.
        
        """ 

        txt_id_list = self.df[3]["id"].tolist()
        return txt_id_list

    def getShapeNameList(self):
        """
        Returns a list of possible shape names.

        Returns:
            shape_name_list-list of shape_name.
            
            shape_name-str-arbitrary shape name.
        
        """ 

        shape_name_list = self.df[4]["shape_name"].tolist()
        return shape_name_list

    def hasLayout(self):
        """
        Returns True if the current SBML model has layout/redner information.

        Returns:
            flag: bool-true (there is layout) or false (there is no layout). 
        """

        flag = True
        sbmlStr = self.sbmlstr
        document = libsbml.readSBMLFromString(sbmlStr)
        if document.getNumErrors() != 0:
            errMsgRead = document.getErrorLog().toString()
            raise Exception("Errors in SBML Model: ", errMsgRead)
        model_layout = document.getModel()
        try:
            mplugin = model_layout.getPlugin("layout")
            layout = mplugin.getLayout(0)
            if layout == None:
                flag = False
        except:
            flag = False

        return flag

    def exportGraphML(self, output_fileName = 'output'):
        """
        Export an output file in the basic GraphML format.
        
        Args:
            output_fileName: str - the exported GraphML file name (default: 'output').

        Returns:
            GraphML file. 

        """
    
        sbmlStr = self.export()
        model = simplesbml.loadSBMLStr(sbmlStr)

        graph = nx.DiGraph() #directed edges
        # g = defaultdict(list)
        nodes = model.getListOfAllSpecies()
        reaction_ids = model.getListOfReactionIds()

        pos = defaultdict(list)
        graph.add_nodes_from(pos.keys())
        for node in nodes:
            #pos_pt = self.getNodePosition(node)
            #position = [pos_pt.x,pos_pt.y]
            graph.add_node(node)

        for rxn_id in reaction_ids:
            graph.add_node(rxn_id) #represent the reaction centroid as a node
            num_rct = model.getNumReactants(rxn_id)
            num_prd = model.getNumProducts(rxn_id)
            for i in range(num_rct):
                rct = model.getReactant(rxn_id, i)
                graph.add_edge(rct, rxn_id)
            for i in range(num_prd):
                prd = model.getProduct(rxn_id, i)
                graph.add_edge(rxn_id, prd)

        nx.write_graphml_lxml(graph, output_fileName + ".graphml")

if __name__ == '__main__':
    DIR = os.path.dirname(os.path.abspath(__file__))
    TEST_FOLDER = os.path.join(DIR, "test_sbml_files")
    
    #filename = "test.xml" 
    #filename = "feedback.xml"
    #filename = "LinearChain.xml"
    #filename = "test_comp.xml"
    #filename = "test_no_comp.xml"
    #filename = "test_modifier.xml"
    #filename = "node_grid.xml"
    #filename = "mass_action_rxn.xml"
    #filename = "test_textGlyph.xml"
    #filename = "test_genGlyph.xml"

    #bioinformatics
    #filename = "test_suite/BIOMD0000000005/BIOMD0000000005.xml"
    #filename = "test_suite/BIOMD0000000005/BIOMD0000000005_layout_render.xml"
    #filename = "test_suite/pdmap-nulceoid/pdmap-nucleoid.xml"
    
    #gradient: 
    #filename = "test_suite/test_gradientLinear/test_gradientLinear.xml"
    #filename = "test_suite/test_gradientRadial/test_gradientRadial.xml"

    #long text and alias nodes
    #filename = "test_suite/Jana_WolfGlycolysis/Jana_WolfGlycolysis.xml"
    #filename = "test_suite/Jana_WolfGlycolysis/Jana_WolfGlycolysis-original.xml"
    #filename = "test_suite/Jana_WolfGlycolysis/Jana_WolfGlycolysis-corrected.xml"

    #sbml with errors
    #filename = "test_suite/sbml_error/testbigmodel.xml"

    #global render
    #filename = "test_suite/global_render/global_render.xml"

    #complex
    #filename = "test_suite/Carcione2020/Carcione2020.xml"
    #filename = "test_suite/Garde2020/Garde2020.xml"
    #filename = "test_suite/test_centroid/test_centroid.xml"

##############################
    #filename = 'output.xml'
    #filename = "save.xml"
    #filename = "Bart/bart_arccenter.xml"
    #filename = "Bart/bart_spRefBezier.xml"
    #filename = "Bart/bart2.xml"
    #filename = "Bart/newSBML.xml"
    #filename = "Bart/newSBML2.xml"
    #filename = "Bart/output.xml"

    #filename = "copasi_global/feedback_AssignRuleGlobalRender.xml"
    #filename = "copasi_global/oscili_V3COPASI.xml"

    #filename = "libSBNW/testWithLayout.xml"

    #filename = "Sauro-Coyote/branch1.xml"
    #filename = "Sauro-Coyote/branch1-straight.xml"
    #filename = "Sauro-Coyote/branch1-straight2.xml"
    #filename = "Sauro-Coyote/branch2.xml"
    #filename = "Sauro-Coyote/branch2-2.xml"
    #filename = "Sauro-Coyote/coyote.xml"
    #filename = "Sauro-Coyote/coyote2.xml"
    #filename = "Sauro-Coyote/cycle1-straight.xml"
    #filename = "Sauro-Coyote/cycle1-straight2.xml"
    #filename = "Sauro-Coyote/test.xml"
    #filename = "Sauro-Coyote/m2.xml"
    #filename = "Sauro-Coyote/small.xml"
    #filename = "Sauro-Coyote/ecoli.xml"

    #filename = "Adel/1.xml"
    #filename = "Adel/2.xml"
    #filename = "Adel/3.xml"

    #filename = "MK/sbmld10_2.sbml"

    #filename = "additional/BrusselatorWithOutJD.xml"
    #filename = "additional/BorisEJB_layoutrender.xml"
    #filename = "additional/m2.xml"
    #filename = "additional/small.xml"
    #filename = "additional/ecoli.xml"
    #filename = "additional/straight_line.xml"
    filename = "additional/E_coli_Millard2016.xml"

    

    f = open(os.path.join(TEST_FOLDER, filename), 'r')
    sbmlStr = f.read()
    f.close()


    # df_excel = _SBMLToDF(sbmlStr)
    # writer = pd.ExcelWriter('output.xlsx')
    # df_excel[0].to_excel(writer, sheet_name='CompartmentData')
    # df_excel[1].to_excel(writer, sheet_name='NodeData')
    # df_excel[2].to_excel(writer, sheet_name='ReactionData')
    # df_excel[3].to_excel(writer, sheet_name='ArbitraryTextData')
    # #df_excel[4].to_excel(writer, sheet_name='ArbitraryShapeData')
    # try:
    #     df_excel[4].to_excel(writer, sheet_name='ArbitraryShapeData')
    # except:
    #     print("did not return shapeData")
    # df_excel[5].to_excel(writer, sheet_name='LineEndingData')
    # df_excel[6].to_excel(writer, sheet_name='ReactionTextData')
    # writer.save()

    df = load(sbmlStr)
    #df = load(os.path.join(TEST_FOLDER, filename))
    #df = load("dfgdg")
    #la = load(sbmlStr)
    #df = load("XXXX.xml")

    # print(df.getCompartmentPosition("_compartment_default_"))
    # print(df.getCompartmentSize("_compartment_default_"))
    # print(df.getCompartmentFillColor("_compartment_default_"))
    # print(df.getCompartmentBorderColor("_compartment_default_"))
    # print(df.getCompartmentBorderWidth("_compartment_default_"))
    # print(df.getCompartmentTextPosition("_compartment_default_"))
    # print(df.getCompartmentTextSize("_compartment_default_"))
    # print(df.getCompartmentTextContent("_compartment_default_"))
    # print(df.getCompartmentTextFontColor("_compartment_default_"))
    # print(df.getCompartmentTextLineWidth("_compartment_default_"))
    # print(df.getCompartmentTextFontSize("_compartment_default_"))
    # print(df.getCompartmentTextAnchor("_compartment_default_"))
    # print(df.getCompartmentTextVAnchor("_compartment_default_"))

    # print(df.isFloatingNode("x_1"))
    # position = df.getNodePosition("x_1")
    # print(type(position) == type(point.Point()))
    # print(df.getNodePosition("x_0"))
    # print(df.getNodeSize("x_0"))
    # print(df.getNodeCenter("x_0"))
    # print(df.getNodeShape("x_0"))
    # print(df.getNodeTextPosition("x_0"))
    # print(df.getNodeTextSize("x_0"))
    # print(df.getNodeFillColor("Species_1"))
    # print(df.getNodeBorderColor("x_1"))
    # print(df.getNodeBorderWidth("x_1"))
    # print(df.getNodeTextContent("x_1"))
    # print(df.getNodeTextFontColor("x_1"))
    # print(df.getNodeTextLineWidth("x_1"))
    # print(df.getNodeTextFontSize("x_1"))
    # print(df.getNodeTextAnchor("x_1"))
    # print(df.getNodeTextVAnchor("x_1"))

    # print("center_position:", df.getReactionCenterPosition("r_0"))
    # print("handle_position:", df.getReactionBezierHandles("r_0"))
    # print(df.getReactionFillColor("r_0"))
    # print(df.getReactionLineThickness("r_0"))
    # print(df._isBezierReactionType("r_0"))
    # print(df.getReactionArrowHeadSize("r_0"))
    # print(df.getReactionDashStyle("r_0"))
    # print(df._getReactionArrowHeadPosition('path_0_re6338'))
    # print(df.getReactionArrowHeadSize('path_0_re6338'))
    # print(df.getReactionArrowHeadFillColor('path_0_re6338'))
    # print(df.getReactionArrowHeadShape('path_0_re6338'))
    # print(df.getReactionArrowHeadShape('path_0_re6337'))

    # print(df._getReactionArrowHeadPosition('r_0'))
    # print(df.getReactionArrowHeadSize('r_0'))
    # print(df.getReactionArrowHeadFillColor('r_0'))
    # print(df.getReactionArrowHeadShape('r_0'))

    # print(df.getReactionModifierNum('path_0_re6338'))
    # print(df._getReactionModifierHeadPosition('path_0_re6338', 2))
    # print(df.getReactionModifierHeadSize('path_0_re6338', 2))
    # print(df.getReactionModifierHeadFillColor('path_0_re6338'))
    # print(df.getReactionModifierHeadShape('path_0_re6338', 2))

    # df.setCompartmentPosition('_compartment_default_', [0,0])
    # df.setCompartmentSize('_compartment_default_', [1000, 1000])
    # df.setCompartmentFillColor('_compartment_default_', [255, 255, 255])
    # df.setCompartmentFillColor('_compartment_default_', 'ForestGreen')
    # df.setCompartmentFillColor('_compartment_default_', "#ff3456")
    # df.setCompartmentFillColor('_compartment_default_', "ForestGreen")
    # df.setCompartmentFillColor('c_0', 'coral')
    # print(df.getCompartmentFillColor('c_0'))
    # print(df.getCompartmentFillColor('_compartment_default_'))
    # df.setCompartmentBorderColor('_compartment_default_', [255, 255, 255])
    # df.setCompartmentBorderWidth('_compartment_default_', 2.)
    # print(df.getCompartmentTextPosition("_compartment_default_"))
    # print(df.getCompartmentTextSize("_compartment_default_"))
    # df.setCompartmentTextPosition('_compartment_default_', [10,10])
    # df.setCompartmentTextSize('_compartment_default_', [1000, 1000])
    # print(df.getCompartmentTextPosition("_compartment_default_"))
    # print(df.getCompartmentTextSize("_compartment_default_"))
    # df.setCompartmentTextContent('_compartment_default_', 'comp')
    # df.setCompartmentTextFontColor("_compartment_default_", 'red')
    # df.setCompartmentTextLineWidth("_compartment_default_", 10.)
    # df.setCompartmentTextFontSize("_compartment_default_", 10)
    # df.setCompartmentTextAnchor("_compartment_default_", "start")
    # df.setCompartmentTextVAnchor('_compartment_default_', 'bottom')

    # df.getNodeAliasNum("ATP")
    # df.setFloatingBoundaryNode("x_1", True)
    # df.setNodePosition("x_0", [100.0, 100.0])
    # df.setNodePosition("x_0", point.Point(100, 100))
    # df.setNodeTextPosition("x_3", [568.0, 229.0])
    # df.setNodeSize("x_1", [50.0, 30.0])
    # print(df.getNodeShape("x_0"))
    # df.setNodeShape("x_0",0)
    # df.setNodeShape("x_0","downTriangle")
    # df.setNodeArbitraryPolygonShape("x_0","self_triangle",[[0,0],[100,0],[0,100]])
    # df.setNodeShape("x_0","ellipse")
    # print(df.getNodeShape("x_0"))
    # df.setNodeTextPosition("x_1", [413., 216.])
    # df.moveNodeTextPosition("x_0", point.Point(0,0))
    # df.setNodeTextPositionCenter("x_0")
    # df.setNodeTextPositionLeftCenter("x_0")
    # df.setNodeTextPositionRightCenter("x_0")
    # df.setNodeTextPositionUpperCenter("x_0")
    # df.setNodeTextPositionLowerCenter("x_0")
    # df.setNodeTextPositionUpperLeft("x_0")
    # df.setNodeTextPositionUpperRight("x_0")
    # df.setNodeTextPositionLowerLeft("x_0")
    # df.setNodeTextPositionLowerRight("x_0")
    # df.setNodeTextPosition("x_0", [160., 107.])
    # print(df.getNodeTextPosition("x_0"))
    # df.setNodeTextSize("x_1", [100, 100])
    # df.setNodeFillColor("x_1", [255, 204, 153], opacity = 0.)
    #df.setNodeFillLinearGradient("Species_1", [[0.0, 0.0], [100.0, 100.0]], [[0.0, [255, 255, 255, 255]], [100.0, [192, 192, 192, 255]]])
    #df.setNodeFillLinearGradient("Species_1", [[0.0, 50.], [100.0, 50.0]],[[0.0, "red", 1.0], [100.0, "blue", 1.0]])
    #df.setNodeFillRadialGradient("Species_1", [[50.0, 50.0], [50.]], [[0.0, [255, 255, 255, 255]], [100.0, [0, 0, 0, 255]]])
    #df.setNodeFillRadialGradient("Species_1", [[50.0, 50.0], [50.]], [[0.0, "red", 1.0], [100.0, "blue", 1.0]])
    # print(df.getNodeFillColor("Species_1"))
    # df.setNodeBorderColor("x_1", [255, 108, 9])
    # print(df.getNodeBorderWidth("x_1"))
    # df.getNodeTextContent("x_1")
    # df.setNodeTextContent("x_1", "x1")
    # df.getNodeTextContent("x_1")
    # df.setNodeBorderWidth("x_0", 0.)
    # print(df.getNodeBorderWidth("x_1"))
    # df.setNodeTextFontColor("x_1", [0, 0, 0])
    # df.setNodeTextLineWidth("x_1", 1.)
    # print(df.getNodeTextFontSize("x_5"))
    # df.setNodeTextFontSize("x_5", 10)
    #print(df.getNodeTextAnchor("x_1"))
    #print(df.getNodeTextVAnchor("x_1"))
    #df.setNodeTextAnchor("x_1", "start")
    #df.setNodeTextVAnchor('x_1', 'bottom')
    #print(df.getNodeTextAnchor("x_1"))
    #print(df.getNodeTextVAnchor("x_1"))

    # df.setReactionFillColor("r_0", [91, 176, 253])
    # df.setReactionFillColor("r_0", [0, 0, 0])
    # df.setReactionLineThickness("r_0", 3.)
    # df._setBezierReactionType("r_0", True)
    # print(df.getReactionCenterPosition("r_0"))
    # print(df.getReactionCenterPosition("r_1"))
    # df.setReactionCenterPosition("r_0", [449.0, 200.0])
    # df.setReactionCenterPosition("r_1", [449.0, 278.0])
    # df.setReactionCenterPosition("r_0", [334.0, 232.0])
    # df.setReactionStraightLine("J1")
    # df.setReactionBezierHandles("r_0", [[334.0, 232.0], [386.0, 231.0], [282.0, 231.0]])
    # df.setReactionBezierHandles("r_0", [point.Point(334.0, 232.0), 
    # point.Point(386.0, 231.0), point.Point(282.0, 231.0)])
    # df.setReactionDefaultCenterAndHandlePositions("r_0")
    # df.setReactionDashStyle("r_0", [6,6])
    # print(df._getReactionArrowHeadPosition('path_0_re6338'))
    # df._setReactionArrowHeadPosition('path_0_re6338', [-12.,-7.])
    # print(df._getReactionArrowHeadPosition('path_0_re6338'))
    # print(df.getReactionArrowHeadSize('path_0_re6338'))
    # print(df.getReactionArrowHeadSize('path_0_re6338'))
    # df.setReactionArrowHeadSize('path_0_re6338', [12.,13.])
    # print(df.getReactionArrowHeadSize('path_0_re6338'))
    # print(df._getReactionArrowHeadPosition('path_0_re6338'))
    # print(df.getReactionArrowHeadFillColor('path_0_re6338'))
    # df.setReactionArrowHeadFillColor('path_0_re6338', "BurlyWood", opacity = 0.5)
    # print(df.getReactionArrowHeadFillColor('path_0_re6338'))
    # print(df._getReactionArrowHeadPosition('path_0_re6338'))
    # print(df.getReactionArrowHeadShape('path_0_re6338'))
    # df.setReactionArrowHeadShape('path_0_re6338', shape_type_list=['polygon'],
    # shape_info_list=[[[0.0, 0.0], [100.0, 60.0], [0.0, 100.0], [0.0, 0.0]]])
    # df.setReactionArrowHeadShape('path_0_re6338', shape_type_list=['ellipse'],
    # shape_info_list=[[[0.0, 0.0], [100.0, 100.0]]])
    # df.setReactionArrowHeadShape('path_0_re6338', shape_type_list=['polygon', 'polygon'],
    # shape_info_list=[[[33.0, 0.0], [100.0, 50.0], [33.0, 100.0], [33.0, 0.0]], [[0.0, 0.0], [0.0, 100.0]]])
    # print(df.getReactionArrowHeadShape('path_0_re6338'))
    # print(df._getReactionArrowHeadPosition('path_0_re6338'))
    # print(df._getReactionModifierHeadPosition('path_0_re6338', 2))
    # df._setReactionModifierHeadPosition('path_0_re6338', [-12.,-7.], 2)
    # print(df._getReactionModifierHeadPosition('path_0_re6338', 0))
    # print("position:", df._getReactionModifierHeadPosition('path_0_re6338'))
    # print('size:', df.getReactionModifierHeadSize('path_0_re6338'))
    # df.setReactionModifierHeadSize('path_0_re6338', [12.,13.], 2)
    # print("size_after:", df.getReactionModifierHeadSize('path_0_re6338', 2))
    # print('size:', df.getReactionModifierHeadSize('r_0'))
    # df.setReactionModifierHeadSize('r_0', [12.,12.])
    # print("size_after:", df.getReactionModifierHeadSize('r_0'))
    # print("position_after:", df._getReactionModifierHeadPosition('path_0_re6338'))
    # print(df._getReactionModifierHeadPosition('path_0_re6338'))
    # print(df.getReactionModifierHeadFillColor('path_0_re6338', 2))
    # df.setReactionModifierHeadFillColor('path_0_re6338', "BurlyWood", opacity = 0.5, mod_idx = 2)
    # print(df.getReactionModifierHeadFillColor('path_0_re6338', 2))
    # print(df._getReactionModifierHeadPosition('path_0_re6338'))
    # print(df._getReactionModifierHeadPosition('path_0_re6338'))
    # print(df.getReactionModifierHeadShape('path_0_re6338'))
    # df.setReactionModifierHeadShape('path_0_re6338', shape_type_list=['polygon'],
    # shape_info_list=[[[0.0, 0.0], [100.0, 60.0], [0.0, 100.0], [0.0, 0.0]]], mod_idx = 2)
    # df.setReactionModifierHeadShape('path_0_re6338', shape_type_list=['polygon', 'polygon'],
    # shape_info_list=[[[33.0, 0.0], [100.0, 50.0], [33.0, 100.0], [33.0, 0.0]], [[0.0, 0.0], [0.0, 100.0]]])
    # print(df.getReactionModifierHeadShape('path_0_re6338'))
    # print(df._getReactionModifierHeadPosition('path_0_re6338'))


    # df.addText("test_id", "test", [413,216], [50,30])
    # df.addText("test1_id", "test1", [400,200], [100, 100], txt_font_color="blue", 
    # opacity= 0.5, txt_line_width=2, txt_font_size=13)
    # df.removeText("test_id")
    # print(df.getTextContent("TextGlyph_01"))
    # print(df.getTextPosition("TextGlyph_01"))
    # print(df.getTextSize("TextGlyph_01"))
    # print(df.getTextFontColor("TextGlyph_01"))
    # print(df.getTextLineWidth("TextGlyph_01"))
    # print(df.getTextFontSize("TextGlyph_01"))
    # df.setTextContent("TextGlyph_01", "update_text")
    # df.setTextPosition("TextGlyph_01", [413., 216.])
    # df.setTextSize("TextGlyph_01", [100, 100])
    # df.setTextFontColor("TextGlyph_01", "red")
    # df.setTextLineWidth("TextGlyph_01", 3.)
    # df.setTextFontSize("TextGlyph_01", 15)


    # df.addRectangle("selfRectangle", [400,200], [100, 100])
    # df.addEllipse("selfEllipse", [400,200], [70, 100], fill_color = "red", fill_opacity = 0.5, 
    # border_color="blue", border_width = 3.)
    # df.addPolygon("self_triangle", [[0,0],[100,0],[0,100]], [400,200], [70, 100])
    # df.removeShape("shape_name")

    # print("NetworkSize:", df.getNetworkSize())
    # print("NetworkBottomRight:", df.getNetworkBottomRightCorner())
    # print("NetworkTopLeft", df.getNetworkTopLeftCorner())

    # print(df.getNodeIdList())
    # print(df.getReactionIdList())
    # print(df.getTextIdList())
    # print(df.getCompartmentIdList())

    #print(df.hasLayout())

    # sbmlStr_layout_render = df.export()
    # f = open("output.xml", "w")
    # f.write(sbmlStr_layout_render)
    # f.close()
    
    # with open('output.xml', 'w') as f:
    #   f.write(sbmlStr_layout_render)   

    #df.draw(reactionLineType='bezier', scale = 2.)
    #df.autolayout(layout = 'graphviz', graphvizProgram = 'dot')
    #df.autolayout()
    #df.autolayout(scale = 400, k = 2)

    
    # import tellurium as te

    # r = te.loada ('''
    # A -> B; v; B -> A; v;
    # v = 0
    # ''')

    # r = te.loada ('''
    # S1 + S2 -> S2; v;
    # v = 0
    # ''')

    # df = load(r.getSBML())
    # df.autolayout(layout = "circular", scale = 500)
    # df.draw(output_fileName = 'output.png')

    sbmlStr_layout_render = df.export()
    f = open("output.xml", "w")
    f.write(sbmlStr_layout_render)
    f.close()

    # df.draw(output_fileName = 'output.png', longText = 'ellipsis')
    df.draw(output_fileName = 'output.png')
    # df.draw(setImageSize = [1000, 1000], scale = 1., output_fileName = 'output.png', 
    #     reactionLineType = 'bezier', showBezierHandles = False, 
    #    showReactionIds = False, showReversible = False, longText = 'auto-font')

    #df.exportGraphML()

    #s4 -> does not work
    # import tellurium as te

    # r = te.loada ('''
    #   $Xo -> S1; k1*Xo
    #    S1 -> S2; k1*S1
    #    S2 -> S3; k1*S2
    #    S3 -> S4; k1*S3
    #    S4 ->;    k1*S3
    #    Xo = 5
    #    k1 = 0.4''')
    # sb = load(r.getSBML())
    # #sb.autolayout()
    # sb.draw(output_fileName = 'output.png')


