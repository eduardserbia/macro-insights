# diagram_lib.py
from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrow

FIG_W, FIG_H, DPI = 38.4, 21.6, 100  # 3840x2160 (4K), 16:9

def init_axes(fig):
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
    ax.set_aspect('equal', adjustable='box')  # equal units on X and Y
    return ax

def draw_card(ax, x, y, w, h, title, lines=None, border="#222", face="#fff", title_fs=22, body_fs=16):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.6,rounding_size=8",
                         linewidth=1.6, edgecolor=border, facecolor=face)
    ax.add_patch(box)
    ax.text(x + w/2, y + h - 1.2, title, ha="center", va="top",
            fontsize=title_fs, fontweight="bold", color="#111")
    if lines:
        ax.text(x + 1.1, y + h - 3.2, "\n".join(lines),
                ha="left", va="top", fontsize=body_fs, color="#222")

def place_logo_fit(ax, path, cx, cy, target_h, max_w, width_squeeze=1, z=10):
    im = Image.open(path).convert("RGBA")
    w0, h0 = im.size
    aspect = (w0 / h0) if h0 else 1.0
    w_nominal = min(max_w, aspect * target_h)
    w = w_nominal * width_squeeze
    h = target_h
    x0, y0 = cx - w/2, cy - h/2
    ax.imshow(im, extent=(x0, x0 + w, y0, y0 + h), zorder=z)

def arrow(ax, x1, y1, x2, y2, label=None, color="#444", fs=16):
    ax.add_patch(FancyArrow(x1, y1, x2-x1, y2-y1, width=0.0,
                            head_width=0.8, head_length=1.3,
                            length_includes_head=True, color=color))
    if label:
        ax.text((x1+x2)/2, (y1+y2)/2 + 0.9, label, fontsize=fs,
                ha='center', va='bottom', color=color)
