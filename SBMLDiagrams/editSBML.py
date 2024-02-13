# -*- coding: utf-8 -*-
# This script was written by Jin Xu and available on Github
# https://github.com/SunnyXu/SBMLDiagrams

"""
Created on Mon Aug 23 13:25:34 2021
@author: Jin Xu
"""

#from numpy.core.fromnumeric import shape
import pandas as pd
import os
from SBMLDiagrams import processSBML
from SBMLDiagrams import point

color_data = {"decimal_rgb": ['[240,248,255]', '[250,235,215]', '[0,255,255]', '[127,255,212]', '[240,255,255]', '[245,245,220]', '[255,228,196]', '[0,0,0]', '[255,235,205]', '[0,0,255]', '[138,43,226]', '[165,42,42]', '[222,184,135]', '[95,158,160]', '[127,255,0]', '[210,105,30]', '[255,127,80]', '[100,149,237]', '[255,248,220]', '[220,20,60]', '[0,255,255]', '[0,0,139]', '[0,139,139]', '[184,134,11]', '[169,169,169]', '[0,100,0]', '[189,183,107]', '[139,0,139]', '[85,107,47]', '[255,140,0]', '[153,50,204]', '[139,0,0]', '[233,150,122]', '[143,188,143]', '[72,61,139]', '[47,79,79]', '[0,206,209]', '[148,0,211]', '[255,20,147]', '[0,191,255]', '[105,105,105]', '[30,144,255]', '[178,34,34]', '[255,250,240]', '[34,139,34]', '[255,0,255]', '[220,220,220]', '[248,248,255]', '[255,215,0]', '[218,165,32]', '[128,128,128]', '[0,128,0]', '[173,255,47]', '[240,255,240]', '[255,105,180]', '[205,92,92]', '[75,0,130]', '[255,255,240]', '[240,230,140]', '[230,230,250]', '[255,240,245]', '[124,252,0]', '[255,250,205]', '[173,216,230]', '[240,128,128]', '[224,255,255]', '[250,250,210]', '[144,238,144]', '[211,211,211]', '[255,182,193]', '[255,160,122]', '[32,178,170]', '[135,206,250]', '[119,136,153]', '[176,196,222]', '[255,255,224]', '[0,255,0]', '[50,205,50]', '[250,240,230]', '[255,0,255]', '[128,0,0]', '[102,205,170]', '[0,0,205]', '[186,85,211]', '[147,112,219]', '[60,179,113]', '[123,104,238]', '[0,250,154]', '[72,209,204]', '[199,21,133]', '[25,25,112]', '[245,255,250]', '[255,228,225]', '[255,228,181]', '[255,222,173]', '[0,0,128]', '[253,245,230]', '[128,128,0]', '[107,142,35]', '[255,165,0]', '[255,69,0]', '[218,112,214]', '[238,232,170]', '[152,251,152]', '[175,238,238]', '[219,112,147]', '[255,239,213]', '[255,218,185]', '[205,133,63]', '[255,192,203]', '[221,160,221]', '[176,224,230]', '[128,0,128]', '[255,0,0]', '[188,143,143]', '[65,105,225]', '[139,69,19]', '[250,128,114]', '[244,164,96]', '[46,139,87]', '[255,245,238]', '[160,82,45]', '[192,192,192]', '[135,206,235]', '[106,90,205]', '[112,128,144]', '[255,250,250]', '[0,255,127]', '[70,130,180]', '[210,180,140]', '[0,128,128]', '[216,191,216]', '[255,99,71]', '[64,224,208]', '[238,130,238]', '[245,222,179]', '[255,255,255]', '[245,245,245]', '[255,255,0]', '[154,205,50]'],\
    "html_name":['AliceBlue', 'AntiqueWhite', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque', 'Black', 'BlanchedAlmond', 'Blue', 'BlueViolet', 'Brown', 'BurlyWood', 'CadetBlue', 'Chartreuse', 'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan', 'DarkBlue', 'DarkCyan', 'DarkGoldenrod', 'DarkGray', 'DarkGreen', 'DarkKhaki', 'DarkMagenta', 'DarkOliveGreen', 'DarkOrange', 'DarkOrchid', 'DarkRed', 'DarkSalmon', 'DarkSeaGreen', 'DarkSlateBlue', 'DarkSlateGray', 'DarkTurquoise', 'DarkViolet', 'DeepPink', 'DeepSkyBlue', 'DimGray', 'DodgerBlue', 'FireBrick', 'FloralWhite', 'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'Goldenrod', 'Gray', 'Green', 'GreenYellow', 'Honeydew', 'HotPink', 'IndianRed', 'Indigo', 'Ivory', 'Khaki', 'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue', 'LightCoral', 'LightCyan', 'LightGoldenrodYellow', 'LightGreen', 'LightGrey', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue', 'LightSlateGray', 'LightSteelBlue', 'LightYellow', 'Lime', 'LimeGreen', 'Linen', 'Magenta', 'Maroon', 'MediumAquamarine', 'MediumBlue', 'MediumOrchid', 'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen', 'MediumTurquoise', 'MediumVioletRed', 'MidnightBlue', 'MintCream', 'MistyRose', 'Moccasin', 'NavajoWhite', 'Navy', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed', 'Orchid', 'PaleGoldenrod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed', 'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple', 'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Salmon', 'SandyBrown', 'SeaGreen', 'Seashell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue', 'SlateGray', 'Snow', 'SpringGreen', 'SteelBlue', 'Tan', 'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White', 'WhiteSmoke', 'Yellow', 'YellowGreen'],\
    "hex_string":['#F0F8FF', '#FAEBD7', '#00FFFF', '#7FFFD4', '#F0FFFF', '#F5F5DC', '#FFE4C4', '#000000', '#FFEBCD', '#0000FF', '#8A2BE2', '#A52A2A', '#DEB887', '#5F9EA0', '#7FFF00', '#D2691E', '#FF7F50', '#6495ED', '#FFF8DC', '#DC143C', '#00FFFF', '#00008B', '#008B8B', '#B8860B', '#A9A9A9', '#006400', '#BDB76B', '#8B008B', '#556B2F', '#FF8C00', '#9932CC', '#8B0000', '#E9967A', '#8FBC8F', '#483D8B', '#2F4F4F', '#00CED1', '#9400D3', '#FF1493', '#00BFFF', '#696969', '#1E90FF', '#B22222', '#FFFAF0', '#228B22', '#FF00FF', '#DCDCDC', '#F8F8FF', '#FFD700', '#DAA520', '#808080', '#008000', '#ADFF2F', '#F0FFF0', '#FF69B4', '#CD5C5C', '#4B0082', '#FFFFF0', '#F0E68C', '#E6E6FA', '#FFF0F5', '#7CFC00', '#FFFACD', '#ADD8E6', '#F08080', '#E0FFFF', '#FAFAD2', '#90EE90', '#D3D3D3', '#FFB6C1', '#FFA07A', '#20B2AA', '#87CEFA', '#778899', '#B0C4DE', '#FFFFE0', '#00FF00', '#32CD32', '#FAF0E6', '#FF00FF', '#800000', '#66CDAA', '#0000CD', '#BA55D3', '#9370DB', '#3CB371', '#7B68EE', '#00FA9A', '#48D1CC', '#C71585', '#191970', '#F5FFFA', '#FFE4E1', '#FFE4B5', '#FFDEAD', '#000080', '#FDF5E6', '#808000', '#6B8E23', '#FFA500', '#FF4500', '#DA70D6', '#EEE8AA', '#98FB98', '#AFEEEE', '#DB7093', '#FFEFD5', '#FFDAB9', '#CD853F', '#FFC0CB', '#DDA0DD', '#B0E0E6', '#800080', '#FF0000', '#BC8F8F', '#4169E1', '#8B4513', '#FA8072', '#F4A460', '#2E8B57', '#FFF5EE', '#A0522D', '#C0C0C0', '#87CEEB', '#6A5ACD', '#708090', '#FFFAFA', '#00FF7F', '#4682B4', '#D2B48C', '#008080', '#D8BFD8', '#FF6347', '#40E0D0', '#EE82EE', '#F5DEB3', '#FFFFFF', '#F5F5F5', '#FFFF00', '#9ACD32']}
df_color = pd.DataFrame(color_data)
#DIR = os.path.dirname(os.path.abspath(__file__))
#df_color = pd.read_csv(os.path.join(DIR, 'colors.txt'), sep="\t")
df_color["html_name"] = df_color["html_name"].str.lower()

def _color_to_rgb(color, opacity):
    def _hex_to_rgb(value):
        value = value.lstrip('#')
        return [int(value[i:i+2], 16) for i in (0, 2, 4)]

    #rgba
    rgb = []
    if isinstance(color, list) and len(color) == 3:
        rgb = color.copy()
    elif isinstance(color, str):
        if '#' in color and len(color) == 7: #hex_string
            rgb = _hex_to_rgb(color)
        else: #html_name
            if color.lower() in df_color.values:
                index = df_color.index[df_color["html_name"] == color.lower()].tolist()[0] #row index 
                rgb_pre = df_color.iloc[index]["decimal_rgb"]
                rgb_pre = rgb_pre[1:-1].split(",")
                rgb = [int(x) for x in rgb_pre]

    if rgb == [] or opacity > 1. or opacity < 0.:
        raise ValueError('Please enter a color or/and opacity in a valid format!')
    else:
        rgba = rgb.copy()
        rgba.append(int(opacity*255/1.))
    return rgba

