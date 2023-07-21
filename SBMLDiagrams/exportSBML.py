# -*- coding: utf-8 -*-
# This script was written by Jin Xu and available on Github
# https://github.com/SunnyXu/SBMLDiagrams

"""
Created on Mon Aug 23 13:25:34 2021
@author: Jin Xu
"""

#from inspect import Parameter
from importlib.util import set_package
import os
import libsbml
import re # to process kinetic_law string
import pandas as pd
import math
import sys
from SBMLDiagrams import processSBML

#def _DFToSBML(df, compartmentDefaultSize = [10000-20,6200-20]):
def _DFToSBML(df, sbmlStr, compartmentDefaultSize = [1000-20,1000-20]):

    """
    Write the information of a set of dataframe to an SBML string. 

    Args:  
        sbmlStr: str-the string of the input sbml file.

        (df_CompartmentData, df_NodeData, df_ReactionData, df_ArbitraryTextData, df_ArbitraryShapeData): tuple.

        df_CompartmentData: DataFrame-Compartment information.

        df_NodeData: DataFrame-Node information.

        df_ReactionData: DataFrame-Reaction information.

        df_ArbitraryTextData: DataFrame-Arbitrary text information.

        df_ArbitrartyShapeData: DataFrame-Arbitrary shape information.

    Returns:
        SBMLStr_layout_render: str-the string of the output sbml file. 
    
    """

    def getSymbols(kinetic_law):
        str = kinetic_law
        str = str.replace(' ', '')  
        list = re.split('[+|\-|*|/|(|)]', str)
        list = [i for i in list if i != '']
        list_update = []
        for i in list:
            x = i.split(',')
            list_update.extend(x)
        res = []
        [res.append(x) for x in list_update if x not in res and not x.isdigit()]
        return res
    

    def _cross_point(arcCenter, c2, s2):
        """
        Get the cross point of a point and a rectangle with position(top left-hand corner) and size 
        given.

        Args:  
            arcCenter:  1*2 matrix-position of the point.
            c2: 1*2 matrix-position of the rectangle (top left-hand corner).
            s2: 1*2 matrix-size of the rectangle.
        """
        pt_center = [c2[0]+.5*s2[0], c2[1]+.5*s2[1]]
        pt_up_left    = c2
        pt_up_right   = [c2[0]+s2[0], c2[1]]
        pt_down_left  = [c2[0], c2[1]+s2[1]]
        pt_down_right = [c2[0]+s2[0], c2[1]+s2[1]]

        def _line_intersection(line1, line2):
            """

            Args:  
                line1: list of 1*2 matrix-two points to represent line1.
                line2: list of 1*2 matrix-two points to represent line2.
            Returns:
                [x,y]: 1*2 matrix-the point position of the crossed two lines.
            """
            xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
            ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

            def _det(a, b):
                return a[0] * b[1] - a[1] * b[0]

            div = _det(xdiff, ydiff)
            if div == 0:
                raise Exception('lines do not intersect1')
            d = (_det(*line1), _det(*line2))
            x = round(_det(d, xdiff) / div,2)
            y = round(_det(d, ydiff) / div,2)
            if round((x-line1[0][0])*(x-line1[1][0]),2)<=0 and round((x-line2[0][0])*(x-line2[1][0]),2)<=0 \
            and round((y-line1[0][1])*(y-line1[1][1]),2)<=0 and round((y-line2[0][1])*(y-line2[1][1]),2)<=0:
                return [x, y]
            else:
                raise Exception('lines do not intersect2')
        try:
            [x,y] = _line_intersection([arcCenter, pt_center], [pt_up_left, pt_down_left])
            return [x,y]
        except:
            pass

        try:
            [x,y] = _line_intersection([arcCenter, pt_center], [pt_up_left, pt_up_right])
            return [x,y]
        except:
            pass
        try:
            [x,y] = _line_intersection([arcCenter, pt_center], [pt_down_left, pt_down_right])
            return [x,y]
        except:
            pass
        try:
            [x,y] = _line_intersection([arcCenter, pt_center], [pt_up_right, pt_down_right])
            return [x,y]
        except:
            pass

    # if df == None:
    #     sys.exit("There is no valid information to process.")
    # else:

    try:
        try: 
            df_CompartmentData = df[0]
        except:
            df_CompartmentData = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_CompartmentData)
        try:
            df_NodeData = df[1]
        except:
            df_NodeData = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_NodeData)
        try:
            df_ReactionData = df[2]
        except:
            df_ReactionData = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_ReactionData)
        try:
            df_TextData = df[3]
        except:
            df_TextData = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_TextData)
        try:
            df_ShapeData = df[4]
        except:
            df_ShapeData = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_ShapeData)
        try:
            df_LineEndingData = df[5]
        except:
            df_LineEndingData = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_LineEndingData)
        try:
            df_ReactionTextData = df[6]
        except:
            df_ReactionTextData = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_ReactionTextData)
  
    except Exception as err:
        raise Exception (err)

    #isReversible = False
    numNodes = len(df_NodeData)
    numReactions = len(df_ReactionData)
    numArbitraryTexts = len(df_TextData)
    numArbitraryShapes = len(df_ShapeData)
    numlineEndings = len(df_LineEndingData)
    numReactionTexts = len(df_ReactionTextData)

    if numNodes != 0 or numArbitraryTexts != 0 or numArbitraryShapes != 0:
        numCompartments = len(df_CompartmentData)   
        # sbmlStr = df.export() 
        # layout_width = visualizeSBML._getNetworkBottomRightCorner(sbmlStr)[0] + 100.
        # layout_height = visualizeSBML._getNetworkBottomRightCorner(sbmlStr)[1] + 100.
        # if visualizeSBML._getNetworkTopLeftCorner(sbmlStr)[0] < 0:
        #     layout_width -= visualizeSBML._getNetworkTopLeftCorner()[0]
        # if visualizeSBML._getNetworkTopLeftCorner()[1] < 0:
        #     layout_height -= visualizeSBML._getNetworkTopLeftCorner()[1] 
        layout_width = 1000 - 20 
        layout_height = 1000 - 20
    # #######################################

        # Creates an SBMLNamespaces object with the given SBML level, version
        # package name, package version.
        # 
        # (NOTE) By default, the name of package (i.e. "layout") will be used
        # if the argument for the prefix is missing or empty. Thus the argument
        # for the prefix can be added as follows:
        # 
        #    SBMLNamespaces sbmlns(3,1,"layout",1,"LAYOUT")
        # 

        
        if sbmlStr != "": 
            document = libsbml.readSBMLFromString(sbmlStr)    
            document.enablePackage(libsbml.LayoutExtension.getXmlnsL3V1V1(), "layout", True)
            
            # set the "required" attribute of layout package  to "true"
            document.setPkgRequired("layout", False)  
            
            model = document.getModel()
            rxn_specRef_id = []
            
            # to avoid conflicts of species reference ids
            for i in range(numReactions):
                reaction = model.getReaction(i)
                reaction_id = reaction.getId()
                try: #from excel sheet
                    rct_list = list(df_ReactionData.iloc[i]['sources'][1:-1].split(","))
                    prd_list = list(df_ReactionData.iloc[i]['targets'][1:-1].split(","))
                    mod_list = list(df_ReactionData.iloc[i]['modifiers'][1:-1].split(","))
                except: #from dataFrame
                    rct_list = df_ReactionData.iloc[i]['sources']
                    prd_list = df_ReactionData.iloc[i]['targets']
                    mod_list = df_ReactionData.iloc[i]['modifiers']

                rct_num = len(rct_list)
                prd_num = len(prd_list)
                mod_num = len(mod_list)
                rct = []
                prd = []
                mod = []
                for j in range(rct_num):
                    try:
                        rct.append(df_NodeData.iloc[int(rct_list[j])]['id'])
                    except:
                        rct_num = 0
                for j in range(prd_num):
                    try:
                        prd.append(df_NodeData.iloc[int(prd_list[j])]['id'])
                    except:
                        prd_num = 0
                
                for j in range(mod_num):
                    try:
                        mod.append(df_NodeData.iloc[int(mod_list[j])]['id'])
                    except:
                        mod_num = 0

                rct_specRef_id = []
                prd_specRef_id = []
                mod_specRef_id = []
                
                for j in range(rct_num):
                    reference = reaction.getReactant(j)
                    if reference != None:
                        ref_id = reference.getId()
                        if ref_id == "":
                            ref_id = "SpecRef_" + reaction_id + "_rct" + str(j)
                            reference.setId(ref_id)
                    else:
                        reference = reaction.createReactant()
                        reference.setSpecies(rct[j])
                        ref_id = "SpecRef_" + reaction_id + "_rct" + str(j)
                        reference.setId(ref_id)
                        reference.setStoichiometry(1.)
                        reference.setConstant(False)
                    rct_specRef_id.append(ref_id)

                for j in range(prd_num):
                    reference = reaction.getProduct(j)
                    if reference != None:
                        ref_id = reference.getId()
                        if ref_id == "":
                            ref_id = "SpecRef_" + reaction_id + "_prd" + str(j)
                            reference.setId(ref_id)
                    else:
                        reference = reaction.createProduct()
                        reference.setSpecies(prd[j])
                        ref_id = "SpecRef_" + reaction_id + "_prd" + str(j)
                        reference.setId(ref_id)
                        reference.setStoichiometry(1.)
                        reference.setConstant(False)
                    prd_specRef_id.append(ref_id)

                for j in range(mod_num):
                    reference = reaction.getModifier(j)
                    if reference != None:
                        ref_id = reference.getId()
                        if ref_id == "":
                            ref_id = "SpecRef_" + reaction_id + "_mod" + str(j)
                            reference.setId(ref_id)
                    else:
                        reference = reaction.createModifier()
                        reference.setSpecies(mod[j])
                        ref_id = "SpecRef_" + reaction_id + "_mod" + str(j)
                        reference.setId(ref_id)
                    mod_specRef_id.append(ref_id)

                temp_rxn_specRef_id = [reaction_id, rct_specRef_id, prd_specRef_id, mod_specRef_id]
                rxn_specRef_id.append(temp_rxn_specRef_id)

        else: #for test_exportSBML.py
            sbmlns = libsbml.SBMLNamespaces(3, 1, "layout", 1)
            # create the document
            document = libsbml.SBMLDocument(sbmlns)

            # set the "required" attribute of layout package  to "true"
            document.setPkgRequired("layout", False)  

            # create the Model
            model = document.createModel()
            model.setId("SBMLDiagrams_model")
            document.setModel(model)

            # create the Compartment and species
            comp_id_list = []
            for i in range(numCompartments):
                comp_id_list.append(df_CompartmentData.iloc[i]['id']) 

            flag_comp_def = 0
            for i in range(numNodes):
                comp_idx = df_NodeData.iloc[i]['comp_idx']
                if comp_idx == -1:
                    flag_comp_def = 1

            if numCompartments != 0:
                if "_compartment_default_" not in comp_id_list and flag_comp_def == 1:
                    compartment = model.createCompartment()
                    comp_id="_compartment_default_"
                    compartment.setId(comp_id)
                    compartment.setConstant(True)
                    compartment.setVolume(1.)
                for i in range(numCompartments):   
                    compartment = model.createCompartment()
                    comp_id=df_CompartmentData.iloc[i]['id']
                    compartment.setId(comp_id)
                    compartment.setConstant(True)
                    compartment.setVolume(1.)
                spec_id_list = []
                for i in range(numNodes):
                    original_index = df_NodeData.iloc[i]['original_idx']
                    if original_index == -1:
                        spec_id = df_NodeData.iloc[i]['id']
                        if spec_id not in spec_id_list:
                            spec_id_list.append(spec_id)
                        species = model.createSpecies()
                        species.setId(spec_id)
                        comp_idx = df_NodeData.iloc[i]['comp_idx']
                        if comp_idx != -1:
                            comp_id = df_CompartmentData.iloc[comp_idx]['id'] 
                            species.setCompartment(comp_id)  
                        else:
                            species.setCompartment("_compartment_default_") 
                        species.setInitialConcentration(float(df_NodeData.iloc[i]['concentration']))	
                        species.setHasOnlySubstanceUnits(False)
                        species.setBoundaryCondition(False)
                        species.setConstant(False)            
                        if df_NodeData.iloc[i]['floating_node'] == 'FALSE':
                            species.setBoundaryCondition(True)
                            species.setConstant(True)   
            else: #set default compartment
                compartment = model.createCompartment()
                comp_id="_compartment_default_"
                compartment.setId(comp_id)
                compartment.setConstant(True)
                compartment.setVolume(1.)
                spec_id_list = []
                for i in range(numNodes):
                    original_index = df_NodeData.iloc[i]['original_idx']
                    if original_index == -1:
                        spec_id = df_NodeData.iloc[i]['id']
                        if spec_id not in spec_id_list:
                            spec_id_list.append(spec_id)
                        species = model.createSpecies()
                        species.setId(spec_id)
                        species.setCompartment(comp_id)
                        species.setInitialConcentration(float(df_NodeData.iloc[i]['concentration']))	
                        species.setHasOnlySubstanceUnits(False)
                        species.setBoundaryCondition(False)
                        species.setConstant(False)             
                        if df_NodeData.iloc[i]['floating_node'] == 'FALSE':
                            species.setBoundaryCondition(True)
                            species.setConstant(True)
            # create reactions:
            parameters_create = []
            for i in range(numReactions):
                reaction_id = df_ReactionData.iloc[i]['id']
                rxn_rev = bool(df_ReactionData.iloc[i]['rxn_reversible'])
                isReversible = rxn_rev
                rct = [] # id list of the rcts
                prd = []
                mod = []
                try: #from excel sheet
                    rct_list = list(df_ReactionData.iloc[i]['sources'][1:-1].split(","))
                    prd_list = list(df_ReactionData.iloc[i]['targets'][1:-1].split(","))
                    mod_list = list(df_ReactionData.iloc[i]['modifiers'][1:-1].split(","))
                except: #from dataFrame
                    rct_list = df_ReactionData.iloc[i]['sources']
                    prd_list = df_ReactionData.iloc[i]['targets']
                    mod_list = df_ReactionData.iloc[i]['modifiers']

                rct_num = len(rct_list)
                prd_num = len(prd_list)
                mod_num = len(mod_list)
                for j in range(rct_num):
                    try:
                        rct.append(df_NodeData.iloc[int(rct_list[j])]['id'])
                    except:
                        rct_num = 0
                for j in range(prd_num):
                    try:
                        prd.append(df_NodeData.iloc[int(prd_list[j])]['id'])
                    except:
                        prd_num = 0
                
                for j in range(mod_num):
                    try:
                        mod.append(df_NodeData.iloc[int(mod_list[j])]['id'])
                    except:
                        mod_num = 0

                kinetic_law_from_user = df_ReactionData.iloc[i]['rate_law']
                flag_nan = 0
                try:
                    math.isnan(kinetic_law_from_user)
                    flag_nan = 1
                except:
                    pass

                #if str(kinetic_law_from_user) == '' or flag_nan == 1:
                kinetic_law = ''
                parameter_list = []
                kinetic_law = kinetic_law + 'E' + str (i) + '*(k' + str (i) 
                parameter_list.append('E' + str (i))
                parameter_list.append('k' + str (i))
                for j in range(rct_num):
                    kinetic_law = kinetic_law + '*' + rct[j]
                    
                if isReversible:
                    kinetic_law = kinetic_law + ' - k' + str (i) + 'r'
                    parameter_list.append('k' + str (i) + 'r')
                    for j in range(prd_num):
                        kinetic_law = kinetic_law + '*' + prd[j]
                kinetic_law = kinetic_law + ')'
                # else:
                #     kinetic_law = kinetic_law_from_user
                #     parameter_spec_list = getSymbols(kinetic_law_from_user) 
                #     parameter_list = []
                #     for j in range(len(parameter_spec_list)):
                #         if parameter_spec_list[j] not in spec_id_list and parameter_spec_list[j] not in comp_id_list and parameter_spec_list[j] not in parameters_create:
                #             parameter_list.append(parameter_spec_list[j])
                #     if len(parameter_list) == 0: #If the input kinetic law is invalid
                #         kinetic_law = ''
                #         parameter_list = []
                #         kinetic_law = kinetic_law + 'E' + str (i) + '*(k' + str (i) 
                #         parameter_list.append('E' + str (i))
                #         parameter_list.append('k' + str (i))
                #         for j in range(rct_num):
                #             kinetic_law = kinetic_law + '*' + rct[j]
                            
                #         if isReversible:
                #             kinetic_law = kinetic_law + ' - k' + str (i) + 'r'
                #             parameter_list.append('k' + str (i) + 'r')
                #             for j in range(prd_num):
                #                 kinetic_law = kinetic_law + '*' + prd[j]
                #         kinetic_law = kinetic_law + ')'
            
                reaction = model.createReaction()
                reaction.setId(df_ReactionData.iloc[i]['id'])
                reaction.setReversible(False)
                reaction.setFast(False)
                if isReversible:
                    reaction.setReversible(True)
                
                for j in range(len(parameter_list)):
                    parameters_create.append(parameter_list[j])
                    parameters = model.createParameter()
                    parameters.setId(parameter_list[j])
                    parameters.setValue(0.1) # needs to set as the true parameter value.
                    parameters.setConstant(True)
                kinetics = reaction.createKineticLaw()
                kinetics.setFormula(kinetic_law)
                
                for j in range(rct_num):
                    reference = reaction.createReactant()
                    reference.setSpecies(rct[j])
                    ref_id = "SpecRef_" + reaction_id + "_rct" + str(j)
                    reference.setId(ref_id)
                    reference.setStoichiometry(1.)
                    reference.setConstant(False)

                for j in range(prd_num):
                    reference = reaction.createProduct()
                    reference.setSpecies(prd[j])
                    ref_id = "SpecRef_" + reaction_id + "_prd" + str(j)
                    reference.setId(ref_id)
                    reference.setStoichiometry(1.)
                    reference.setConstant(False)

                for j in range(mod_num):
                    reference = reaction.createModifier()
                    reference.setSpecies(mod[j])
                    ref_id = "SpecRef_" + reaction_id + "_mod" + str(j)
                    reference.setId(ref_id)

        sbmlStr = libsbml.writeSBMLToString(document) #sbmlStr is w/o layout or render info

        # create the Layout

        #
        # set the LayoutPkgNamespaces for Level 3 Version1 Layout Version 1
        #
        layoutns = libsbml.LayoutPkgNamespaces(3, 1, 1)

        renderns = libsbml.RenderPkgNamespaces(3, 1, 1)

        #
        # Get a LayoutModelPlugin object plugged in the model object.
        #
        # The type of the returned value of SBase::getPlugin() function is SBasePlugin, and
        # thus the value needs to be casted for the corresponding derived class.
        #

        model_layout = document.getModel()

        mplugin = model.getPlugin("layout")

        # rPlugin = model.getPlugin("render")
        # if rPlugin is None:
        #   print("there is no render outside layout.")
                
        # lolPlugin = mplugin.getListOfLayouts().getPlugin("render")
        # if lolPlugin is None:
        #   print("there is no render info inside layout.")
        
        # if mplugin is None:
            # print(
            #     "[Fatal Error] Layout Extension Level " + layoutns.getLevel() + " Version " + layoutns.getVersion() + " package version " + layoutns.getPackageVersion() + " is not registered.")
            # sys.exit(1)
        #
        # Creates a Layout object via LayoutModelPlugin object.
        #
        if mplugin != None: #remove existed layout with local render
            numPlugins = mplugin.getNumLayouts()
            for i in range(numPlugins):
                mplugin.removeLayout(i)
        try: 
            grPlugin = mplugin.getListOfLayouts().getPlugin("render")
        except:
            pass

        if grPlugin != None: #remove existed global render
            numgrPlugin = grPlugin.getNumGlobalRenderInformationObjects()
            for i in range(numgrPlugin):
                grPlugin.removeGlobalRenderInformation(i)

        layout = mplugin.createLayout()
        layout.setId("SBMLDiagrams_layout")
        layout.setDimensions(libsbml.Dimensions(layoutns, layout_width, layout_height))
        #layout.setDimensions(libsbml.Dimensions(layoutns, 10000-20, 6200-20))
        #layout.setDimensions(libsbml.Dimensions(layoutns, 1000-20, 1000-20))
        compartmentDefaultSize = [layout_width, layout_height]
        # compartmentDefaultSize = [10000-20, 6200-20]
        # compartmentDefaultSize = [1000-20,1000-20]
        # random network (40+800x, 40+800y)

        #create the CompartmentGlyph and SpeciesGlyphs
        if numCompartments != 0:
            for i in range(numCompartments):   
                comp_id=df_CompartmentData.iloc[i]['id']
                if comp_id != "_compartment_default_":
                    compartmentGlyph = layout.createCompartmentGlyph()
                    compG_id = "CompG_" + comp_id
                    compartmentGlyph.setId(compG_id)
                    compartmentGlyph.setCompartmentId(comp_id)
                    bb_id  = "bb_" + comp_id
                    try: 
                        position_list = list(df_CompartmentData.iloc[i]['position'][1:-1].split(","))
                        size_list = list(df_CompartmentData.iloc[i]['size'][1:-1].split(","))
                    except: 
                        position_list = df_CompartmentData.iloc[i]['position']
                        size_list = df_CompartmentData.iloc[i]['size']
                    pos_x  = float(position_list[0])
                    pos_y  = float(position_list[1])
                    width  = float(size_list[0])
                    height = float(size_list[1])
                    compartmentGlyph.setBoundingBox(libsbml.BoundingBox(layoutns, bb_id, pos_x, pos_y, width, height))
            
                    textGlyph = layout.createTextGlyph()
                    textG_id = "TextG_" + comp_id
                    textGlyph.setId(textG_id)
                    content = str(df_CompartmentData.iloc[i]['txt_content'])
                    textGlyph.setText(content)
                    bb_id  = "bb_comp_text_" + comp_id 
                    try:
                        position_list = list(df_CompartmentData.iloc[i]['txt_position'][1:-1].split(","))
                        size_list = list(df_CompartmentData.iloc[i]['txt_size'][1:-1].split(","))
                    except:
                        position_list = df_CompartmentData.iloc[i]['txt_position']
                        size_list = df_CompartmentData.iloc[i]['txt_size']
                    pos_x_text  = float(position_list[0])
                    pos_y_text  = float(position_list[1])
                    width_text  = float(size_list[0])
                    height_text = float(size_list[1])
                    textGlyph.setBoundingBox(libsbml.BoundingBox(layoutns, bb_id, pos_x_text, pos_y_text, width_text, height_text))
                    textGlyph.setGraphicalObjectId(compG_id)
            for i in range(numNodes): 
                spec_id = df_NodeData.iloc[i]['id']  
                spec_index = df_NodeData.iloc[i]['idx']
                spec_shapeIdx = int(df_NodeData.iloc[i]['shape_idx'])
                spec_shapeType = df_NodeData.iloc[i]['shape_type']
                try:
                    spec_shapeInfo_list_pre = list(df_NodeData.iloc[i]['shape_info'][1:-1].split(","))
                except:
                    spec_shapeInfo_list_pre = df_NodeData.iloc[i]['shape_info']
                #from excel sheet
                if spec_shapeInfo_list_pre == ['']:
                    spec_shapeInfo = []
                elif len(spec_shapeInfo_list_pre) == 0:
                    spec_shapeInfo = []
                else:
                    spec_shapeInfo_pre = []
                    spec_shapeInfo = []
                    if type(spec_shapeInfo_list_pre[0]) is str:
                        for ii in range(len(spec_shapeInfo_list_pre)):
                            temp = spec_shapeInfo_list_pre[ii]
                            if temp.find('[') != -1:
                                temp_update = temp.replace('[', '')
                            elif temp.find(']') != -1:
                                temp_update = temp.replace(']', '')
                            spec_shapeInfo_pre.append(float(temp_update))
                        for ii in range(0,len(spec_shapeInfo_pre),2):
                            spec_shapeInfo.append([spec_shapeInfo_pre[ii], spec_shapeInfo_pre[ii+1]])
                    else:
                        spec_shapeInfo = spec_shapeInfo_list_pre
                speciesGlyph = layout.createSpeciesGlyph()
                specG_id = "SpecG_"  + spec_id + '_idx_' + str(spec_index)
                speciesGlyph.setId(specG_id)
                speciesGlyph.setSpeciesId(spec_id)
                bb_id  = "bb_" + spec_id + '_idx_' + str(spec_index)

                try:
                    position_list = list(df_NodeData.iloc[i]['position'][1:-1].split(","))
                    size_list = list(df_NodeData.iloc[i]['size'][1:-1].split(","))
                except:
                    position_list = df_NodeData.iloc[i]['position']
                    size_list = df_NodeData.iloc[i]['size']
                pos_x  = float(position_list[0])
                pos_y  = float(position_list[1])
                width  = float(size_list[0])
                height = float(size_list[1])
                speciesGlyph.setBoundingBox(libsbml.BoundingBox(layoutns, bb_id, pos_x, pos_y, width, height))
                content = str(df_NodeData.iloc[i]['txt_content'])


                textGlyph = layout.createTextGlyph()
                textG_id = "TextG_" + spec_id + '_idx_' + str(spec_index)
                textGlyph.setId(textG_id)
                textGlyph.setText(content) # this will merge "setOriginOfTextId"
                bb_id  = "bb_spec_text_" + spec_id + '_idx_' + str(spec_index)
                try:
                    position_list = list(df_NodeData.iloc[i]['txt_position'][1:-1].split(","))
                    size_list = list(df_NodeData.iloc[i]['txt_size'][1:-1].split(","))
                except:
                    position_list = df_NodeData.iloc[i]['txt_position']
                    size_list = df_NodeData.iloc[i]['txt_size']
                pos_x_text  = float(position_list[0])
                pos_y_text  = float(position_list[1])
                width_text  = float(size_list[0])
                height_text = float(size_list[1])
                textGlyph.setBoundingBox(libsbml.BoundingBox(layoutns, bb_id, pos_x_text, pos_y_text, width_text, height_text))
                #textGlyph.setOriginOfTextId(specG_id)
                textGlyph.setGraphicalObjectId(specG_id)
        else:#there is no compartment  
            comp_id= "_compartment_default_"
            compartmentGlyph = layout.createCompartmentGlyph()
            compG_id = "CompG_" + comp_id
            compartmentGlyph.setId(compG_id)
            compartmentGlyph.setCompartmentId(comp_id)
            bb_id  = "bb_" + comp_id
            pos_x  = 10.
            pos_y  = 10.
            width  = compartmentDefaultSize[0]
            height = compartmentDefaultSize[1]
            compartmentGlyph.setBoundingBox(libsbml.BoundingBox(layoutns, bb_id, pos_x, pos_y, width, height))
        
            for i in range(numNodes):
                spec_id = df_NodeData.iloc[i]['id']  
                spec_index = df_NodeData.iloc[i]['idx']
                spec_shapeIdx = int(df_NodeData.iloc[i]['shape_idx'])
                spec_shapeIdx = df_NodeData.iloc[i]['shape_idx']
                spec_shapeType = df_NodeData.iloc[i]['shape_type']
                try:
                    spec_shapeInfo_list_pre = list(df_NodeData.iloc[i]['shape_info'][1:-1].split(","))
                except:
                    spec_shapeInfo_list_pre = df_NodeData.iloc[i]['shape_info']
                if spec_shapeInfo_list_pre == ['']:
                    spec_shapeInfo = []
                elif len(spec_shapeInfo_list_pre) == 0:
                    spec_shapeInfo = []
                else:
                    spec_shapeInfo_pre = []
                    spec_shapeInfo = []
                    if type(spec_shapeInfo_list_pre[0]) is str:
                        for ii in range(len(spec_shapeInfo_list_pre)):
                            temp = spec_shapeInfo_list_pre[ii]
                            if temp.find('[') != -1:
                                temp_update = temp.replace('[', '')
                            elif temp.find(']') != -1:
                                temp_update = temp.replace(']', '')
                            spec_shapeInfo_pre.append(float(temp_update))
                        for ii in range(0,len(spec_shapeInfo_pre),2):
                            spec_shapeInfo.append([spec_shapeInfo_pre[ii], spec_shapeInfo_pre[ii+1]])
                    else:
                        spec_shapeInfo = spec_shapeInfo_list_pre
                speciesGlyph = layout.createSpeciesGlyph()
                specG_id = "SpecG_"  + spec_id + '_idx_' + str(spec_index)
                speciesGlyph.setId(specG_id)
                speciesGlyph.setSpeciesId(spec_id)
                bb_id  = "bb_" + spec_id + '_idx_' + str(spec_index)
                try:
                    position_list = list(df_NodeData.iloc[i]['position'][1:-1].split(","))
                    size_list = list(df_NodeData.iloc[i]['size'][1:-1].split(","))
                except:
                    position_list = df_NodeData.iloc[i]['position']
                    size_list = df_NodeData.iloc[i]['size']
                pos_x  = float(position_list[0])
                pos_y  = float(position_list[1])
                width  = float(size_list[0])
                height = float(size_list[1])
                content = str(df_NodeData.iloc[i]['txt_content'])

                speciesGlyph.setBoundingBox(libsbml.BoundingBox(layoutns, bb_id, pos_x, pos_y, width, height))

                textGlyph = layout.createTextGlyph()
                textG_id = "TextG_" + spec_id + '_idx_' + str(spec_index)
                textGlyph.setId(textG_id)
                textGlyph.setText(content) # this will merge "setOriginOfTextId
                try:
                    position_list = list(df_NodeData.iloc[i]['txt_position'][1:-1].split(","))
                    size_list = list(df_NodeData.iloc[i]['txt_size'][1:-1].split(","))
                except:
                    position_list = df_NodeData.iloc[i]['txt_position']
                    size_list = df_NodeData.iloc[i]['txt_size']
                pos_x_text  = float(position_list[0])
                pos_y_text  = float(position_list[1])
                width_text  = float(size_list[0])
                height_text = float(size_list[1])
                bb_id  = "bb_spec_text_" + spec_id + '_idx_' + str(spec_index)
                textGlyph.setBoundingBox(libsbml.BoundingBox(layoutns, bb_id, pos_x_text, pos_y_text, width_text, height_text))
                #textGlyph.setOriginOfTextId(specG_id)
                textGlyph.setGraphicalObjectId(specG_id)

        # create the ReactionGlyphs and SpeciesReferenceGlyphs
        for i in range(numReactions):
            reaction_id = df_ReactionData.iloc[i]['id']
            try: #for test_exportSBML.py
                for xx in range(len(rxn_specRef_id)):
                    if rxn_specRef_id[xx][0] == reaction_id:
                        temp_rxn_specRef_id = rxn_specRef_id[xx]
            except:
                pass

            center_size = [0.,0.]
            try:
                center_size = list(df_ReactionData.iloc[i]['center_size'][1:-1].split(","))
            except:
                center_size = df_ReactionData.iloc[i]['center_size']

            reactionGlyph = layout.createReactionGlyph()
            reactionG_id = "ReactionG_" + reaction_id
            reactionGlyph.setId(reactionG_id)
            reactionGlyph.setReactionId(reaction_id)

            reaction_line_thickness = float(df_ReactionData.iloc[i]['line_thickness'])
            
            rct = [] # id list of the rcts
            prd = []
            mod = []
            try:
                rct_list = list(df_ReactionData.iloc[i]['sources'][1:-1].split(","))
                prd_list = list(df_ReactionData.iloc[i]['targets'][1:-1].split(","))
                mod_list = list(df_ReactionData.iloc[i]['modifiers'][1:-1].split(","))
            except:
                rct_list = df_ReactionData.iloc[i]['sources']
                prd_list = df_ReactionData.iloc[i]['targets']
                mod_list = df_ReactionData.iloc[i]['modifiers']
            rct_index = []
            prd_index = []
            mod_index = []
            rct_num = len(rct_list)
            prd_num = len(prd_list)
            mod_num = len(mod_list)

            try:
                rct_lineend_pos_list = list(df_ReactionData.iloc[i]['src_lineend_position'][1:-1].split(","))
                prd_lineend_pos_list = list(df_ReactionData.iloc[i]['tgt_lineend_position'][1:-1].split(","))
                mod_lineend_pos_list = list(df_ReactionData.iloc[i]['mod_lineend_position'][1:-1].split(","))
            except:
                rct_lineend_pos_list = df_ReactionData.iloc[i]['src_lineend_position']
                prd_lineend_pos_list = df_ReactionData.iloc[i]['tgt_lineend_position']
                mod_lineend_pos_list = df_ReactionData.iloc[i]['mod_lineend_position']


            for j in range(rct_num):
                try:
                    rct.append(df_NodeData.iloc[int(rct_list[j])]['id'])
                    rct_index.append(df_NodeData.iloc[int(rct_list[j])]['idx'])
                except:
                    rct_num = 0
            for j in range(prd_num):
                try:
                    prd.append(df_NodeData.iloc[int(prd_list[j])]['id'])
                    prd_index.append(df_NodeData.iloc[int(prd_list[j])]['idx'])
                except:
                    prd_num = 0
            for j in range(mod_num):
                try:
                    mod.append(df_NodeData.iloc[int(mod_list[j])]['id'])
                    mod_index.append(df_NodeData.iloc[int(mod_list[j])]['idx'])
                except:
                    mod_num = 0

            #calculate center_position and handles by ourselves
            center_x = 0.
            center_y = 0.
            for j in range(rct_num):
                try:
                    src_position = list(df_NodeData.iloc[int(rct_list[j])]['position'][1:-1].split(","))
                    src_dimension = list(df_NodeData.iloc[int(rct_list[j])]['size'][1:-1].split(",")) 
                except:
                    src_position = df_NodeData.iloc[int(rct_list[j])]['position']
                    src_dimension = df_NodeData.iloc[int(rct_list[j])]['size']
                center_x += float(src_position[0])+.5*float(src_dimension[0])
                center_y += float(src_position[1])+.5*float(src_dimension[1])
            for j in range(prd_num):
                try:
                    dst_position = list(df_NodeData.iloc[int(prd_list[j])]['position'][1:-1].split(","))
                    dst_dimension = list(df_NodeData.iloc[int(prd_list[j])]['size'][1:-1].split(",")) 
                except:
                    dst_position = df_NodeData.iloc[int(prd_list[j])]['position']
                    dst_dimension = df_NodeData.iloc[int(prd_list[j])]['size']
                center_x += float(dst_position[0])+.5*float(dst_dimension[0])
                center_y += float(dst_position[1])+.5*float(dst_dimension[1])
            center_x = center_x/(rct_num + prd_num) 
            center_y = center_y/(rct_num + prd_num)
            center_position = [center_x, center_y]
 
            handles = [center_position] #here should be center_handle_position but it is unknown
            
            for j in range(rct_num):
                src_handle_x = .5*(center_position[0] + float(src_position[0]) + .5*float(src_dimension[0]))
                src_handle_y = .5*(center_position[1] + float(src_position[1]) + .5*float(src_dimension[1]))
                handles.append([src_handle_x,src_handle_y])
            for j in range(prd_num):
                dst_handle_x = .5*(center_position[0] + float(dst_position[0]) + .5*float(dst_dimension[0]))
                dst_handle_y = .5*(center_position[1] + float(dst_position[1]) + .5*float(dst_dimension[1]))
                handles.append([dst_handle_x,dst_handle_y])
            
            try:
                try:
                    center_pos = list(df_ReactionData.iloc[i]['center_pos'][1:-1].split(","))
                    handles_list_pre = list(df_ReactionData.iloc[i]['handles'][1:-1].split(","))
                except:
                    center_pos = df_ReactionData.iloc[i]['center_pos']
                    handles_list_pre = df_ReactionData.iloc[i]['handles']
                #from excel sheet
                handles_pre = []
                handles_update = []

                if type(handles_list_pre[0]) is str:
                    for i in range(len(handles_list_pre)):
                        temp = handles_list_pre[i]
                        if temp.find('[') != -1:
                            temp_update = temp.replace('[', '')
                        elif temp.find(']') != -1:
                            temp_update = temp.replace(']', '')
                        handles_pre.append(float(temp_update))
                    for i in range(0,len(handles_pre),2):
                        handles_update.append([handles_pre[i], handles_pre[i+1]])
                else:
                    handles_update = handles_list_pre
                #print("export:", handles)
                center_value = [float(center_pos[0]),float(center_pos[1])]
            except:
                center_value = center_position

            # if len(handles_update) < 3: # if updated handles info is invalid
            #     center_value = center_position
            # else:

            if [] not in handles_update and handles_update != []:
                try:
                    for i in range(len(handles)):
                        handles[i] = handles_update[i]
                except:
                    pass

            reactionCurve = reactionGlyph.getCurve()
            ls = reactionCurve.createLineSegment()

            ls.setStart(libsbml.Point(layoutns, center_value[0], center_value[1]))
            ls.setEnd(libsbml.Point(layoutns, center_value[0], center_value[1]))

            if center_size != [0.,0.] and center_size != []:
                bb_id  = "bb_" + reaction_id
                width  = float(center_size[0])
                height = float(center_size[1])
                pos_x  = center_value[0]-.5*width
                pos_y  = center_value[1]-.5*height
                reactionGlyph.setBoundingBox(libsbml.BoundingBox(layoutns, bb_id, pos_x, pos_y, width, height))
                      
            for j in range(rct_num):
                #to make the species reference consistent
                try: #for test_exportSBML.py if there is no temp_rxn_specRef_id
                    if temp_rxn_specRef_id[1] != []: #check rct_num error
                        ref_id = temp_rxn_specRef_id[1][j]
                except:
                    ref_id = "SpecRef_" + reaction_id + "_rct" + str(j)
                speciesReferenceGlyph = reactionGlyph.createSpeciesReferenceGlyph()
                specsRefG_id = "SpecRefG_" + reaction_id + "_rct" + str(j)
                specG_id = "SpecG_" + rct[j] + '_idx_' + str(rct_index[j])
                speciesReferenceGlyph.setId(specsRefG_id)
                speciesReferenceGlyph.setSpeciesGlyphId(specG_id)
                speciesReferenceGlyph.setSpeciesReferenceId(ref_id)
                speciesReferenceGlyph.setRole(libsbml.SPECIES_ROLE_SUBSTRATE)
                speciesReferenceCurve = speciesReferenceGlyph.getCurve()
                cb = speciesReferenceCurve.createCubicBezier()
                # try: 
                #     handle1 = handles_update[0]
                #     handle2 = handles_update[j+1]
                # except:
                #     handle1 = handles[0]
                #     handle2 = handles[j+1]
                handle1 = handles[0]
                handle2 = handles[j+1]


                try:
                    src_position = list(df_NodeData.iloc[int(rct_list[j])]['position'][1:-1].split(","))
                    src_dimension = list(df_NodeData.iloc[int(rct_list[j])]['size'][1:-1].split(",")) 
                except:
                    src_position = df_NodeData.iloc[int(rct_list[j])]['position']
                    src_dimension = df_NodeData.iloc[int(rct_list[j])]['size']
                pos_x = float(src_position[0])
                pos_y = float(src_position[1])
                width = float(src_dimension[0])
                height = float(src_dimension[1])

                try:
                    line_end_pt = rct_lineend_pos_list[j]
                    if line_end_pt[0] < (pos_x + width) and line_end_pt[0] > pos_x  and line_end_pt[1] > pos_y and line_end_pt[1] < (pos_y+height):
                        line_end_pt = _cross_point(handle2, 
                        [pos_x-reaction_line_thickness, pos_y-reaction_line_thickness], 
                        [width+2.*reaction_line_thickness,height+2.*reaction_line_thickness])
                        if line_end_pt == None:
                            line_end_pt = _cross_point(center_value, 
                            [pos_x-reaction_line_thickness, pos_y-reaction_line_thickness], 
                            [width+2.*reaction_line_thickness,height+2.*reaction_line_thickness])                  
                except:               
                    line_end_pt = _cross_point(handle2, 
                    [pos_x-reaction_line_thickness, pos_y-reaction_line_thickness], 
                    [width+2.*reaction_line_thickness,height+2.*reaction_line_thickness])
                    if line_end_pt == None:
                        line_end_pt = _cross_point(center_value, 
                        [pos_x-reaction_line_thickness, pos_y-reaction_line_thickness], 
                        [width+2.*reaction_line_thickness,height+2.*reaction_line_thickness])
                
                try:
                    cb.setStart(libsbml.Point(layoutns, line_end_pt[0], line_end_pt[1]))
                except:
                    cb.setStart(libsbml.Point(layoutns, pos_x + 0.5*width, pos_y + 0.5*height))
                cb.setBasePoint1(libsbml.Point(layoutns, handle2[0], handle2[1]))
                cb.setBasePoint2(libsbml.Point(layoutns, handle1[0], handle1[1]))
                cb.setEnd(libsbml.Point(layoutns, center_value[0], center_value[1]))


            for j in range(prd_num):
                try:
                    if temp_rxn_specRef_id[2] != []:
                        ref_id = temp_rxn_specRef_id[2][j]
                except:
                    ref_id = "SpecRef_" + reaction_id + "_prd" + str(j)
                speciesReferenceGlyph = reactionGlyph.createSpeciesReferenceGlyph()
                specsRefG_id = "SpecRefG_" + reaction_id + "_prd" + str(j)
                specG_id = "SpecG_" + prd[j]  + '_idx_' + str(prd_index[j])
                speciesReferenceGlyph.setId(specsRefG_id)
                speciesReferenceGlyph.setSpeciesGlyphId(specG_id)
                speciesReferenceGlyph.setSpeciesReferenceId(ref_id)
                speciesReferenceGlyph.setRole(libsbml.SPECIES_ROLE_PRODUCT)

                speciesReferenceCurve = speciesReferenceGlyph.getCurve()
                cb = speciesReferenceCurve.createCubicBezier()
                cb.setStart(libsbml.Point(layoutns, center_value[0], center_value[1]))
                # try:
                #     handle1 = [2.*center_value[0]-handles_update[0][0], 2.*center_value[1]-handles_update[0][1]]
                #     handle2 = handles_update[rct_num+1+j]
                # except:
                #     handle1 = [2.*center_value[0]-handles[0][0], 2.*center_value[1]-handles[0][1]]
                #     handle2 = handles[rct_num+1+j]
                handle1 = [2.*center_value[0]-handles[0][0], 2.*center_value[1]-handles[0][1]]
                handle2 = handles[rct_num+1+j]
                cb.setBasePoint1(libsbml.Point(layoutns, handle1[0], handle1[1]))
                cb.setBasePoint2(libsbml.Point(layoutns, handle2[0], handle2[1]))
            

                try:
                    dst_position = list(df_NodeData.iloc[int(prd_list[j])]['position'][1:-1].split(","))
                    dst_dimension = list(df_NodeData.iloc[int(prd_list[j])]['size'][1:-1].split(","))
                except:
                    dst_position = df_NodeData.iloc[int(prd_list[j])]['position']
                    dst_dimension = df_NodeData.iloc[int(prd_list[j])]['size']     

                pos_x = float(dst_position[0])
                pos_y = float(dst_position[1])
                width = float(dst_dimension[0])
                height = float(dst_dimension[1])

                try:
                    line_head_pt = prd_lineend_pos_list[j]
                    if line_head_pt[0] < (pos_x + width) and line_head_pt[0] > pos_x  and line_head_pt[1] > pos_y and line_head_pt[1] < (pos_y+height):
                        line_head_pt = _cross_point(handle2, 
                        [pos_x-reaction_line_thickness, pos_y-reaction_line_thickness], 
                        [width+2.*reaction_line_thickness,height+2.*reaction_line_thickness])
                        if line_head_pt == None:
                            line_head_pt = _cross_point(center_value, 
                            [pos_x-reaction_line_thickness, pos_y-reaction_line_thickness], 
                            [width+2.*reaction_line_thickness,height+2.*reaction_line_thickness])            
                except:
                    line_head_pt = _cross_point(handle2, 
                    [pos_x-reaction_line_thickness, pos_y-reaction_line_thickness], 
                    [width+2.*reaction_line_thickness,height+2.*reaction_line_thickness])
                    if line_head_pt == None:
                        line_head_pt = _cross_point(center_value, 
                        [pos_x-reaction_line_thickness, pos_y-reaction_line_thickness], 
                        [width+2.*reaction_line_thickness,height+2.*reaction_line_thickness])
                
                try:
                    cb.setEnd(libsbml.Point(layoutns, line_head_pt[0], line_head_pt[1]))
                except:
                    cb.setEnd(libsbml.Point(layoutns, pos_x + 0.5*width, pos_y + 0.5*height))

            for j in range(mod_num):
                try:
                    if temp_rxn_specRef_id[3] != []:
                        ref_id = temp_rxn_specRef_id[3][j]
                except:
                    ref_id = "SpecRef_" + reaction_id + "_mod" + str(j)
                speciesReferenceGlyph = reactionGlyph.createSpeciesReferenceGlyph()
                specsRefG_id = "SpecRefG_" + reaction_id + "_mod" + str(j)
                specG_id = "SpecG_" + mod[j]  + '_idx_' + str(mod_index[j])
                speciesReferenceGlyph.setId(specsRefG_id)
                speciesReferenceGlyph.setSpeciesGlyphId(specG_id)
                speciesReferenceGlyph.setSpeciesReferenceId(ref_id)
                speciesReferenceGlyph.setRole(libsbml.SPECIES_ROLE_MODIFIER)

                speciesReferenceCurve = speciesReferenceGlyph.getCurve()
                mod_ls = speciesReferenceCurve.createLineSegment()
                try:
                    mod_position = list(df_NodeData.iloc[int(mod_list[j])]['position'][1:-1].split(","))
                    mod_dimension = list(df_NodeData.iloc[int(mod_list[j])]['size'][1:-1].split(","))
                except:
                    mod_position = df_NodeData.iloc[int(mod_list[j])]['position']
                    mod_dimension = df_NodeData.iloc[int(mod_list[j])]['size']     

                pos_x = float(mod_position[0])
                pos_y = float(mod_position[1])
                width = float(mod_dimension[0])
                height = float(mod_dimension[1])

                mod_start_virtual_x = pos_x + 0.5*width 
                mod_start_virtual_y = pos_y + 0.5*height
                try: 
                    [mod_start_x, mod_start_y] = _cross_point(center_value, 
                    [pos_x-reaction_line_thickness*2.,pos_y-reaction_line_thickness*2.],
                    [width+reaction_line_thickness*4., height+reaction_line_thickness*4.]) 
                except: 
                    mod_start_x = mod_start_virtual_x
                    mod_start_y = mod_start_virtual_y
                mod_ls.setStart(libsbml.Point(layoutns, mod_start_x, mod_start_y))

                try:
                    [mod_end_x, mod_end_y] = mod_lineend_pos_list[j]
                except:
                    try: 
                        [mod_end_x, mod_end_y] = _cross_point([mod_start_virtual_x, mod_start_virtual_y],
                        [center_value[0]-5.*reaction_line_thickness, center_value[1]-5.*reaction_line_thickness], 
                        [10.*reaction_line_thickness, 10.*reaction_line_thickness])
                    except: 
                        [mod_end_x, mod_end_y] = center_value
                try:
                    mod_ls.setEnd(libsbml.Point(layoutns, mod_end_x, mod_end_y))
                except:
                    mod_ls.setEnd(libsbml.Point(layoutns, center_value[0], center_value[1]))
        #arbitrary texts
        for i in range(numArbitraryTexts):
            txt_content = str(df_TextData.iloc[i]['txt_content']) 
            try:
                position_list = list(df_TextData.iloc[i]['txt_position'][1:-1].split(","))
                size_list = list(df_TextData.iloc[i]['txt_size'][1:-1].split(","))
            except:
                position_list = df_TextData.iloc[i]['txt_position']
                size_list = df_TextData.iloc[i]['txt_size'] 

            textGlyph = layout.createTextGlyph()
            if ' ' in txt_content:
                txt_content_adapt = txt_content.replace(' ', '_')
            else:
                txt_content_adapt = txt_content
            textG_id = "TextG_" + txt_content_adapt + '_idx_' + str(i)
            textGlyph.setId(textG_id)
            textGlyph.setText(txt_content)
            bb_id  = "bb_text_" + txt_content + '_idx_' + str(i)
            pos_x_text  = float(position_list[0])
            pos_y_text  = float(position_list[1])
            width_text  = float(size_list[0])
            height_text = float(size_list[1])
            textGlyph.setBoundingBox(libsbml.BoundingBox(layoutns, bb_id, pos_x_text, pos_y_text, width_text, height_text))

        for i in range(numReactionTexts):
            rxn_id = str(df_ReactionTextData.iloc[i]['rxn_id'])
            reactionG_id = "ReactionG_" + rxn_id
            txt_id = str(df_ReactionTextData.iloc[i]['txt_id'])
            txt_content = str(df_ReactionTextData.iloc[i]['txt_content']) 
            try:
                position_list = list(df_ReactionTextData.iloc[i]['txt_position'][1:-1].split(","))
                size_list = list(df_ReactionTextData.iloc[i]['txt_size'][1:-1].split(","))
            except:
                position_list = df_ReactionTextData.iloc[i]['txt_position']
                size_list = df_ReactionTextData.iloc[i]['txt_size'] 

            textGlyph = layout.createTextGlyph()
            textG_id = "TextG_" + rxn_id + '_idx_' + str(txt_id)
            textGlyph.setId(textG_id)
            textGlyph.setText(txt_content)
            bb_id  = "bb_text_" + txt_content + '_idx_' + str(i)
            pos_x_text  = float(position_list[0])
            pos_y_text  = float(position_list[1])
            width_text  = float(size_list[0])
            height_text = float(size_list[1])
            textGlyph.setBoundingBox(libsbml.BoundingBox(layoutns, bb_id, pos_x_text, pos_y_text, width_text, height_text))
            textGlyph.setGraphicalObjectId(reactionG_id)

        #arbitrary shape
        for i in range(numArbitraryShapes):
            gen_shape_name = str(df_ShapeData.iloc[i]['shape_name']) 
            try:
                position_list = list(df_ShapeData.iloc[i]['position'][1:-1].split(","))
                size_list = list(df_ShapeData.iloc[i]['size'][1:-1].split(","))
            except:
                position_list = df_ShapeData.iloc[i]['position']
                size_list = df_ShapeData.iloc[i]['size'] 

            genGlyph = layout.createGeneralGlyph()
            genG_id = gen_shape_name
            genGlyph.setId(genG_id)
            bb_id  = "bb_shape_" + gen_shape_name
            pos_x_text  = float(position_list[0])
            pos_y_text  = float(position_list[1])
            width_text  = float(size_list[0])
            height_text = float(size_list[1])
            genGlyph.setBoundingBox(libsbml.BoundingBox(layoutns, bb_id, pos_x_text, pos_y_text, width_text, height_text))


        sbmlStr_layout = libsbml.writeSBMLToString(document) #sbmlStr_layout is w layout info but w/o render info

        doc = libsbml.readSBMLFromString(sbmlStr_layout)
        model_layout = doc.getModel()
        mplugin = model_layout.getPlugin("layout")

        # add render information to the first layout
        layout = mplugin.getLayout(0)

        rPlugin = layout.getPlugin("render")

        uri = libsbml.RenderExtension.getXmlnsL2() if doc.getLevel() == 2 else libsbml.RenderExtension.getXmlnsL3V1V1();

        #enable render package
        doc.enablePackage(uri, "render", True)
        doc.setPackageRequired("render", False)

        rPlugin = layout.getPlugin("render")

        rInfo = rPlugin.createLocalRenderInformation()
        rInfo.setId("info")
        rInfo.setName("Render Information")
        rInfo.setProgramName("RenderInformation")
        rInfo.setProgramVersion("1.0")

        #lineEnding
        for i in range(numlineEndings):
            lineEnding_id = df_LineEndingData.iloc[i]['id']
            #print(lineEnding_id)
            try:
                position = list(df_LineEndingData.iloc[i]['position'][1:-1].split(","))
                size = list(df_LineEndingData.iloc[i]['size'][1:-1].split(","))
                fill_color = list(df_LineEndingData.iloc[i]['fill_color'][1:-1].split(","))
                shape_type_list = list(df_LineEndingData.iloc[i]['shape_type'][1:-1].split(","))
                shape_info_list = list(df_LineEndingData.iloc[i]['shape_info'][1:-1].split(","))
                border_color = list(df_LineEndingData.iloc[i]['border_color'][1:-1].split(","))
            except:    
                position = df_LineEndingData.iloc[i]['position']
                size = df_LineEndingData.iloc[i]['size']
                fill_color = df_LineEndingData.iloc[i]['fill_color'] 
                shape_type_list = df_LineEndingData.iloc[i]['shape_type']
                shape_info_list = df_LineEndingData.iloc[i]['shape_info']
                border_color = df_LineEndingData.iloc[i]['border_color']

            lineEnding = rInfo.createLineEnding()
            lineEnding.setId(lineEnding_id)
            #if lineEnding_id != '_line_ending_default_NONE_':
            if len(fill_color) == 4:
                fill_color_str    = '#%02x%02x%02x%02x' % (int(fill_color[0]),int(fill_color[1]),int(fill_color[2]),int(fill_color[3]))
                color = rInfo.createColorDefinition()
                color.setId("lineEnding_fill_color" + "_" + lineEnding_id)
                color.setColorValue(fill_color_str)
                lineEnding.getGroup().setFill('lineEnding_fill_color' + '_' + lineEnding_id)

            elif len(fill_color) == 3:
                fill_color_str    = '#%02x%02x%02x' % (int(fill_color[0]),int(fill_color[1]),int(fill_color[2]))     
                color = rInfo.createColorDefinition()
                color.setId("lineEnding_fill_color" + "_" + lineEnding_id)
                color.setColorValue(fill_color_str)
                lineEnding.getGroup().setFill('lineEnding_fill_color' + '_' + lineEnding_id)

            if len(border_color) == 4:
                border_color_str    = '#%02x%02x%02x%02x' % (int(border_color[0]),int(border_color[1]),int(border_color[2]),int(border_color[3]))
                color = rInfo.createColorDefinition()
                color.setId("lineEnding_border_color" + "_" + lineEnding_id)
                color.setColorValue(border_color_str)
                lineEnding.getGroup().setStroke('lineEnding_border_color' + '_' + lineEnding_id)

            elif len(border_color) == 3:
                border_color_str    = '#%02x%02x%02x' % (int(border_color[0]),int(border_color[1]),int(border_color[2]))     
                color = rInfo.createColorDefinition()
                color.setId("lineEnding_border_color" + "_" + lineEnding_id)
                color.setColorValue(border_color_str)
                lineEnding.getGroup().setStroke('lineEnding_border_color' + '_' + lineEnding_id)

            bb_id = "bb_" + lineEnding_id
            [pos_x, pos_y] = position
            [width, height] = size
            if size != [0.,0.]:
                lineEnding.setEnableRotationalMapping(True)
                lineEnding.setBoundingBox(libsbml.BoundingBox(layoutns, bb_id, pos_x, pos_y, width, height))

                for j in range(len(shape_type_list)):
                    if shape_type_list[j] == 'polygon':
                        polygon = lineEnding.getGroup().createPolygon()
                        for k in range(len(shape_info_list[j])):
                            x = shape_info_list[j][k][0]
                            y = shape_info_list[j][k][1]                           
                            renderPoint = polygon.createPoint()
                            renderPoint.setCoordinates(libsbml.RelAbsVector(0,x), libsbml.RelAbsVector(0,y))

                    elif shape_type_list[j] == 'ellipse':
                        ellipse = lineEnding.getGroup().createEllipse()
                        cx = shape_info_list[j][0][0]
                        cy = shape_info_list[j][0][1]
                        rx = shape_info_list[j][1][0]
                        ry = shape_info_list[j][1][1] 
                        ellipse.setCenter2D(libsbml.RelAbsVector(0, cx), libsbml.RelAbsVector(0, cy))
                        ellipse.setRadii(libsbml.RelAbsVector(0, rx),libsbml.RelAbsVector(0, ry))
            
                    elif shape_type_list[j] == 'rectangle':
                        rectangle = lineEnding.getGroup().createRectangle()
                        w = shape_info_list[j][0]
                        h = shape_info_list[j][1]  
                        rectangle.setCoordinatesAndSize(libsbml.RelAbsVector(0,0),
                        libsbml.RelAbsVector(0,0),libsbml.RelAbsVector(0,0),
                        libsbml.RelAbsVector(0,w),libsbml.RelAbsVector(0,h))

        if numCompartments != 0:  
            for i in range(numCompartments):
                comp_id = df_CompartmentData.iloc[i]['id']
                compG_id = "CompG_" + comp_id
                textG_id = "TextG_" + comp_id
                #print(comp_id)
                #if comp_id != '_compartment_default':

                comp_shapeType = df_CompartmentData.iloc[i]['shape_type']

                try:
                    comp_shapeInfo_list_pre = list(df_CompartmentData.iloc[i]['shape_info'][1:-1].split(","))
                except:
                    comp_shapeInfo_list_pre = df_CompartmentData.iloc[i]['shape_info']
                if comp_shapeInfo_list_pre == ['']:
                    comp_shapeInfo = []
                elif len(comp_shapeInfo_list_pre) == 0:
                    comp_shapeInfo = []
                else:
                    comp_shapeInfo_pre = []
                    comp_shapeInfo = []
                    if type(comp_shapeInfo_list_pre[0]) is str:
                        for ii in range(len(comp_shapeInfo_list_pre)):
                            temp = comp_shapeInfo_list_pre[ii]
                            if temp.find('[') != -1:
                                temp_update = temp.replace('[', '')
                            elif temp.find(']') != -1:
                                temp_update = temp.replace(']', '')
                            comp_shapeInfo_pre.append(float(temp_update))
                        for ii in range(0,len(comp_shapeInfo_pre),2):
                            comp_shapeInfo.append([comp_shapeInfo_pre[ii], comp_shapeInfo_pre[ii+1]])
                    else:
                        comp_shapeInfo = comp_shapeInfo_list_pre

                try:
                    fill_color   = list(df_CompartmentData.iloc[i]['fill_color'][1:-1].split(","))
                    border_color = list(df_CompartmentData.iloc[i]['border_color'][1:-1].split(","))
                except:    
                    fill_color   = df_CompartmentData.iloc[i]['fill_color']
                    border_color = df_CompartmentData.iloc[i]['border_color']

                comp_border_width = float(df_CompartmentData.iloc[i]['border_width'])
                if len(fill_color) == 4:
                    fill_color_str    = '#%02x%02x%02x%02x' % (int(fill_color[0]),int(fill_color[1]),int(fill_color[2]),int(fill_color[3]))
                elif len(fill_color) == 3:
                    fill_color_str    = '#%02x%02x%02x' % (int(fill_color[0]),int(fill_color[1]),int(fill_color[2]))
                
                if len(border_color) == 4:    
                    border_color_str  = '#%02x%02x%02x%02x' % (int(border_color[0]),int(border_color[1]),int(border_color[2]),int(border_color[3]))
                elif len(border_color) == 3:
                    border_color_str  = '#%02x%02x%02x' % (int(border_color[0]),int(border_color[1]),int(border_color[2]))

                #print(fill_color, fill_color_str)
                try:
                    font_color = list(df_CompartmentData.iloc[i]['txt_font_color'][1:-1].split(","))
                    text_anchor_list = list(df_CompartmentData.iloc[i]['txt_anchor'][1:-1].split(","))
                except:
                    font_color = df_CompartmentData.iloc[i]['txt_font_color']
                    text_anchor_list = df_CompartmentData.iloc[i]['txt_anchor']
                if len(font_color) == 4:
                    text_line_color_str =  '#%02x%02x%02x%02x' % (int(font_color[0]),int(font_color[1]),int(font_color[2]),int(font_color[3]))
                elif len(font_color) == 3:
                    text_line_color_str =  '#%02x%02x%02x' % (int(font_color[0]),int(font_color[1]),int(font_color[2]))
                text_line_width = float(df_CompartmentData.iloc[i]['txt_line_width'])
                text_font_size = float(df_CompartmentData.iloc[i]['txt_font_size'])
                [text_anchor, text_vanchor] = text_anchor_list

                color = rInfo.createColorDefinition()
                color.setId("comp_fill_color" + "_" + comp_id)
                color.setColorValue(fill_color_str)

                color = rInfo.createColorDefinition()
                color.setId("comp_border_color" + "_" + comp_id)
                color.setColorValue(border_color_str)

                # add a list of styles 
                style = rInfo.createStyle("compStyle" + "_" + comp_id)
                style.getGroup().setFillColor("comp_fill_color" + "_" + comp_id)
                style.getGroup().setStroke("comp_border_color" + "_" + comp_id)
                style.getGroup().setStrokeWidth(comp_border_width)
                style.addType("COMPARTMENTGLYPH")
                style.addId(compG_id)
                rectangle = style.getGroup().createRectangle()
                rectangle.setCoordinatesAndSize(libsbml.RelAbsVector(0,0),libsbml.RelAbsVector(0,0),
                libsbml.RelAbsVector(0,0),libsbml.RelAbsVector(0,100),libsbml.RelAbsVector(0,100))
                try:
                    rectangle.setRadiusX(libsbml.RelAbsVector(0,comp_shapeInfo[0][0]))
                    rectangle.setRadiusY(libsbml.RelAbsVector(0,comp_shapeInfo[0][0]))
                except:
                    pass

                style = rInfo.createStyle("textStyle" + "_" + comp_id)
                style.getGroup().setStroke("text_line_color" + "_" + comp_id)
                style.getGroup().setStrokeWidth(text_line_width)
                style.getGroup().setFontSize(libsbml.RelAbsVector(text_font_size,0))
                style.getGroup().setTextAnchor(text_anchor)
                style.getGroup().setVTextAnchor(text_vanchor)
                style.addType("TEXTGLYPH")
                style.addId(textG_id)
        else:
            comp_id= "_compartment_default_"
            compG_id = "CompG_" + comp_id
            comp_border_width = 2.
            #set default compartment with white color
            fill_color_str = '#ffffffff'
            border_color_str = '#ffffffff'

            color = rInfo.createColorDefinition()
            color.setId("comp_fill_color")
            color.setColorValue(fill_color_str)

            color = rInfo.createColorDefinition()
            color.setId("comp_border_color")
            color.setColorValue(border_color_str)

            # add a list of styles 
            style = rInfo.createStyle("compStyle")
            style.getGroup().setFillColor("comp_fill_color")
            style.getGroup().setStroke("comp_border_color")
            style.getGroup().setStrokeWidth(comp_border_width)
            style.addType("COMPARTMENTGLYPH")
            style.addId(compG_id)
            rectangle = style.getGroup().createRectangle()
            rectangle.setCoordinatesAndSize(libsbml.RelAbsVector(0,0),libsbml.RelAbsVector(0,0),
            libsbml.RelAbsVector(0,0),libsbml.RelAbsVector(0,100),libsbml.RelAbsVector(0,100))


        for i in range(numNodes):
            gradient_type = ''
            spec_id = df_NodeData.iloc[i]['id'] 
            spec_index = df_NodeData.iloc[i]['idx'] 
            specG_id = "SpecG_"  + spec_id + '_idx_' + str(spec_index)
            spec_shapeIdx = int(df_NodeData.iloc[i]['shape_idx'])
            spec_shapeType = df_NodeData.iloc[i]['shape_type']
            textG_id = "TextG_" + spec_id + '_idx_' + str(spec_index)

            try:
                spec_dash = list(df_NodeData.iloc[i]['spec_dash'][1:-1].split(","))
            except:
                spec_dash = list(df_NodeData.iloc[i]['spec_dash'])

            try:
                spec_shapeInfo_list_pre = list(df_NodeData.iloc[i]['shape_info'][1:-1].split(","))
            except:
                spec_shapeInfo_list_pre = df_NodeData.iloc[i]['shape_info']
            if spec_shapeInfo_list_pre == ['']:
                spec_shapeInfo = []
            elif len(spec_shapeInfo_list_pre) == 0:
                spec_shapeInfo = []
            else:
                spec_shapeInfo_pre = []
                spec_shapeInfo = []
                if type(spec_shapeInfo_list_pre[0]) is str:
                    for ii in range(len(spec_shapeInfo_list_pre)):
                        temp = spec_shapeInfo_list_pre[ii]
                        if temp.find('[') != -1:
                            temp_update = temp.replace('[', '')
                        elif temp.find(']') != -1:
                            temp_update = temp.replace(']', '')
                        spec_shapeInfo_pre.append(float(temp_update))
                    for ii in range(0,len(spec_shapeInfo_pre),2):
                        spec_shapeInfo.append([spec_shapeInfo_pre[ii], spec_shapeInfo_pre[ii+1]])
                else:
                    spec_shapeInfo = spec_shapeInfo_list_pre

            try: 
                try:
                    spec_fill_color   = list(df_NodeData.iloc[i]['fill_color'][1:-1].split(","))
                    spec_border_color = list(df_NodeData.iloc[i]['border_color'][1:-1].split(","))
                except:
                    spec_fill_color   = df_NodeData.iloc[i]['fill_color']
                    spec_border_color = df_NodeData.iloc[i]['border_color']
                if len(spec_fill_color) == 4:
                    spec_fill_color_str   = '#%02x%02x%02x%02x' % (int(spec_fill_color[0]),int(spec_fill_color[1]),int(spec_fill_color[2]),int(spec_fill_color[3]))
                elif len(spec_fill_color) == 3 and type(spec_fill_color[0]) != str:
                    spec_fill_color_str   = '#%02x%02x%02x' % (int(spec_fill_color[0]),int(spec_fill_color[1]),int(spec_fill_color[2]))
                elif len(spec_fill_color) and type(spec_fill_color[0]) == str:
                    gradient_type = spec_fill_color[0]
                    gradient_info = spec_fill_color[1]
                    stop_info = spec_fill_color[2]  

                if len(spec_border_color) == 4:    
                    spec_border_color_str = '#%02x%02x%02x%02x' % (int(spec_border_color[0]),int(spec_border_color[1]),int(spec_border_color[2]),int(spec_border_color[3]))
                elif len(spec_border_color) == 3:
                    spec_border_color_str = '#%02x%02x%02x' % (int(spec_border_color[0]),int(spec_border_color[1]),int(spec_border_color[2]))   

                spec_border_width = float(df_NodeData.iloc[i]['border_width'])
                if spec_border_width <= 0:
                    spec_border_color_str = '#ffffffff'

                try:
                    font_color = list(df_NodeData.iloc[i]['txt_font_color'][1:-1].split(","))
                    text_anchor_list = list(df_NodeData.iloc[i]['txt_anchor'][1:-1].split(","))
                except:
                    font_color = df_NodeData.iloc[i]['txt_font_color']
                    text_anchor_list = df_NodeData.iloc[i]['txt_anchor']
                if len(font_color) == 4:
                    text_line_color_str =  '#%02x%02x%02x%02x' % (int(font_color[0]),int(font_color[1]),int(font_color[2]),int(font_color[3]))
                elif len(font_color) == 3:
                    text_line_color_str =  '#%02x%02x%02x' % (int(font_color[0]),int(font_color[1]),int(font_color[2]))
                text_line_width = float(df_NodeData.iloc[i]['txt_line_width'])
                text_font_size = float(df_NodeData.iloc[i]['txt_font_size'])
                [text_anchor, text_vanchor] = text_anchor_list
                text_font_family = (df_NodeData.iloc[i]['txt_font_family'])
            except: #text-only: set default species/node with white color
                spec_fill_color_str = '#ffffffff'
                spec_border_color_str = '#ffffffff'
                spec_border_width = 2.
                spec_dash = []
                text_line_color_str = '#000000ff'
                text_line_width = 1.
                text_font_size = 12.
                text_font_family = ""
                [text_anchor, text_vanchor] = ['middle', 'middle']

            if gradient_type == '':
                color = rInfo.createColorDefinition()
                color.setId("spec_fill_color" + "_" + spec_id)
                color.setColorValue(spec_fill_color_str)

                color = rInfo.createColorDefinition()
                color.setId("spec_border_color" + "_" + spec_id)
                color.setColorValue(spec_border_color_str)

                color = rInfo.createColorDefinition()
                color.setId("text_line_color" + "_" + spec_id)
                color.setColorValue(text_line_color_str)

                style = rInfo.createStyle("specStyle" + "_" + spec_id)
                style.getGroup().setFillColor("spec_fill_color" + "_" + spec_id)
                style.getGroup().setStroke("spec_border_color" + "_" + spec_id)
                style.getGroup().setStrokeWidth(spec_border_width)
                style.addType("SPECIESGLYPH")
                #style.addId(spec_id)
                style.addId(specG_id)
            elif gradient_type == 'linearGradient':
                color = rInfo.createColorDefinition()
                color.setId("spec_border_color" + "_" + spec_id)
                color.setColorValue(spec_border_color_str)

                color = rInfo.createColorDefinition()
                color.setId("text_line_color" + "_" + spec_id)
                color.setColorValue(text_line_color_str)

                gradient = rInfo.createLinearGradientDefinition()
                gradient.setId("spec_fill_gradient" + "_" + spec_id)
                gradient.setPoint1(libsbml.RelAbsVector(0, gradient_info[0][0]), libsbml.RelAbsVector(0, gradient_info[0][1]))
                gradient.setPoint2(libsbml.RelAbsVector(0, gradient_info[1][0]), libsbml.RelAbsVector(0, gradient_info[1][1]))

                for ii in range(len(stop_info)):
                    color = rInfo.createColorDefinition()
                    stop_color_id = "spec_fill_stop_color" + "_" + spec_id + '_' + str(ii)
                    color.setId(stop_color_id)
                    stop_color = stop_info[ii][1]
                    spec_fill_stop_color_str = '#%02x%02x%02x%02x' % (int(stop_color[0]),int(stop_color[1]),int(stop_color[2]),int(stop_color[3]))
                    color.setColorValue(spec_fill_stop_color_str)

                    stop = gradient.createGradientStop()
                    stop.setOffset(libsbml.RelAbsVector(0, stop_info[ii][0]))
                    stop.setStopColor(stop_color_id)

                style = rInfo.createStyle("specStyle" + "_" + spec_id)
                style.getGroup().setFillColor("spec_fill_gradient" + "_" + spec_id)
                style.getGroup().setStroke("spec_border_color" + "_" + spec_id)
                style.getGroup().setStrokeWidth(spec_border_width)
                style.addType("SPECIESGLYPH")
                #style.addId(spec_id)
                style.addId(specG_id)
            elif gradient_type == 'radialGradient':
                color = rInfo.createColorDefinition()
                color.setId("spec_border_color" + "_" + spec_id)
                color.setColorValue(spec_border_color_str)

                color = rInfo.createColorDefinition()
                color.setId("text_line_color" + "_" + spec_id)
                color.setColorValue(text_line_color_str)

                gradient = rInfo.createRadialGradientDefinition()
                gradient.setId("spec_fill_gradient" + "_" + spec_id)
                gradient.setCenter(libsbml.RelAbsVector(0, gradient_info[0][0]), libsbml.RelAbsVector(0, gradient_info[0][1]))
                gradient.setRadius(libsbml.RelAbsVector(0, gradient_info[1][0]))

                for ii in range(len(stop_info)):
                    color = rInfo.createColorDefinition()
                    stop_color_id = "spec_fill_stop_color" + "_" + spec_id + '_' + str(ii)
                    color.setId(stop_color_id)
                    stop_color = stop_info[ii][1]
                    spec_fill_stop_color_str = '#%02x%02x%02x%02x' % (int(stop_color[0]),int(stop_color[1]),int(stop_color[2]),int(stop_color[3]))
                    color.setColorValue(spec_fill_stop_color_str)

                    stop = gradient.createGradientStop()
                    stop.setOffset(libsbml.RelAbsVector(0, stop_info[ii][0]))
                    stop.setStopColor(stop_color_id)

                style = rInfo.createStyle("specStyle" + "_" + spec_id)
                style.getGroup().setFillColor("spec_fill_gradient" + "_" + spec_id)
                style.getGroup().setStroke("spec_border_color" + "_" + spec_id)
                style.getGroup().setStrokeWidth(spec_border_width)
                style.addType("SPECIESGLYPH")
                #style.addId(spec_id)
                style.addId(specG_id)


            if spec_shapeIdx == 1 or spec_shapeType == 'rectangle': #rectangle
                rectangle = style.getGroup().createRectangle()
                rectangle.setCoordinatesAndSize(libsbml.RelAbsVector(0,0),libsbml.RelAbsVector(0,0),
                libsbml.RelAbsVector(0,0),libsbml.RelAbsVector(0,100.),libsbml.RelAbsVector(0,100.))
                try:
                    rectangle.setRadiusX(libsbml.RelAbsVector(0,spec_shapeInfo[0][0]))
                    rectangle.setRadiusY(libsbml.RelAbsVector(0,spec_shapeInfo[0][0]))
                except:
                    pass


            elif spec_shapeType == 'polygon':            
                polygon = style.getGroup().createPolygon()
                for pts in range(len(spec_shapeInfo)):
                    renderPoint = polygon.createPoint()
                    renderPoint.setCoordinates(libsbml.RelAbsVector(0,spec_shapeInfo[pts][0]),
                    libsbml.RelAbsVector(0,spec_shapeInfo[pts][1]))

            elif spec_shapeIdx == 2 or spec_shapeType == 'ellipse':
                ellipse = style.getGroup().createEllipse()
                ellipse.setCenter2D(libsbml.RelAbsVector(0, 50.), libsbml.RelAbsVector(0, 50.))
                ellipse.setRadii(libsbml.RelAbsVector(0, 50.),libsbml.RelAbsVector(0, 50.))
                # try: #from dataFrame
                #     ellipse = style.getGroup().createEllipse()
                #     ellipse.setCenter2D(libsbml.RelAbsVector(0, spec_shapeInfo[0][0][0]), 
                #     libsbml.RelAbsVector(0, spec_shapeInfo[0][0][1]))
                #     ellipse.setRadii(libsbml.RelAbsVector(0, spec_shapeInfo[0][1][0]),
                #     libsbml.RelAbsVector(0, spec_shapeInfo[0][1][1]))
                #     #percentage of width
                # except: #from excel sheet
                #     ellipse = style.getGroup().createEllipse()
                #     ellipse.setCenter2D(libsbml.RelAbsVector(0, spec_shapeInfo[0][0]), 
                #     libsbml.RelAbsVector(0, spec_shapeInfo[0][1]))
                #     ellipse.setRadii(libsbml.RelAbsVector(0, spec_shapeInfo[1][0]),
                #     libsbml.RelAbsVector(0, spec_shapeInfo[1][1]))

            if len(spec_dash) != 0:
                for pt in range(len(spec_dash)):
                    try:
                        style.getGroup().addDash(int(spec_dash[pt]))
                    except:
                        pass
            
            style = rInfo.createStyle("textStyle" + "_" + spec_id)
            style.getGroup().setStroke("text_line_color" + "_" + spec_id)
            style.getGroup().setStrokeWidth(text_line_width)
            style.getGroup().setFontSize(libsbml.RelAbsVector(text_font_size,0))
            style.getGroup().setTextAnchor(text_anchor)
            style.getGroup().setVTextAnchor(text_vanchor)
            try:
                style.getGroup().setFontFamily(text_font_family)
            except:
                pass
            style.addType("TEXTGLYPH")
            style.addId(textG_id)

        if numReactions != 0:
            for i in range(numReactions):
                rxn_id = df_ReactionData.iloc[i]['id']
                reactionG_id = "ReactionG_" + rxn_id
                try:
                    rct_list = list(df_ReactionData.iloc[i]['sources'][1:-1].split(","))
                    prd_list = list(df_ReactionData.iloc[i]['targets'][1:-1].split(","))
                    mod_list = list(df_ReactionData.iloc[i]['modifiers'][1:-1].split(","))
                except:
                    rct_list = df_ReactionData.iloc[i]['sources']
                    prd_list = df_ReactionData.iloc[i]['targets']
                    mod_list = df_ReactionData.iloc[i]['modifiers']
               
                rct_num = len(rct_list)
                prd_num = len(prd_list)
                mod_num = len(mod_list)

                try:
                    reaction_fill_color = list(df_ReactionData.iloc[i]['fill_color'][1:-1].split(","))
                except:
                    reaction_fill_color = df_ReactionData.iloc[i]['fill_color']
                try:
                    reaction_stroke_color = list(df_ReactionData.iloc[i]['stroke_color'][1:-1].split(","))
                except:
                    reaction_stroke_color = df_ReactionData.iloc[i]['stroke_color']

                rxn_shapeType = df_ReactionData.iloc[i]['shape_type']
                
                try:
                    rxn_shapeInfo_list_pre = list(df_ReactionData.iloc[i]['shape_info'][1:-1].split(","))
                except:
                    rxn_shapeInfo_list_pre = df_ReactionData.iloc[i]['shape_info']
                #from excel sheet
                if rxn_shapeInfo_list_pre == ['']:
                    rxn_shapeInfo = []
                elif len(rxn_shapeInfo_list_pre) == 0:
                    rxn_shapeInfo = []
                else:
                    rxn_shapeInfo_pre = []
                    rxn_shapeInfo = []
                    if type(rxn_shapeInfo_list_pre[0]) is str:
                        for ii in range(len(rxn_shapeInfo_list_pre)):
                            temp = rxn_shapeInfo_list_pre[ii]
                            if temp.find('[') != -1:
                                temp_update = temp.replace('[', '')
                            elif temp.find(']') != -1:
                                temp_update = temp.replace(']', '')
                            rxn_shapeInfo_pre.append(float(temp_update))
                        for ii in range(0,len(rxn_shapeInfo_pre),2):
                            rxn_shapeInfo.append([rxn_shapeInfo_pre[ii], rxn_shapeInfo_pre[ii+1]])
                    else:
                        rxn_shapeInfo = rxn_shapeInfo_list_pre
                
                if len(reaction_fill_color) == 4:
                    reaction_fill_color_str = '#%02x%02x%02x%02x' % (int(reaction_fill_color[0]),int(reaction_fill_color[1]),int(reaction_fill_color[2]),int(reaction_fill_color[3]))           
                elif len(reaction_fill_color) == 3:
                    reaction_fill_color_str = '#%02x%02x%02x' % (int(reaction_fill_color[0]),int(reaction_fill_color[1]),int(reaction_fill_color[2]))           
                
                if len(reaction_stroke_color) == 4:
                    reaction_stroke_color_str = '#%02x%02x%02x%02x' % (int(reaction_stroke_color[0]),int(reaction_stroke_color[1]),int(reaction_stroke_color[2]),int(reaction_stroke_color[3]))           
                elif len(reaction_stroke_color) == 3:
                    reaction_stroke_color_str = '#%02x%02x%02x' % (int(reaction_stroke_color[0]),int(reaction_stroke_color[1]),int(reaction_stroke_color[2]))           
                
                reaction_line_thickness = float(df_ReactionData.iloc[i]['line_thickness'])
                # try:
                #     reaction_arrow_head_size = list(df_ReactionData.iloc[i]['arrow_head_size'][1:-1].split(","))
                # except:
                #     reaction_arrow_head_size = df_ReactionData.iloc[i]['arrow_head_size']

                try:
                    reaction_dash = list(df_ReactionData.iloc[i]['rxn_dash'][1:-1].split(","))
                except:
                    reaction_dash = list(df_ReactionData.iloc[i]['rxn_dash'])

                color = rInfo.createColorDefinition()
                color.setId("reaction_fill_color" + "_" + rxn_id)
                color.setColorValue(reaction_fill_color_str)

                color = rInfo.createColorDefinition()
                color.setId("reaction_stroke_color" + "_" + rxn_id)
                color.setColorValue(reaction_stroke_color_str)

                style = rInfo.createStyle("reactionStyle" + "_" + rxn_id)
                style.getGroup().setStroke("reaction_stroke_color" + "_" + rxn_id)
                style.getGroup().setFill("reaction_fill_color" + "_" + rxn_id)
                style.getGroup().setStrokeWidth(reaction_line_thickness)

                if rxn_shapeType == 'rectangle': #rectangle
                    rectangle = style.getGroup().createRectangle()
                    rectangle.setCoordinatesAndSize(libsbml.RelAbsVector(0,0),libsbml.RelAbsVector(0,0),
                    libsbml.RelAbsVector(0,0),libsbml.RelAbsVector(0,100),libsbml.RelAbsVector(0,100))

                elif rxn_shapeType == 'polygon':            
                    polygon = style.getGroup().createPolygon()
                    for pts in range(len(rxn_shapeInfo)):
                        renderPoint = polygon.createPoint()
                        renderPoint.setCoordinates(libsbml.RelAbsVector(0,rxn_shapeInfo[pts][0]),
                        libsbml.RelAbsVector(0,rxn_shapeInfo[pts][1]))

                elif rxn_shapeType == 'ellipse':
                    ellipse = style.getGroup().createEllipse()
                    ellipse.setCenter2D(libsbml.RelAbsVector(0, 50.), libsbml.RelAbsVector(0, 50.))
                    ellipse.setRadii(libsbml.RelAbsVector(0, 50.),libsbml.RelAbsVector(0, 50.))
                
                if len(reaction_dash) != 0:
                    for pt in range(len(reaction_dash)):
                        try:
                            style.getGroup().addDash(int(reaction_dash[pt]))
                        except:
                            pass
                style.addType("REACTIONGLYPH")
                #style.addId(rxn_id)
                style.addId(reactionG_id)

                try:
                    src_lineending = list(df_ReactionData.iloc[i]['sources_lineending'][1:-1].split(","))
                    dst_lineending = list(df_ReactionData.iloc[i]['targets_lineending'][1:-1].split(","))
                    mod_lineending = list(df_ReactionData.iloc[i]['modifiers_lineending'][1:-1].split(","))
                except:
                    src_lineending = list(df_ReactionData.iloc[i]['sources_lineending'])
                    dst_lineending = list(df_ReactionData.iloc[i]['targets_lineending'])
                    mod_lineending = list(df_ReactionData.iloc[i]['modifiers_lineending'])

                try:
                    src_dash = list(df_ReactionData.iloc[i]['src_dash'][1:-1].split(","))
                    dst_dash = list(df_ReactionData.iloc[i]['tgt_dash'][1:-1].split(","))
                except:
                    src_dash = list(df_ReactionData.iloc[i]['src_dash'])
                    dst_dash = list(df_ReactionData.iloc[i]['tgt_dash'])

                for j in range(rct_num):
                    specsRefG_id = "SpecRefG_" + rxn_id + "_rct" + str(j)
                    style = rInfo.createStyle("specRefGlyphStyle" + rxn_id + "_rct" + str(j))
                    style.getGroup().setEndHead(src_lineending[0])
                    style.getGroup().setStroke("reaction_stroke_color" + "_" + rxn_id)
                    style.getGroup().setFill("reaction_fill_color" + "_" + rxn_id)
                    # lineEnding_id = src_lineending[j]
                    # style.getGroup().setEndHead(lineEnding_id)
                    # style.getGroup().setStroke("lineEnding_border_color" + "_" + lineEnding_id)
                    # style.getGroup().setFill("lineEnding_fill_color" + "_" + lineEnding_id)
                    style.getGroup().setStrokeWidth(reaction_line_thickness)
                    if len(src_dash) != 0:
                        for pt in range(len(src_dash)):
                            try:
                                style.getGroup().addDash(int(src_dash[pt]))
                            except:
                                pass
                    else:
                        if len(reaction_dash) != 0:
                            for pt in range(len(reaction_dash)):
                                try:
                                    style.getGroup().addDash(int(reaction_dash[pt]))
                                except:
                                    pass
                    style.addType('SPECIESREFERENCEGLYPH')
                    style.addId(specsRefG_id)
                for j in range(prd_num):
                    specsRefG_id = "SpecRefG_" + rxn_id + "_prd" + str(j)
                    style = rInfo.createStyle("specRefGlyphStyle" + rxn_id + "_prd" + str(j))
                    style.getGroup().setEndHead(dst_lineending[0])
                    style.getGroup().setStroke("reaction_stroke_color" + "_" + rxn_id)
                    style.getGroup().setFill("reaction_fill_color" + "_" + rxn_id)
                    # lineEnding_id = dst_lineending[j]
                    # style.getGroup().setEndHead(lineEnding_id)
                    # style.getGroup().setStroke("lineEnding_border_color" + "_" + lineEnding_id)
                    # style.getGroup().setFill("lineEnding_fill_color" + "_" + lineEnding_id)
                    style.getGroup().setStrokeWidth(reaction_line_thickness)
                    if len(dst_dash) != 0:
                        for pt in range(len(dst_dash)):
                            try:
                                style.getGroup().addDash(int(dst_dash[pt]))
                            except:
                                pass
                    else:
                        if len(reaction_dash) != 0:
                            for pt in range(len(reaction_dash)):
                                try:
                                    style.getGroup().addDash(int(reaction_dash[pt]))
                                except:
                                    pass
                    style.addType('SPECIESREFERENCEGLYPH')
                    style.addId(specsRefG_id)
                for j in range(mod_num):
                    specsRefG_id = "SpecRefG_" + rxn_id + "_mod" + str(j)
                    style = rInfo.createStyle("specRefGlyphStyle" + rxn_id + "_mod" + str(j))
                    style.getGroup().setEndHead(mod_lineending[0])
                    style.getGroup().setStroke("reaction_stroke_color" + "_" + rxn_id)
                    style.getGroup().setFill("reaction_fill_color" + "_" + rxn_id)
                    # lineEnding_id = mod_lineending[j]
                    # style.getGroup().setEndHead(lineEnding_id)
                    # style.getGroup().setStroke("lineEnding_border_color" + "_" + lineEnding_id)
                    # style.getGroup().setFill("lineEnding_fill_color" + "_" + lineEnding_id)
                    style.getGroup().setStrokeWidth(reaction_line_thickness)
                    style.addType('SPECIESREFERENCEGLYPH')
                    style.addId(specsRefG_id)

        if numArbitraryTexts != 0:
            for i in range(numArbitraryTexts):
                text_content = df_TextData.iloc[i]['txt_content'] 
                textG_id = "TextG_" + txt_content + '_idx_' + str(i) 

                try: 
                    try:
                        font_color = list(df_TextData.iloc[i]['txt_font_color'][1:-1].split(","))
                        text_anchor_list = list(df_TextData.iloc[i]['txt_anchor'][1:-1].split(","))
                    except:
                        font_color = df_TextData.iloc[i]['txt_font_color']
                        text_anchor_list = df_TextData.iloc[i]['txt_anchor']

                    if len(font_color) == 4:
                        text_line_color_str =  '#%02x%02x%02x%02x' % (int(font_color[0]),int(font_color[1]),int(font_color[2]),int(font_color[3]))
                    elif len(font_color) == 3:
                        text_line_color_str =  '#%02x%02x%02x' % (int(font_color[0]),int(font_color[1]),int(font_color[2]))
                    text_line_width = float(df_TextData.iloc[i]['txt_line_width'])
                    text_font_size = float(df_TextData.iloc[i]['txt_font_size'])
                    [text_anchor, text_vanchor] = text_anchor_list
                except: #text-only: set default species/node with white color
                    text_line_color_str = '#000000ff'
                    text_line_width = 1.
                    text_font_size = 12.
                    [text_anchor, text_vanchor] = ['middle', 'middle']

                color = rInfo.createColorDefinition()
                color.setId("text_line_color" + "_" + textG_id)
                color.setColorValue(text_line_color_str)
                
                style = rInfo.createStyle("textStyle" + "_" + textG_id)
                style.getGroup().setStroke("text_line_color" + "_" + textG_id)
                style.getGroup().setStrokeWidth(text_line_width)
                style.getGroup().setFontSize(libsbml.RelAbsVector(text_font_size,0))
                style.getGroup().setTextAnchor(text_anchor)
                style.getGroup().setVTextAnchor(text_vanchor)
                style.addType("TEXTGLYPH")
                style.addId(textG_id)

        if numReactionTexts != 0:
            for i in range(numReactionTexts):
                rxn_id = df_ReactionTextData.iloc[i]['rxn_id']
                txt_id = df_ReactionTextData.iloc[i]['txt_id']
                textG_id = "TextG_" + rxn_id + '_idx_' + str(txt_id)
                try: 
                    try:
                        font_color = list(df_ReactionTextData.iloc[i]['txt_font_color'][1:-1].split(","))
                        text_anchor_list = list(df_ReactionTextData.iloc[i]['txt_anchor'][1:-1].split(","))
                    except:
                        font_color = df_ReactionTextData.iloc[i]['txt_font_color']
                        text_anchor_list = df_ReactionTextData.iloc[i]['txt_anchor']

                    if len(font_color) == 4:
                        text_line_color_str =  '#%02x%02x%02x%02x' % (int(font_color[0]),int(font_color[1]),int(font_color[2]),int(font_color[3]))
                    elif len(font_color) == 3:
                        text_line_color_str =  '#%02x%02x%02x' % (int(font_color[0]),int(font_color[1]),int(font_color[2]))
                    text_line_width = float(df_ReactionTextData.iloc[i]['txt_line_width'])
                    text_font_size = float(df_ReactionTextData.iloc[i]['txt_font_size'])
                    [text_anchor, text_vanchor] = text_anchor_list
                except: #text-only: set default species/node with white color
                    text_line_color_str = '#000000ff'
                    text_line_width = 1.
                    text_font_size = 12.
                    [text_anchor, text_vanchor] = ['middle', 'middle']

                color = rInfo.createColorDefinition()
                color.setId("text_line_color" + "_" + textG_id)
                color.setColorValue(text_line_color_str)
                
                style = rInfo.createStyle("textStyle" + "_" + textG_id)
                style.getGroup().setStroke("text_line_color" + "_" + textG_id)
                style.getGroup().setStrokeWidth(text_line_width)
                style.getGroup().setFontSize(libsbml.RelAbsVector(text_font_size,0))
                style.getGroup().setTextAnchor(text_anchor)
                style.getGroup().setVTextAnchor(text_vanchor)
                style.addType("TEXTGLYPH")
                style.addId(textG_id)


        #arbitrary shape
        if numArbitraryShapes != 0:
            for i in range(numArbitraryShapes):
                gen_shape_name = str(df_ShapeData.iloc[i]['shape_name'])   
                gen_shape_type = df_ShapeData.iloc[i]['shape_type']
                genG_id = gen_shape_name

                try:
                    gen_shapeInfo_list_pre = list(df_ShapeData.iloc[i]['shape_info'][1:-1].split(","))
                except:
                    gen_shapeInfo_list_pre = df_ShapeData.iloc[i]['shape_info']
                if gen_shapeInfo_list_pre == ['']:
                    gen_shapeInfo = []
                elif len(gen_shapeInfo_list_pre) == 0:
                    gen_shapeInfo = []
                else:
                    gen_shapeInfo_pre = []
                    gen_shapeInfo = []
                    if type(gen_shapeInfo_list_pre[0]) is str:
                        for ii in range(len(gen_shapeInfo_list_pre)):
                            temp = gen_shapeInfo_list_pre[ii]
                            if temp.find('[') != -1:
                                temp_update = temp.replace('[', '')
                            elif temp.find(']') != -1:
                                temp_update = temp.replace(']', '')
                            gen_shapeInfo_pre.append(float(temp_update))
                        for ii in range(0,len(gen_shapeInfo_pre),2):
                            gen_shapeInfo.append([gen_shapeInfo_pre[ii], gen_shapeInfo_pre[ii+1]])
                    else:
                        gen_shapeInfo = gen_shapeInfo_list_pre

                try: 
                    try:
                        gen_fill_color   = list(df_ShapeData.iloc[i]['fill_color'][1:-1].split(","))
                        gen_border_color = list(df_ShapeData.iloc[i]['border_color'][1:-1].split(","))
                    except:
                        gen_fill_color   = df_ShapeData.iloc[i]['fill_color']
                        gen_border_color = df_ShapeData.iloc[i]['border_color']
                    if len(gen_fill_color) == 4:
                        gen_fill_color_str   = '#%02x%02x%02x%02x' % (int(gen_fill_color[0]),
                        int(gen_fill_color[1]),int(gen_fill_color[2]),int(gen_fill_color[3]))
                    elif len(gen_fill_color) == 3:
                        gen_fill_color_str   = '#%02x%02x%02x' % (int(gen_fill_color[0]),
                        int(gen_fill_color[1]),int(gen_fill_color[2]))
                
                    if len(gen_border_color) == 4:    
                        gen_border_color_str = '#%02x%02x%02x%02x' % (int(gen_border_color[0]),
                        int(gen_border_color[1]),int(gen_border_color[2]),int(gen_border_color[3]))
                    elif len(gen_border_color) == 3:
                        gen_border_color_str = '#%02x%02x%02x' % (int(gen_border_color[0]),
                        int(gen_border_color[1]),int(gen_border_color[2]))   

                    gen_border_width = float(df_ShapeData.iloc[i]['border_width'])

                # print(gen_fill_color_str)
                # print(gen_border_color_str)
                # print(gen_border_width)

                except: #set default shape border color as black, fill color as white
                    gen_fill_color_str = '#ffffffff'
                    gen_border_color_str = '#000000ff'
                    gen_border_width = 2.


                color = rInfo.createColorDefinition()
                color.setId("gen_fill_color" + "_" + gen_shape_name)
                color.setColorValue(gen_fill_color_str)

                color = rInfo.createColorDefinition()
                color.setId("gen_border_color" + "_" + gen_shape_name)
                color.setColorValue(gen_border_color_str)


                style = rInfo.createStyle("genStyle" + "_" + gen_shape_name)
                style.getGroup().setFillColor("gen_fill_color" + "_" + gen_shape_name)
                style.getGroup().setStroke("gen_border_color" + "_" + gen_shape_name)
                style.getGroup().setStrokeWidth(gen_border_width)
                style.addType("GENERALGLYPH")
                #style.addId(gen_shape_name)
                style.addId(genG_id)

                if gen_shape_type == 'rectangle': #rectangle
                    rectangle = style.getGroup().createRectangle()
                    rectangle.setCoordinatesAndSize(libsbml.RelAbsVector(0,0),libsbml.RelAbsVector(0,0),
                    libsbml.RelAbsVector(0,0),libsbml.RelAbsVector(0,100),libsbml.RelAbsVector(0,100))

                elif gen_shape_type == 'polygon':            
                    polygon = style.getGroup().createPolygon()
                    for pts in range(len(gen_shapeInfo)):
                        renderPoint = polygon.createPoint()
                        renderPoint.setCoordinates(libsbml.RelAbsVector(0,gen_shapeInfo[pts][0]),
                        libsbml.RelAbsVector(0,gen_shapeInfo[pts][1]))

                elif gen_shape_type == 'ellipse':
                    ellipse = style.getGroup().createEllipse()
                    ellipse.setCenter2D(libsbml.RelAbsVector(0, 50.), libsbml.RelAbsVector(0, 50.))
                    ellipse.setRadii(libsbml.RelAbsVector(0, 50.),libsbml.RelAbsVector(0, 50.))

        sbmlStr_layout_render = libsbml.writeSBMLToString(doc) #sbmlStr_layout_render includes both layout and render
    
        return sbmlStr_layout_render
    else:
        raise ValueError('There is no node or arbitrary text or arbitrary shape!')



