#The gallery "gallery.json" color styles are designed by Sejal Akerkar <sejal.akerkar@outlook.com>
import SBMLDiagrams
import os

colors = SBMLDiagrams.loadColorStyle("gallery.json")

DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FOLDER = os.path.join(DIR, "gallery")

filename = "Jana_WolfGlycolysis-corrected.xml"
f = open(os.path.join(TEST_FOLDER, filename), 'r')
sbmlStr = f.read()
f.close()
# # sbmlStr = r.getSBML()
df = SBMLDiagrams.load(sbmlStr)

df.setColorStyle("default")
df.draw(output_fileName="gallery/default.png")

df.setColorStyle(colors["red ombre"])
df.draw(output_fileName="gallery/red_obmre.png")

df.setColorStyle(colors["blue ombre"])
df.draw(output_fileName="gallery/blue_obmre.png")

df.setColorStyle(colors["green ombre"])
df.draw(output_fileName="gallery/green_obmre.png")

df.setColorStyle(colors["grey ombre"])
df.draw(output_fileName="gallery/grey_obmre.png")

df.setColorStyle(colors["orange blue"])
df.draw(output_fileName="gallery/orange_blue.png")

df.setColorStyle(colors["purple yellow"])
df.draw(output_fileName="gallery/purple_yellow.png")

df.setColorStyle(colors["green red"])
df.draw(output_fileName="gallery/green_red.png")

df.setColorStyle(colors["power"])
df.draw(output_fileName="gallery/power.png")

df.setColorStyle(colors["vibrance"])
df.draw(output_fileName="gallery/vibrance.png")

df.setColorStyle(colors["calm"])
df.draw(output_fileName="gallery/calm.png")

df.setColorStyle(colors["sunset"])
df.draw(output_fileName="gallery/sunset.png")

df.setColorStyle(colors["electric"])
df.draw(output_fileName="gallery/electric.png")

df.setColorStyle(colors["midnight"])
df.draw(output_fileName="gallery/midnight.png")

df.setColorStyle(colors["purple ombre"])
df.draw(output_fileName="gallery/purple_obmre.png")

df.setColorStyle(colors["orange ombre"])
df.draw(output_fileName="gallery/orange_obmre.png")

df.setColorStyle(colors["ocean"])
df.draw(output_fileName="gallery/ocean.png")

df.setColorStyle(colors["forest"])
df.draw(output_fileName="gallery/forest.png")

df.setColorStyle(colors["brown ombre"])
df.draw(output_fileName="gallery/brown_obmre.png")

df.setColorStyle(colors["warm tone"])
df.draw(output_fileName="gallery/warm_tone.png")

df.setColorStyle(colors["cool tone"])
df.draw(output_fileName="gallery/cool_tone.png")