def _setCompartmentPosition(df, id, position):

    """
    Set the x,y coordinates of the compartment position.

    Args:  
        df: DataFrame-initial information.

        id: str-compartment id.

        position: list or point.Point()
            
        list-
        [position_x, position_y], the coordinate represents the top-left hand corner of 
        the compartment.

        point.Point()-
        a Point object with attributes x and y representing
        the x/y position of the top-left hand corner of the compartment.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_CompartmentData_temp = df[0].copy()
    idx_list = df[0].index[df[0]["id"] == id].tolist() 
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    if type(position) != list and type(position) != type(point.Point()):
        raise Exception("Please enter a valid position type.")
    if type(position) == type(point.Point()):
        position = [position.x, position.y]
    for i in range(len(idx_list)):
        df_CompartmentData_temp.at[idx_list[i],"position"] = position
    df_temp = (df_CompartmentData_temp, df[1], df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setCompartmentSize(df, id, size):

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

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_CompartmentData_temp = df[0].copy()   
    idx_list = df[0].index[df[0]["id"] == id].tolist() 
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.") 
    if type(size) != list and type(size) != type(point.Point()):
        raise Exception("Please enter a valid size type.")
    if type(size) == type(point.Point()):
        size = [size.x, size.y]
    for i in range(len(idx_list)):
        df_CompartmentData_temp.at[idx_list[i],"size"] = size
    df_temp = (df_CompartmentData_temp, df[1], df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setCompartmentFillColor(df, id, fill_color, opacity):

    """
    Set the compartment fill color

    Args:  
        df: DataFrame-initial information.

        id: str-compartment id.

        fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

        opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_CompartmentData_temp = df[0].copy()      
    idx_list = df[0].index[df[0]["id"] == id].tolist() 
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    fill_color = _color_to_rgb(fill_color, opacity)
    for i in range(len(idx_list)):
        df_CompartmentData_temp.at[idx_list[i],"fill_color"] = fill_color
    df_temp = (df_CompartmentData_temp, df[1], df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setCompartmentBorderColor(df, id, border_color, opacity):

    """
    Set the compartment border color.

    Args:  
        df: DataFrame-initial information.

        id: str-compartment id.

        border_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

        opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """

    df_CompartmentData_temp = df[0].copy()
    idx_list = df[0].index[df[0]["id"] == id].tolist() 
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    border_color = _color_to_rgb(border_color, opacity)
    for i in range(len(idx_list)):
        df_CompartmentData_temp.at[idx_list[i],"border_color"] = border_color
    df_temp = (df_CompartmentData_temp, df[1], df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setCompartmentBorderWidth(df, id, border_width):

    """
    Set the compartment border width.

    Args:  
        df: DataFrame-initial information.

        id: str-compartment id.

        border_width: float-compartment border line width.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_CompartmentData_temp = df[0].copy()
    idx_list = df[0].index[df[0]["id"] == id].tolist() 
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")  
    for i in range(len(idx_list)):
        df_CompartmentData_temp.at[idx_list[i],"border_width"] = border_width  
    df_temp = (df_CompartmentData_temp, df[1], df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setCompartmentTextPosition(df, id, position):

    """
    Set the x,y coordinates of the compartment text position.

    Args:  
        df: DataFrame-initial information.

        id: str-compartment id.

        position: list or point.Point()
            
        list-
        [position_x, position_y], the coordinate represents the top-left hand corner of 
        the compartment.

        point.Point()-
        a Point object with attributes x and y representing
        the x/y position of the top-left hand corner of the compartment.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_CompartmentData_temp = df[0].copy()
    idx_list = df[0].index[df[0]["id"] == id].tolist() 
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    if type(position) != list and type(position) != type(point.Point()):
        raise Exception("Please enter a valid position type.")
    if type(position) == type(point.Point()):
        position = [position.x, position.y]
    for i in range(len(idx_list)):
        df_CompartmentData_temp.at[idx_list[i],"txt_position"] = position
    df_temp = (df_CompartmentData_temp, df[1], df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setCompartmentTextSize(df, id, size):

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

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_CompartmentData_temp = df[0].copy()   
    idx_list = df[0].index[df[0]["id"] == id].tolist() 
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.") 
    if type(size) != list and type(size) != type(point.Point()):
        raise Exception("Please enter a valid size type.")
    if type(size) == type(point.Point()):
        size = [size.x, size.y]
    for i in range(len(idx_list)):
        df_CompartmentData_temp.at[idx_list[i],"txt_size"] = size
    df_temp = (df_CompartmentData_temp, df[1], df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setCompartmentTextContent(df, id, txt_content):

    """
    Set the compartment text content.

    Args:  
        df: DataFrame-initial information.

        id: str-compartment id.

        txt_content: str-compartment text content.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_CompartmentData_temp = df[0].copy()
    idx_list = df[0].index[df[0]["id"] == id].tolist()
    if len(idx_list) != 1:
        raise Exception("This is not a valid id.")
    else:
        df_CompartmentData_temp.at[idx_list[0],"txt_content"] = txt_content

    df_temp = (df_CompartmentData_temp, df[1], df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setCompartmentTextFontColor(df, id, txt_font_color, opacity):

    """
    Set the compartment text font color.

    Args:  
        df: DataFrame-initial information.

        id: str-compartment id.

        txt_font_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

        opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_CompartmentData_temp = df[0].copy()
    idx_list = df[0].index[df[0]["id"] == id].tolist()
    if len(idx_list) != 1:
        raise Exception("This is not a valid id.")
    else:
        txt_font_color = _color_to_rgb(txt_font_color, opacity)
        df_CompartmentData_temp.at[idx_list[0],"txt_font_color"] = txt_font_color

    df_temp = (df_CompartmentData_temp, df[1], df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setCompartmentTextLineWidth(df, id, txt_line_width):

    """
    Set the compartment text line width (the stroke width value of the TEXTGLYPH).

    Args:  
        df: DataFrame-initial information.

        id: str-compartment id.

        txt_line_width: float-compartment text line width.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_CompartmentData_temp = df[0].copy()
    idx_list = df[0].index[df[0]["id"] == id].tolist()
    if len(idx_list) != 1:
        raise Exception("This is not a valid id.")
    else:
        df_CompartmentData_temp.at[idx_list[0],"txt_line_width"] = txt_line_width

    df_temp = (df_CompartmentData_temp, df[1], df[2], df[3], df[4], df[5], df[6])

    return df_temp


def _setCompartmentTextFontSize(df, id, txt_font_size):

    """
    Set the compartment text font size.

    Args:  
        df: DataFrame-initial information.

        id: str-compartment id.

        txt_font_size: float-compartment text font size.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_CompartmentData_temp = df[0].copy()
    idx_list = df[0].index[df[0]["id"] == id].tolist()
    if len(idx_list) != 1:
        raise Exception("This is not a valid id.")
    else:
        df_CompartmentData_temp.at[idx_list[0],"txt_font_size"] = txt_font_size

    df_temp = (df_CompartmentData_temp, df[1], df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setCompartmentTextAnchor(df, id, txt_anchor):

    """
    Set the compartment text horizontal anchor.

    Args:  
        df: DataFrame-initial information.

        id: str-compartment id.

        txt_anchor: str-compartment text horizontal anchor, which can be "start",
            "middle" and "end".

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_CompartmentData_temp = df[0].copy()
    idx_list = df[0].index[df[0]["id"] == id].tolist()
    if len(idx_list) != 1:
        raise Exception("This is not a valid id.")
    else:
        txt_vanchor = df_CompartmentData_temp.at[idx_list[0],"txt_anchor"][1]
        df_CompartmentData_temp.at[idx_list[0],"txt_anchor"] = [txt_anchor, txt_vanchor]

    if txt_anchor not in ['start', 'middle', 'end']:
        raise Exception("Please enter a valid horizontal anchor.")

    df_temp = (df_CompartmentData_temp, df[1], df[2], df[3], df[4], df[5], df[6])

    return df_temp


def _setCompartmentTextVAnchor(df, id, txt_vanchor):

    """
    Set the compartment text vertical anchor.

    Args:  
        df: DataFrame-initial information.

        id: str-compartment id.

        txt_vanchor: str-compartment text horizontal anchor, which can be which can be "top", 
            "middle", "baseline" and "bottom".

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_CompartmentData_temp = df[0].copy()
    idx_list = df[0].index[df[0]["id"] == id].tolist()
    if len(idx_list) != 1:
        raise Exception("This is not a valid id.")
    else:
        txt_anchor = df_CompartmentData_temp.at[idx_list[0],"txt_anchor"][0]
        df_CompartmentData_temp.at[idx_list[0],"txt_anchor"] = [txt_anchor, txt_vanchor]

    if txt_vanchor not in ['top', 'middle', 'baseline', 'bottom']:
        raise Exception("Please enter a valid vertical anchor.")


    df_temp = (df_CompartmentData_temp, df[1], df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setFloatingBoundaryNode(df, id, floating_node, alias = 0):

    """
    Set a node to be floating node (True) or boundary node (False).

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        floating_node: bool-floating node (True) or not (False).

        alias: int-alias node index [0, num_alias).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    # for i in range(len(idx_list)):
    #     df_NodeData_temp.at[idx_list[i],"floating_node"] = floating_node
    if alias < len(idx_list) and alias >= 0:
        df_NodeData_temp.at[idx_list[alias],"floating_node"] = floating_node
    else:
        raise Exception("Alias index is beyond number of alias.")
    
    df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setNodePosition(df, id, position, alias = 0):

    """
    Set the x,y coordinates of the node position.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        position: list or point.Point()
            
        list-
        [position_x, position_y], the coordinate represents the top-left hand corner of the node.

        point.Point()-
        a Point object with attributes x and y representing
        the x/y position of the top-left hand corner of the node.

        alias: int-alias node index [0, num_alias).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    if type(position) != list and type(position) != type(point.Point()):
        raise Exception("Please enter a valid position type.")
    if type(position) == type(point.Point()):
        position = [position.x, position.y]
    # for i in range(len(idx_list)):
    #     df_NodeData_temp.at[idx_list[i],"position"] = position
    if alias < len(idx_list) and alias >= 0:
        df_NodeData_temp.at[idx_list[alias],"position"] = position
    else:
        raise Exception("Alias index is beyond number of alias.")
    df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setNodeSize(df, id, size, alias = 0):

    """
    Set the node size.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        size: list or point.Point()
            
        list-
        1*2 matrix-size of the node [width, height].

        point.Point()-
        a Point object with attributes x and y representing the width and height of 
        the node.

        alias: int-alias node index [0, num_alias).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    if type(size) != list and type(size) != type(point.Point()):
        raise Exception("Please enter a valid size type.")
    if type(size) == type(point.Point()):
        size = [size.x, size.y]
    # for i in range(len(idx_list)):
    #     df_NodeData_temp.at[idx_list[i],"size"] = size
    if alias < len(idx_list) and alias >= 0:
        df_NodeData_temp.at[idx_list[alias],"size"] = size
    else:
        raise Exception("Alias index is beyond number of alias.")

    df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setNodeShape(df, id, shape, alias = 0):

    """
    Set the node shape by shape index or name string.

    Args:  
        df: DataFrame-initial information.

        id: int-node id.

        shape: int/str-

        int-0:text_only, 1:rectangle, 2:ellipse, 3:hexagon, 4:line, or 5:triangle;
            6:upTriangle, 7:downTriangle, 8:leftTriangle, 9: rightTriangle.
        str-"text_only", "rectangle", "ellipse", "hexagon", "line", or "triangle";
            "upTriangle", "downTriangle", "leftTriangle", "rightTriangle".

        alias: int-alias node index [0, num_alias).
            
    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    shape_idx = -1 #undefined shape
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    shape_info = []
    shape_type = ''
    if isinstance(shape, str):
        shape_name = shape
        if shape == 'text_only':
            shape_idx = 0
        elif shape == 'rectangle':
            shape_idx = 1
            shape_type = 'rectangle'
        elif shape == 'ellipse':
            shape_idx = 2
            shape_type = 'ellipse'
            shape_info = [[[50.0, 50.0], [50.0, 50.0]]]
        elif shape == 'hexagon':
            shape_idx = 3
            shape_type = 'polygon'
            shape_info = [[100.0, 50.0], [75.0, 7.0], [25.0, 7.0], [0.0, 50.0], [25.0, 86.0], [75.0, 86.0]]
        elif shape == "line":
            shape_idx = 4
            shape_type = 'polygon'
            shape_info = [[0.0, 50.0], [100.0, 50.0]]
        elif shape == "triangle":
            shape_idx = 5
            shape_type = 'polygon'
            shape_info = [[100.0, 50.0], [25.0, 7.0], [25.0, 86.0]]
        elif shape == "upTriangle":
            shape_idx = 6
            shape_type = 'polygon'
            shape_info = [[50.0, 0.0], [100.0, 80.6], [0.0, 80.6]]
        elif shape == "downTriangle":
            shape_idx = 7
            shape_type = 'polygon'
            shape_info = [[0.0, 19.4], [100.0, 19.4], [50.0, 100.]]
        elif shape == "leftTriangle":
            shape_idx = 8
            shape_type = 'polygon'
            shape_info = [[80.6, 0.0], [80.6, 100.0], [0.0, 50.0]]
        elif shape == "rightTriangle":
            shape_idx = 9
            shape_type = 'polygon'
            shape_info = [[19.4, 0.0], [100., 50.0], [19.4, 100.0]]
        else:
            raise Exception("This is not a valid node shape information.")
    elif isinstance(shape, int):
        if 0 <= shape <= 9:
            shape_idx = shape
            if shape == 0:
                shape_name = 'text_only'
            elif shape == 1:
                shape_name = 'rectangle'
                shape_type = 'rectangle'
            elif shape == 2:
                shape_name = 'ellipse'
                shape_type = 'ellipse'
                shape_info = [[[50.0, 50.0], [50.0, 50.0]]]
            elif shape == 3:
                shape_name = 'hexagon'
                shape_type = 'polygon'
                shape_info = [[100.0, 50.0], [75.0, 7.0], [25.0, 7.0], [0.0, 50.0], [25.0, 86.0], [75.0, 86.0]]
            elif shape == 4:
                shape_name = 'line'
                shape_type = 'polygon'
                shape_info = [[0.0, 50.0], [100.0, 50.0]]
            elif shape == 5:
                shape_name = 'triangle'
                shape_type = 'polygon'
                shape_info = [[100.0, 50.0], [25.0, 7.0], [25.0, 86.0]]
            elif shape == 6:
                shape_name = 'upTriangle'
                shape_type = 'polygon'
                shape_info = [[50.0, 0.0], [100.0, 80.6], [0.0, 80.6]]
            elif shape == 7:
                shape_name = 'downTirangle'
                shape_type = 'polygon'
                shape_info = [[0.0, 19.4], [100.0, 19.4], [50.0, 100.]]
            elif shape == 8:
                shape_name = 'leftTriangle'
                shape_type = 'polygon'
                shape_info = [[80.6, 0.0], [80.6, 100.0], [0.0, 50.0]]
            elif shape == 9:
                shape_name = 'rightTriangle'
                shape_type = 'polygon'
                shape_info = [[19.4, 0.0], [100., 50.0], [19.4, 100.0]]
        else:
            raise Exception("This is not a valid node shape information.")
    else:
        raise Exception("This is not a valid node shape information.")
    # for i in range(len(idx_list)):
    #     df_NodeData_temp.at[idx_list[i],"shape_idx"] = shape_idx
    #     df_NodeData_temp.at[idx_list[i],"shape_name"] = shape_name
    #     df_NodeData_temp.at[idx_list[i],"shape_type"] = shape_type
    #     df_NodeData_temp.at[idx_list[i],"shape_info"] = shape_info
    
    if alias < len(idx_list) and alias >= 0:
        i = alias
        df_NodeData_temp.at[idx_list[i],"shape_idx"] = shape_idx
        df_NodeData_temp.at[idx_list[i],"shape_name"] = shape_name
        df_NodeData_temp.at[idx_list[i],"shape_type"] = shape_type
        df_NodeData_temp.at[idx_list[i],"shape_info"] = shape_info
    else:
        raise Exception("Alias index is beyond number of alias.")

    df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setNodeArbitraryPolygonShape(df, id, shape_name, shape_info, alias = 0):

    """
    Set an arbitrary polygon shape to a node by shape name and shape info.

    Args:  
        id: str-node id.

        shape_name: str-name of the arbitrary polygon shape.

        shape_info: list-[[x1,y1],[x2,y2],[x3,y3],etc], where x,y are floating numbers from 0 to 100.        
        x represents the percentage of width, and y represents the percentage of height.

        alias: int-alias node index [0, num_alias).

    """
    shape_idx = -2 #arbitrary polygon
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    if isinstance(shape_name, str):
        for i in range(len(idx_list)):
            df_NodeData_temp.at[idx_list[i],"shape_name"] = shape_name
    else:
        raise Exception("This is not a valid node shape name.")
    #check the shape_info is in the correct format:
    shape_info_flag = True
    if isinstance(shape_info, list) and len(shape_info) >= 2:
        for ii in range(len(shape_info)):
            if isinstance(shape_info[ii], list) and len(shape_info[ii]) == 2:
                if all(isinstance(float(item), float) for item in shape_info[ii]):
                    pass
                else:
                    shape_info_flag = False
                    raise Exception("This is not a valid node shape info.")
            else:
                shape_info_flag = False
                raise Exception("This is not a valid node shape info.")               
    else:
        shape_info_flag = False
        raise Exception("This is not a valid node shape info.")
    if shape_info_flag == True:
        for i in range(len(idx_list)):
            df_NodeData_temp.at[idx_list[i],"shape_info"] = shape_info
    # for i in range(len(idx_list)):
    #     df_NodeData_temp.at[idx_list[i],"shape_idx"] = shape_idx
    #     df_NodeData_temp.at[idx_list[i],"shape_type"] = 'polygon'
    
    if alias < len(idx_list) and alias >= 0:  
        i = alias 
        df_NodeData_temp.at[idx_list[i],"shape_idx"] = shape_idx
        df_NodeData_temp.at[idx_list[i],"shape_type"] = 'polygon'
    else:
        raise Exception("Alias index is beyond number of alias.")

    df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

    return df_temp

# def _setNodeArbitraryEllipseShape(df, id, shape_name, shape_info):

#     """
#         Set an arbitrary ellipse shape to a node by shape name and shape info.

#         Args:  
#             id: str-node id.

#             shape_name: str-name of the arbitrary ellipse shape.

#             shape_info: list-[[[x1,y1],[r1,r2]]], where x,y,r are floating numbers from 0 to 100.        
    
#     """
#     shape_idx = -3 #arbitrary ellipse
#     df_NodeData_temp = df[1].copy()
#     idx_list = df[1].index[df[1]["id"] == id].tolist()
#     if len(idx_list) == 0:
#         raise Exception("This is not a valid id.")
#     if isinstance(shape_name, str):
#         for i in range(len(idx_list)):
#             df_NodeData_temp.at[idx_list[i],"shape_name"] = shape_name
#     else:
#         raise Exception("This is not a valid node shape name.")
#     #check the shape_info is in the correct format:
#     shape_info_flag = True
#     if isinstance(shape_info, list) and len(shape_info) == 1:
#         if isinstance(shape_info[0], list) and len(shape_info[0]) == 2:
#             for ii in range(len(shape_info[0])):
#                 if all(isinstance(float(item), float) for item in shape_info[0][ii]):
#                     pass
#                 else:
#                     shape_info_flag = False
#                     raise Exception("This is not a valid node shape info.")
#         else:
#             shape_info_flag = False
#             raise Exception("This is not a valid node shape info.")               
#     else:
#         shape_info_flag = False
#         raise Exception("This is not a valid node shape info.")
#     if shape_info_flag == True:
#         for i in range(len(idx_list)):
#             df_NodeData_temp.at[idx_list[i],"shape_info"] = shape_info
#     for i in range(len(idx_list)):
#         df_NodeData_temp.at[idx_list[i],"shape_idx"] = shape_idx
#         df_NodeData_temp.at[idx_list[i],"shape_type"] = 'ellipse'
#     df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

#     return df_temp

def _setNodeTextPosition(df, id, txt_position, alias = 0):

    """
    Set the x,y coordinates of the node text position.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        txt_position: list or point.Point()
            
        list-
        [txt_position_x, txt_position_y], the coordinate represents the top-left hand 
        corner of the node text.

        point.Point()-
        a Point object with attributes x and y representing
        the x/y position of the top-left hand corner of the node text.

        alias: alias node index [0, num_alias).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    if type(txt_position) != list and type(txt_position) != type(point.Point()):
        raise Exception("Please enter a valid txt_position type.")
    if type(txt_position) == type(point.Point()):
        txt_position = [txt_position.x, txt_position.y]
    # for i in range(len(idx_list)):
    #     df_NodeData_temp.at[idx_list[i],"txt_position"] = txt_position
    if alias < len(idx_list) and alias >= 0:
        df_NodeData_temp.at[idx_list[alias],"txt_position"] = txt_position
    else:
        raise Exception("Alias index is beyond number of alias.")

    df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setNodeTextPositionCenter(df, id, alias = 0):

    """
    Set the node text position as the center of the node.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        alias: int-alias node index [0, num_alias).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """

    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    # for i in range(len(idx_list)):
    #     # txt_str = df_NodeData_temp.at[idx_list[i],"id"]
    #     node_position = df_NodeData_temp.at[idx_list[i],"position"]
    #     node_size = df_NodeData_temp.at[idx_list[i],"size"]
    #     #shape_type = df_NodeData_temp.at[idx_list[i],"shape_type"]
    #     txt_position = node_position
    #     txt_size = node_size
    #     # if shape_type == "polygon":
    #     #     vertex = []
    #     #     shape_info = df_NodeData_temp.at[idx_list[i],"shape_info"]
    #     #     for j in range(len(shape_info)):
    #     #         vertex_x = node_position[0]+node_size[0]*shape_info[j][0]/100.
    #     #         vertex_y = node_position[1]+node_size[1]*shape_info[j][1]/100.
    #     #         vertex.append([vertex_x,vertex_y])
    #     #     def centroid(vertexes):
    #     #         _x_list = [vertex [0] for vertex in vertexes]
    #     #         _y_list = [vertex [1] for vertex in vertexes]
    #     #         _len = len(vertexes)
    #     #         _x = sum(_x_list) / _len
    #     #         _y = sum(_y_list) / _len
    #     #         return[_x, _y]         
    #     #     centroid_pos = centroid(vertex)

    #     df_NodeData_temp.at[idx_list[i],"txt_position"] = txt_position
    #     df_NodeData_temp.at[idx_list[i],"txt_size"] = txt_size
    if alias < len(idx_list) and alias >= 0:
        i = alias
        node_position = df_NodeData_temp.at[idx_list[i],"position"]
        node_size = df_NodeData_temp.at[idx_list[i],"size"]
        txt_position = node_position
        txt_size = node_size
        df_NodeData_temp.at[idx_list[i],"txt_position"] = txt_position
        df_NodeData_temp.at[idx_list[i],"txt_size"] = txt_size
    else:
        raise Exception("Alias index is beyond number of alias.")

    df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setNodeTextPositionLeftCenter(df, id, alias = 0):

    """
    Set the node text position as the left center of the node.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        alias: int-alias node index [0, num_alias).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """

    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    # for i in range(len(idx_list)):
    #     node_position = df_NodeData_temp.at[idx_list[i],"position"]
    #     node_size = df_NodeData_temp.at[idx_list[i],"size"]
    #     txt_position = [node_position[0]-node_size[0], node_position[1]]
    #     df_NodeData_temp.at[idx_list[i],"txt_position"] = txt_position
    #     df_NodeData_temp.at[idx_list[i],"txt_size"] = node_size
    if alias < len(idx_list) and alias >= 0:  
        i = alias
        node_position = df_NodeData_temp.at[idx_list[i],"position"]
        node_size = df_NodeData_temp.at[idx_list[i],"size"]
        txt_position = [node_position[0]-node_size[0], node_position[1]]
        df_NodeData_temp.at[idx_list[i],"txt_position"] = txt_position
        df_NodeData_temp.at[idx_list[i],"txt_size"] = node_size
    else:
        raise Exception("Alias index is beyond number of alias.")

    df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setNodeTextPositionRightCenter(df, id, alias = 0):

    """
    Set the node text position as the right center of the node.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        alias: int-alias node index [0, num_alias).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """

    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0 and alias >= 0:
        raise Exception("This is not a valid id.")
    # for i in range(len(idx_list)):
    #     node_position = df_NodeData_temp.at[idx_list[i],"position"]
    #     node_size = df_NodeData_temp.at[idx_list[i],"size"]
    #     txt_position = [node_position[0]+node_size[0], node_position[1]]
    #     df_NodeData_temp.at[idx_list[i],"txt_position"] = txt_position
    #     df_NodeData_temp.at[idx_list[i],"txt_size"] = node_size
    if alias < len(idx_list) and alias >= 0:   
        i = alias
        node_position = df_NodeData_temp.at[idx_list[i],"position"]
        node_size = df_NodeData_temp.at[idx_list[i],"size"]
        txt_position = [node_position[0]+node_size[0], node_position[1]]
        df_NodeData_temp.at[idx_list[i],"txt_position"] = txt_position
        df_NodeData_temp.at[idx_list[i],"txt_size"] = node_size
    else:
        raise Exception("Alias index is beyond number of alias.")

    df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setNodeTextPositionUpperCenter(df, id, alias = 0):

    """
    Set the node text position as the upper center of the node.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        alias: int-alias node index [0, num_alias).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """

    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0 and alias >= 0:
        raise Exception("This is not a valid id.")
    # for i in range(len(idx_list)):
    #     node_position = df_NodeData_temp.at[idx_list[i],"position"]
    #     node_size = df_NodeData_temp.at[idx_list[i],"size"]
    #     txt_position = [node_position[0], node_position[1]-node_size[1]]
    #     df_NodeData_temp.at[idx_list[i],"txt_position"] = txt_position
    #     df_NodeData_temp.at[idx_list[i],"txt_size"] = node_size
    if alias < len(idx_list) and alias >= 0:    
        i = alias
        node_position = df_NodeData_temp.at[idx_list[i],"position"]
        node_size = df_NodeData_temp.at[idx_list[i],"size"]
        txt_position = [node_position[0], node_position[1]-node_size[1]]
        df_NodeData_temp.at[idx_list[i],"txt_position"] = txt_position
        df_NodeData_temp.at[idx_list[i],"txt_size"] = node_size
    else:
        raise Exception("Alias index is beyond number of alias.")

    df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setNodeTextPositionLowerCenter(df, id, alias = 0):

    """
    Set the node text position as the lower center of the node.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        alias: int-alias node index [0, num_alias).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """

    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    # for i in range(len(idx_list)):
    #     node_position = df_NodeData_temp.at[idx_list[i],"position"]
    #     node_size = df_NodeData_temp.at[idx_list[i],"size"]
    #     txt_position = [node_position[0], node_position[1]+node_size[1]]
    #     df_NodeData_temp.at[idx_list[i],"txt_position"] = txt_position
    #     df_NodeData_temp.at[idx_list[i],"txt_size"] = node_size
    if alias < len(idx_list) and alias >= 0:   
        i = alias
        node_position = df_NodeData_temp.at[idx_list[i],"position"]
        node_size = df_NodeData_temp.at[idx_list[i],"size"]
        txt_position = [node_position[0], node_position[1]+node_size[1]]
        df_NodeData_temp.at[idx_list[i],"txt_position"] = txt_position
        df_NodeData_temp.at[idx_list[i],"txt_size"] = node_size
    else:
        raise Exception("Alias index is beyond number of alias.")

    df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setNodeTextPositionUpperLeft(df, id, alias = 0):

    """
    Set the node text position as the upper left of the node.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        alias: int-alias node index [0, num_alias).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """

    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    # for i in range(len(idx_list)):
    #     node_position = df_NodeData_temp.at[idx_list[i],"position"]
    #     node_size = df_NodeData_temp.at[idx_list[i],"size"]
    #     txt_position = [node_position[0]-node_size[0], node_position[1]-node_size[1]]
    #     df_NodeData_temp.at[idx_list[i],"txt_position"] = txt_position
    #     df_NodeData_temp.at[idx_list[i],"txt_size"] = node_size
    if alias < len(idx_list) and alias >= 0:
        i = alias
        node_position = df_NodeData_temp.at[idx_list[i],"position"]
        node_size = df_NodeData_temp.at[idx_list[i],"size"]
        txt_position = [node_position[0]-node_size[0], node_position[1]-node_size[1]]
        df_NodeData_temp.at[idx_list[i],"txt_position"] = txt_position
        df_NodeData_temp.at[idx_list[i],"txt_size"] = node_size
    else:
        raise Exception("Alias index is beyond number of alias.")

    df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setNodeTextPositionUpperRight(df, id, alias = 0):

    """
    Set the node text position as the upper right of the node.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        alias: int-alias node index [0, num_alias).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """

    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    # for i in range(len(idx_list)):
    #     node_position = df_NodeData_temp.at[idx_list[i],"position"]
    #     node_size = df_NodeData_temp.at[idx_list[i],"size"]
    #     txt_position = [node_position[0]+node_size[0], node_position[1]-node_size[1]]
    #     df_NodeData_temp.at[idx_list[i],"txt_position"] = txt_position
    #     df_NodeData_temp.at[idx_list[i],"txt_size"] = node_size
    if alias < len(idx_list) and alias >= 0:
        i = alias
        node_position = df_NodeData_temp.at[idx_list[i],"position"]
        node_size = df_NodeData_temp.at[idx_list[i],"size"]
        txt_position = [node_position[0]+node_size[0], node_position[1]-node_size[1]]
        df_NodeData_temp.at[idx_list[i],"txt_position"] = txt_position
        df_NodeData_temp.at[idx_list[i],"txt_size"] = node_size
    else:
        raise Exception("Alias index is beyond number of alias.")

    df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setNodeTextPositionLowerLeft(df, id, alias = 0):

    """
    Set the node text position as the lower left of the node.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        alias: int-alias node index [0, num_alias).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """

    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    # for i in range(len(idx_list)):
    #     node_position = df_NodeData_temp.at[idx_list[i],"position"]
    #     node_size = df_NodeData_temp.at[idx_list[i],"size"]
    #     txt_position = [node_position[0]-node_size[0], node_position[1]+node_size[1]]
    #     df_NodeData_temp.at[idx_list[i],"txt_position"] = txt_position
    #     df_NodeData_temp.at[idx_list[i],"txt_size"] = node_size
    if alias < len(idx_list) and alias >= 0:
        i = alias
        node_position = df_NodeData_temp.at[idx_list[i],"position"]
        node_size = df_NodeData_temp.at[idx_list[i],"size"]
        txt_position = [node_position[0]-node_size[0], node_position[1]+node_size[1]]
        df_NodeData_temp.at[idx_list[i],"txt_position"] = txt_position
        df_NodeData_temp.at[idx_list[i],"txt_size"] = node_size     
    else:
        raise Exception("Alias index is beyond number of alias.")
    df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])
    return df_temp

def _setNodeTextPositionLowerRight(df, id, alias = 0):

    """
    Set the node text position as the lower right of the node.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        alias: int-alias node index [0, num_alias).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """

    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0 and alias >= 0:
        raise Exception("This is not a valid id.")
    # for i in range(len(idx_list)):
    #     node_position = df_NodeData_temp.at[idx_list[i],"position"]
    #     node_size = df_NodeData_temp.at[idx_list[i],"size"]
    #     txt_position = [node_position[0]+node_size[0], node_position[1]+node_size[1]]
    #     df_NodeData_temp.at[idx_list[i],"txt_position"] = txt_position
    #     df_NodeData_temp.at[idx_list[i],"txt_size"] = node_size
    if alias < len(idx_list) and alias >= 0:
        i = alias
        node_position = df_NodeData_temp.at[idx_list[i],"position"]
        node_size = df_NodeData_temp.at[idx_list[i],"size"]
        txt_position = [node_position[0]+node_size[0], node_position[1]+node_size[1]]
        df_NodeData_temp.at[idx_list[i],"txt_position"] = txt_position
        df_NodeData_temp.at[idx_list[i],"txt_size"] = node_size
    else:
        raise Exception("Alias index is beyond number of alias.")

    df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setNodeTextSize(df, id, txt_size, alias = 0):

    """
    Set the node text size.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        txt_size: list or point.Point()
            
        list-
        1*2 matrix-size of the node text [width, height].

        point.Point()-
        a Point object with attributes x and y representing the width and height of 
        the node text.

        alias: alias node index [0, num_alias).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    if type(txt_size) != list and type(txt_size) != type(point.Point()):
        raise Exception("Please enter a valid txt_size type.")
    if type(txt_size) == type(point.Point()):
        txt_size = [txt_size.x, txt_size.y]
    # for i in range(len(idx_list)):
    #     df_NodeData_temp.at[idx_list[i],"txt_size"] = txt_size
    if alias < len(idx_list) and alias >= 0:
        df_NodeData_temp.at[idx_list[alias],"txt_size"] = txt_size
    else:
        raise Exception("Alias index is beyond number of alias.")
    
    df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setNodeFillColor(df, id, fill_color, opacity, alias = 0 ):

    """
    Set the node fill color.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

        opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

        alias: int-alias node index [0, num_alias).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """

    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    fill_color = _color_to_rgb(fill_color, opacity)
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    # for i in range(len(idx_list)):
    #     df_NodeData_temp.at[idx_list[i],"fill_color"] = fill_color
    if alias < len(idx_list) and alias >= 0:
        df_NodeData_temp.at[idx_list[alias],"fill_color"] = fill_color
    else:
        raise Exception("Alias index is beyond number of alias.")
    
    df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setNodeFillLinearGradient(df, id, gradient_info, stop_info, alias = 0):
    """
    Set the node fill linear gradient.

    Args:  
        id: str-node id.

        gradient_info: list - [[x1,y1],[x2,y2]], where x,y are floating numbers from 0 to 100.
        x represents the percentage of width, and y represents the percentage of height.

        stop_info, list - [[x1,[r1,g1,b1,a1]],[x2,[r2,g2,b2,a2]],etc],
        where x is floating number from 0 to 100.

        alias: int-alias node index [0, num_alias).

    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    #check the gradient_info is in the correct format:
    gradient_info_flag = True
    stop_info_flag = True
    if isinstance(gradient_info, list) and len(gradient_info) == 2:
        for ii in range(len(gradient_info)):
            if isinstance(gradient_info[ii], list) and len(gradient_info[ii]) == 2:
                if all(isinstance(float(item), float) for item in gradient_info[ii]):
                    pass
                else:
                    gradient_info_flag = False
                    raise Exception("This is not a valid gradient info.")
            else:
                gradient_info_flag = False
                raise Exception("This is not a valid gradient info.")               
    else:
        gradient_info_flag = False
        raise Exception("This is not a valid gradient info.")

    if isinstance(stop_info, list) and len(stop_info) >= 2:
        for ii in range(len(stop_info)):
            if isinstance(stop_info[ii], list): 
                if len(stop_info[ii]) == 2:
                    if type(stop_info[ii][0]) == float and type(stop_info[ii][1]) == list:
                        if len(stop_info[ii][1]) == 4 and all(isinstance(int(item), int) and int(item) <= 255 and int(item) >= 0 for item in stop_info[ii][1]):
                            pass
                        else:
                            stop_info_flag = False
                            raise Exception("This is not a valid stop info.")
                    else:
                        stop_info_flag = False
                        raise Exception("This is not a valid stop info.")
                elif len(stop_info[ii]) == 3:
                    if type(stop_info[ii][0]) == float and type(stop_info[ii][1]) == str and type(stop_info[ii][2]) == float:
                        html_to_rgba = _color_to_rgb(stop_info[ii][1], stop_info[ii][2])
                        stop_info[ii] = [stop_info[ii][0], html_to_rgba]
                    else:
                        stop_info_flag = False
                        raise Exception("This is not a valid stop info.")
                else:
                    stop_info_flag = False
            else:
                stop_info_flag = False
                raise Exception("This is not a valid stop info.")               
    else:
        stop_info_flag = False
        raise Exception("This is not a valid stop info.")

    if gradient_info_flag == True and stop_info_flag == True:
        fill_color = ['linearGradient', gradient_info, stop_info]
        # for i in range(len(idx_list)):
        #     df_NodeData_temp.at[idx_list[i],"fill_color"] = fill_color
        if alias < len(idx_list) and alias >= 0:
            df_NodeData_temp.at[idx_list[alias],"fill_color"] = fill_color
        else:
            raise Exception("Alias index is beyond number of alias.")
        
        df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])
        return df_temp

def _setNodeFillRadialGradient(df, id, gradient_info, stop_info, alias = 0):
    """
    Set the node fill radial gradient.

    Args:  
        id: str-node id.

        gradient_info: list - [[x1,y1],[r]], where x,y,r are floating numbers from 0 to 100.
        x represents the center with percentage of width and height; r represents the radius.

        stop_info, list - [[x1,[r1,g1,b1,a1]],[x2,[r2,g2,b2,a2]],etc],
        where x is floating number from 0 to 100.

        alias: int-alias node index [0, num_alias).

    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    #check the gradient_info is in the correct format:
    gradient_info_flag = True
    stop_info_flag = True
    if isinstance(gradient_info, list) and len(gradient_info) == 2:
        if isinstance(gradient_info[0], list) and len(gradient_info[0]) == 2:
            if all(isinstance(float(item), float) for item in gradient_info[0]):
                pass
            else:
                gradient_info_flag = False
                raise Exception("This is not a valid gradient info.")
        else:
            gradient_info_flag = False
            raise Exception("This is not a valid gradient info.")   
        if isinstance(gradient_info[1], list) and len(gradient_info[1]) == 1:
            if type(gradient_info[1][0]) == float:
                pass
            else:
                gradient_info_flag = False
                raise Exception("This is not a valid gradient info.")
        else:
            gradient_info_flag = False
            raise Exception("This is not a valid gradient info.")            
    else:
        gradient_info_flag = False
        raise Exception("This is not a valid gradient info.")

    if isinstance(stop_info, list) and len(stop_info) >= 2:
        for ii in range(len(stop_info)):
            if isinstance(stop_info[ii], list): 
                if len(stop_info[ii]) == 2:
                    if type(stop_info[ii][0]) == float and type(stop_info[ii][1]) == list:
                        if len(stop_info[ii][1]) == 4 and all(isinstance(int(item), int) and int(item) <= 255 and int(item) >= 0 for item in stop_info[ii][1]):
                            pass
                        else:
                            stop_info_flag = False
                            raise Exception("This is not a valid stop info.")
                    else:
                        stop_info_flag = False
                        raise Exception("This is not a valid stop info.")
                elif len(stop_info[ii]) == 3:
                    if type(stop_info[ii][0]) == float and type(stop_info[ii][1]) == str and type(stop_info[ii][2]) == float:
                        html_to_rgba = _color_to_rgb(stop_info[ii][1], stop_info[ii][2])
                        stop_info[ii] = [stop_info[ii][0], html_to_rgba]
                    else:
                        stop_info_flag = False
                        raise Exception("This is not a valid stop info.")
                else:
                    stop_info_flag = False
            else:
                stop_info_flag = False
                raise Exception("This is not a valid stop info.")              
    else:
        stop_info_flag = False
        raise Exception("This is not a valid stop info.")

    if gradient_info_flag == True and stop_info_flag == True:
        fill_color = ['radialGradient', gradient_info, stop_info]
        # for i in range(len(idx_list)):
        #     df_NodeData_temp.at[idx_list[i],"fill_color"] = fill_color
        if alias < len(idx_list) and alias >= 0:
            df_NodeData_temp.at[idx_list[alias],"fill_color"] = fill_color
        else:
            raise Exception("Alias index is beyond number of alias.")
        
        df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

        return df_temp

def _setNodeBorderColor(df, id, border_color, opacity, alias = 0):

    """
    Set the node border color.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        border_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

        opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

        alias: int-alias node index [0, num_alias).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    border_color = _color_to_rgb(border_color, opacity)
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    # for i in range(len(idx_list)):
    #     df_NodeData_temp.at[idx_list[i],"border_color"] = border_color
    if alias < len(idx_list) and alias >= 0:
        df_NodeData_temp.at[idx_list[alias],"border_color"] = border_color
    else:
        raise Exception("Alias index is beyond number of alias.")
    
    df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setNodeBorderWidth(df, id, border_width, alias = 0):

    """
    Set the node border width.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        border_width: float-node border line width.

        alias: int-alias node index [0, num_alias).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    # for i in range(len(idx_list)):
    #     df_NodeData_temp.at[idx_list[i],"border_width"] = border_width
    if alias < len(idx_list) and alias >= 0:
        df_NodeData_temp.at[idx_list[alias],"border_width"] = border_width
    else:
        raise Exception("Alias index is beyond number of alias.")
    
    df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setNodeTextContent(df, id, txt_content, alias = 0):

    """
    Set the node text content.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        txt_content: str-node text content.

        alias: int-alias node index [0, num_alias).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    # for i in range(len(idx_list)):
    #     df_NodeData_temp.at[idx_list[i],"txt_line_width"] = txt_line_width
    if alias < len(idx_list) and alias >= 0:
        df_NodeData_temp.at[idx_list[alias],"txt_content"] = txt_content
    else:
        raise Exception("Alias index is beyond number of alias.")
   
    df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setNodeTextFontColor(df, id, txt_font_color, opacity, alias = 0):

    """
    Set the node text font color.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        txt_font_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

        opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

        alias: int-alias node index [0, num_alias).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    txt_font_color = _color_to_rgb(txt_font_color, opacity)
    # for i in range(len(idx_list)):
    #     df_NodeData_temp.at[idx_list[i],"txt_font_color"] = txt_font_color
    if alias < len(idx_list) and alias >= 0:
        df_NodeData_temp.at[idx_list[alias],"txt_font_color"] = txt_font_color
    else:
        raise Exception("Alias index is beyond number of alias.")
    
    df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setNodeTextLineWidth(df, id, txt_line_width, alias = 0):

    """
    Set the node text line width (the stroke width value of the TEXTGLYPH).

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        txt_line_width: float-node text line width.

        alias: int-alias node index [0, num_alias).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    # for i in range(len(idx_list)):
    #     df_NodeData_temp.at[idx_list[i],"txt_line_width"] = txt_line_width
    if alias < len(idx_list) and alias >= 0:
        df_NodeData_temp.at[idx_list[alias],"txt_line_width"] = txt_line_width
    else:
        raise Exception("Alias index is beyond number of alias.")
   
    df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

    return df_temp


def _setNodeTextFontSize(df, id, txt_font_size, alias = 0):

    """
    Set the node text font size.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        txt_font_size: float-node text font size.

        alias: int-alias node index [0, num_alias).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    # for i in range(len(idx_list)):
    #     df_NodeData_temp.at[idx_list[i],"txt_font_size"] = txt_font_size
    if alias < len(idx_list) and alias >= 0:
        df_NodeData_temp.at[idx_list[alias],"txt_font_size"] = txt_font_size
    else:
        raise Exception("Alias index is beyond number of alias.")
    
    df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setNodeTextAnchor(df, id, txt_anchor, alias = 0):

    """
    Set the node text horizontal anchor.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        txt_anchor: str-node text horizontal anchor, which can be "start",
            "middle" and "end".

        alias: int-alias node index [0, num_alias).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    if txt_anchor not in ['start', 'middle', 'end']:
        raise Exception("Please enter a valid horizontal anchor.")
    # for i in range(len(idx_list)):
    #     df_NodeData_temp.at[idx_list[i],"txt_line_width"] = txt_line_width
    if alias < len(idx_list) and alias >= 0:
        txt_vanchor = df_NodeData_temp.at[idx_list[alias],"txt_anchor"][1]
        df_NodeData_temp.at[idx_list[alias],"txt_anchor"] = [txt_anchor, txt_vanchor]
    else:
        raise Exception("Alias index is beyond number of alias.")
   
    df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

    return df_temp


def _setNodeTextVAnchor(df, id, txt_vanchor, alias = 0):

    """
    Set the node text vertical anchor.

    Args:  
        df: DataFrame-initial information.

        id: str-node id.

        txt_vanchor: str-node text horizontal anchor, which can be which can be "top", 
            "middle", "baseline" and "bottom".

        alias: int-alias node index [0, num_alias).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_NodeData_temp = df[1].copy()
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    if txt_vanchor not in ['top', 'middle', 'baseline', 'bottom']:
        raise Exception("Please enter a valid vertical anchor.")
    # for i in range(len(idx_list)):
    #     df_NodeData_temp.at[idx_list[i],"txt_line_width"] = txt_line_width
    if alias < len(idx_list) and alias >= 0:
        txt_anchor = df_NodeData_temp.at[idx_list[alias],"txt_anchor"][0]
        df_NodeData_temp.at[idx_list[alias],"txt_anchor"] = [txt_anchor, txt_vanchor]
    else:
        raise Exception("Alias index is beyond number of alias.")
   
    df_temp = (df[0], df_NodeData_temp, df[2], df[3], df[4], df[5], df[6])

    return df_temp

def _setReactionCenterPosition(df, id, position):

    """
    Set the reaction center position.

    Args:  
        df: DataFrame-initial information.

        id: str-reaction id.
        
        position: list or point.Point()
            
        list-
        1*2 matrix-[position_x, position_y].

        point.Point()-
        a Point object with attributes x and y representing the x/y position.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_ReactionData_temp = df[2].copy()
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    if type(position) != list and type(position) != type(point.Point()):
        raise Exception("Please enter a valid position type.")
    if type(position) == type(point.Point()):
        position = [position.x, position.y]
    for i in range(len(idx_list)):
        df_ReactionData_temp.at[idx_list[i],"center_pos"] = position
    df_temp = (df[0], df[1], df_ReactionData_temp, df[3], df[4], df[5], df[6])
    
    return df_temp

def _setReactionBezierHandles(df, id, position):

    """
    Set the reaction bezier handle positions.

    Args:  
        df: DataFrame-initial information.

        id: str-reaction id.
        
        position: list-position of the handles: [center handle, reactant handle1, ..., product handle1, ...].
                        
        center handle/reactant handle1/product handle1: list or point.Point()
            
        list-
        [position_x, position_y], the coordinate represents the top-left hand 
        corner of the node.

        point.Point()-
        a Point object with attributes x and y representing the x/y position.
    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_ReactionData_temp = df[2].copy()
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    if type(position) != list:
        raise Exception("Please enter a valid position type.")
    else:
        if all(isinstance(item, list) for item in position):
            pass
        elif all(type(item) == type(point.Point()) for item in position):
            position_to_list = []
            for item in position:
                position_to_list.append([item.x,item.y])
            position = position_to_list
        else:
            raise Exception("Please enter a valid position type.")
    for i in range(len(idx_list)):
        df_ReactionData_temp.at[idx_list[i],"handles"] = position
    df_temp = (df[0], df[1], df_ReactionData_temp, df[3], df[4], df[5], df[6])
    
    return df_temp

def _setReactionFillColor(df, id, fill_color, opacity):

    """
    Set the reaction fill color.

    Args:  
        df: DataFrame-initial information.

        id: str-reaction id.

        fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

        opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_ReactionData_temp = df[2].copy()
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    fill_color = _color_to_rgb(fill_color, opacity)
    for i in range(len(idx_list)):
        df_ReactionData_temp.at[idx_list[i],"stroke_color"] = fill_color
    df_temp = (df[0], df[1], df_ReactionData_temp, df[3], df[4], df[5], df[6])
    
    return df_temp

def _setReactionLineThickness(df, id, line_thickness):

    """
    Set the reaction line thickness.

    Args:  
        df: DataFrame-initial information.

        id: str-reaction id.

        line_thickness: float-reaction border line width.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_ReactionData_temp = df[2].copy()
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    for i in range(len(idx_list)):
        df_ReactionData_temp.at[idx_list[i],"line_thickness"] = line_thickness
    df_temp = (df[0], df[1], df_ReactionData_temp, df[3], df[4], df[5], df[6])

    return df_temp

def _setBezierReactionType(df, id, bezier):

    """
    Set the reaction type to bezier curve or not with a certain reaction id.

    Args:  
        df: DataFrame-initial information.

        id: str-reaction id.
 
        bezier: bool-bezier reaction (True as default) or not (False as straightline).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_ReactionData_temp = df[2].copy()
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    for i in range(len(idx_list)):
        df_ReactionData_temp.at[idx_list[i],"bezier"] = bezier
    df_temp = (df[0], df[1], df_ReactionData_temp, df[3], df[4], df[5], df[6])

    return df_temp


def _setReactionDashStyle(df, id, dash):

    """
    Set the reaction dash information with a certain reaction id.

    Args:  
        df: DataFrame-initial information.

        id: str-reaction id.
 
        dash: list - [] means solid; 
            [a,b] means drawing a a-point line and following a b-point gap and etc;
            [a,b,c,d] means drawing a a-point line and following a b-point gap, and then
            drawing a c-point line followed by a d-point gap.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_ReactionData_temp = df[2].copy()
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    if type(dash) != list:
        raise Exception("Please enter a valid dash type.")
    for i in range(len(idx_list)):
        df_ReactionData_temp.at[idx_list[i],"rxn_dash"] = dash
        df_ReactionData_temp.at[idx_list[i],"src_dash"] = dash
        df_ReactionData_temp.at[idx_list[i],"tgt_dash"] = dash
    df_temp = (df[0], df[1], df_ReactionData_temp, df[3], df[4], df[5], df[6])

    return df_temp

def _setReactionArrowHeadPosition(df, id, position):

    """
    Set the reaction arrow head position with a certain reaction id.

    Args:  
        df: DataFrame-initial information.
            
        position: list or point.Point()
                
        list-
        [position_x, position_y], the coordinate represents the relative position of the 
        arrow head as an line ending.

        point.Point()-
        a Point object with attributes x and y representing
        the x/y position of the relative position of the arrow head as an line ending.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_ReactionData_temp = df[2].copy()
    df_LineEndingData_temp = df[5].copy()
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    line_ending_id = []
    if type(position) != list and type(position) != type(point.Point()):
        raise Exception("Please enter a valid position type.")
    if type(position) == type(point.Point()):
        position = [position.x, position.y]
    for i in range(len(idx_list)):
        line_ending_id.append(df[2].iloc[idx_list[i]]["targets_lineending"][0]) 
    if len(line_ending_id) == 1:
        if line_ending_id != ['line_ending_' + id]:
            df_ReactionData_temp.at[idx_list[0],"targets_lineending"] = ['line_ending_' + id]
            idx_lineending = df_LineEndingData_temp.index[df[5]["id"] == line_ending_id[0]].tolist()
            if len(idx_lineending) == 1:
                row = len(df[5])
                LineEndingData_row_dct = df_LineEndingData_temp.to_dict('records')[idx_lineending[0]]
                keys = list(LineEndingData_row_dct.keys())
                values = list(LineEndingData_row_dct.values())
                for k in range(len(keys)):
                    LineEndingData_row_dct[keys[k]] = [values[k]]
                df_LineEndingData_temp = pd.concat([df_LineEndingData_temp,\
                                pd.DataFrame(LineEndingData_row_dct)], ignore_index=True)
                df_LineEndingData_temp.at[row,"id"] = 'line_ending_' + id
                df_LineEndingData_temp.at[row,"position"] = position
        else:
            idx_lineending = df_LineEndingData_temp.index[df[5]["id"] == line_ending_id[0]].tolist()
            if len(idx_lineending) == 1:
                #df_LineEndingData_temp.at[idx_lineending[0],"id"] = 'line_ending_' + id
                df_LineEndingData_temp.at[idx_lineending[0],"position"] = position
            else:
                raise Exception("There is no initial arrow head information to edit.")
                
    else:
        raise Exception("This is not a valid id.")

    df_temp = (df[0], df[1], df_ReactionData_temp, df[3], df[4], df_LineEndingData_temp, df[6])

    return df_temp

def _setReactionArrowHeadSize(df, id, size):

    """
    Set the reaction arrow head size with a certain reaction id.

    Args:  
        df: DataFrame-initial information.

        size: list or point.Point()
                
        list-
        1*2 matrix-size of the arrow head [width, height].

        point.Point()-
        a Point object with attributes x and y representing the width and height of 
        the arrow head.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_ReactionData_temp = df[2].copy()
    df_LineEndingData_temp = df[5].copy()
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    line_ending_id = []
    if type(size) != list and type(size) != type(point.Point()):
        raise Exception("Please enter a valid size type.")
    if type(size) == type(point.Point()):
        size = [size.x, size.y]
    for i in range(len(idx_list)):
        line_ending_id.append(df[2].iloc[idx_list[i]]["targets_lineending"][0]) 
    if len(line_ending_id) == 1:
        if line_ending_id != ['line_ending_' + id]:
            df_ReactionData_temp.at[idx_list[0],"targets_lineending"] = ['line_ending_' + id]
            idx_lineending = df_LineEndingData_temp.index[df[5]["id"] == line_ending_id[0]].tolist()
            if len(idx_lineending) == 1:
                row = len(df[5])
                LineEndingData_row_dct = df_LineEndingData_temp.to_dict('records')[idx_lineending[0]]
                keys = list(LineEndingData_row_dct.keys())
                values = list(LineEndingData_row_dct.values())
                for k in range(len(keys)):
                    LineEndingData_row_dct[keys[k]] = [values[k]]
                df_LineEndingData_temp = pd.concat([df_LineEndingData_temp,\
                                pd.DataFrame(LineEndingData_row_dct)], ignore_index=True)
                df_LineEndingData_temp.at[row,"id"] = 'line_ending_' + id
                df_LineEndingData_temp.at[row,"size"] = size
        else:
            idx_lineending = df_LineEndingData_temp.index[df[5]["id"] == line_ending_id[0]].tolist()
            if len(idx_lineending) == 1:
                df_LineEndingData_temp.at[idx_lineending[0],"size"] = size
            else:
                raise Exception("There is no initial arrow head information to edit.")

    else:
        raise Exception("This is not a valid id.")

    df_temp = (df[0], df[1], df_ReactionData_temp, df[3], df[4], df_LineEndingData_temp, df[6])

    return df_temp

# def _setReactionArrowHeadSize(df, id, size):
##This is the old version of arrow head size without defining lineending

#     """
#     Set the reaction arrow head size with a certain reaction id.

#     Args:  
#         df: DataFrame-initial information.

#         size: list or point.Point()
            
#         list-
#         1*2 matrix-size of the arrow head [width, height].

#         point.Point()-
#         a Point object with attributes x and y representing the width and height of 
#         the arrow head.

#     Returns:
#         df_temp: DataFrame-information after updates. 
    
#     """
#     df_ReactionData_temp = df[2].copy()
#     idx_list = df[2].index[df[2]["id"] == id].tolist()
#     if len(idx_list) == 0:
#         raise Exception("This is not a valid id.")
#     if type(size) != list and type(size) != type(point.Point()):
#         raise Exception("Please enter a valid size type.")
#     if type(size) == type(point.Point()):
#         size = [size.x, size.y]
#     for i in range(len(idx_list)):
#         df_ReactionData_temp.at[idx_list[i],"arrow_head_size"] = size
#     df_temp = (df[0], df[1], df_ReactionData_temp, df[3], df[4], df[5], df[6])
#     # df_ReactionData_temp = df[2].copy()
#     # for i in range(len(df_ReactionData_temp)):
#     #     df_ReactionData_temp.at[i,"arrow_head_size"] = size
#     # df_temp = (df[0], df[1], df_ReactionData_temp, df[3])

#     return df_temp

def _setReactionArrowHeadFillColor(df, id, fill_color, opacity = 1.):

    """
    Set the reaction arrow head fill color with a certain reaction id.

    Args:  
        df: DataFrame-initial information.

        fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

        opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """

    df_ReactionData_temp = df[2].copy()
    df_LineEndingData_temp = df[5].copy()
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    line_ending_id = []
    fill_color = _color_to_rgb(fill_color, opacity)
    for i in range(len(idx_list)):
        line_ending_id.append(df[2].iloc[idx_list[i]]["targets_lineending"][0]) 
        #df_ReactionData_temp.at[idx_list[0],"targets_lineending"] = ['line_ending_' + id]
    if len(line_ending_id) == 1:
        if line_ending_id != ['line_ending_' + id]:
            df_ReactionData_temp.at[idx_list[0],"targets_lineending"] = ['line_ending_' + id]
            idx_lineending = df_LineEndingData_temp.index[df[5]["id"] == line_ending_id[0]].tolist()
            if len(idx_lineending) == 1:
                row = len(df[5])
                LineEndingData_row_dct = df_LineEndingData_temp.to_dict('records')[idx_lineending[0]]
                keys = list(LineEndingData_row_dct.keys())
                values = list(LineEndingData_row_dct.values())
                for k in range(len(keys)):
                    LineEndingData_row_dct[keys[k]] = [values[k]]
                df_LineEndingData_temp = pd.concat([df_LineEndingData_temp,\
                                pd.DataFrame(LineEndingData_row_dct)], ignore_index=True)
                df_LineEndingData_temp.at[row,"id"] = 'line_ending_' + id
                df_LineEndingData_temp.at[row,"fill_color"] = fill_color
        else:
            idx_lineending = df_LineEndingData_temp.index[df[5]["id"] == line_ending_id[0]].tolist()
            if len(idx_lineending) == 1:
                df_LineEndingData_temp.at[idx_lineending[0],"fill_color"] = fill_color
            else:
                raise Exception("There is no initial arrow head information to edit.")
        
    else:
        raise Exception("This is not a valid id.")

    df_temp = (df[0], df[1], df_ReactionData_temp, df[3], df[4], df_LineEndingData_temp, df[6])

    return df_temp

def _setReactionArrowHeadBorderColor(df, id, border_color, opacity = 1.):

    """
    Set the reaction arrow head border color with a certain reaction id.

    Args:  
        df: DataFrame-initial information.

        border_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

        opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """

    df_ReactionData_temp = df[2].copy()
    df_LineEndingData_temp = df[5].copy()
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    line_ending_id = []
    border_color = _color_to_rgb(border_color, opacity)
    for i in range(len(idx_list)):
        line_ending_id.append(df[2].iloc[idx_list[i]]["targets_lineending"][0]) 
        #df_ReactionData_temp.at[idx_list[0],"targets_lineending"] = ['line_ending_' + id]
    if len(line_ending_id) == 1:
        if line_ending_id != ['line_ending_' + id]:
            df_ReactionData_temp.at[idx_list[0],"targets_lineending"] = ['line_ending_' + id]
            idx_lineending = df_LineEndingData_temp.index[df[5]["id"] == line_ending_id[0]].tolist()
            if len(idx_lineending) == 1:
                row = len(df[5])
                LineEndingData_row_dct = df_LineEndingData_temp.to_dict('records')[idx_lineending[0]]
                keys = list(LineEndingData_row_dct.keys())
                values = list(LineEndingData_row_dct.values())
                for k in range(len(keys)):
                    LineEndingData_row_dct[keys[k]] = [values[k]]
                df_LineEndingData_temp = pd.concat([df_LineEndingData_temp,\
                                pd.DataFrame(LineEndingData_row_dct)], ignore_index=True)
                df_LineEndingData_temp.at[row,"id"] = 'line_ending_' + id
                df_LineEndingData_temp.at[row,"border_color"] = border_color
        else:
            idx_lineending = df_LineEndingData_temp.index[df[5]["id"] == line_ending_id[0]].tolist()
            if len(idx_lineending) == 1:
                df_LineEndingData_temp.at[idx_lineending[0],"border_color"] = border_color
            else:
                raise Exception("There is no initial arrow head information to edit.")
        
    else:
        raise Exception("This is not a valid id.")

    df_temp = (df[0], df[1], df_ReactionData_temp, df[3], df[4], df_LineEndingData_temp, df[6])

    return df_temp

def _setReactionArrowHeadShape(df, id, shape_type_list, shape_info_list):

    """
    Set the reaction arrow head fill color with a certain reaction id.

    Args:  
        df: DataFrame-initial information.

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
        [w, h], where each number is a floating number from 0 to 100. w represents the
        width of the rectangle, and h represents the height of the rectangle.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """

    if isinstance(shape_info_list, list) and isinstance(shape_type_list, list) and len(shape_type_list) == len(shape_info_list):
        for i in range(len(shape_info_list)):
            shape_type = shape_type_list[i]
            shape_info = shape_info_list[i]
            if shape_type == 'polygon':
                if isinstance(shape_info, list) and len(shape_info) >= 2:
                    for ii in range(len(shape_info)):
                        if isinstance(shape_info[ii], list) and len(shape_info[ii]) == 2:
                            if all((float(item) >= 0. and float(item) <= 100.) for item in shape_info[ii]):
                                pass
                            else:
                                raise Exception("This is not a valid polygon shape info.")
                        else:
                            raise Exception("This is not a valid polygon shape info.")               
                else:
                    raise Exception("This is not a valid polygon shape info.")
            elif shape_type == 'rectangle':
                if isinstance(shape_info, list) and len(shape_info) == 2:
                    if all((float(item) >= 0. and float(item) <= 100.) for item in shape_info):
                        pass
                    else:
                        raise Exception("This is not a valid rectangle shape info.")
                else:
                    raise Exception("This is not a valid rectangle shape info.")
                # if shape_info != []:
                #     raise Exception("This is not a valid rectangle shape info.")
            elif shape_type == 'ellipse':
                # [[0.0, 0.0], [100.0, 100.0]]
                if isinstance(shape_info, list) and len(shape_info) == 2:
                    for ii in range(len(shape_info)):
                        if len(shape_info[ii]) == 2 and all((float(item) >= 0. and float(item) <= 100.) for item in shape_info[ii]):
                            pass
                        else:
                            raise Exception("This is not a valid ellipse shape info.")
                else:
                    raise Exception("This is not a valid ellipse shape info.")

    else:
        raise Exception("This is not a valid shape.")

    df_ReactionData_temp = df[2].copy()
    df_LineEndingData_temp = df[5].copy()
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    line_ending_id = []
    
    for i in range(len(idx_list)):
        line_ending_id.append(df[2].iloc[idx_list[i]]["targets_lineending"][0]) 
        #df_ReactionData_temp.at[idx_list[0],"targets_lineending"] = ['line_ending_' + id]
    if len(line_ending_id) == 1:
        if line_ending_id != ['line_ending_' + id]:
            df_ReactionData_temp.at[idx_list[0],"targets_lineending"] = ['line_ending_' + id]
            idx_lineending = df_LineEndingData_temp.index[df[5]["id"] == line_ending_id[0]].tolist()
            if len(idx_lineending) == 1:
                row = len(df[5])
                LineEndingData_row_dct = df_LineEndingData_temp.to_dict('records')[idx_lineending[0]]
                keys = list(LineEndingData_row_dct.keys())
                values = list(LineEndingData_row_dct.values())
                for k in range(len(keys)):
                    LineEndingData_row_dct[keys[k]] = [values[k]]
                df_LineEndingData_temp = pd.concat([df_LineEndingData_temp,\
                                pd.DataFrame(LineEndingData_row_dct)], ignore_index=True)
                df_LineEndingData_temp.at[row,"id"] = 'line_ending_' + id
                df_LineEndingData_temp.at[row,"shape_type"] = shape_type_list
                df_LineEndingData_temp.at[row,"shape_info"] = shape_info_list
        else:
            idx_lineending = df_LineEndingData_temp.index[df[5]["id"] == line_ending_id[0]].tolist()
            if len(idx_lineending) == 1:
                df_LineEndingData_temp.at[idx_lineending[0],"shape_type"] = shape_type_list
                df_LineEndingData_temp.at[idx_lineending[0],"shape_info"] = shape_info_list
            else:
                raise Exception("There is no initial arrow head information to edit.")
    else:
        raise Exception("This is not a valid id.")

    df_temp = (df[0], df[1], df_ReactionData_temp, df[3], df[4], df_LineEndingData_temp, df[6])

    return df_temp

def _setReactionModifierHeadPosition(df, id, position, mod_idx = 0):

    """
    Set the reaction modifier head position with a certain reaction id.

    Args:  
        df: DataFrame-initial information.
            
        position: list or point.Point()
                
        list-
        [position_x, position_y], the coordinate represents the relative position of the 
        modifier head as an line ending.

        point.Point()-
        a Point object with attributes x and y representing
        the x/y position of the relative position of the modifier head as an line ending.

        mod_idx: int-the index of the modifier: 0 to number of modifiers -1.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_ReactionData_temp = df[2].copy()
    df_LineEndingData_temp = df[5].copy()
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    line_ending_id = []
    if type(position) != list and type(position) != type(point.Point()):
        raise Exception("Please enter a valid position type.")
    if type(position) == type(point.Point()):
        position = [position.x, position.y]
    for i in range(len(idx_list)):
        line_ending_id.append(df[2].iloc[idx_list[i]]["modifiers_lineending"][mod_idx]) 
    if len(line_ending_id) == 1:
        if line_ending_id != ['line_ending_modifier_' + id + '_'+ str(mod_idx)]:
            df_ReactionData_temp.at[idx_list[0],"modifiers_lineending"][mod_idx] = 'line_ending_modifier_' + id + '_' + str(mod_idx)
            idx_lineending = df_LineEndingData_temp.index[df[5]["id"] == line_ending_id[0]].tolist()
            if len(idx_lineending) == 1:
                row = len(df[5])
                LineEndingData_row_dct = df_LineEndingData_temp.to_dict('records')[idx_lineending[0]]
                keys = list(LineEndingData_row_dct.keys())
                values = list(LineEndingData_row_dct.values())
                for k in range(len(keys)):
                    LineEndingData_row_dct[keys[k]] = [values[k]]
                df_LineEndingData_temp = pd.concat([df_LineEndingData_temp,\
                                pd.DataFrame(LineEndingData_row_dct)], ignore_index=True)
                df_LineEndingData_temp.at[row,"id"] = 'line_ending_modifier_' + id + '_'+ str(mod_idx)
                df_LineEndingData_temp.at[row,"position"] = position
        else:
            idx_lineending = df_LineEndingData_temp.index[df[5]["id"] == line_ending_id[0]].tolist()
            if len(idx_lineending) == 1:
                #df_LineEndingData_temp.at[idx_lineending[0],"id"] = 'line_ending_' + id
                df_LineEndingData_temp.at[idx_lineending[0],"position"] = position
            else:
                raise Exception("There is no initial modifier head information to edit.")
                
    else:
        raise Exception("This is not a valid id.")

    df_temp = (df[0], df[1], df_ReactionData_temp, df[3], df[4], df_LineEndingData_temp, df[6])

    return df_temp

def _setReactionModifierHeadSize(df, id, size, mod_idx = 0):

    """
    Set the reaction modifier head size with a certain reaction id.

    Args:  
        df: DataFrame-initial information.

        size: list or point.Point()
                
        list-
        1*2 matrix-size of the modifier head [width, height].

        point.Point()-
        a Point object with attributes x and y representing the width and height of 
        the modifier head.
        
        mod_idx: int-the index of the modifier: 0 to number of modifiers -1.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_ReactionData_temp = df[2].copy()
    df_LineEndingData_temp = df[5].copy()
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    line_ending_id = []
    if type(size) != list and type(size) != type(point.Point()):
        raise Exception("Please enter a valid size type.")
    if type(size) == type(point.Point()):
        size = [size.x, size.y]
    for i in range(len(idx_list)):
        line_ending_id.append(df[2].iloc[idx_list[i]]["modifiers_lineending"][mod_idx]) 
    if len(line_ending_id) == 1:
        if line_ending_id != ['line_ending_modifier_' + id + '_' + str(mod_idx)]:
            df_ReactionData_temp.at[idx_list[0],"modifiers_lineending"][mod_idx] = 'line_ending_modifier_' + id + '_' + str(mod_idx)
            idx_lineending = df_LineEndingData_temp.index[df[5]["id"] == line_ending_id[0]].tolist()
            if len(idx_lineending) == 1:
                row = len(df[5])
                LineEndingData_row_dct = df_LineEndingData_temp.to_dict('records')[idx_lineending[0]]
                keys = list(LineEndingData_row_dct.keys())
                values = list(LineEndingData_row_dct.values())
                for k in range(len(keys)):
                    LineEndingData_row_dct[keys[k]] = [values[k]]
                df_LineEndingData_temp = pd.concat([df_LineEndingData_temp,\
                                pd.DataFrame(LineEndingData_row_dct)], ignore_index=True)
                df_LineEndingData_temp.at[row,"id"] = 'line_ending_modifier_' + id + "_" + str(mod_idx)
                df_LineEndingData_temp.at[row,"size"] = size
        else:
            idx_lineending = df_LineEndingData_temp.index[df[5]["id"] == line_ending_id[0]].tolist()
            if len(idx_lineending) == 1:
                df_LineEndingData_temp.at[idx_lineending[0],"size"] = size
            else:
                raise Exception("There is no initial modifier head information to edit.")

    else:
        raise Exception("This is not a valid id.")

    df_temp = (df[0], df[1], df_ReactionData_temp, df[3], df[4], df_LineEndingData_temp, df[6])

    return df_temp

def _setReactionModifierHeadFillColor(df, id, fill_color, opacity = 1., mod_idx = 0):

    """
    Set the reaction modifier head fill color with a certain reaction id.

    Args:  
        df: DataFrame-initial information.

        fill_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

        opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).
        
        mod_idx: int-the index of the modifier: 0 to number of modifiers -1.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """

    df_ReactionData_temp = df[2].copy()
    df_LineEndingData_temp = df[5].copy()
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    line_ending_id = []
    fill_color = _color_to_rgb(fill_color, opacity)
    for i in range(len(idx_list)):
        line_ending_id.append(df[2].iloc[idx_list[i]]["modifiers_lineending"][mod_idx]) 
    if len(line_ending_id) == 1:
        if line_ending_id != ['line_ending_modifier_' + id + '_' + str(mod_idx)]:
            df_ReactionData_temp.at[idx_list[0],"modifiers_lineending"][mod_idx] ='line_ending_modifier_' + id + '_' + str(mod_idx)
            idx_lineending = df_LineEndingData_temp.index[df[5]["id"] == line_ending_id[0]].tolist()
            if len(idx_lineending) == 1:
                row = len(df[5])
                LineEndingData_row_dct = df_LineEndingData_temp.to_dict('records')[idx_lineending[0]]
                keys = list(LineEndingData_row_dct.keys())
                values = list(LineEndingData_row_dct.values())
                for k in range(len(keys)):
                    LineEndingData_row_dct[keys[k]] = [values[k]]
                df_LineEndingData_temp = pd.concat([df_LineEndingData_temp,\
                                pd.DataFrame(LineEndingData_row_dct)], ignore_index=True)
                df_LineEndingData_temp.at[row,"id"] = 'line_ending_modifier_' + id + '_' + str(mod_idx)
                df_LineEndingData_temp.at[row,"fill_color"] = fill_color
        else:
            idx_lineending = df_LineEndingData_temp.index[df[5]["id"] == line_ending_id[0]].tolist()
            if len(idx_lineending) == 1:
                df_LineEndingData_temp.at[idx_lineending[0],"fill_color"] = fill_color
            else:
                raise Exception("There is no initial modifier head information to edit.")
        
    else:
        raise Exception("This is not a valid id.")

    df_temp = (df[0], df[1], df_ReactionData_temp, df[3], df[4], df_LineEndingData_temp, df[6])

    return df_temp

def _setReactionModifierHeadBorderColor(df, id, border_color, opacity = 1., mod_idx = 0):

    """
    Set the reaction modifier head border color with a certain reaction id.

    Args:  
        df: DataFrame-initial information.

        border_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

        opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).
        
        mod_idx: int-the index of the modifier: 0 to number of modifiers -1.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """

    df_ReactionData_temp = df[2].copy()
    df_LineEndingData_temp = df[5].copy()
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    line_ending_id = []
    border_color = _color_to_rgb(border_color, opacity)
    for i in range(len(idx_list)):
        line_ending_id.append(df[2].iloc[idx_list[i]]["modifiers_lineending"][mod_idx]) 
    if len(line_ending_id) == 1:
        if line_ending_id != ['line_ending_modifier_' + id + '_' + str(mod_idx)]:
            df_ReactionData_temp.at[idx_list[0],"modifiers_lineending"][mod_idx] ='line_ending_modifier_' + id + '_' + str(mod_idx)
            idx_lineending = df_LineEndingData_temp.index[df[5]["id"] == line_ending_id[0]].tolist()
            if len(idx_lineending) == 1:
                row = len(df[5])
                LineEndingData_row_dct = df_LineEndingData_temp.to_dict('records')[idx_lineending[0]]
                keys = list(LineEndingData_row_dct.keys())
                values = list(LineEndingData_row_dct.values())
                for k in range(len(keys)):
                    LineEndingData_row_dct[keys[k]] = [values[k]]
                df_LineEndingData_temp = pd.concat([df_LineEndingData_temp,\
                                pd.DataFrame(LineEndingData_row_dct)], ignore_index=True)
                df_LineEndingData_temp.at[row,"id"] = 'line_ending_modifier_' + id + '_' + str(mod_idx)
                df_LineEndingData_temp.at[row,"border_color"] = border_color
        else:
            idx_lineending = df_LineEndingData_temp.index[df[5]["id"] == line_ending_id[0]].tolist()
            if len(idx_lineending) == 1:
                df_LineEndingData_temp.at[idx_lineending[0],"border_color"] = border_color
            else:
                raise Exception("There is no initial modifier head information to edit.")
        
    else:
        raise Exception("This is not a valid id.")

    df_temp = (df[0], df[1], df_ReactionData_temp, df[3], df[4], df_LineEndingData_temp, df[6])

    return df_temp

def _setReactionModifierHeadShape(df, id, shape_type_list, shape_info_list, mod_idx = 0):

    """
    Set the reaction arrow head fill color with a certain reaction id.

    Args:  
        df: DataFrame-initial information.

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

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """

    if isinstance(shape_info_list, list) and isinstance(shape_type_list, list) and len(shape_type_list) == len(shape_info_list):
        for i in range(len(shape_info_list)):
            shape_type = shape_type_list[i]
            shape_info = shape_info_list[i]
            if shape_type == 'polygon':
                if isinstance(shape_info, list) and len(shape_info) >= 2:
                    for ii in range(len(shape_info)):
                        if isinstance(shape_info[ii], list) and len(shape_info[ii]) == 2:
                            if all((float(item) >= 0. and float(item) <= 100.) for item in shape_info[ii]):
                                pass
                            else:
                                raise Exception("This is not a valid polygon shape info.")
                        else:
                            raise Exception("This is not a valid polygon shape info.")               
                else:
                    raise Exception("This is not a valid polygon shape info.")
            elif shape_type == 'rectangle':
                if shape_info != []:
                    raise Exception("This is not a valid rectangle shape info.")
            elif shape_type == 'ellipse':
                # [[0.0, 0.0], [100.0, 100.0]]
                if isinstance(shape_info, list) and len(shape_info) == 2:
                    for ii in range(len(shape_info)):
                        if len(shape_info[ii]) == 2 and all((float(item) >= 0. and float(item) <= 100.) for item in shape_info[ii]):
                            pass
                        else:
                            raise Exception("This is not a valid ellipse shape info.")
                else:
                    raise Exception("This is not a valid ellipse shape info.")

    else:
        raise Exception("This is not a valid shape.")

    df_ReactionData_temp = df[2].copy()
    df_LineEndingData_temp = df[5].copy()
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    line_ending_id = []
    
    for i in range(len(idx_list)):
        line_ending_id.append(df[2].iloc[idx_list[i]]["modifiers_lineending"][mod_idx]) 
    if len(line_ending_id) == 1:
        if line_ending_id != ['line_ending_modifier_' + id + '_' + str(mod_idx)]:
            df_ReactionData_temp.at[idx_list[0],"modifiers_lineending"][mod_idx] = 'line_ending_modifier_' + id + '_' + str(mod_idx)
            idx_lineending = df_LineEndingData_temp.index[df[5]["id"] == line_ending_id[0]].tolist()
            if len(idx_lineending) == 1:
                row = len(df[5])
                LineEndingData_row_dct = df_LineEndingData_temp.to_dict('records')[idx_lineending[0]]
                keys = list(LineEndingData_row_dct.keys())
                values = list(LineEndingData_row_dct.values())
                for k in range(len(keys)):
                    LineEndingData_row_dct[keys[k]] = [values[k]]
                df_LineEndingData_temp = pd.concat([df_LineEndingData_temp,\
                                pd.DataFrame(LineEndingData_row_dct)], ignore_index=True)
                df_LineEndingData_temp.at[row,"id"] = 'line_ending_modifier_' + id + '_' + str(mod_idx)
                df_LineEndingData_temp.at[row,"shape_type"] = shape_type_list
                df_LineEndingData_temp.at[row,"shape_info"] = shape_info_list
        else:
            idx_lineending = df_LineEndingData_temp.index[df[5]["id"] == line_ending_id[0]].tolist()
            if len(idx_lineending) == 1:
                df_LineEndingData_temp.at[idx_lineending[0],"shape_type"] = shape_type_list
                df_LineEndingData_temp.at[idx_lineending[0],"shape_info"] = shape_info_list
            else:
                raise Exception("There is no initial modifier head information to edit.")
    else:
        raise Exception("This is not a valid id.")

    df_temp = (df[0], df[1], df_ReactionData_temp, df[3], df[4], df_LineEndingData_temp, df[6])

    return df_temp


# def _addText(df_text, txt_str, txt_position, txt_font_color = [0, 0, 0], opacity = 1., 
#     txt_line_width = 1., txt_font_size = 12.):
#     """
#     Set arbitray text onto canvas.

#     Args:  
#         txt_str: str-the text content.

#         txt_position: list-[position_x, position_y], the coordinate represents the top-left hand 
#         corner of the node text.

#         txt_font_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

#         opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

#         txt_line_width: float-node text line width.

#         txt_font_size: float-node text font size.
        
#     """
#     txt_font_color_rgba = _color_to_rgb(txt_font_color, opacity)
#     df_text_temp = df_text.copy()
#     text_row_dct = {k:[] for k in processSBML.COLUMN_NAME_df_text}
#     text_row_dct[processSBML.ID].append(txt_str)
#     text_row_dct[processSBML.TXTPOSITION].append(txt_position)
#     text_row_dct[processSBML.TXTFONTCOLOR].append(txt_font_color_rgba)
#     text_row_dct[processSBML.TXTLINEWIDTH].append(txt_line_width)
#     text_row_dct[processSBML.TXTFONTSIZE].append(txt_font_size)
#     if len(df_text_temp) == 0:
#         df_text_temp = pd.DataFrame(text_row_dct)
#     else:
#         df_text_temp = pd.concat([df_text_temp,\
#             pd.DataFrame(text_row_dct)], ignore_index=True)

#     return df_text_temp

# def _removeText(df_text, txt_str):
#     """
#     Set arbitray text onto canvas.

#     Args:  
#         txt_str: str-the text content.
        
#     """
#     df_text_temp = df_text.copy()
#     idx_list = df_text_temp.index[df_text_temp[processSBML.ID] == txt_str].tolist()
#     if len(idx_list) == 0:
#         raise Exception("This is not a valid text content.")
#     df_text_temp = df_text_temp.drop(idx_list)

#     return df_text_temp

def _setTextContent(df, txt_id, txt_content):

    """
    Set the arbitrary text content.

    Args:  
        df: DataFrame-initial information.

        txt_id: str-the text id.

        txt_content: str-the text content.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_TextData_temp = df[3].copy()
    idx_list = df[3].index[df[3]["id"] == txt_id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    for i in range(len(idx_list)):
        df_TextData_temp.at[idx_list[i],"txt_content"] = txt_content
    df_temp = (df[0], df[1], df[2], df_TextData_temp, df[4], df[5], df[6])

    return df_temp

def _setTextPosition(df, txt_id, txt_position):

    """
    Set the x,y coordinates of the node text position.

    Args:  
        df: DataFrame-initial information.

        txt_id: str-the text id.
        
        txt_position: list or point.Point()
            
        list-
        [txt_position_x, txt_position_y], the coordinate represents the top-left hand corner of 
        the node text.

        point.Point()-
        a Point object with attributes x and y representing
        the x/y position of the top-left hand corner of the text.
    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_TextData_temp = df[3].copy()
    idx_list = df[3].index[df[3]["id"] == txt_id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    if type(txt_position) != list and type(txt_position) != type(point.Point()):
        raise Exception("Please enter a valid txt_position type.")
    if type(txt_position) == type(point.Point()):
        txt_position = [txt_position.x, txt_position.y]
    for i in range(len(idx_list)):
        df_TextData_temp.at[idx_list[i],"txt_position"] = txt_position
    df_temp = (df[0], df[1], df[2], df_TextData_temp, df[4], df[5], df[6])

    return df_temp

def _setTextSize(df, txt_id, txt_size):

    """
    Set the arbitrary text size.

    Args:  
        df: DataFrame-initial information.

        txt_id: str-the text id.

        txt_size: list or point.Point()
            
        list-
        1*2 matrix-size of the text [width, height].

        point.Point()-
        a Point object with attributes x and y representing the width and height of 
        the text.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_TextData_temp = df[3].copy()
    idx_list = df[3].index[df[3]["id"] == txt_id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    if type(txt_size) != list and type(txt_size) != type(point.Point()):
        raise Exception("Please enter a valid txt_size type.")
    if type(txt_size) == type(point.Point()):
        txt_size = [txt_size.x, txt_size.y]
    for i in range(len(idx_list)):
        df_TextData_temp.at[idx_list[i],"txt_size"] = txt_size
    df_temp = (df[0], df[1], df[2], df_TextData_temp, df[4], df[5], df[6])

    return df_temp

def _setTextFontColor(df, txt_id, txt_font_color, opacity):

    """
    Set the arbitrary text font color.

    Args:  
        df: DataFrame-initial information.

        txt_id: str-the text id.

        txt_font_color: list-decimal_rgb 1*3 matrix/str-html_name/str-hex_string (6-digit).

        opacity: float-value is between [0,1], default is fully opaque (opacity = 1.).

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_TextData_temp = df[3].copy()
    idx_list = df[3].index[df[3]["id"] == txt_id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    txt_font_color = _color_to_rgb(txt_font_color, opacity)
    for i in range(len(idx_list)):
        df_TextData_temp.at[idx_list[i],"txt_font_color"] = txt_font_color
    df_temp = (df[0], df[1], df[2], df_TextData_temp, df[4], df[5], df[6])

    return df_temp

def _setTextLineWidth(df, txt_id, txt_line_width):

    """
    Set the arbitrary text line width (the stroke width value of the TEXTGLYPH).

    Args:  
        df: DataFrame-initial information.

        txt_id: str-the text id.

        txt_line_width: float-node text line width.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_TextData_temp = df[3].copy()
    idx_list = df[3].index[df[3]["id"] == txt_id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    for i in range(len(idx_list)):
        df_TextData_temp.at[idx_list[i],"txt_line_width"] = txt_line_width
    df_temp = (df[0], df[1], df[2], df_TextData_temp, df[4], df[5], df[6])

    return df_temp


def _setTextFontSize(df, txt_id, txt_font_size):

    """
    Set the arbitrary text font size.

    Args:  
        df: DataFrame-initial information.

        txt_id: str-the text id.

        txt_font_size: float-text font size.

    Returns:
        df_temp: DataFrame-information after updates. 
    
    """
    df_TextData_temp = df[3].copy()
    idx_list = df[3].index[df[3]["id"] == txt_id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    for i in range(len(idx_list)):
        df_TextData_temp.at[idx_list[i],"txt_font_size"] = txt_font_size
    df_temp = (df[0], df[1], df[2], df_TextData_temp, df[4], df[5], df[6])

    return df_temp



def _addText(df, txt_id, txt_content, txt_position, txt_size, 
    txt_font_color = [0, 0, 0], opacity = 1., txt_line_width = 1., txt_font_size = 12.,
    text_anchor = 'middle', text_vanchor = 'middle'):
    """
    Set arbitray text onto canvas.

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
    if type(txt_position) != list and type(txt_position) != type(point.Point()):
        raise Exception("Please enter a valid txt_position type.")
    if type(txt_position) == type(point.Point()):
        txt_position = [txt_position.x, txt_position.y]
    if type(txt_size) != list and type(txt_size) != type(point.Point()):
        raise Exception("Please enter a valid txt_size type.")
    if type(txt_size) == type(point.Point()):
        txt_size = [txt_size.x, txt_size.y]
    txt_font_color_rgba = _color_to_rgb(txt_font_color, opacity)
    df_TextData_temp = df[3].copy()
    text_row_dct = {k:[] for k in processSBML.COLUMN_NAME_df_TextData}
    text_row_dct[processSBML.TXTCONTENT].append(txt_content)
    text_row_dct[processSBML.TXTPOSITION].append(txt_position)
    text_row_dct[processSBML.TXTSIZE].append(txt_size)
    text_row_dct[processSBML.TXTFONTCOLOR].append(txt_font_color_rgba)
    text_row_dct[processSBML.TXTLINEWIDTH].append(txt_line_width)
    text_row_dct[processSBML.TXTFONTSIZE].append(txt_font_size)
    text_row_dct[processSBML.ID].append(txt_id)
    text_row_dct[processSBML.TXTANCHOR].append([text_anchor, text_vanchor])
                
    if len(df_TextData_temp) == 0:
        df_TextData_temp = pd.DataFrame(text_row_dct)
    else:
        df_TextData_temp = pd.concat([df_TextData_temp,\
            pd.DataFrame(text_row_dct)], ignore_index=True)

    df_temp = (df[0], df[1], df[2], df_TextData_temp, df[4], df[5], df[6])
    return df_temp


def _removeText(df, txt_id):
    """
    Remove the arbitray text.

    Args:  
        txt_id: str-the text id.
        
    """
    df_TextData_temp = df[3].copy()
    idx_list = df[3].index[df[3]["id"] == txt_id].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    df_TextData_temp = df_TextData_temp.drop(idx_list)
    df_temp = (df[0], df[1], df[2], df_TextData_temp, df[4], df[5], df[6])

    return df_temp

def _addRectangle(df, shape_name, position, size, fill_color=[255,255,255], fill_opacity = 1., border_color = [0,0,0], 
    border_opacity = 1., border_width = 2.):
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

    if type(position) != list and type(position) != type(point.Point()):
        raise Exception("Please enter a valid position type.")
    if type(position) == type(point.Point()):
        position = [position.x, position.y]
    if type(size) != list and type(size) != type(point.Point()):
        raise Exception("Please enter a valid size type.")
    if type(size) == type(point.Point()):
        size = [size.x, size.y]
    fill_color_rgba = _color_to_rgb(fill_color, fill_opacity)
    border_color_rgba = _color_to_rgb(border_color, border_opacity)
    df_ShapeData_temp = df[4].copy()
    shape_row_dct = {k:[] for k in processSBML.COLUMN_NAME_df_ShapeData}
    shape_row_dct[processSBML.SHAPENAME].append(shape_name)
    shape_row_dct[processSBML.POSITION].append(position)
    shape_row_dct[processSBML.SIZE].append(size)
    shape_row_dct[processSBML.FILLCOLOR].append(fill_color_rgba)
    shape_row_dct[processSBML.BORDERCOLOR].append(border_color_rgba)
    shape_row_dct[processSBML.BORDERWIDTH].append(border_width)
    shape_row_dct[processSBML.SHAPETYPE].append('rectangle')
    shape_row_dct[processSBML.SHAPEINFO].append([])
    if len(df_ShapeData_temp) == 0:
        df_ShapeData_temp = pd.DataFrame(shape_row_dct)
    else:
        df_ShapeData_temp = pd.concat([df_ShapeData_temp,\
            pd.DataFrame(shape_row_dct)], ignore_index=True)

    df_temp = (df[0], df[1], df[2], df[3], df_ShapeData_temp, df[5], df[6])
    return df_temp

def _addEllipse(df, shape_name, position, size, fill_color = [255,255,255], fill_opacity = 1., border_color = [0,0,0], 
    border_opacity = 1., border_width = 2.):
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
    
    if type(position) != list and type(position) != type(point.Point()):
        raise Exception("Please enter a valid position type.")
    if type(position) == type(point.Point()):
        position = [position.x, position.y]
    if type(size) != list and type(size) != type(point.Point()):
        raise Exception("Please enter a valid size type.")
    if type(size) == type(point.Point()):
        size = [size.x, size.y]
    fill_color_rgba = _color_to_rgb(fill_color, fill_opacity)
    border_color_rgba = _color_to_rgb(border_color, border_opacity)
    df_ShapeData_temp = df[4].copy()
    shape_row_dct = {k:[] for k in processSBML.COLUMN_NAME_df_ShapeData}
    shape_row_dct[processSBML.SHAPENAME].append(shape_name)
    shape_row_dct[processSBML.POSITION].append(position)
    shape_row_dct[processSBML.SIZE].append(size)
    shape_row_dct[processSBML.FILLCOLOR].append(fill_color_rgba)
    shape_row_dct[processSBML.BORDERCOLOR].append(border_color_rgba)
    shape_row_dct[processSBML.BORDERWIDTH].append(border_width)
    shape_row_dct[processSBML.SHAPETYPE].append('ellipse')
    shape_row_dct[processSBML.SHAPEINFO].append([])
    if len(df_ShapeData_temp) == 0:
        df_ShapeData_temp = pd.DataFrame(shape_row_dct)
    else:
        df_ShapeData_temp = pd.concat([df_ShapeData_temp,\
            pd.DataFrame(shape_row_dct)], ignore_index=True)

    df_temp = (df[0], df[1], df[2], df[3], df_ShapeData_temp, df[5], df[6])
    return df_temp

def _addPolygon(df, shape_name, shape_info, position, size, fill_color=[255,255,255], fill_opacity = 1., 
    border_color = [0,0,0], border_opacity = 1., border_width = 2.):
    """
    Add an polygon onto canvas.

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

    if type(position) != list and type(position) != type(point.Point()):
        raise Exception("Please enter a valid position type.")
    if type(position) == type(point.Point()):
        position = [position.x, position.y]
    if type(size) != list and type(size) != type(point.Point()):
        raise Exception("Please enter a valid size type.")
    if type(size) == type(point.Point()):
        size = [size.x, size.y]
    fill_color_rgba = _color_to_rgb(fill_color, fill_opacity)
    border_color_rgba = _color_to_rgb(border_color, border_opacity)
    df_ShapeData_temp = df[4].copy()
    shape_row_dct = {k:[] for k in processSBML.COLUMN_NAME_df_ShapeData}
    shape_row_dct[processSBML.SHAPENAME].append(shape_name)
    shape_row_dct[processSBML.POSITION].append(position)
    shape_row_dct[processSBML.SIZE].append(size)
    shape_row_dct[processSBML.FILLCOLOR].append(fill_color_rgba)
    shape_row_dct[processSBML.BORDERCOLOR].append(border_color_rgba)
    shape_row_dct[processSBML.BORDERWIDTH].append(border_width)
    shape_row_dct[processSBML.SHAPETYPE].append('polygon')
    shape_row_dct[processSBML.SHAPEINFO].append(shape_info)
    if len(df_ShapeData_temp) == 0:
        df_ShapeData_temp = pd.DataFrame(shape_row_dct)
    else:
        df_ShapeData_temp = pd.concat([df_ShapeData_temp,\
            pd.DataFrame(shape_row_dct)], ignore_index=True)

    df_temp = (df[0], df[1], df[2], df[3], df_ShapeData_temp, df[5], df[6])
    return df_temp


def _removeShape(df, shape_name_str):
    """
    Remove the arbitray shape.

    Args:  
        shape_name_str: str-the shape name.
        
    """
    df_ShapeData_temp = df[4].copy()
    idx_list = df[4].index[df[4]["shape_name"] == shape_name_str].tolist()
    if len(idx_list) == 0:
        raise Exception("This is not a valid id.")
    df_ShapeData_temp = df_ShapeData_temp.drop(idx_list)
    df_temp = (df[0], df[1], df[2], df[3], df_ShapeData_temp, df[5], df[6])

    return df_temp