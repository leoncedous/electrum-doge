#!/usr/bin/env python
#
# Electrum - lightweight Bitcoin client
# Copyright (C) 2015 Thomas Voegtlin
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys

from .logging import get_logger
from .i18n import _


_logger = get_logger(__name__)


try:
    import cv2
except ImportError as e:
    cv2 = None
    if sys.platform != 'darwin':
        _logger.error(f"failed to load cv2: {e!r}")

scanner_available = cv2 is not None


def _resolve_video_device(device: str):
    if not device:
        return 0
    try:
        return int(device)
    except ValueError:
        return device  # e.g. a Linux /dev/videoN path


def scan_barcode_cv2(device=''):
    if not scanner_available:
        raise RuntimeError("Cannot start QR scanner; opencv not available.")
    from PyQt5.QtCore import QTimer
    from PyQt5.QtGui import QImage, QPixmap
    from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout

    resolved_device = _resolve_video_device(device)
    if sys.platform == 'win32' and isinstance(resolved_device, int):
        capture = cv2.VideoCapture(resolved_device, cv2.CAP_DSHOW)
    else:
        capture = cv2.VideoCapture(resolved_device)
    if not capture.isOpened():
        capture.release()
        raise RuntimeError("Cannot start QR scanner; camera not available.")
    # request a higher resolution than the (often low) camera default, so QR
    # modules are large enough in pixels for the detector to decode reliably
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Note: cv2.QRCodeDetector (and QRCodeDetectorAruco) reliably fail to decode
    # QR codes with a logo overlaid in the center (e.g. this wallet's own
    # receive-address QR) -- zbar handles that erasure recovery far better,
    # but would reintroduce the libzbar/MSVCR120.dll dependency.
    detector = cv2.QRCodeDetector()
    dialog = QDialog()
    dialog.setWindowTitle(_("Scan QR code"))
    label = QLabel()
    label.setScaledContents(True)
    label.setFixedSize(640, 480)
    layout = QVBoxLayout(dialog)
    layout.addWidget(label)

    result = None

    def update_frame():
        nonlocal result
        ok, frame = capture.read()
        if not ok:
            return
        data, _points, _straight_qrcode = detector.detectAndDecode(frame)
        if data:
            result = data
            dialog.accept()
            return
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channels = rgb_frame.shape
        qimage = QImage(rgb_frame.data, width, height, channels * width, QImage.Format_RGB888)
        label.setPixmap(QPixmap.fromImage(qimage))

    timer = QTimer()
    timer.timeout.connect(update_frame)
    timer.start(30)
    try:
        dialog.exec_()
    finally:
        timer.stop()
        capture.release()

    return result

def scan_barcode_osx(*args_ignored, **kwargs_ignored):
    import subprocess
    # NOTE: This code needs to be modified if the positions of this file changes with respect to the helper app!
    # This assumes the built macOS .app bundle which ends up putting the helper app in
    # .app/contrib/osx/CalinsQRReader/build/Release/CalinsQRReader.app.
    root_ec_dir = os.path.abspath(os.path.dirname(__file__) + "/../")
    prog = root_ec_dir + "/" + "contrib/osx/CalinsQRReader/build/Release/CalinsQRReader.app/Contents/MacOS/CalinsQRReader"
    if not os.path.exists(prog):
        raise RuntimeError("Cannot start QR scanner; helper app not found.")
    data = ''
    try:
        # This will run the "CalinsQRReader" helper app (which also gets bundled with the built .app)
        # Just like the zbar implementation -- the main app will hang until the QR window returns a QR code
        # (or is closed). Communication with the subprocess is done via stdout.
        # See contrib/CalinsQRReader for the helper app source code.
        with subprocess.Popen([prog], stdout=subprocess.PIPE) as p:
            data = p.stdout.read().decode('utf-8').strip()
        return data
    except OSError as e:
        raise RuntimeError("Cannot start camera helper app; {}".format(e.strerror))

scan_barcode = scan_barcode_osx if sys.platform == 'darwin' else scan_barcode_cv2

def _find_system_cameras():
    device_root = "/sys/class/video4linux"
    devices = {} # Name -> device
    if os.path.exists(device_root):
        for device in os.listdir(device_root):
            path = os.path.join(device_root, device, 'name')
            try:
                with open(path, encoding='utf-8') as f:
                    name = f.read()
            except Exception:
                continue
            name = name.strip('\n')
            devices[name] = os.path.join("/dev", device)
    return devices


if __name__ == "__main__":
    print(scan_barcode())
