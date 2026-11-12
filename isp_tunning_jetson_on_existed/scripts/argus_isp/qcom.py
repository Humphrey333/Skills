"""Readers for Qualcomm Chromatix XML blocks (Spectra 680/780 layout).

Each block is one XML file with a trigger tree ending in <region> elements.
Every reader returns plain numpy data plus the trigger range of each region,
so the caller decides which region to use.
"""
import os
import xml.etree.ElementTree as ET

import numpy as np


def _nums(el):
    return np.array([float(v) for v in el.text.split()])


def _regions(root):
    """Yield (path, region): path = list of (start, end) from root to region."""
    def walk(node, path):
        s, e = node.find("start"), node.find("end")
        if s is not None and e is not None:
            path = path + [(float(s.text), float(e.text))]
        for ch in node:
            if ch.tag == "region":
                yield path, ch
            elif ch.tag in ("trigger",) or ch.tag.endswith("_trigger_data"):
                yield from walk(ch, path)
    core = next(el for el in root if el.tag.endswith("_core"))
    for td in core:
        yield from walk(td, [])


def load(project_xml_dir, rel):
    return ET.parse(os.path.join(project_xml_dir, rel)).getroot()


def lsc42(xml_dir, rows=13, cols=17):
    """IFE/lsc42 rolloff mesh: list of dicts {path, r, gr, gb, b} (rows x cols)."""
    out = []
    for path, reg in _regions(load(xml_dir, "IFE/lsc42_ife_v2.xml")):
        d = {"path": path}
        for ch in ("r", "gr", "gb", "b"):
            d[ch] = _nums(reg.find(f"{ch}_gain_tab/{ch}_gain")).reshape(rows, cols)
        out.append(d)
    return out


def cc14(xml_dir):
    """IPE/cc14 CCMs: list of dicts {path, cct, ccm(3x3, rows = output R,G,B)}.

    The last trigger level is CCT. Qualcomm rows sum to 1.
    """
    out = []
    for path, reg in _regions(load(xml_dir, "IPE/cc14_ipe_v2.xml")):
        out.append({"path": path, "cct": path[-1],
                    "ccm": _nums(reg.find("c_tab/c")).reshape(3, 3)})
    return out


def gamma15(xml_dir, block="IPE/gamma15_ipe_v2.xml", full_scale=1023.0):
    """Gamma curves: list of dicts {path, lux, g (257 values, 0..1)}.

    The 4th trigger level is lux index. IPE curves are 10-bit (0..1023).
    """
    out = []
    for path, reg in _regions(load(xml_dir, block)):
        g = _nums(reg.find("channel_g_tab/channel_g")) / full_scale
        out.append({"path": path, "lux": path[3] if len(path) > 3 else None, "g": g})
    return out


def bls12_offset(xml_dir):
    """IFE/bls12 black offset (first region), in Spectra 780 18-bit units."""
    root = load(xml_dir, "IFE/bls12_ife_v2.xml")
    for _, reg in _regions(root):
        el = reg.find(".//offset")
        if el is not None:
            return float(el.text)
    el = root.find(".//offset")
    return float(el.text)
