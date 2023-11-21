import re
import shutil
import os
from pathlib import Path
import sys

d_parental = "C:/Users/ghhrr/Documents"
dirs = ('images', 'video', 'docs', 'audio', 'archives', 'other')
p_dirs = []
imgs = []
vids = []
txts = []
sons = []
arcs = []
oths = []

img = {'.jpeg', '.png', '.jpg', '.svg'}
vid = {'.avi', '.mp4', '.mov', '.mkv'}
txt = {'.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'}
son = {'.mp3', '.ogg', '.wav', '.amr'}
arc = {'.zip', '.gz', '.tar'}
extentions = set()

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()
    
def d_creator(parental):
    try:
        for i in dirs:
            path = os.path.join(parental, i)
            p_dirs.append(path)
            os.mkdir(path) 
    except FileExistsError:
        pass


def translate(name):
    name = name.split('.')
    oname = re.sub(r"[^a-zA-Zа-яА-Я0-9]+", "_", name[0])
    oname = name[0].translate(TRANS)
    rname = f"{oname}.{name[1]}"
    
    return rname


def action(path):
    for i in path.iterdir():
        if i.is_file():
            ext = Path(i).suffix
            i  = translate(i.name)
            ext = set(ext)
            if ext & img:
                imgs.append(i)
                extentions.add(ext)
                shutil.move(i, p_dirs[0])
            elif ext & vid:
                vids.append(i)
                extentions.add(ext)   
                shutil.move(i, p_dirs[1])
            elif ext & txt:
                txts.append(i)
                extentions.add(ext)
                shutil.move(i, p_dirs[2])
            elif ext & son:
                sons.append(i)
                extentions.add(ext)
                shutil.move(i, p_dirs[3])
            elif ext & arc:
                arcs.append(i)
                extentions.add(ext)
                path = os.path.join(p_dirs[4], i.name)
                os.mkdir(path)
                shutil.unpack_archive(i, path)
            else:
                oths.append(i)
                extentions.add(ext)
                shutil.move(i, p_dirs[5])

        else:
            if os.listdir(i):
                action(i)
            else:
                os.rmdir(i)
                
def output():
    print(f"{imgs}\n{vids}\n{txts}\n{sons}\n{arcs}\n{oths}")
    print(extentions)
            
def main():
    d_creator(d_parental)
    action(Path(sys.argv[1]))


if __name__ == "__main__":
    main()