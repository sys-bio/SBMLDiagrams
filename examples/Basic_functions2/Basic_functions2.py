
import SBMLDiagrams
import os


dirname = ""
filename = "Jana_WolfGlycolysis-corrected.xml"
with open(os.path.join(dirname, filename), 'r', encoding="utf8") as f:
     sbmlStr = f.read()

la = SBMLDiagrams.load(sbmlStr)

def createCircleNode (la, id):
    #get center and size of the node

    num_alias = la.getNodeAliasNum(id)

    if num_alias == 1:
        # Change the node size and corectly adjust for the new position
        center = la.getNodeCenter(id)
        la.setNodeSize(id, [18, 18])
        la.setNodePosition(id, [center.x-9, center.y-9])

        # get the new position and size
        p = la.getNodePosition(id)    
        size = la.getNodeSize(id)

        # Position the text just outside the node
        q = [p.x + 1.2*size.x, p.y-5]

        la.setNodeTextPosition(id, q)
        la.setNodeShape(id, 'ellipse')
        la.setNodeBorderWidth (id, 0) 
    else:
        for alias in range(num_alias):
            # Change the node size and corectly adjust for the new position
            center = la.getNodeCenter(id, alias = alias)
            la.setNodeSize(id, [18, 18], alias = alias)
            la.setNodePosition(id, [center.x-9, center.y-9], alias = alias)

            # get the new position and size
            p = la.getNodePosition(id, alias = alias)   
            size = la.getNodeSize(id, alias = alias)

            # Position the text just outside the node
            q = [p.x + 1.2*size.x, p.y-5]

            la.setNodeTextPosition(id, q, alias = alias)
            la.setNodeShape(id, 'ellipse', alias = alias)
            la.setNodeBorderWidth (id, 0, alias = alias) 

sp = la.getNodeIdList()
for s in sp:
    createCircleNode(la, s)

la.draw(output_fileName = 'output.png')
# sbmlStr_layout_render = la.export()
# f = open("output.xml", "w")
# f.write(sbmlStr_layout_render)
# f.close()
