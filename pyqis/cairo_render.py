from math import pi
import cmath

import numpy as np
try:
    import cairocffi as cairo
except ImportError:
    import cairo

from pyqis.label import create_label

# we use the cielab color space so each hue has the same perceived intensity.
def cielchToRGB(l, c, h):
    # l and c go from 0 to 100
    # h is an angle in radians

    # based on http://www.easyrgb.com/index.php?X=MATH

    # convert to XYZ
    y = (l + 16) / 116.
    x = c * np.cos(h) / 500. + y
    z = y - c * np.sin(h) / 200.
    mp = lambda y: y * y * y if y > 0.206893 else (y - 16 / 116.) / 7.787
    y = mp(y)
    x = mp(x) * 0.95047
    z = mp(z) * 1.08883

    # convert to RGB
    r = x *  3.2406 + y * -1.5372 + z * -0.4986
    g = x * -0.9689 + y *  1.8758 + z *  0.0415
    b = x *  0.0557 + y * -0.2040 + z *  1.0570
    mp = lambda r: 1.055 * (r ** (1 / 2.4)) - 0.055 if r > 0.0031308 else 12.92 * r
    r = mp(r)
    g = mp(g)
    b = mp(b)

    # ensure it's in bounds and scale it to be between 0 and 255
    m = lambda v: max((min((1., v)), 0.))
    return (m(r), m(g), m(b))

def render_state(state, filename, use_color=True, label_format=None, states_per_row=4):
    svg_filename = None
    png_filename = None
    if filename.endswith(".svg"):
        svg_filename = filename
    elif filename.endswith(".png"):
        png_filename = filename
    else:
        raise RuntimeError("Cannot determine file type from extension: %r" % filename)

    vec = state.state / np.linalg.norm(state.state)
    basis_size = 1 << state.nqubits
    labels = [create_label(i, state.nqubits, label_format)
              for i in range(basis_size)]

    # Determine dimensions of image
    if states_per_row <= 0 or (states_per_row & (states_per_row - 1)) != 0:
        raise RuntimeError("`states_per_row` must be a power of two.")
    rows = (basis_size - 1) // states_per_row + 1
    cols = min([basis_size, states_per_row])

    hpadding = 10
    vpadding = 10
    label_height = 30
    img_width = cols * 100 + (cols - 1) * hpadding
    img_height = rows * (100 + label_height) + (rows - 1) * vpadding

    s = cairo.SVGSurface(svg_filename, img_width, img_height)
    c = cairo.Context(s)

    for i, label in enumerate(labels):
        row = i // states_per_row
        col = i % states_per_row

        radius, phi = cmath.polar(vec[i])

        c.save()
        ctrx = col * (100 + hpadding) + 50
        ctry = row * (100 + vpadding + label_height) + 50
        c.translate(ctrx, ctry)

        if radius > 1e-6:
            c.save()
            c.scale(3.2 * radius, 3.2 * radius)
            c.rotate(-phi)

            # box
            c.save()
            c.rectangle(-9, -9, 18, 18)
            c.set_line_width(2.)
            r, g, b = cielchToRGB(80, 35, phi)
            c.set_source_rgba(r, g, b, 0.8)
            c.fill_preserve()
            c.set_source_rgb(0, 0, 0)
            c.stroke()
            c.restore()

            # arrow
            c.save()
            c.move_to(0, -8)
            c.line_to(5, -3)
            c.line_to(1, -4)
            c.line_to(1, 8)
            c.line_to(-1, 8)
            c.line_to(-1, -4)
            c.line_to(-5, -3)
            c.close_path()
            c.set_source_rgba(0, 0, 0)
            c.fill()
            c.restore()

            c.restore()

        # label
        c.set_font_size(14)
        text_width, text_height = c.text_extents(label)[2:4]
        c.move_to(-text_width / 2., 50 + 10 + text_height)
        c.show_text(label)

        c.restore()

    # Save as a SVG and PNG
    if png_filename is not None:
        s.write_to_png(png_filename)
    s.finish()
