"""Downscale the original generated art to the installed native icon canvas size."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
source = Image.open(ROOT/'art/loaded-nachos-source.png').convert('RGBA')
assert source.getextrema()[3] == (0,255), 'source must preserve transparent alpha'
subject = source.crop(source.getbbox())
subject.thumbnail((30,30), Image.Resampling.LANCZOS)
icon = Image.new('RGBA',(32,32))
icon.alpha_composite(subject, ((32-subject.width)//2,(32-subject.height)//2))
target=ROOT/'EwingsFoods/common/media/textures/Item_EwingsFoods_LoadedNachos.png'
target.parent.mkdir(parents=True,exist_ok=True)
icon.save(target)
preview=Image.new('RGB',(400,192),(28,30,34))
draw=ImageDraw.Draw(preview)
draw.text((12,8),'32x32 native canvas / original art',fill='white')
for x,bg in [(12,(28,30,34)),(64,(238,235,225))]:
    square=Image.new('RGBA',(40,40),bg+(255,));square.alpha_composite(icon,(4,4));preview.paste(square.convert('RGB'),(x,40))
preview.paste(icon.resize((128,128),Image.Resampling.NEAREST),(130,40),icon.resize((128,128),Image.Resampling.NEAREST))
preview.paste(icon.resize((128,128),Image.Resampling.LANCZOS),(266,40),icon.resize((128,128),Image.Resampling.LANCZOS))
draw.text((12,100),'actual size',fill='white')
draw.text((130,174),'4x pixels',fill='white');draw.text((266,174),'4x smooth',fill='white')
(ROOT/'art').mkdir(exist_ok=True)
preview.save(ROOT/'art/loaded-nachos-icon-qa.png')
print('Built original RGBA 32x32 icon; native Item_Plate/CornChips untrimmed canvas is 32x32')
