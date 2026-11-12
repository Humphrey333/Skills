#!/usr/bin/env bash
# Regression test: the converter must rebuild the IMX586 variant 24 tune that
# was confirmed good on the Jetson board (2026-11-11).
# Usage: bash selftest.sh <Reverse_ISP_Tune repo> <scratch dir>
set -euo pipefail
R=${1:?repo path}; T=${2:?scratch dir}
HERE=$(cd "$(dirname "$0")" && pwd)
X=$R/IMX586_Qualcomm/sm8550_qtech_imx586/Scenario.Default/XML
python3 "$HERE/argus_isp.py" build-qcom "$X" -o "$T/selftest24.isp" --variant selftest24 \
  --gamma 2.06 --ccm-mode grey --ccm-base "$R/IMX586/camera_overrides.isp" -k 0.15
python3 "$HERE/argus_isp.py" check "$T/selftest24.isp" \
  --ref "$R/IMX586_Jetson/camera_overrides.isp" --tol 0.0005