if __name__ == '__main__':

    DIR = os.path.dirname(os.path.abspath(__file__))
    TEST_FOLDER = os.path.join(DIR, "initiate_excel_files")

#     # df_CompartmentData = pd.read_csv(os.path.join(TEST_FOLDER, 'CompartmentData.csv')) 
#     # df_NodeData = pd.read_csv(os.path.join(TEST_FOLDER, 'NodeData.csv'))
#     # df_ReactionData = pd.read_csv(os.path.join(TEST_FOLDER, 'ReactionData.csv'))

    xls = pd.ExcelFile(os.path.join(TEST_FOLDER, 'output.xlsx'))
    df_CompartmentData = pd.read_excel(xls, 'CompartmentData')
    df_NodeData = pd.read_excel(xls, 'NodeData')
    df_ReactionData = pd.read_excel(xls, 'ReactionData')
    df_ArbitraryTextData = pd.read_excel(xls, "ArbitraryTextData")
    df_ArbitraryShapeData = pd.read_excel(xls, "ArbitraryShapeData")

    df = (df_CompartmentData, df_NodeData, df_ReactionData, df_ArbitraryTextData, df_ArbitraryShapeData)

    sbmlStr_layout_render = _DFToSBML(df)

    f = open("output.xml", "w")
    f.write(sbmlStr_layout_render)
    f.close()
        
