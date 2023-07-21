# -*- coding: utf-8 -*-
# This script was written by Jin Xu and available on Github
# https://github.com/SunnyXu/SBMLDiagrams

"""
@author: Jin Xu and Jessie Jiang
"""

from operator import pos
import os
import re
from pandas import DataFrame
import skia
import simplesbml
import libsbml
import math
import random as _random
import string
from SBMLDiagrams import drawNetwork
from SBMLDiagrams import styleSBML
from SBMLDiagrams import processSBML
from SBMLDiagrams import visualizeInfo
from collections import defaultdict
import numpy as np
import cv2
import shutil
from IPython.core.display import Video 
#colab requires Ipython.core.display instead of Ipython.display
import json


def loadColorStyle(filename):
    """
    Load the color style information from a JSON file. 
    Note that the color style named default couldn't be changed.
    
    Args:
        filename: str-input json file name. Refer to the example in "Tutorial".

    Returns: 
        res: dictionary with the key of style name and the value with its corresponding style object.

    """
    file = open(filename)
    data = json.load(file)
    res = {}
    if "colorStyle" in data:
        for d in data["colorStyle"]:
            new_style = styleSBML.Style(d.get('style_name'),
                                        tuple(d.get('compartment_fill_color')),
                                        tuple(d.get('compartment_border_color')),
                                        tuple(d.get('species_fill_color')),
                                        tuple(d.get('species_border_color')),
                                        tuple(d.get('reaction_line_color')),
                                        tuple(d.get('lineending_fill_color')),
                                        tuple(d.get('lineending_border_color')),
                                        tuple(d.get('font_color')),
                                        tuple(d.get('progress_bar_fill_color')),
                                        tuple(d.get('progress_bar_full_fill_color')),
                                        tuple(d.get('progress_bar_border_color')),
                                        d.get('reaction_line_width'),
                                        d.get('species_border_width'),
                                        d.get('compartment_border_width'))
            res[d.get('style_name')] = new_style
    else:
        new_style = styleSBML.Style(data.get('style_name'),
                                    tuple(data.get('compartment_fill_color')),
                                    tuple(data.get('compartment_border_color')),
                                    tuple(data.get('species_fill_color')),
                                    tuple(data.get('species_border_color')),
                                    tuple(data.get('reaction_line_color')),
                                    tuple(data.get('lineending_fill_color')),
                                    tuple(data.get('lineending_border_color')),
                                    tuple(data.get('font_color')),
                                    tuple(data.get('progress_bar_fill_color')),
                                    tuple(data.get('progress_bar_full_fill_color')),
                                    tuple(data.get('progress_bar_border_color')),
                                    data.get('reaction_line_width'),
                                    data.get('species_border_width'),
                                    data.get('compartment_border_width'))
        res[data.get('style_name')] = new_style
    return res
        

