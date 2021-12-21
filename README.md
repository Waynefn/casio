# casio
Scripts/sources for casio e-dictionary image format.

## About GRA

Casio dictionary [*](https://casio.jp/exword/) uses a special image format as its dictionary main graph.
By analysing the image file binary format, we can know that:

- 15 bits color (32768 levels for R,G,B) as
```python
    (data & 0b1111100000000000) >> 11
    (data & 0b0000011111000000) >> 6
    (data & 0b0000000000011111) >> 0
```
- very simple header which contains height and width of the image
```
    b'\x21\xe0\x00\xa4'
```

## gra_reader.py

### gra2png

Convert gra file to png format. Show png using pyplot.imshow

### gra2png_mono

Convernt gra file to monocolor png file.

### png2gra

Convert png file to gra format. Only support the standard size for now.
