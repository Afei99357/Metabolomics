### put two png files together by top and bottom, the grids of the two png files should be the same
from PIL import Image
import os
from PIL import Image, ImageDraw, ImageFont

# read the 6 png files
fig_1 = Image.open("/Users/ericliao/Desktop/dissertation/metabolomic_signature/2_hours.png", "r",)
fig_2 = Image.open("/Users/ericliao/Desktop/dissertation/metabolomic_signature/4_hours.png", "r",)
fig_3 = Image.open("/Users/ericliao/Desktop/dissertation/metabolomic_signature/8_hours.png", "r",)
fig_4 = Image.open("/Users/ericliao/Desktop/dissertation/metabolomic_signature/12_hours.png", "r",)
fig_5 = Image.open("/Users/ericliao/Desktop/dissertation/metabolomic_signature/24_hours.png", "r",)
fig_6 = Image.open("/Users/ericliao/Desktop/dissertation/metabolomic_signature/48_hours.png", "r",)

## adding text "A" to the top of the fig_1
# get a font
fnt = ImageFont.truetype("/Library/Fonts/Arial.ttf", 80)
# get a drawing context
d = ImageDraw.Draw(fig_1)
# draw text, half opacity
d.text((10, 10), "(A)", font=fnt, fill=(0, 0, 0))

## adding text "B" to the top of the fig_2
# get a drawing context
d = ImageDraw.Draw(fig_2)
# draw text, half opacity
d.text((10, 10), "(B)", font=fnt, fill=(0, 0, 0))

## adding text "C" to the top of the fig_3
# get a drawing context
d = ImageDraw.Draw(fig_3)
# draw text, half opacity
d.text((10, 10), "(C)", font=fnt, fill=(0, 0, 0))

## adding text "D" to the top of the fig_4
# get a drawing context
d = ImageDraw.Draw(fig_4)
# draw text, half opacity
d.text((10, 10), "(D)", font=fnt, fill=(0, 0, 0))

## adding text "E" to the top of the fig_5
# get a drawing context
d = ImageDraw.Draw(fig_5)
# draw text, half opacity
d.text((10, 10), "(E)", font=fnt, fill=(0, 0, 0))

## adding text "F" to the top of the fig_6
# get a drawing context
d = ImageDraw.Draw(fig_6)
# draw text, half opacity
d.text((10, 10), "(F)", font=fnt, fill=(0, 0, 0))

# get the size of the fig_1
width, height = fig_1.size

new_image = Image.new('RGB', (width * 2, height * 3), (250, 250, 250))

# Paste each image into the new image
new_image.paste(fig_1, (0, 0))
new_image.paste(fig_2, (width, 0))
new_image.paste(fig_3, (0, height))
new_image.paste(fig_4, (width, height))
new_image.paste(fig_5, (0, height *2))
new_image.paste(fig_6, (width, height * 2))

# save the new image
new_image.save("/Users/ericliao/Desktop/dissertation/metabolomic_signature/metabolic_signature_plsda_plot.png")
