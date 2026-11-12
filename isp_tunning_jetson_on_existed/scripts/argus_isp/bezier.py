"""Argus lens-shading Bezier net: 10x10 control points per channel.

Per axis the net is 3 cubic Bezier patches that share end points
(3*3 + 1 = 10 control points). Patch widths come from the .isp keys
leftPatchFactor/centerPatchFactor (x) and topPatchFactor/middlePatchFactor (y);
the third patch takes the rest. With 0.25/0.5 the patch edges are 0, .25, .75, 1.

Index convention used here (unverified on the board, see reference/argus_keys.md):
controlPoint[i][j] -> i = row (top to bottom), j = column (left to right).
"""
import numpy as np

N_CTRL = 10


def edges(first=0.25, center=0.5):
    return np.array([0.0, first, first + center, 1.0])


def basis(u, e):
    """Matrix B (len(u) x 10): surface along one axis = B @ ctrl."""
    u = np.asarray(u, float)
    B = np.zeros((u.size, N_CTRL))
    for n, x in enumerate(u):
        p = min(int(np.searchsorted(e, x, side="right")) - 1, 2)
        p = max(p, 0)
        t = (x - e[p]) / (e[p + 1] - e[p])
        b = [(1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t ** 2 * (1 - t), t ** 3]
        for k in range(4):
            B[n, 3 * p + k] += b[k]
    return B


def surface(ctrl, ny, nx, e_x=None, e_y=None):
    """Evaluate a 10x10 net on an ny x nx grid spanning [0,1]^2."""
    e_x = edges() if e_x is None else e_x
    e_y = edges() if e_y is None else e_y
    By = basis(np.linspace(0, 1, ny), e_y)
    Bx = basis(np.linspace(0, 1, nx), e_x)
    return By @ ctrl @ Bx.T


def fit(grid, e_x=None, e_y=None, dense=(73, 97)):
    """Least-squares 10x10 net for a gain grid (rows = y, cols = x, nodes on [0,1]).

    The grid is first densified bilinearly to `dense` (rows, cols) so the fit
    sees the whole surface, not only the mesh nodes.
    Returns (ctrl, max_rel_err, rms_rel_err) measured on the dense grid.
    """
    e_x = edges() if e_x is None else e_x
    e_y = edges() if e_y is None else e_y
    g = bilinear(np.asarray(grid, float), *dense)
    By = np.linalg.pinv(basis(np.linspace(0, 1, dense[0]), e_y))
    Bx = np.linalg.pinv(basis(np.linspace(0, 1, dense[1]), e_x))
    ctrl = By @ g @ Bx.T
    rel = surface(ctrl, *dense, e_x, e_y) / g - 1
    return ctrl, float(np.abs(rel).max()), float(np.sqrt((rel ** 2).mean()))


def bilinear(grid, ny, nx):
    r, c = grid.shape
    ys, xs = np.linspace(0, r - 1, ny), np.linspace(0, c - 1, nx)
    tmp = np.array([np.interp(xs, np.arange(c), row) for row in grid])
    return np.array([np.interp(ys, np.arange(r), col) for col in tmp.T]).T
