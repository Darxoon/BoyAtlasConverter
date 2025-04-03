from array import array
from dataclasses import dataclass
from pathlib import Path
from sys import argv
from PIL import Image

@dataclass
class ImageEntry:
    name: str
    x: int
    y: int
    width: int
    height: int

def get_atlas_definition(buf: bytes):
    assert len(buf) >= 12, "Atlas file too small, must be at least 12 (0xC) bytes long"
    
    # Check header
    assert buf[0:4] == 'boya'.encode(), "Invalid atlas file"
    assert buf[4:8] == (1).to_bytes(4, 'little'), "Invalid atlas file"
    
    file_count = int.from_bytes(buf[8:0xc], 'little')
    images: list[ImageEntry] = []
    
    for i in range(file_count):
        offset = 0xc + 0x50 * i
        assert len(buf) >= offset + 0x50, f"Atlas file too small (at image definition {i})"
        
        name_bytelen = min(0x40, next(i for i, value in enumerate(buf[offset:]) if value == 0))
        name = buf[offset:offset + name_bytelen].decode()
        
        other_fields = array('I', buf[offset + 0x40:offset + 0x50])
        
        images.append(ImageEntry(name, other_fields[0], other_fields[1], other_fields[2], other_fields[3]))
    
    return images

def dump_image(entry: ImageEntry, atlas: Image.Image, out_dir: Path):
    left = entry.x
    top = entry.y
    right = entry.x + entry.width
    bottom = entry.y + entry.height
    
    image = atlas.crop((left, top, right, bottom))
    image.save(out_dir / (entry.name + '.png'))

def main():
    if len(argv) < 2 or argv[1] == '-h' or argv[1] == '--help':
        print("Usage: boyatlas <your atlas.image>")
        exit(0)
    
    atlas_path = Path(argv[1])
    parent_dir = atlas_path.parent
    filename = atlas_path.stem
    
    if atlas_path.suffix not in ('.image', '.png'):
        print("Please supply a .image or .png file.")
        print("Make sure that you have extracted the .image file using boyi_convert \
in either case.")
        exit(1)
    
    # read atlas defintion file
    definition_file = parent_dir / (filename + '.image.atlas')
    with open(definition_file, 'rb') as f:
        images = get_atlas_definition(f.read())
    
    # read png file
    png_file = parent_dir / (filename + '.png')
    if not png_file.is_file():
        print(f"Could not find file {png_file.as_posix()}. Please extract the {filename}.image file using boyi_convert first.")
        exit(1)
    
    atlas = Image.open(png_file)
    out_dir = parent_dir / filename
    
    if not out_dir.is_dir():
        out_dir.mkdir()
    
    for image in images:
        dump_image(image, atlas, out_dir)

if __name__ == '__main__':
    main()
