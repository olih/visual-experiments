# Brush

## Line thickness

> A full set of pens would have the following nib sizes: 0.13, 0.18, 0.25, 0.35, 0.5, 0.7, 1.0, 1.4, and 2.0 mm, which correspond to the line widths as defined in ISO 128 (Wikipedia)

So, a 0.13 mm thick line should be represented by at least a 1 pixel wide line.

|Nib size|pix/mm|Dot/inch|
|--------|------|--------|
| 0.13   | 8    | 203    |
| 0.065  | 16   | 406    |

Colors printers tend to be 300 DPI while black & white tend to 600 DPI. This is coherent. It looks like we should probably store our images at 600 DPI or even 1200 DPI. If we zoom on an image, higher resolution matters, but perhaps we don't need to deal with zoom this way.

## Paper sizes

Most comics should fit on a A4 page. Posters and printed art works may require much larger format such as A0.

## Relationship between paper size and pen thickness

It would possible to use a very thick pen (1 cm wide or more) on a A4 piece of paper, but artistically very unlikely, unless you intend to fill some surface.
Drawing tends to require accuracy and this is not quite compatible with extreme thickness.

Assuming A4, we would have between 0.065 mm and 10 mm possible thickness, which give us 154 acceptable nib sizes.

## Brushes requirements

Brushes:

* are expected to be monochrome
* should be a simple Bézier path.
* should have a single state. For now, and to keep things simple.
* should be able to be represented as Bamboo Swing Gesture file.
* should be able to rendered as SVG to facilitate selection in a UI.
* should be able to scale quite precisely.
* should have a thickness between 0.065 mm and 10 mm on A4.
* for scaling, it would be possible to have 20 mm thickness on A3.
* we could almost assume the thickness is between 1 and 154.
* brush thickness should vary when part of a stroke.
* brush strokes are often curvy in organic drawing.
* very long brush strokes are difficult to reuse, 2-3 cm may be a maximum.
* could be contained in a 600 x 600 square.
* could be contained in a circle of diameter 600.
* should preferably be asymmetric as symmetry is easy to construct later.

