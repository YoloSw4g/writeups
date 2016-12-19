# Pwn - Camera Model

```
m33d@hack:/tmp $ r2 Image_Viewer
 -- Use '-e bin.strings=false' to disable automatic string search when loading the binary.
[0x00401060]> aa
[x] Analyze all flags starting with sym. and entry0 (aa)
[0x00401060]> iz
vaddr=0x00401468 paddr=0x00001468 ordinal=000 sz=13 len=12 section=.rodata type=ascii string=Image Viewer
vaddr=0x00401475 paddr=0x00001475 ordinal=001 sz=8 len=7 section=.rodata type=ascii string=destroy
vaddr=0x0040147d paddr=0x0000147d ordinal=002 sz=18 len=17 section=.rodata type=ascii string=/org/CTF/pic1.jpg
```

We can see the string `/org/CTF/pic1.jpg`, let's try to extract some content of the binary:
```
root@hack:/tmp# binwalk --dd=".*" Image_Viewer 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             ELF 64-bit LSB executable, AMD x86-64, version 1 (SYSV)
5432          0x1538          Zlib compressed data, best compression, uncompressed size >= 65536
142856        0x22E08         LZMA compressed data, properties: 0x89, dictionary size: 16777216 bytes, uncompressed size: 100663296 bytes
142984        0x22E88         LZMA compressed data, properties: 0x9A, dictionary size: 16777216 bytes, uncompressed size: 100663296 bytes
```

We just decompress the zipped file :
```
root@hack:/tmp/_Image_Viewer.extracted# printf "\x1f\x8b\x08\x00\x00\x00\x00\x00" |cat - 1538 |gzip -dc > output.jpg
```

Then we use the tool named `identify` to dump EXIF info from the file:
```
root@hack:~# identify -verbose /tmp/ouput.jpg
[...]
    exif:ExifVersion: Exif Version 2.21
    exif:FlashPixVersion: FlashPix Version 1.0
    exif:ImageLength: 768
    exif:ImageWidth: 1366
    exif:Model: DSLR4781
    exif:Orientation: Top-left
    exif:PhotometricInterpretation: RGB
    exif:PixelXDimension: 1366
    exif:PixelYDimension: 768
    exif:ResolutionUnit: Inch
    exif:SamplesPerPixel: 3
    exif:Software: Adobe Photoshop CS5.1 Windows
    exif:thumbnail:Compression: 6
[...]
```

So we have the model : `DSLR4781` and the flag:
```
m33d@hack:/tmp $ python
>>> import md5
>>> s="SharifCTF{%s}"
>>> print s %md5.md5("DSLR4781").hexdigest()
SharifCTF{ccb7ed56eea6576263abeca4cdb03f62}
```