def animate(start, end, points , r, thick_changing_rate, sbmlStr = None, frame_per_second = 10, show_digit = True,
            bar_dimension = (10,50), numDigit = 4, folderName = 'animation', outputName="output",
            horizontal_offset = 15, vertical_offset = 9, text_color = (0, 0, 0, 200), savePngs = False, showImage = False,
            user_reaction_line_color = None):
    """
    Animate to an mp4 file.

    Args:
        start: start point for the simulation.

        end: end point for the simulation.

        points: total points for the simulation.

        r: tellurium loada object.

        thick_changing_rate: thickness for the arrow, smaller means thinner.

        sbmlStr: sbml layout information if any.

        frame_per_second: number of frames per second of the ouput video.

        show_digit: if show digits.

        bar_dimension: width and height of the bar.

        numDigit: number of digits displayed.

        folderName: output folder name.

        outputName: ouput video name.

        horizontal_offset:  horizontal_offset of the bar from the node.

        vertical_offset: vertical offset of text from the node.

        text_color: color for the text.

        savePngs: if save all the pngs used for video generation.

        showImage: if display all the generated pngs in console.

        user_reaction_line_color: user defined reaction line color.

    """
    if not sbmlStr:
        sbmlStr = r.getSBML()
    v_info = _draw(sbmlStr,save = False, drawArrow = False)
    simulationData = r.simulate(start, end, points, selections=['time'] + r.getFloatingSpeciesIds())
    reactionRates = r.simulate(start, end, points, selections=r.getReactionIds())

    mx = float("-inf")
    floatingSpecies = r.getFloatingSpeciesIds()
    reactionIds = r.getReactionIds()
    baseImageArray = v_info.baseImageArray
    arrow_info = v_info.arrow_info
    color_style = v_info.color_style
    posDict = v_info.posDict
    dimDict = v_info.dimDict
    allPosDict = v_info.allPosDict
    allDimDict = v_info.allDimDict
    img_width, img_height = color_style.getImageSize()
    upNode = set()
    downNode = set()
    leftNode = set()

    def addNode(pos_list):
        n = len(pos_list)
        for i in range(n):
            cur_name = pos_list[i][0]
            cur_pos = pos_list[i][1]
            if cur_pos[0] + bar_dimension[0] + horizontal_offset > img_width // 2:
                leftNode.add(cur_name)
            if i > 0:
                old_name = pos_list[i - 1][0]
                old_pos = pos_list[i - 1][1]
                if abs(cur_pos[0] - old_pos[0]) < bar_dimension[0] + allDimDict[old_name][0] \
                        and abs(cur_pos[1] - old_pos[1]) < bar_dimension[1] - allDimDict[old_name][1]:
                    if cur_pos[1] - bar_dimension[1] - vertical_offset - allDimDict[cur_name][1] > 0:
                        upNode.add(cur_name)
                    else:
                        downNode.add(cur_name)
                    leftNode.add(old_name)

    pos_list = list(allPosDict.items())
    pos_list.sort(key=lambda x:x[1][0])
    addNode(pos_list)
    pos_list.sort(key=lambda x: x[1][1])
    addNode(pos_list)

    for species in floatingSpecies:
        mx = max(mx,max(simulationData[species]))

    mx_reaction_rate = float('-inf')
    min_reaction_rate = float('inf')
    for reaction in reactionIds:
        mx_reaction_rate = max(mx_reaction_rate,max(reactionRates[reaction]))
        min_reaction_rate = min(min_reaction_rate, min(reactionRates[reaction]))

    for i in range(len(simulationData)):
        temp = np.array(baseImageArray, copy=True)
        surface = skia.Surface(temp)
        canvas = surface.getCanvas()
        for j,info in enumerate(arrow_info):
            rate = reactionRates[reactionIds[j]][i]*(1/mx_reaction_rate*min_reaction_rate*thick_changing_rate)
            temp_id, src_position, dst_position, mod_position,center_position, \
            handles, src_dimension, dst_dimension, mod_dimension,\
            reaction_line_color, reaction_line_width, reactionLineType,\
            showBezierHandles, showReactionIds, head, scale, reaction_dash, rxn_rev, showReversible= info

            if not user_reaction_line_color:
                user_reaction_line_color = reaction_line_color

            
            drawNetwork.addReaction(canvas,temp_id, src_position, dst_position, mod_position,
                            center_position, handles, src_dimension, dst_dimension, mod_dimension,
                            reaction_line_color = user_reaction_line_color, reaction_line_width = reaction_line_width*rate,
                            reaction_line_type = reactionLineType, show_bezier_handles = showBezierHandles,
                            reaction_arrow_head_size = head, show_reaction_ids = showReactionIds, scale = scale,
                            reaction_dash = reaction_dash, reverse = rxn_rev, showReversible = showReversible)

        for letter, pos in posDict.items():
            [node_width, node_height] = dimDict[letter]
            if letter in upNode:
                cur_pos = [pos[0]+node_width//2, pos[1] - node_height//2]
                txt_pos = [pos[0]+node_width//2-vertical_offset, pos[1] - node_height//2 + vertical_offset]
            elif letter in downNode:
                cur_pos = [pos[0]+node_width//2, pos[1] + bar_dimension[1]*2]
                txt_pos = [pos[0]+node_width//2, pos[1] + vertical_offset + bar_dimension[1]*2]
            elif letter in leftNode:
                cur_pos = [pos[0], pos[1]+node_height]
                txt_pos = [pos[0] - horizontal_offset, pos[1]+node_height+vertical_offset]
            else:
                cur_pos = [pos[0] + node_width + horizontal_offset, pos[1]+node_height]
                txt_pos = [pos[0] + node_width, pos[1]+node_height+vertical_offset]
            percent = simulationData[letter][i]/mx
            drawNetwork.addProgressBar(canvas, cur_pos, bar_dimension, percent, 1,
                                       color_style)
            if show_digit:
                drawNetwork.addSimpleText(canvas, str(simulationData[letter][i])[:numDigit+1],txt_pos, text_color)

        drawNetwork.showPlot(surface, folderName='animation', fileName=str(i), file_format='PNG', showImage = showImage)

    imgs = []
    size = None
    files = os.listdir(os.getcwd() + '/' + folderName)
    files.sort(key=lambda f: int(re.sub('\D', '', f)))
    for filename in files:
        if filename[-4:] == ".png":
            imgName = os.path.join(os.getcwd() + '/' + folderName, filename)
            img = cv2.imread(imgName)
            height, width, layers = img.shape
            size = (width, height)
            imgs.append(img)

    out = cv2.VideoWriter(os.path.join(os.getcwd() + '/' + outputName + ".mp4"),
                          cv2.VideoWriter_fourcc(*'MP4V'), frame_per_second, size)

    for i in range(len(imgs)):
        out.write(imgs[i])
    out.release()

    if not savePngs:
        print(os.path.join(os.getcwd())  + '/' + folderName)
        shutil.rmtree(os.path.join(os.getcwd())  + '/' + folderName)

    Video(outputName + ".mp4")

def _draw(sbmlStr, setImageSize = [], scale = 1.,\
    output_fileName = '', complexShape = '', reactionLineType = 'bezier', \
    showBezierHandles = False, showReactionIds = False, showReversible = False, longText = 'auto-font',\
    newStyle = styleSBML.Style(), drawArrow = True, showImage = True, save = True): 
    #df_text = DataFrame(columns = processSBML.COLUMN_NAME_df_text), #dataframe-arbitrary text

    """
    Plot from an sbml string to a PNG/JPG/PDF file.

    Args:  
        sbmlStr: str-the string of the input sbml file.

        setImageSize: list-1*2 matrix-size of the image [width, height].

        scale: float-makes the figure output size = scale * default output size.
        Increasing the scale can make the resolution higher.

        output_fileName: str-filename: '' (default: will not save the file), 
        or 'fileName.png' (self-designed file name) which has to end up with '.png', '.jpg', or 'pdf'.
        
        complexShape: str-type of complex shapes: '' (default) or 'monomer' or 'dimer' or 'trimer' 
        or 'tetramer'.

        reactionLineType: str-type of the reaction line: 'straight' or 'bezier' (default).
        If there is no layout information from the SBML file, all reaction lines will look like
        straight lines even set as 'bezier' because they are set as default center and handle positions.

        showBezierHandles: bool-show the Bezier handles (True) or not (False as default).

        showReactionIds: bool-show the reaction ids (True) or not (False as default).

        showReversible: bool-show reversible reactions or not.

        longText: str-'auto-font'(default) will automatically decrease the font size to fit to the 
        node; 'ellipsis' will show '....' if the text is too long to show in the node

        newStyle: color style class.

        drawArrow: bool-draw arrow or not

        showImage: whether to display the image inside console.

        save: whether to save the png.

    Returns:
        The visualization info object containing the drawing information of the plot
    """

    df = processSBML.load(sbmlStr)
    sbmlStr = df.export()
    
    topLeftCorner = _getNetworkTopLeftCorner(sbmlStr)
    networkSize = _getNetworkSize(sbmlStr)

    topLeftCorner = [topLeftCorner[0]-10, topLeftCorner[1]-10]

    if setImageSize == []:
        imageSize = [(networkSize[0]*scale+20*scale), (networkSize[1]*scale+20*scale)]
    else:
        imageSize = setImageSize
        scale = min(setImageSize[0]/(networkSize[0]+20), setImageSize[1]/(networkSize[1]+20))

    color_style = newStyle
    color_style.setImageSize(imageSize)

    def draw_on_canvas(canvas, color_style):
        arrow_info = []
        def hex_to_rgb(value):
            value = value.lstrip('#')
            if len(value) == 6:
                value = value + 'ff'
            return tuple(int(value[i:i+2], 16) for i in (0, 2, 4, 6))

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
        specRefGlyph_id_list = []
        specGlyph_specRefGlyph_id_list = []
        allNodes_pos_dict = defaultdict(list)
        allNodes_dim_dict = defaultdict(list)
        floatingNodes_pos_dict = defaultdict(list)
        floatingNodes_dim_dict = defaultdict(list)
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
        comp_border_width = 2.0
        spec_border_width = 2.0
        spec_dash = []
        shapeIdx = 1
        shape_name = ''
        shape_type = ''
        shape_info = []
        reaction_line_width = 3.0
        reaction_arrow_head_size = [reaction_line_width*5, reaction_line_width*4]
        reaction_dash = []
        reaction_line_fill = [255, 255, 255, 255]
        reaction_shape_name = ''
        reaction_shape_type = ''
        reaction_shape_info = []
        text_content = ''
        text_line_color = [0, 0, 0, 255]
        text_line_width = 1.
        text_font_size = 12. 
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

        edges = []
        id_to_name = defaultdict(lambda:"")
        name_to_id = defaultdict(lambda:"")

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

                        reaction = model_layout.getReaction(reaction_id)
                        rev = reaction.getReversible()
                        reaction_id_list.append(reaction_id)
                        reactionGlyph_id_list.append(reactionGlyph_id)
                        reaction_rev_list.append(rev)
                        reaction = model_layout.getReaction(reaction_id)
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
                            spec_boundingbox = specGlyph.getBoundingBox()
                            width = spec_boundingbox.getWidth()
                            height = spec_boundingbox.getHeight()
                            pos_x = spec_boundingbox.getX()
                            pos_y = spec_boundingbox.getY()
                            
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

                            # if text_content == 'Mt-DNA repair':
                            #         print("node:", [pos_x, pos_y])
                            #         print("text:", [text_pos_x, text_pos_y])


                            if specGlyph_id not in specGlyph_id_list:
                                spec_id_list.append(spec_id)
                                specGlyph_id_list.append(specGlyph_id)
                                spec_specGlyph_id_list.append([spec_id,specGlyph_id])
                                id_to_name[specGlyph_id] = spec_id
                                name_to_id[spec_id] = specGlyph_id
                                spec_dimension_list.append([width,height])
                                spec_position_list.append([pos_x,pos_y])
                                if text_content == '':
                                    text_content = spec_id
                                spec_text_content_list.append(text_content)
                                spec_text_position_list.append([text_pos_x, text_pos_y])
                                spec_text_dimension_list.append([text_dim_w, text_dim_h])

                            if role == "substrate" or role == "sidesubstrate": #it is a rct
                                #rct_specGlyph_temp_list.append(specGlyph_id)
                                rct_specGlyph_handles_temp_list.append([specGlyph_id,spec_handle,specRefGlyph_id,spec_lineend_pos])
                                if center_handle == []:
                                    center_handle.append(center_handle_candidate)
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

                    #orphan nodes
                    for i in range(numSpecGlyphs):
                        specGlyph = layout.getSpeciesGlyph(i)
                        specGlyph_id = specGlyph.getId()
                        if specGlyph_id not in specGlyph_id_list:
                            specGlyph_id_list.append(specGlyph_id)
                            spec_id = specGlyph.getSpeciesId()
                            spec_id_list.append(spec_id)
                            spec_specGlyph_id_list.append([spec_id,specGlyph_id])
                            id_to_name[specGlyph_id] = spec_id
                            name_to_id[spec_id] = specGlyph_id
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

                    rPlugin = layout.getPlugin("render")
                    if (rPlugin != None and rPlugin.getNumLocalRenderInformationObjects() > 0):
                        info = rPlugin.getRenderInformation(0)
                        color_list = []
                        gradient_list = []
                        # comp_render = []
                        # spec_render = []
                        # rxn_render = []
                        # text_render = []
                        # lineEnding_render = []
                        # gen_render = []
                        # specRefGlyph_render = []
                        arrowHeadSize = reaction_arrow_head_size #default if there is no lineEnding
                        id_arrowHeadSize = []

                        for  j in range ( 0, info.getNumColorDefinitions()):
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
                            if not color_style.getStyleName():
                                color_style.setLineEndingFillColor(lineEnding_fill_color)
                                
                            lineEnding_border_color = []
                            for k in range(len(color_list)):
                                if color_list[k][0] == group.getStroke():
                                    lineEnding_border_color = hex_to_rgb(color_list[k][1])
                            if not color_style.getStyleName():
                                color_style.setLineEndingBorderColor(lineEnding_border_color)

                                    
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
                                
                            lineEnding_render.append([temp_id, temp_pos, temp_size, 
                            color_style.getLineEndingFillColor(), shape_type, shapeInfo, color_style.getLineEndingBorderColor()])

                        #print(info.getNumGradientDefinitions())
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
                                for kk in range(len(color_list)):
                                    if color_list[kk][0] == stop_color_name:
                                        stop_color = hex_to_rgb(color_list[kk][1])
                                stop_info.append([offset,stop_color])
                            gradient_list.append([id,grad_type,grad_info,stop_info])

                        for j in range (0, info.getNumStyles()):
                            style = info.getStyle(j)
                            group = style.getGroup()
                            typeList = style.createTypeString()
                            idList = style.createIdString()
                                
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

                            if 'COMPARTMENTGLYPH' in typeList:
                                #change layout id to id for later to build the list of render
                                render_comp_id = idList
                                for k in range(len(compGlyph_id_list)):    
                                    if compGlyph_id_list[k] == idList:
                                        render_comp_id = comp_id_list[k] 
                                if idList == 'CompG__compartment_default_':
                                    render_comp_id = '_compartment_default_'                        

                                for k in range(len(color_list)):
                                    if color_list[k][0] == group.getFill():
                                        if not color_style.getStyleName():
                                            color_style.setCompFillColor(hex_to_rgb(color_list[k][1]))
                                    if color_list[k][0] == group.getStroke():
                                        if not color_style.getStyleName():
                                            color_style.setCompBorderColor(hex_to_rgb(color_list[k][1]))

                                comp_border_width = group.getStrokeWidth()
                                if not color_style.getStyleName():
                                    color_style.setCompBorderWidth(comp_border_width)
                                
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
                                comp_render.append([render_comp_id, color_style.getCompFillColor(),
                                                    color_style.getCompBorderColor(),color_style.getCompBorderWidth(),
                                                    shape_name, shape_type, shapeInfo])
                            elif 'SPECIESGLYPH' in typeList:
                                #change layout id to id for later to build the list of render
                                render_spec_id = idList

                                for k in range(len(spec_specGlyph_id_list)):    
                                    if spec_specGlyph_id_list[k][1] == idList:
                                        render_spec_id = spec_specGlyph_id_list[k][0] 
                                        spec_dimension = spec_dimension_list[k]
                                for k in range(len(color_list)):
                                    if color_list[k][0] == group.getFill():
                                        if not color_style.getStyleName():
                                            color_style.setSpecFillColor(hex_to_rgb(color_list[k][1]))
                                    if color_list[k][0] == group.getStroke():
                                        if not color_style.getStyleName():
                                            color_style.setSpecBorderColor(hex_to_rgb(color_list[k][1]))
                                spec_fill_color = []
                                for k in range(len(gradient_list)):
                                    if gradient_list[k][0] == group.getFill():
                                        spec_fill_color = gradient_list[k][1:]
                                
                                spec_border_width = group.getStrokeWidth()
                                if not color_style.getStyleName():
                                    color_style.setSpecBorderWidth(spec_border_width)

                                spec_dash = []
                                if group.isSetDashArray():
                                    spec_num_dash = group.getNumDashes()
                                    for num in range(spec_num_dash):
                                        spec_dash.append(group.getDashByIndex(num))
                                
                                #name_list = []
                                shape_type = ''
                                #print(group.getNumElements())# There is only one element
                                #for element in group.getListOfElements():
                                element = group.getElement(0)
                                shapeIdx = 0
                                shape_name = 'text_only'
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
                                            downTriangle_vertex = [[0,19.4],[100,19.4],[50.,100.]]
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

                                if spec_fill_color != []:
                                   spec_render.append([render_spec_id,spec_fill_color,
                                   color_style.getSpecBorderColor(),color_style.getSpecBorderWidth(),
                                   shapeIdx,shape_name,shape_type,shapeInfo,spec_dash])
                                else:
                                    spec_render.append([render_spec_id,
                                    color_style.getSpecFillColor(),color_style.getSpecBorderColor(),color_style.getSpecBorderWidth(),
                                    shapeIdx,shape_name,shape_type,shapeInfo,spec_dash])
                                
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
                                for k in range(len(id_arrowHeadSize)):
                                    if temp_id == id_arrowHeadSize[k][0]:
                                        arrowHeadSize = id_arrowHeadSize[k][1]
                                for k in range(len(color_list)):
                                    if color_list[k][0] == group.getStroke():
                                        if not color_style.getStyleName():
                                            color_style.setReactionLineColor(hex_to_rgb(color_list[k][1]))
                                    if color_list[k][0] == group.getFill():
                                        reaction_line_fill = hex_to_rgb(color_list[k][1])
                                        
                                reaction_line_width = group.getStrokeWidth()
                                if not color_style.getStyleName():
                                    color_style.setReactionLineWidth(reaction_line_width)
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

                                rxn_render.append([render_rxn_id, color_style.getReactionLineColor(), 
                                color_style.getReactionLineWidth(), arrowHeadSize, reaction_dash, reaction_line_fill,
                                shape_name, shape_type, shape_info])
                            elif 'TEXTGLYPH' in typeList:
                                render_text_id = idList
                                for k in range(len(textGlyph_comp_id_list)):    
                                    if textGlyph_comp_id_list[k][1] == idList:
                                        render_text_id = textGlyph_comp_id_list[k][0] 
                                for k in range(len(textGlyph_spec_id_list)):    
                                    if textGlyph_spec_id_list[k][1] == idList:
                                        render_text_id = textGlyph_spec_id_list[k][0]
                                    
                                for k in range(len(color_list)):
                                    if color_list[k][0] == group.getStroke():
                                        if not color_style.getStyleName():
                                            color_style.setTextLineColor(hex_to_rgb(color_list[k][1]))
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
                                text_render.append([render_text_id,color_style.getTextLineColor(),
								text_line_width, text_font_size,[text_anchor, text_vanchor],
                                idList, text_font_family])

                            elif 'GENERALGLYPH' in typeList:
                                render_gen_id = idList
                                for k in range(len(color_list)):
                                    if color_list[k][0] == group.getFill():
                                        gen_fill_color = hex_to_rgb(color_list[k][1])
                                    if color_list[k][0] == group.getStroke():
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


        #try: 
            model = simplesbml.loadSBMLStr(sbmlStr)
            numFloatingNodes  = model.getNumFloatingSpecies()
            FloatingNodes_ids = model.getListOfFloatingSpecies()
            numBoundaryNodes  = model.getNumBoundarySpecies()
            BoundaryNodes_ids = model.getListOfBoundarySpecies()
            numRxns   = model.getNumReactions()
            Rxns_ids  = model.getListOfReactionIds()
            numComps  = model.getNumCompartments()
            Comps_ids = model.getListOfCompartmentIds()
            # if "_compartment_default_" in Comps_ids:
            #     numComps -= 1
            #     Comps_ids.remove("_compartment_default_")
            numNodes = numFloatingNodes + numBoundaryNodes
            comp_node_list = [0]*numComps #Note: numComps is different from numCompGlyphs
            comp_specs_in_list = []
            for i in range(numComps):
                comp_node_list[i] = []
            for i in range(numComps):#only consider the compartment with species in
                for j in range(numFloatingNodes):
                    comp_id = model.getCompartmentIdSpeciesIsIn(FloatingNodes_ids[j])
                    if comp_id not in comp_specs_in_list:
                        comp_specs_in_list.append(comp_id)
                for j in range(numBoundaryNodes):
                    comp_id = model.getCompartmentIdSpeciesIsIn(BoundaryNodes_ids[j])
                    if comp_id not in comp_specs_in_list:
                        comp_specs_in_list.append(comp_id)

            #if there is layout info:
            if len(spec_id_list) != 0 or len(textGlyph_id_list) != 0 or len(gen_id_list) != 0:
                for i in range(numComps):
                    temp_id = Comps_ids[i]
                    if temp_id in comp_specs_in_list:
                        vol= model.getCompartmentVolume(i)
                        dimension = imageSize
                        position = [0.,0.]
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
                                dimension = imageSize
                                color_style.setImageSize(dimension)
                                position = [0, 0]
                            for j in range(len(comp_id_list)):
                                if comp_id_list[j] == temp_id:
                                    dimension = [comp_dimension_list[j][0]*scale,
                                    comp_dimension_list[j][1]*scale]
                                    color_style.setImageSize(dimension)
                                    position = [(comp_position_list[j][0] - topLeftCorner[0])*scale,
                                    (comp_position_list[j][1] - topLeftCorner[1])*scale]
                            for j in range(len(comp_text_content_list)):
                                if comp_id_list[j] == temp_id:
                                    text_content = comp_text_content_list[j]
                                    text_position = [(comp_text_position_list[j][0] - topLeftCorner[0])*scale,
                                    (comp_text_position_list[j][1] - topLeftCorner[1])*scale]
                                    text_dimension = [comp_text_dimension_list[j][0]*scale,
                                    comp_text_dimension_list[j][1]*scale]
                                    #print(dimension, position, text_content, text_position, text_dimension)

                            for j in range(len(comp_render)):
                                if temp_id == comp_render[j][0]:
                                    if not color_style.getStyleName():
                                        color_style.setCompFillColor(comp_render[j][1])
                                        color_style.setCompBorderColor(comp_render[j][2])
                                        color_style.setCompBorderWidth(comp_render[j][3])
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
                

                        else:# no layout info about compartment,
                            # then the whole size of the canvas is the compartment size
                            dimension = imageSize
                            color_style.setImageSize(dimension)
                            position = [0.,0.]
                            text_content = ''
                            text_position = [0.,0.]
                            text_dimension = [0.,0.]
                            comp_shape_name = ''
                            comp_shape_type = ''
                            comp_shape_info = []
                            #allows users to set the color of the "_compartment_default" as the canvas
                            #color_style.setCompBorderColor((255, 255, 255, 255))
                            #color_style.setCompFillColor((255, 255, 255, 255)
                        drawNetwork.addCompartment(canvas, position, dimension,
                        color_style.getCompBorderColor(), color_style.getCompFillColor(),color_style.getCompBorderWidth()*scale, 
                        comp_shape_type=comp_shape_type, comp_shape_info=comp_shape_info)

                        if text_content != '':
                            drawNetwork.addText(canvas, text_content, text_position, text_dimension,
                        text_line_color, text_line_width*scale, text_font_size*scale, textAnchor = [text_anchor, text_vanchor]) 
                    
                
                #add reactions before adding nodes to help with the line positions
                numSpec_in_reaction = len(spec_specGlyph_id_list)
                for i in range (numReactionGlyphs):
                    src_position = []
                    src_dimension = [] 
                    src_endhead = []
                    src_dash = []
                    src_lineend_pos = []
                    dst_position = []
                    dst_dimension = []
                    dst_endhead = []
                    dst_dash = []
                    dst_lineend_pos = []
                    mod_position = []
                    mod_dimension = []
                    mod_endhead = []
                    mod_lineend_pos = []
                    src_handle = []
                    dst_handle = []
                    temp_id = reaction_id_list[i]
                    rxn_rev = reaction_rev_list[i]
                    kinetics = kinetics_list[i]
                    #rct_num = len(rct_specGlyph_list[i])
                    #prd_num = len(prd_specGlyph_list[i])
                    #rct_num = max(len(rct_specGlyph_handle_list[i]),len(reaction_rct_list[i]))
                    # prd_num = max(len(prd_specGlyph_handle_list[i]),len(reaction_prd_list[i]))
                    # mod_num = max(len(mod_specGlyph_list[i]),len(reaction_mod_list[i]))
                    rct_num = len(rct_specGlyph_handle_list[i])
                    prd_num = len(prd_specGlyph_handle_list[i])
                    mod_num = len(mod_specGlyph_list[i])

                    add_rct_cnt = 0
                    for j in range(rct_num):
                        temp_specGlyph_id = rct_specGlyph_handle_list[i][j][0]
                        temp_specRefGlyph_id = rct_specGlyph_handle_list[i][j][2]
                        for k in range(numSpec_in_reaction):
                            if temp_specGlyph_id == specGlyph_id_list[k]:
                                src_position.append([(spec_position_list[k][0]-topLeftCorner[0])*scale,
                                (spec_position_list[k][1]-topLeftCorner[1])*scale])
                                src_dimension.append([spec_dimension_list[k][0]*scale,
                                spec_dimension_list[k][1]*scale])
                        for k in range(len(specRefGlyph_render)):
                            if temp_specRefGlyph_id == specRefGlyph_render[k][0]:
                                src_endhead.append(specRefGlyph_render[k][1])
                        for k in range(len(specRefGlyph_render)):
                            if temp_specRefGlyph_id == specRefGlyph_render[k][0]:
                                src_dash = specRefGlyph_render[k][2]
                        src_handle.append(rct_specGlyph_handle_list[i][j][1])
                        src_lineend_pos.append(rct_specGlyph_handle_list[i][j][3])
                        add_rct_cnt += 1
                        edges.append([id_to_name[temp_specGlyph_id]])

                    for j in range(prd_num):
                        temp_specGlyph_id = prd_specGlyph_handle_list[i][j][0]
                        temp_specRefGlyph_id = prd_specGlyph_handle_list[i][j][2]
                        for k in range(numSpec_in_reaction):
                            if temp_specGlyph_id == specGlyph_id_list[k]:
                                dst_position.append([(spec_position_list[k][0]-topLeftCorner[0])*scale,
                                (spec_position_list[k][1]-topLeftCorner[1])*scale])
                                dst_dimension.append([spec_dimension_list[k][0]*scale,
                                spec_dimension_list[k][1]*scale])
                        for k in range(len(specRefGlyph_render)):
                            if temp_specRefGlyph_id == specRefGlyph_render[k][0]:
                                dst_endhead.append(specRefGlyph_render[k][1])
                        for k in range(len(specRefGlyph_render)):
                            if temp_specRefGlyph_id == specRefGlyph_render[k][0]:
                                dst_dash = specRefGlyph_render[k][2]
                        dst_handle.append(prd_specGlyph_handle_list[i][j][1])
                        dst_lineend_pos.append(prd_specGlyph_handle_list[i][j][3])
                        try:
                            edges[-add_rct_cnt].append(id_to_name[temp_specGlyph_id])
                        except:
                            pass
                        add_rct_cnt -= 1

                    for j in range(mod_num):
                        #if len(mod_specGlyph_list[i]) != 0:
                        if len(mod_specGlyph_list[i]) == mod_num: 
                            #all the modifiers are defined as role in the SpecRefGlyph
                            temp_specGlyph_id = mod_specGlyph_list[i][j][0]      
                            temp_specRefGlyph_id = mod_specGlyph_list[i][j][1]
                            mod_lineend_pos.append(mod_specGlyph_list[i][j][2])
                            for k in range(numSpec_in_reaction):
                                if temp_specGlyph_id == specGlyph_id_list[k]:
                                    mod_position.append([(spec_position_list[k][0]-topLeftCorner[0])*scale,
                                    (spec_position_list[k][1]-topLeftCorner[1])*scale])
                                    mod_dimension.append([spec_dimension_list[k][0]*scale,
                                    spec_dimension_list[k][1]*scale])
                            for k in range(len(specRefGlyph_render)):
                                if temp_specRefGlyph_id == specRefGlyph_render[k][0]:
                                    mod_endhead.append(specRefGlyph_render[k][1])
                        else:
                            for k in range(len(spec_specGlyph_id_list)):
                                if reaction_mod_list[i][j] == spec_specGlyph_id_list[k][0]:
                                    temp_specGlyph_id = spec_specGlyph_id_list[k][1]
                            for k in range(numSpec_in_reaction):
                                if temp_specGlyph_id == specGlyph_id_list[k]:
                                    mod_position.append([(spec_position_list[k][0]-topLeftCorner[0])*scale,
                                    (spec_position_list[k][1]-topLeftCorner[1])*scale])
                                    mod_dimension.append([spec_dimension_list[k][0]*scale,
                                    spec_dimension_list[k][1]*scale])
                            for k in range(len(specRefGlyph_render)):
                                if temp_specRefGlyph_id == specRefGlyph_render[k][0]:
                                    mod_endhead.append(specRefGlyph_render[k][1])

                    for j in range(len(rxn_render)):
                        if temp_id == rxn_render[j][0]:
                            if not color_style.getStyleName():
                                color_style.setReactionLineColor(rxn_render[j][1])
                                color_style.setReactionLineWidth(rxn_render[j][2])
                            reaction_line_width = rxn_render[j][2]
                            reaction_arrow_head_size = rxn_render[j][3]
                            reaction_dash = rxn_render[j][4]
                            reaction_line_fill = rxn_render[j][5]
                            reaction_shape_name = rxn_render[j][6]
                            reaction_shape_type = rxn_render[j][7]
                            reaction_shape_info = rxn_render[j][8]

                    try:
                        if reaction_dash == [] and src_dash != []:
                            reaction_dash = src_dash
                    except:
                        if reaction_dash == [] and dst_dash != []:
                            reaction_dash = dst_dash
                    
                    src_endhead_render = []
                    dst_endhead_render = []
                    mod_endhead_render = []
                    #print(lineEnding_render)
                    for j in range(len(src_endhead)):
                        for k in range(len(lineEnding_render)):
                            if src_endhead[j] == lineEnding_render[k][0]:
                                temp_lineending_render = lineEnding_render[k][1:]
                                color_style.setLineEndingFillColor(temp_lineending_render[2]) 
                                color_style.setLineEndingBorderColor(temp_lineending_render[5])
                                src_endhead_render.append(temp_lineending_render)
                    for j in range(len(dst_endhead)):
                        for k in range(len(lineEnding_render)):
                            if dst_endhead[j] == lineEnding_render[k][0]:
                                # if dst_endhead[j] == '_line_ending_default_':
                                #     dst_endhead_render = []
                                # else:
                                temp_lineending_render = lineEnding_render[k][1:]
                                color_style.setLineEndingFillColor(temp_lineending_render[2]) 
                                color_style.setLineEndingBorderColor(temp_lineending_render[5])
                                dst_endhead_render.append(temp_lineending_render)
                    for j in range(len(mod_endhead)):
                        for k in range(len(lineEnding_render)):
                            if mod_endhead[j] == lineEnding_render[k][0]:
                                temp_lineending_render = lineEnding_render[k][1:]
                                color_style.setLineEndingFillColor(temp_lineending_render[2]) 
                                color_style.setLineEndingBorderColor(temp_lineending_render[5])
                                mod_endhead_render.append(temp_lineending_render)

                    for j in range(len(src_lineend_pos)):
                        try:
                            src_lineend_pos[j] = [(src_lineend_pos[j][0]-topLeftCorner[0])*scale, 
                            (src_lineend_pos[j][1]-topLeftCorner[1])*scale]
                        except:
                            src_lineend_pos[j] = []
                    for j in range(len(dst_lineend_pos)):
                        try:
                            dst_lineend_pos[j] = [(dst_lineend_pos[j][0]-topLeftCorner[0])*scale, 
                            (dst_lineend_pos[j][1]-topLeftCorner[1])*scale]
                        except:
                            dst_lineend_pos[j] = []
                    for j in range(len(mod_lineend_pos)):
                        try:
                            mod_lineend_pos[j] = [(mod_lineend_pos[j][0]-topLeftCorner[0])*scale, 
                            (mod_lineend_pos[j][1]-topLeftCorner[1])*scale]
                        except:
                            mod_lineend_pos[j] = []

                    try: 
                        center_size = [0.,0.]
                        center_position = reaction_center_list[i]
                        center_size = reaction_size_list[i]
                        center_size = [center_size[0]*scale,center_size[1]*scale]
                        center_handle = reaction_center_handle_list[i]
                        if center_handle != []:
                            handles = [center_handle]
                        else:
                            handles = [center_position]
                        handles.extend(src_handle)
                        handles.extend(dst_handle)
                    
                        center_position = [(center_position[0]-topLeftCorner[0])*scale, 
                        (center_position[1]-topLeftCorner[1])*scale]
                        for j in range(len(handles)):
                            handles[j] = [(handles[j][0]-topLeftCorner[0])*scale, 
                            (handles[j][1]-topLeftCorner[1])*scale]

                        if drawArrow:
                            drawNetwork.addReaction(canvas, temp_id, src_position, dst_position, mod_position,
                                center_position, handles, src_dimension, dst_dimension, mod_dimension,
                                color_style.getReactionLineColor(), color_style.getReactionLineWidth()*scale,
                                reaction_line_type = reactionLineType, show_bezier_handles = showBezierHandles,
                                show_reaction_ids = showReactionIds,
                                reaction_arrow_head_size = [reaction_arrow_head_size[0]*scale, reaction_arrow_head_size[1]*scale],
                                scale = scale, reaction_dash = reaction_dash, reverse = rxn_rev, showReversible = showReversible,
                                rct_endhead_render = src_endhead_render, prd_endhead_render = dst_endhead_render, mod_endhead_render = mod_endhead_render,
                                rct_lineend_pos = src_lineend_pos, prd_lineend_pos = dst_lineend_pos, mod_lineend_pos = mod_lineend_pos,
                                center_size = center_size, shape_name = shape_name, shape_type = shape_type, shape_info = shape_info,
                                reaction_line_fill = reaction_line_fill)
                        arrow_info.append(
                            [temp_id, src_position, dst_position, mod_position, center_position, handles, src_dimension,
                             dst_dimension, mod_dimension,
                             color_style.getReactionLineColor(), color_style.getReactionLineWidth() * scale, reactionLineType,
                             showBezierHandles, showReactionIds,
                             [reaction_arrow_head_size[0] * scale, reaction_arrow_head_size[1] * scale],
                             scale, reaction_dash, rxn_rev, showReversible])
                    except:
                        center_x = 0.
                        center_y = 0.
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
                        if drawArrow:
                            drawNetwork.addReaction(canvas, temp_id, src_position, dst_position, mod_position,
                                center_position, handles, src_dimension, dst_dimension, mod_dimension,
                                color_style.getReactionLineColor(), color_style.getReactionLineWidth()*scale,
                                reaction_line_type = reactionLineType, show_bezier_handles = showBezierHandles,
                                show_reaction_ids = showReactionIds,
                                reaction_arrow_head_size = [reaction_arrow_head_size[0]*scale, reaction_arrow_head_size[1]*scale],
                                scale = scale, reaction_dash = reaction_dash, reverse = rxn_rev, showReversible = showReversible,
                                rct_endhead_render = src_endhead_render, prd_endhead_render = dst_endhead_render, mod_endhead_render = mod_endhead_render,
                                rct_lineend_pos = src_lineend_pos, prd_lineend_pos = dst_lineend_pos, mod_lineend_pos = mod_lineend_pos,
                                center_size = center_size, shape_name = shape_name, shape_type = shape_type, shape_info = shape_info,
                                reaction_line_fill = reaction_line_fill)
                        arrow_info.append(
                            [temp_id, src_position, dst_position, mod_position, center_position, handles, src_dimension,
                             dst_dimension, mod_dimension,
                             color_style.getReactionLineColor(), color_style.getReactionLineWidth()*scale, reactionLineType,
                             showBezierHandles, showReactionIds,
                             [reaction_arrow_head_size[0] * scale, reaction_arrow_head_size[1] * scale],
                             scale, reaction_dash, rxn_rev, showReversible])

                id_list = []
                # orphan nodes have been considered, so numSpec_in_reaction should equals to numSpecGlyphs
                # if numSpecGlyphs > numSpec_in_reaction:
                #     print("Orphan nodes are removed.")
                for i in range (numSpec_in_reaction):
                    temp_id = spec_specGlyph_id_list[i][0]
                    tempGlyph_id = spec_specGlyph_id_list[i][1]
                    position = [(spec_position_list[i][0]-topLeftCorner[0])*scale, 
                    (spec_position_list[i][1]-topLeftCorner[1])*scale]
                    dimension = [spec_dimension_list[i][0]*scale,spec_dimension_list[i][1]*scale]
                    color_style.setNodeDimension(dimension)
                    text_content = spec_text_content_list[i]
                    text_position = [(spec_text_position_list[i][0]-topLeftCorner[0])*scale,
                    (spec_text_position_list[i][1]-topLeftCorner[1])*scale]
                    text_dimension = [spec_text_dimension_list[i][0]*scale,
                    spec_text_dimension_list[i][1]*scale]
                    gradient_fill_color = []
                    for j in range(numFloatingNodes):
                        if temp_id == FloatingNodes_ids[j]:
                            if temp_id not in id_list: 
                                for k in range(len(spec_render)):
                                    if temp_id == spec_render[k][0]:
                                        if type(spec_render[k][1][0]) == str:
                                            gradient_fill_color = spec_render[k][1]
                                        else:
                                            if not color_style.getStyleName():
                                                color_style.setSpecFillColor(spec_render[k][1])
                                        if not color_style.getStyleName():
                                            color_style.setSpecBorderColor(spec_render[k][2])
                                            color_style.setSpecBorderWidth(spec_render[k][3])
                                        shapeIdx = spec_render[k][4]
                                        shape_name = spec_render[k][5]
                                        shape_type = spec_render[k][6]
                                        shape_info = spec_render[k][7]
                                        spec_dash = spec_render[k][8]
                                for k in range(len(text_render)):
                                    if tempGlyph_id == text_render[k][0]:
                                        if not color_style.getStyleName():
                                            color_style.setTextLineColor(text_render[k][1])
                                        text_line_width = text_render[k][2]
                                        text_font_size = text_render[k][3]
                                        [text_anchor, text_vanchor] = text_render[k][4]
                                        text_font_family = text_render[k][6]
                                floatingNodes_pos_dict[temp_id] = position
                                floatingNodes_dim_dict[temp_id] = dimension
                                allNodes_pos_dict[temp_id] = position
                                allNodes_dim_dict[temp_id] = dimension
                                if gradient_fill_color == []:
                                    drawNetwork.addNode(canvas, 'floating', '', position, dimension,
                                                        color_style.getSpecBorderColor(), color_style.getSpecFillColor(),
                                                        color_style.getSpecBorderWidth()*scale, shapeIdx, shape_name, shape_type, shape_info,
                                                        spec_dash, complex_shape = complexShape)
                                    
                                else:
                                    drawNetwork.addNode(canvas, 'floating', '', position, dimension,
                                                        color_style.getSpecBorderColor(), gradient_fill_color,
                                                        color_style.getSpecBorderWidth()*scale, shapeIdx, shape_name, shape_type, shape_info,
                                                        spec_dash, complex_shape = complexShape)
                                if text_content == '':
                                    text_content = temp_id
                                # if text_content == 'Mt-DNA repair':
                                #     print("node:", position, dimension)
                                #     print("text:", text_position, text_dimension)

                                drawNetwork.addText(canvas, text_content, text_position, text_dimension,
                                                    color_style.getTextLineColor(), text_line_width*scale, 
													fontSize = text_font_size*scale, textAnchor = [text_anchor, text_vanchor],
                                                    text_font_family = text_font_family, longText = longText)
                                id_list.append(temp_id)                    
                            else:
                                for k in range(len(spec_render)):
                                    if temp_id == spec_render[k][0]:
                                        if type(spec_render[k][1][0]) == str:
                                            gradient_fill_color = spec_render[k][1]
                                        else:
                                            if not color_style.getStyleName():
                                                color_style.setSpecFillColor(spec_render[k][1])
                                        if not color_style.getStyleName():
                                            color_style.setSpecBorderColor(spec_render[k][2])
                                            color_style.setSpecBorderWidth(spec_render[k][3])
                                        shapeIdx = spec_render[k][4]
                                        shape_name = spec_render[k][5]
                                        shape_type = spec_render[k][6]
                                        shape_info = spec_render[k][7]
                                        spec_dash = spec_render[k][8]
                                for k in range(len(text_render)):
                                    if tempGlyph_id == text_render[k][0]:
                                        if not color_style.getStyleName():
                                            color_style.setTextLineColor(text_render[k][1])
                                        text_line_width = text_render[k][2]
                                        text_font_size = text_render[k][3]
                                        [text_anchor, text_vanchor] = text_render[k][4]
                                        text_font_family = text_render[k][6]
                                floatingNodes_pos_dict[temp_id] = position
                                floatingNodes_dim_dict[temp_id] = dimension
                                allNodes_pos_dict[temp_id] = position
                                allNodes_dim_dict[temp_id] = dimension
                                if gradient_fill_color == []:
                                    drawNetwork.addNode(canvas, 'floating', 'alias', position, dimension,
                                                        color_style.getSpecBorderColor(), color_style.getSpecFillColor(),
                                                        color_style.getSpecBorderWidth()*scale, shapeIdx, shape_name, shape_type, shape_info,
                                                        spec_dash, complex_shape=complexShape)
                                else:
                                    drawNetwork.addNode(canvas, 'floating', 'alias', position, dimension,
                                                        color_style.getSpecBorderColor(), gradient_fill_color,
                                                        color_style.getSpecBorderWidth()*scale, shapeIdx, shape_name, shape_type, shape_info,
                                                        spec_dash, complex_shape=complexShape)
                                if text_content == '':
                                    text_content = temp_id

                                drawNetwork.addText(canvas, text_content, text_position, text_dimension,
                                                    color_style.getTextLineColor(), text_line_width*scale,
													fontSize = text_font_size*scale, textAnchor = [text_anchor, text_vanchor],
                                                    text_font_family = text_font_family, longText = longText)
                                id_list.append(temp_id)
                    for j in range(numBoundaryNodes):
                        if temp_id == BoundaryNodes_ids[j]:
                            if temp_id not in id_list:
                                for k in range(len(spec_render)):
                                    if temp_id == spec_render[k][0]:
                                        if type(spec_render[k][1][0]) == str:
                                            gradient_fill_color = spec_render[k][1]
                                        else:
                                            if not color_style.getStyleName():
                                                color_style.setSpecFillColor(spec_render[k][1])
                                        if not color_style.getStyleName():
                                            color_style.setSpecBorderColor(spec_render[k][2])
                                            color_style.setSpecBorderWidth(spec_render[k][3])
                                        shapeIdx = spec_render[k][4]
                                        shape_name = spec_render[k][5]
                                        shape_type = spec_render[k][6]
                                        shape_info = spec_render[k][7]
                                        spec_dash = spec_render[k][8]
                                for k in range(len(text_render)):
                                    if tempGlyph_id == text_render[k][0]:
                                        if not color_style.getStyleName():
                                            color_style.setTextLineColor(text_render[k][1])
                                        text_line_width = text_render[k][2]
                                        text_font_size = text_render[k][3]
                                        [text_anchor, text_vanchor] = text_render[k][4]
                                        text_font_family = text_render[k][6]
                                if gradient_fill_color == []:
                                    drawNetwork.addNode(canvas, 'boundary', '', position, dimension,
                                                        color_style.getSpecBorderColor(), color_style.getSpecFillColor(),
                                                        color_style.getSpecBorderWidth()*scale, shapeIdx, shape_name, shape_type, shape_info,
                                                        spec_dash, complex_shape=complexShape)
                                else:
                                    drawNetwork.addNode(canvas, 'boundary', '', position, dimension,
                                                        color_style.getSpecBorderColor(), gradient_fill_color,
                                                        color_style.getSpecBorderWidth()*scale, shapeIdx, shape_name, shape_type, shape_info,
                                                        spec_dash, complex_shape=complexShape)
                                allNodes_pos_dict[temp_id] = position
                                allNodes_dim_dict[temp_id] = dimension
                                if text_content == '':
                                    text_content = temp_id
                                drawNetwork.addText(canvas, text_content, text_position, text_dimension,
                                                    color_style.getTextLineColor(), text_line_width*scale, 
													fontSize = text_font_size*scale, textAnchor = [text_anchor, text_vanchor],
                                                    text_font_family = text_font_family, longText = longText)
                                id_list.append(temp_id)
                            else:
                                for k in range(len(spec_render)):
                                    if temp_id == spec_render[k][0]:
                                        if type(spec_render[k][1][0]) == str:
                                            gradient_fill_color = spec_render[k][1]
                                        else:
                                            if not color_style.getStyleName():
                                                color_style.setSpecFillColor(spec_render[k][1])
                                        if not color_style.getStyleName():
                                            color_style.setSpecBorderColor(spec_render[k][2])
                                            color_style.setSpecBorderWidth(spec_render[k][3])
                                        shapeIdx = spec_render[k][4]
                                        shape_name = spec_render[k][5]
                                        shape_type = spec_render[k][6]
                                        shape_info = spec_render[k][7]
                                        spec_dash = spec_render[k][8]
                                for k in range(len(text_render)):
                                    if tempGlyph_id == text_render[k][0]:
                                        if not color_style.getStyleName():
                                            color_style.setTextLineColor(text_render[k][1])
                                        text_line_width = text_render[k][2]
                                        text_font_size = text_render[k][3]
                                        [text_anchor, text_vanchor] = text_render[k][4]
                                        text_font_family = text_render[k][6]
                                if gradient_fill_color == []:
                                 
                                    drawNetwork.addNode(canvas, 'boundary', 'alias', position, dimension,
                                                        color_style.getSpecBorderColor(), color_style.getSpecFillColor(),
                                                        color_style.getSpecBorderWidth()*scale, shapeIdx, shape_name, shape_type, shape_info,
                                                        spec_dash, complex_shape=complexShape)
                                else:
                                    drawNetwork.addNode(canvas, 'boundary', 'alias', position, dimension,
                                                    color_style.getSpecBorderColor(), gradient_fill_color,
                                                    color_style.getSpecBorderWidth()*scale, shapeIdx, shape_name, shape_type, shape_info,
                                                    spec_dash, complex_shape=complexShape)
                                allNodes_pos_dict[temp_id] = position
                                allNodes_dim_dict[temp_id] = dimension
                                if text_content == '':
                                    text_content = temp_id
                                drawNetwork.addText(canvas, text_content, text_position, text_dimension,
                                                    color_style.getTextLineColor(), text_line_width*scale, 
													fontSize = text_font_size*scale, textAnchor = [text_anchor, text_vanchor], 
                                                    text_font_family = text_font_family, longText = longText)
                                id_list.append(temp_id)

                #arbitrary shape
                if len(gen_id_list) > 0:
                    for i in range(len(gen_id_list)):
                        genGlyph = layout.getGeneralGlyph(gen_id_list[i])
                        genGlyph_id = gen_id_list[i]
                        shape_position = gen_position_list[i]
                        shape_dimension = gen_dimension_list[i]
                        for k in range(len(gen_render)):
                            if genGlyph_id == gen_render[k][0]:
                                shape_fill_color = gen_render[k][1]
                                shape_border_color = gen_render[k][2]
                                shape_border_width = gen_render[k][3]
                                shape_type = gen_render[k][4]
                                shape_info = gen_render[k][5]
                        shape_position = [(shape_position[0]-topLeftCorner[0])*scale,
                        (shape_position[1]-topLeftCorner[1])*scale]
                        shape_dimension = [shape_dimension[0]*scale,shape_dimension[1]*scale]
                        shape_border_width = shape_border_width*scale
                    
                        [x, y] = shape_position
                        [width, height] = shape_dimension
                        fill = skia.Color(shape_fill_color[0], shape_fill_color[1], 
                        shape_fill_color[2], shape_fill_color[3])
                        outline = skia.Color(shape_border_color[0], shape_border_color[1], 
                        shape_border_color[2], shape_border_color[3])
                        linewidth = shape_border_width
                        if shape_type == 'rectangle':
                            drawNetwork._drawRoundedRectangle(canvas, x, y, width, height, outline, fill, linewidth)
                        elif shape_type == 'ellipse':
                            drawNetwork._drawEllipse (canvas, x, y, width, height, outline, fill, linewidth)
                        elif shape_type == 'polygon':
                            pts = []
                            for ii in range(len(shape_info)):
                                pts.append([x+width*shape_info[ii][0]/100.,y+height*shape_info[ii][1]/100.])
                            drawNetwork._drawPolygon (canvas, pts, outline, fill, linewidth)

                #arbitrary text
                for i in range(len(textGlyph_id_list)):
                    textGlyph = layout.getTextGlyph(textGlyph_id_list[i])
                    #if not textGlyph.isSetOriginOfTextId() and not textGlyph.isSetGraphicalObjectId():
                    textGlyph_id = textGlyph_id_list[i]
                    text_content = text_content_list[i]
                    text_position = text_position_list[i]
                    text_dimension = text_dimension_list[i]
                    for k in range(len(text_render)):
                        if textGlyph_id == text_render[k][0]:
                            text_line_color = text_render[k][1]
                            text_line_width = text_render[k][2]
                            text_font_size = text_render[k][3]
                            [text_anchor, text_vanchor] = text_render[k][4]
                            text_font_family = text_render[k][6]

                    text_position = [(text_position[0]-topLeftCorner[0])*scale,
                    (text_position[1]-topLeftCorner[1])*scale]
                    text_dimension = [text_dimension[0]*scale,text_dimension[1]*scale]
                    text_line_width = text_line_width*scale
                    text_font_size = text_font_size*scale 
                    drawNetwork.addText(canvas, text_content, text_position, text_dimension,
                    text_line_color, text_line_width, text_font_size, textAnchor = [text_anchor, text_vanchor])  

                #reaction text
                for i in range(len(textGlyph_rxn_id_list)):
                    textGlyph_id = textGlyph_rxn_id_list[i][1]
                    text_content = rxn_text_content_list[i]
                    text_position = rxn_text_position_list[i]
                    text_dimension = rxn_text_dimension_list[i]

                    for k in range(len(text_render)):
                        if textGlyph_id == text_render[k][5]:
                            text_line_color = text_render[k][1]
                            text_line_width = text_render[k][2]
                            text_font_size = text_render[k][3]
                            [text_anchor, text_vanchor] = text_render[k][4]
                            text_font_family = text_render[k][6]

                    text_position = [(text_position[0]-topLeftCorner[0])*scale,
                    (text_position[1]-topLeftCorner[1])*scale]
                    text_dimension = [text_dimension[0]*scale,text_dimension[1]*scale]
                    text_line_width = text_line_width*scale
                    text_font_size = text_font_size*scale 
                    drawNetwork.addText(canvas, text_content, text_position, text_dimension,
                    text_line_color, text_line_width, text_font_size, textAnchor = [text_anchor, text_vanchor])  

            else: # there is no layout information, assign position randomly and size as default
                comp_id_list = Comps_ids
                nodeIdx_temp = 0 #to track the node index    
                for i in range(numComps):
                    temp_id = Comps_ids[i]
                    vol= model.getCompartmentVolume(i)
                    dimension = imageSize
                    position = [0,0]
                    drawNetwork.addCompartment(canvas, position, dimension,
                    color_style.getCompBorderColor(), color_style.getCompFillColor(), color_style.getCompBorderWidth()*scale,
                    comp_shape_type=comp_shape_type, comp_shape_info=comp_shape_info)
                spec_id_list = [] 
                spec_dimension_list = []
                spec_position_list = []
                for i in range (numFloatingNodes):
                    temp_id = FloatingNodes_ids[i]
                    dimension = [60,40]
                    color_style.setNodeDimension(dimension)
                    position = [40 + math.trunc (_random.random()*800), 40 + math.trunc (_random.random()*800)]
                    spec_id_list.append(temp_id)
                    spec_dimension_list.append(dimension)
                    spec_position_list.append(position)
                for i in range (numBoundaryNodes):
                    temp_id = BoundaryNodes_ids[i]
                    dimension = [60,40]
                    position = [40 + math.trunc (_random.random()*800), 40 + math.trunc (_random.random()*800)]
                    spec_id_list.append(temp_id)
                    spec_dimension_list.append(dimension)
                    spec_position_list.append(position)
                for i in range (numRxns):
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
                    kinetics = model.getRateLaw(i)
                    rct_num = model.getNumReactants(i)
                    prd_num = model.getNumProducts(i)
                    mod_num = model.getNumModifiers(temp_id)
                    rct_add_cnt = 0
                    for j in range(rct_num):
                        rct_id = model.getReactant(temp_id,j)
                        for k in range(numNodes):
                            if spec_id_list[k] == rct_id:
                                src_position.append(spec_position_list[k])
                                src_dimension.append(spec_dimension_list[k])
                        edges.append([rct_id])
                        rct_add_cnt += 1

                    for j in range(prd_num):
                        prd_id = model.getProduct(temp_id,j)
                        for k in range(numNodes):
                            if spec_id_list[k] == prd_id:
                                dst_position.append(spec_position_list[k])
                                dst_dimension.append(spec_dimension_list[k])
                        edges[-rct_add_cnt].append(prd_id)
                        rct_add_cnt -= 1

                    modifiers = model.getListOfModifiers(temp_id)
                    for j in range(mod_num):
                        mod_id = modifiers[j]
                        for k in range(numNodes):
                            if spec_id_list[k] == mod_id:
                                mod_position.append(spec_position_list[k])
                                mod_dimension.append(spec_dimension_list[k])
                    center_x = 0.
                    center_y = 0.
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
                    if drawArrow:
                        drawNetwork.addReaction(canvas, temp_id, src_position, dst_position, mod_position,
                            center_position, handles, src_dimension, dst_dimension, mod_dimension,
                            color_style.getReactionLineColor(), color_style.getReactionLineWidth()*scale,
                            reaction_line_type = reactionLineType, show_bezier_handles = showBezierHandles,
                            show_reaction_ids = showReactionIds,
                            reaction_arrow_head_size = [reaction_arrow_head_size[0]*scale, reaction_arrow_head_size[1]*scale],
                            scale = scale, reaction_dash = reaction_dash, reverse = rxn_rev, showReversible = showReversible)
                    arrow_info.append(
                        [temp_id, src_position, dst_position, mod_position, center_position, handles, src_dimension,
                         dst_dimension, mod_dimension,
                         color_style.getReactionLineColor(), color_style.getReactionLineWidth()*scale, reactionLineType,
                         showBezierHandles, showReactionIds,
                         [reaction_arrow_head_size[0] * scale, reaction_arrow_head_size[1] * scale],
                         scale, reaction_dash, rxn_rev, showReversible])

                for i in range (numFloatingNodes):
                    temp_id = FloatingNodes_ids[i]
                    text_content = temp_id
                    for k in range(numNodes):
                        if spec_id_list[k] == temp_id:
                            position = [(spec_position_list[k][0]-topLeftCorner[0])*scale,
                            (spec_position_list[k][0]-topLeftCorner[1])*scale]
                            dimension = [spec_dimension_list[k][0]*scale,spec_dimension_list[k][1]*scale]
                    color_style.setNodeDimension(dimension)
                    drawNetwork.addNode(canvas, 'floating', '', position, dimension,
                                        color_style.getSpecBorderColor(), color_style.getSpecFillColor(), color_style.getSpecBorderWidth()*scale,
                                        shapeIdx, shape_name, shape_type, shape_info, spec_dash, complex_shape=complexShape)
                    if text_content == '':
                        text_content = temp_id
                    drawNetwork.addText(canvas, text_content, position, dimension, color_style.getTextLineColor(), 
                    text_line_width*scale, fontSize = text_font_size*scale, textAnchor = [text_anchor, text_vanchor],
                    text_font_family = text_font_family, longText = longText)
                    floatingNodes_pos_dict[temp_id] = position
                    floatingNodes_dim_dict[temp_id] = dimension
                    allNodes_pos_dict[temp_id] = position
                    allNodes_dim_dict[temp_id] = dimension
                for i in range (numBoundaryNodes):
                    temp_id = BoundaryNodes_ids[i]
                    text_content = temp_id
                    for k in range(numNodes):
                        if spec_id_list[k] == temp_id:
                            position = [(spec_position_list[k][0]-topLeftCorner[0])*scale,
                            (spec_position_list[k][1]-topLeftCorner[1])*scale]
                            dimension = [spec_dimension_list[k][0]*scale,spec_dimension_list[k][1]*scale]
                    drawNetwork.addNode(canvas, 'boundary', '', position, dimension,
                                        color_style.getSpecBorderColor(), color_style.getSpecFillColor(), color_style.getSpecBorderWidth()*scale,
                                        shapeIdx, shape_name, shape_type, shape_info, spec_dash, complex_shape=complexShape)
                    allNodes_pos_dict[temp_id] = position
                    allNodes_dim_dict[temp_id] = dimension
                    if text_content == '':
                        text_content = temp_id
                    drawNetwork.addText(canvas, text_content, position, dimension, color_style.getTextLineColor(),
                    text_line_width*scale, fontSize = text_font_size*scale, textAnchor = [text_anchor, text_vanchor],
                    text_font_family = text_font_family, longText = longText)

        # except Exception as e:
        #     raise Exception (e)  
        except:
            raise ValueError('Invalid SBML!')


        #add arbitrary text
        # if len(df_text) != 0:
        #     for i in range(len(df_text)):
        #         text_content = df_text.iloc[i][processSBML.TXTCONTENT] 
        #         text_position = df_text.iloc[i][processSBML.TXTPOSITION]
        #         text_position = [(text_position[0]-topLeftCorner[0])*scale,
        #         (text_position[1]-topLeftCorner[1])*scale]
        #         text_size = df_text.iloc[i][processSBML.TXTSIZE]
        #         text_size = [text_size[0]*scale,text_size[1]*scale]
        #         text_font_color = df_text.iloc[i][processSBML.TXTFONTCOLOR]
        #         text_line_width = df_text.iloc[i][processSBML.TXTLINEWIDTH]
        #         text_line_width = text_line_width*scale
        #         text_font_size = df_text.iloc[i][processSBML.TXTFONTSIZE]
        #         text_font_size = text_font_size*scale
        #         drawNetwork.addSimpleText(canvas, text_content, text_position, text_font_color,
        #         text_line_width, text_font_size) 
        
        return floatingNodes_pos_dict, floatingNodes_dim_dict, allNodes_pos_dict, allNodes_dim_dict, edges, arrow_info, name_to_id
    
    if output_fileName != '':
        output_fileName_lower = str(output_fileName).lower()
        if '.png' == output_fileName_lower[-4:]:
            fileFormat = 'PNG'
            #fileName = output_fileName.replace('.png', '')
            fileName = output_fileName[:-4]
        elif '.jpg' == output_fileName_lower[-4:]:
            fileFormat = 'JPEG' 
            fileName = output_fileName[:-4]
        elif '.pdf' == output_fileName_lower[-4:]:
            fileFormat = 'PDF'
            fileName = output_fileName[:-4]
        else:
            raise Exception("Please enter an output fileName ending with .png/.jpg/.pdf.")
    else:
        fileFormat = 'PNG'
        fileName = ''

    baseImageArray = []
    
    surface = skia.Surface(int(imageSize[0]), int(imageSize[1]))
    canvas = surface.getCanvas()   
    pos_dict, dim_dict, all_pos_dict, all_dim_dict, edges, arrow_info, name_to_id = draw_on_canvas(canvas, color_style)
    baseImageArray = drawNetwork.showPlot(surface, save=save, fileName = fileName, file_format = fileFormat, showImage=showImage)
    
    if output_fileName == '':
        tmpfileName = "temp.png" #display the file in drawNetwork
        try:
            os.remove(tmpfileName)
        except:
            pass

    if fileFormat == "PDF" and fileName != '':
        # if output_fileName == '':
        #     random_string = ''.join(_random.choices(string.ascii_uppercase + string.digits, k=10)) 
        #     fileName = os.path.join(os.getcwd(), random_string)
        #     fileNamepdf = fileName + '.pdf'
        #     stream = skia.FILEWStream(fileNamepdf)
        fileName = os.path.join(os.getcwd(), fileName)
        fileNamepdf = fileName + '.pdf'
        stream = skia.FILEWStream(fileNamepdf)
        fileNamepng = fileName + '.png' #display the file in drawNetwork
        try:
            os.remove(fileNamepng)
        except:
            pass
        with skia.PDF.MakeDocument(stream) as document:
            with document.page(int(imageSize[0]), int(imageSize[1])) as canvas:
                pos_dict, dim_dict,  all_pos_dict, all_dim_dict, edges, arrow_info, name_to_id = draw_on_canvas(canvas, color_style)
        
    return visualizeInfo.visualizeInfo(baseImageArray, pos_dict, dim_dict, all_pos_dict, all_dim_dict, color_style, edges, arrow_info, name_to_id)

def _getNetworkTopLeftCorner(sbmlStr):
    """
    Get the top left-hand corner of the network(s) from the SBML string.

    Args:  
        sbmlStr: str-the string of the input sbml file.

    Returns:
        position: list-[position_x, position_y], top left-hand corner of the network(s).
        It is calculated by the minimum positions of compartments, nodes, center and handle 
        positions of reactions, aribitrary text, arbitrary shape,
        excluding the compartment with the id of _compartment_default_.
    
    """    
    model = simplesbml.loadSBMLStr(sbmlStr)
    numFloatingNodes  = model.getNumFloatingSpecies()
    FloatingNodes_ids = model.getListOfFloatingSpecies()
    numBoundaryNodes  = model.getNumBoundarySpecies()
    BoundaryNodes_ids = model.getListOfBoundarySpecies()
    #numComps  = model.getNumCompartments()
    #Comps_ids = model.getListOfCompartmentIds()
    numRxns   = model.getNumReactions()
    Rxns_ids  = model.getListOfReactionIds()

    df = processSBML.load(sbmlStr)
    _df = processSBML._SBMLToDF(sbmlStr)
    txt_id = df.getTextIdList()
    numTexts = len(txt_id)
    shape_name = df.getShapeNameList()
    numShapes = len(shape_name)

    Comps_ids = [] #only considers to visualize the compartments with species in

    if numFloatingNodes > 0 :
        position = _getNodePosition(_df, FloatingNodes_ids[0])[0]
    if numBoundaryNodes > 0:
        position = _getNodePosition(_df, BoundaryNodes_ids[0])[0]
    # if numTexts > 0:
    #     position_list = _getTextPosition(_df, txt_id[0])
    #     size = _getTextSize(_df, txt_id[0])[0]
    #     position = [position_list[0][0], position_list[0][1]-size[1]]
    if numTexts > 0:
        position_list = _getTextPosition(_df, txt_id[0])
        position = position_list[0]
    if numShapes > 0:
        position_list = _getShapePosition(_df, shape_name[0])
        position = position_list[0]
    for i in range(numFloatingNodes):
        node_temp_position = _getNodePosition(_df, FloatingNodes_ids[i])
        text_temp_position = _getNodeTextPosition(_df, FloatingNodes_ids[i])
        for j in range(len(node_temp_position)):
            if node_temp_position[j][0] < position[0]:
                position[0] = node_temp_position[j][0]
            if node_temp_position[j][1] < position[1]:
                position[1] = node_temp_position[j][1]
            if text_temp_position[j][0] < position[0]:
                position[0] = text_temp_position[j][0]
            if text_temp_position[j][1] < position[1]:
                position[1] = text_temp_position[j][1]
        comp_id = model.getCompartmentIdSpeciesIsIn(FloatingNodes_ids[i])
        if comp_id not in Comps_ids:
            Comps_ids.append(comp_id)
    for i in range(numBoundaryNodes):
        node_temp_position = _getNodePosition(_df, BoundaryNodes_ids[i])
        text_temp_position = _getNodeTextPosition(_df, BoundaryNodes_ids[i])
        for j in range(len(node_temp_position)):
            if node_temp_position[j][0] < position[0]:
                position[0] = node_temp_position[j][0]
            if node_temp_position[j][1] < position[1]:
                position[1] = node_temp_position[j][1]
            if text_temp_position[j][0] < position[0]:
                position[0] = text_temp_position[j][0]
            if text_temp_position[j][1] < position[1]:
                position[1] = text_temp_position[j][1]
        comp_id = model.getCompartmentIdSpeciesIsIn(BoundaryNodes_ids[i])
        if comp_id not in Comps_ids:
            Comps_ids.append(comp_id)

    for i in range(len(Comps_ids)):
        if Comps_ids[i] != "_compartment_default_":
            comp_temp_fill_color = df.getCompartmentFillColor(Comps_ids[i])
            comp_temp_border_color = df.getCompartmentBorderColor(Comps_ids[i])
            if comp_temp_fill_color[0][:3] != [255,255,255] or comp_temp_border_color[0][:3] != [255,255,255]:
                comp_temp_position = _getCompartmentPosition(_df, Comps_ids[i])[0]
                if comp_temp_position[0] < position[0]:
                    position[0] = comp_temp_position[0]
                if comp_temp_position[1] < position[1]:
                    position[1] = comp_temp_position[1]

    # for i in range(numComps):
    #     if Comps_ids[i] != "_compartment_default_":
    #         comp_temp_fill_color = df.getCompartmentFillColor(Comps_ids[i])
    #         comp_temp_border_color = df.getCompartmentBorderColor(Comps_ids[i])
    #         if comp_temp_fill_color[0][:3] != [255,255,255] or comp_temp_border_color[0][:3] != [255,255,255]:
    #             comp_temp_position = _getCompartmentPosition(_df, Comps_ids[i])[0]
    #             if comp_temp_position[0] < position[0]:
    #                 position[0] = comp_temp_position[0]
    #             if comp_temp_position[1] < position[1]:
    #                 position[1] = comp_temp_position[1]
    for i in range(numRxns):
        center_position = _getReactionCenterPosition(_df, Rxns_ids[i])[0]
        handle_positions = _getReactionBezierHandles(_df, Rxns_ids[i])[0]
        try:
            if center_position[0] < position[0]:
                position[0] = center_position[0]
            if center_position[1] < position[1]:
                position[1] = center_position[1]
        except:
            pass

        #print(handle_positions)
        #print(position)
        for j in range(len(handle_positions)):
            try:#does not work on colab
                if handle_positions[j][0] < position[0]:
                    position[0] = handle_positions[j][0]
                if handle_positions[j][1] < position[1]:
                    position[1] = handle_positions[j][1]
            except:
                pass

    # for i in range(numTexts):
    #     text_position_list = _getTextPosition(_df, txt_id[i])
    #     text_size = _getTextSize(_df, txt_id[i])[0]
    #     text_position = [text_position_list[0][0],text_position_list[0][1]-text_size[1]] 
    #     if text_position[0] < position[0]:
    #         position[0] = text_position[0]
    #     if text_position[1] < position[1]:
    #         position[1] = text_position[1]

    for i in range(numTexts):
        text_position_list = _getTextPosition(_df, txt_id[i])
        text_position = text_position_list[0]
        if text_position[0] < position[0]:
            position[0] = text_position[0]
        if text_position[1] < position[1]:
            position[1] = text_position[1]

    for i in range(numShapes):
        shape_position_list = _getShapePosition(_df, shape_name[i])
        shape_position = shape_position_list[0]
        if shape_position[0] < position[0]:
            position[0] = shape_position[0]
        if shape_position[1] < position[1]:
            position[1] = shape_position[1]

    return position

def _getNetworkBottomRightCorner(sbmlStr):
    """
    Get the bottom right-hand corner of the network(s) from the SBML string.

    Args:  
        sbmlStr: str-the string of the input sbml file.

    Returns:
        position: list-[position_x, position_y],bottom right-hand corner of the network(s).
        It is calculated by the maximum right down corner positions of positions of compartments, 
        nodes, center and handle positions of reactions, aribitrary text, arbitrary shape,
        excluding the compartment with the id of _compartment_default_.
    
    
    """    
    model = simplesbml.loadSBMLStr(sbmlStr)
    numFloatingNodes  = model.getNumFloatingSpecies()
    FloatingNodes_ids = model.getListOfFloatingSpecies()
    numBoundaryNodes  = model.getNumBoundarySpecies()
    BoundaryNodes_ids = model.getListOfBoundarySpecies()
    #numComps  = model.getNumCompartments()
    #Comps_ids = model.getListOfCompartmentIds()
    numRxns   = model.getNumReactions()
    Rxns_ids  = model.getListOfReactionIds()

    df = processSBML.load(sbmlStr)
    _df = processSBML._SBMLToDF(sbmlStr)
    txt_id = df.getTextIdList()
    numTexts = len(txt_id)

    shape_name = df.getShapeNameList()
    numShapes = len(shape_name)

    Comps_ids = [] #only considers to visualize the compartments with species in

    if numFloatingNodes > 0:
        position_list = _getNodePosition(_df, FloatingNodes_ids[0])
        size = _getNodeSize(_df, FloatingNodes_ids[0])[0]
        position = [position_list[0][0]+size[0], position_list[0][1]+size[1]]
    if numBoundaryNodes > 0:
        position_list = _getNodePosition(_df, BoundaryNodes_ids[0])
        size = _getNodeSize(_df, BoundaryNodes_ids[0])[0]
        position = [position_list[0][0]+size[0], position_list[0][1]+size[1]]
    # if numTexts > 0:
    #     position_list = _getTextPosition(_df, txt_id[0])
    #     size = _getTextSize(_df, txt_id[0])[0]
    #     position = [position_list[0][0]+size[0],position_list[0][1]]
    if numTexts > 0:
        position_list = _getTextPosition(_df, txt_id[0])
        size = _getTextSize(_df, txt_id[0])[0]
        position = [position_list[0][0]+size[0],position_list[0][1]+size[1]]
    if numShapes > 0:
        position_list = _getShapePosition(_df, shape_name[0])
        position = position_list[0]

    for i in range(numFloatingNodes):
        node_temp_position_list = _getNodePosition(_df, FloatingNodes_ids[i])
        text_temp_position_list = _getNodeTextPosition(_df, FloatingNodes_ids[i])
        for j in range(len(node_temp_position_list)):
            node_temp_size = _getNodeSize(_df, FloatingNodes_ids[i])
            text_temp_size = _getNodeTextSize(_df, FloatingNodes_ids[i])
            node_temp_position = [node_temp_position_list[j][0]+node_temp_size[j][0], 
            node_temp_position_list[j][1]+node_temp_size[j][1]]
            text_temp_position = [text_temp_position_list[j][0]+text_temp_size[j][0], 
            text_temp_position_list[j][1]+text_temp_size[j][1]]
            if node_temp_position[0] > position[0]:
                position[0] = node_temp_position[0]
            if node_temp_position[1] > position[1]:
                position[1] = node_temp_position[1]
            if text_temp_position[0] > position[0]:
                position[0] = text_temp_position[0]
            if text_temp_position[1] > position[1]:
                position[1] = text_temp_position[1]
        comp_id = model.getCompartmentIdSpeciesIsIn(FloatingNodes_ids[i])
        if comp_id not in Comps_ids:
            Comps_ids.append(comp_id)
    for i in range(numBoundaryNodes):
        node_temp_position_list = _getNodePosition(_df, BoundaryNodes_ids[i])
        text_temp_position_list = _getNodeTextPosition(_df, BoundaryNodes_ids[i])
        for j in range(len(node_temp_position_list)):
            node_temp_size = _getNodeSize(_df, BoundaryNodes_ids[i])
            text_temp_size = _getNodeTextSize(_df, BoundaryNodes_ids[i])
            node_temp_position = [node_temp_position_list[j][0]+node_temp_size[j][0], 
            node_temp_position_list[j][1]+node_temp_size[j][1]]
            text_temp_position = [text_temp_position_list[j][0]+text_temp_size[j][0], 
            text_temp_position_list[j][1]+text_temp_size[j][1]]
            if node_temp_position[0] > position[0]:
                position[0] = node_temp_position[0]
            if node_temp_position[1] > position[1]:
                position[1] = node_temp_position[1]
            if text_temp_position[0] > position[0]:
                position[0] = text_temp_position[0]
            if text_temp_position[1] > position[1]:
                position[1] = text_temp_position[1]

        comp_id = model.getCompartmentIdSpeciesIsIn(BoundaryNodes_ids[i])
        if comp_id not in Comps_ids:
            Comps_ids.append(comp_id)
    for i in range(len(Comps_ids)):
        if Comps_ids[i] != "_compartment_default_":
            comp_temp_fill_color = df.getCompartmentFillColor(Comps_ids[i])
            comp_temp_border_color = df.getCompartmentBorderColor(Comps_ids[i])
            if comp_temp_fill_color[0][:3] != [255,255,255] or comp_temp_border_color[0][:3] != [255,255,255]:
                comp_temp_size = _getCompartmentSize(_df, Comps_ids[i])[0]
                comp_temp_position_list = _getCompartmentPosition(_df, Comps_ids[i])
                comp_temp_position = [comp_temp_position_list[0][0]+comp_temp_size[0],
                comp_temp_position_list[0][1]+comp_temp_size[1]]
                if comp_temp_position[0] > position[0]:
                    position[0] = comp_temp_position[0]
                if comp_temp_position[1] > position[1]:
                    position[1] = comp_temp_position[1]
    # for i in range(numComps):
    #     if Comps_ids[i] != "_compartment_default_":
    #         comp_temp_fill_color = df.getCompartmentFillColor(Comps_ids[i])
    #         comp_temp_border_color = df.getCompartmentBorderColor(Comps_ids[i])
    #         if comp_temp_fill_color[0][:3] != [255,255,255] or comp_temp_border_color[0][:3] != [255,255,255]:
    #             comp_temp_size = _getCompartmentSize(_df, Comps_ids[i])[0]
    #             comp_temp_position_list = _getCompartmentPosition(_df, Comps_ids[i])
    #             comp_temp_position = [comp_temp_position_list[0][0]+comp_temp_size[0],
    #             comp_temp_position_list[0][1]+comp_temp_size[1]]
    #             if comp_temp_position[0] > position[0]:
    #                 position[0] = comp_temp_position[0]
    #             if comp_temp_position[1] > position[1]:
    #                 position[1] = comp_temp_position[1]
    for i in range(numRxns):
        center_position = _getReactionCenterPosition(_df, Rxns_ids[i])[0]
        handle_positions = _getReactionBezierHandles(_df, Rxns_ids[i])[0]
        try:
            if center_position[0] > position[0]:
                position[0] = center_position[0]
            if center_position[1] > position[1]:
                position[1] = center_position[1]
        except:
            pass
        for j in range(len(handle_positions)):
            try:#does not work on colab
                if handle_positions[j][0] > position[0]:
                    position[0] = handle_positions[j][0]
                if handle_positions[j][1] > position[1]:
                    position[1] = handle_positions[j][1]
            except:
                pass

    # for i in range(numTexts):
    #     text_position_list = _getTextPosition(_df, txt_id[i])
    #     text_size = _getTextSize(_df, txt_id[i])[0]
    #     text_position = [text_position_list[0][0] + text_size[0],text_position_list[0][1]] 
    #     if text_position[0] > position[0]:
    #         position[0] = text_position[0]
    #     if text_position[1] > position[1]:
    #         position[1] = text_position[1]

    for i in range(numTexts):
        text_position_list = _getTextPosition(_df, txt_id[i])
        text_size = _getTextSize(_df, txt_id[i])[0]
        text_position = [text_position_list[0][0] + text_size[0],
                        text_position_list[0][1] + text_size[1]] 
        if text_position[0] > position[0]:
            position[0] = text_position[0]
        if text_position[1] > position[1]:
            position[1] = text_position[1]

    for i in range(numShapes):
        shape_position_list = _getShapePosition(_df, shape_name[i])
        shape_size = _getShapeSize(_df, shape_name[i])[0]
        shape_position = [shape_position_list[0][0] + shape_size[0],
                        shape_position_list[0][1] + shape_size[1]] 
        if shape_position[0] > position[0]:
            position[0] = shape_position[0]
        if shape_position[1] > position[1]:
            position[1] = shape_position[1]

    return position

def _getNetworkSize(sbmlStr):
    """
    Get the size of the network(s) from the SBML string.

    Args:  
        sbmlStr: str-the string of the input sbml file.

    Returns:
        list-1*2 matrix-size of the network size [width, height].
    
    """ 
    position_topLeft = _getNetworkTopLeftCorner(sbmlStr)
    position_bottomRight = _getNetworkBottomRightCorner(sbmlStr)
    size = [int(position_bottomRight[0]-position_topLeft[0]), 
    int(position_bottomRight[1]-position_topLeft[1])]

    return size

def _getCompartmentPosition(df, id):
    """
    Get the position of a compartment with its certain compartment id.

    Args: 
        df: tuple-(df_CompartmentData, df_NodeData, df_ReactionData, df_ArbitraryTextData, df_ArbitraryShapeData).

        id: str-the id of the compartment.

    Returns:
        position_list: list of position.

        position: list-1*2 matrix-top left-hand corner of the compartment [position_x, position_y].
    """

    idx_list = df[0].index[df[0]["id"] == id].tolist()
    position_list =[] 
    for i in range(len(idx_list)):
        position_list.append(df[0].iloc[idx_list[i]]["position"])

    return position_list

def _getCompartmentSize(df, id):
    """
    Get the size of a compartment with its certain compartment id.

    Args: 
        df: tuple-(df_CompartmentData, df_NodeData, df_ReactionData, df_ArbitraryTextData, df_ArbitraryShapeData).

        id: str-the id of the compartment.

    Returns:
        size_list: list of size.

        size: list-1*2 matrix-size of the compartment [width, height].
    """

    idx_list = df[0].index[df[0]["id"] == id].tolist()
    size_list =[] 
    for i in range(len(idx_list)):
        size_list.append(df[0].iloc[idx_list[i]]["size"])

    return size_list


def _getCompartmentTextPosition(df, id):
    """
    Get the text position of a compartment with its certain compartment id.

    Args: 
        df: tuple-(df_CompartmentData, df_NodeData, df_ReactionData, df_ArbitraryTextData, df_ArbitraryShapeData).

        id: str-the id of the compartment.

    Returns:
        position_list: list of position.

        position: list-1*2 matrix-top left-hand corner of the compartment [position_x, position_y].
    """

    idx_list = df[0].index[df[0]["id"] == id].tolist()
    position_list =[] 
    for i in range(len(idx_list)):
        position_list.append(df[0].iloc[idx_list[i]]["txt_position"])

    return position_list

def _getCompartmentTextSize(df, id):
    """
    Get the text size of a compartment with its certain compartment id.

    Args: 
        df: tuple-(df_CompartmentData, df_NodeData, df_ReactionData, df_ArbitraryTextData, df_ArbitraryShapeData).

        id: str-the id of the compartment.

    Returns:
        size_list: list of size.

        size: list-1*2 matrix-size of the compartment [width, height].
    """

    idx_list = df[0].index[df[0]["id"] == id].tolist()
    size_list =[] 
    for i in range(len(idx_list)):
        size_list.append(df[0].iloc[idx_list[i]]["txt_size"])

    return size_list


def _getNodePosition(df, id):
    """
    Get the position of a node with its certain node id.

    Args: 
        df: tuple-(df_CompartmentData, df_NodeData, df_ReactionData, df_ArbitraryTextData, df_ArbitraryShapeData).

        id: str-the id of the Node.

    Returns:
        position_list: list of position.

        position: list-[position_x, position_y]-top left-hand corner of the node.           

    """

    idx_list = df[1].index[df[1]["id"] == id].tolist()
    position_list =[] 
    for i in range(len(idx_list)):
        position_list.append(df[1].iloc[idx_list[i]]["position"])

    return position_list

def _getNodeSize(df, id):
    """
    Get the size of a node with its certain node id.

    Args: 
        df: tuple-(df_CompartmentData, df_NodeData, df_ReactionData, df_ArbitraryTextData, df_ArbitraryShapeData).

        id: str-the id of the node.

    Returns:
        size_list: list of size.

        size: list-1*2 matrix-size of the node [width, height].

    """
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    size_list =[] 
    for i in range(len(idx_list)):
        size_list.append(df[1].iloc[idx_list[i]]["size"])

    return size_list

def _getNodeTextPosition(df, id):
        """
        Get the text position of a node with its certain node id.

        Args: 
            df: tuple-(df_CompartmentData, df_NodeData, df_ReactionData, df_ArbitraryTextData, df_ArbitraryShapeData).

            id: str-the id of node.

        Returns:
            txt_position_list: list of txt_position.

            txt_position: list-[position_x, position_y]-top left-hand corner of the node text.
        """
        idx_list = df[1].index[df[1]["id"] == id].tolist()
        txt_position_list =[] 
        for i in range(len(idx_list)):
            txt_position_list.append(df[1].iloc[idx_list[i]]["txt_position"])

        return txt_position_list

def _getNodeTextSize(df, id):
    """
    Get the text size of a node with its certain node id.

    Args: 
        df: tuple-(df_CompartmentData, df_NodeData, df_ReactionData, df_ArbitraryTextData, df_ArbitraryShapeData).

        id: str-the id of the node.

    Returns:
        txt_size_list: list of txt_size.

        txt_size: list-1*2 matrix-size of the node text [width, height].
    """
    idx_list = df[1].index[df[1]["id"] == id].tolist()
    txt_size_list =[] 
    for i in range(len(idx_list)):
        txt_size_list.append(df[1].iloc[idx_list[i]]["txt_size"])

    return txt_size_list

def _getReactionCenterPosition(df, id):
    """
    Get the center position of a reaction with its certain reaction id.

    Args: 
        df: tuple-(df_CompartmentData, df_NodeData, df_ReactionData, df_ArbitraryTextData, df_ArbitraryShapeData).

        id: str-the id of the reaction.

    Returns:
        line_center_position_list: list of center_position.

        center_position:  list-1*2 matrix: position of the center.
    """
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    center_position_list =[] 
    for i in range(len(idx_list)):
        center_position_list.append(df[2].iloc[idx_list[i]]["center_pos"])

    return center_position_list

def _getReactionBezierHandles(df, id):
    """
    Get the bezier handle positions of a reaction with its certain reaction id.

    Args:
        df: tuple-(df_CompartmentData, df_NodeData, df_ReactionData, df_ArbitraryTextData, df_ArbitraryShapeData).
    
        id: str-the id of the reaction.

    Returns:
        line_handle_positions_list: list of handle_positions.

        handle_positions: list-position of the handles: 
        [center handle, reactant handles, product handles].
    """
    idx_list = df[2].index[df[2]["id"] == id].tolist()
    handle_positions_list =[] 
    for i in range(len(idx_list)):
        handle_positions_list.append(df[2].iloc[idx_list[i]]["handles"])

    return handle_positions_list


def _getTextPosition(df, txt_id):
    """
    Get the arbitrary text position with its id.

    Args: 
        df: tuple-(df_CompartmentData, df_NodeData, df_ReactionData, df_ArbitraryTextData, df_ArbitraryShapeData).
    
        txt_id: str-the id of the text.

    Returns:
        position_list: list of position.

        position: list-[position_x, position_y]-top left-hand corner of the text.
    """

    idx_list = df[3].index[df[3]["id"] == txt_id].tolist()
    position_list =[] 
    for i in range(len(idx_list)):
        position_list.append(df[3].iloc[idx_list[i]]["txt_position"])
    return position_list

def _getTextSize(df, txt_id):
    """
    Get the arbitrary text size with its text id.

    Args: 
        df: tuple-(df_CompartmentData, df_NodeData, df_ReactionData, df_ArbitraryTextData, df_ArbitraryShapeData).
    
        txt_id: str-the text id.

    Returns:
        txt_size_list: list of txt_size.

        txt_size: list-1*2 matrix-size of text [width, height].
    """

    idx_list = df[3].index[df[3]["id"] == txt_id].tolist()
    txt_size_list =[] 
    for i in range(len(idx_list)):
        txt_size_list.append(df[3].iloc[idx_list[i]]["txt_size"])
    return txt_size_list

def _getShapePosition(df, shape_name_str):
    """
    Get the arbitrary shape position with its shape name.

    Args: 
        df: tuple-(df_CompartmentData, df_NodeData, df_ReactionData, df_ArbitraryTextData, df_ArbitraryShapeData).
    
        shape_name_str: str-the shape name of the arbitrary shape.

    Returns:
        position_list: list of position.

        position: list-[position_x, position_y]-top left-hand corner of the shape.
    """

    idx_list = df[4].index[df[4]["shape_name"] == shape_name_str].tolist()
    position_list =[] 
    for i in range(len(idx_list)):
        position_list.append(df[4].iloc[idx_list[i]]["position"])
    return position_list

def _getShapeSize(df, shape_name_str):
    """
    Get the arbitrary shape size with its shape name.

    Args: 
        df: tuple-(df_CompartmentData, df_NodeData, df_ReactionData, df_ArbitraryTextData, df_ArbitraryShapeData).
    
        shape_name_str: str-the shape name.

    Returns:
        shape_size_list: list of shape_size.

        shape_size: list-1*2 matrix-size of the shape [width, height].
    """

    idx_list = df[4].index[df[4]["shape_name"] == shape_name_str].tolist()
    shape_size_list =[] 
    for i in range(len(idx_list)):
        shape_size_list.append(df[4].iloc[idx_list[i]]["size"])
    return shape_size_list

if __name__ == '__main__':
    DIR = os.path.dirname(os.path.abspath(__file__))
    TEST_FOLDER = os.path.join(DIR, "test_sbml_files")

    #filename = "test.xml"
    #filename = "feedback.xml"
    #filename = "LinearChain.xml"
    #filename = "test_no_comp.xml"
    #filename = "mass_action_rxn.xml"
    #filename = "test_comp.xml"
    #filename = "test_modifier.xml"
    #filename = "node_grid.xml"

    #filename = "Jana_WolfGlycolysis.xml"
    #filename = "Jana_WolfGlycolysis-original.xml"
    #filename = "output.xml"

    #filename = "test_suite/pdmap-nulceoid/pdmap-nucleoid.xml"

    filename = "Adel/1.xml"
    #filename = "output.xml"

    f = open(os.path.join(TEST_FOLDER, filename), 'r')
    sbmlStr = f.read()
    f.close()


    if len(sbmlStr) == 0:
        print("empty sbml")
    else:
        #_draw(sbmlStr, showReactionIds=True)
        _draw(sbmlStr,output_fileName='output.png')
        #print("finished!")

