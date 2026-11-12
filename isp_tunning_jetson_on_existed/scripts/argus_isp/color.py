"""CCM and tone conversions between a vendor tune and Argus.

Argus colorCorrection.srgbMatrix is stored TRANSPOSED compared with the usual
"rows = output channel" form: its COLUMNS sum to 1 (NVIDIA Char-lite IMX477
file). Qualcomm cc14 rows sum to 1. So argus = qcom.T.
"""
import numpy as np

I3 = np.eye(3)


def qcom_to_argus(ccm_rows_out):
    return np.asarray(ccm_rows_out, float).T


def blend_identity(m_argus, k):
    """M = I + k*(M - I). Keeps column sums; k<1 lowers saturation.

    Not enough on its own when Argus default AWB leaves a cast: IMX586 still
    showed green at k=0.3 (variant 21).
    """
    return I3 + k * (np.asarray(m_argus, float) - I3)


def grey_preserving(base_argus, m_argus, k):
    """M = S @ base, S = I + k*(m - I).

    S has unit column sums, so the grey response of M equals that of `base`
    (a CCM already known good on the board). Only saturation from `m` is added.
    This is what fixed the IMX586 green cast (variant 24, k=0.15).
    """
    return blend_identity(m_argus, k) @ np.asarray(base_argus, float)


def gamma_power_fit(curve, lo=0.01):
    """Best G for y = x**(1/G), least squares in log space over x >= lo.

    The result depends on the method (linear-space fit gives ~0.2 higher on
    the IMX586 SM8550 curve), so print it next to the alternatives.
    """
    y = np.asarray(curve, float)
    x = np.linspace(0, 1, y.size)
    m = (x >= lo) & (y > 0)
    lx, ly = np.log(x[m]), np.log(y[m])
    return float(np.sum(lx * lx) / np.sum(lx * ly))


def gamma_power_fit_linear(curve):
    y = np.asarray(curve, float)
    x = np.linspace(0, 1, y.size)
    gs = np.arange(1.0, 3.5, 0.005)
    return float(min(gs, key=lambda g: ((x ** (1 / g) - y) ** 2).sum()))


def black_level(offset, offset_bits, sensor_bits=10):
    """Vendor black offset -> (Argus int bias @sensor_bits, float bias)."""
    frac = offset / 2 ** offset_bits
    full = 2 ** sensor_bits - 1
    ival = int(round(frac * 2 ** sensor_bits))
    return ival, ival / full
