import machine, time, ustruct
from micropython import const
from machine import SoftI2C, Pin

from setting import *
from utility import *

_COMMAND_BIT = const(0x80)

_REGISTER_ENABLE = const(0x00)
_REGISTER_ATIME = const(0x01)

_REGISTER_AILT = const(0x04)
_REGISTER_AIHT = const(0x06)

_REGISTER_ID = const(0x12)

_REGISTER_APERS = const(0x0c)

_REGISTER_CONTROL = const(0x0f)

_REGISTER_SENSORID = const(0x12)

_REGISTER_STATUS = const(0x13)
_REGISTER_CDATA = const(0x14)
_REGISTER_RDATA = const(0x16)
_REGISTER_GDATA = const(0x18)
_REGISTER_BDATA = const(0x1a)

_ENABLE_AIEN = const(0x10)
_ENABLE_WEN = const(0x08)
_ENABLE_AEN = const(0x02)
_ENABLE_PON = const(0x01)

_GAINS = (1, 4, 16, 60)
_CYCLES = (0, 1, 2, 3, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60)

# Brightness thresholds for environment warnings
_BRIGHTNESS_TOO_DARK  = 8    # below this → warn too dark
_BRIGHTNESS_TOO_BRIGHT = 92  # above this → warn too bright

COLOR = {
    'r': 0,
    'g': 1,
    'b': 2,
    'd': 3,
    'w': 4,
    'y': 5
}

class TCS34725:
    def __init__(self, address=0x29):
        self.address = address

        # --- I2C init with bus scan ---
        try:
            self.i2c = machine.SoftI2C(scl=machine.Pin(SCL_PIN), sda=machine.Pin(SDA_PIN))
            found = self.i2c.scan()
            if self.address not in found:
                raise Exception('TCS34725 not found on I2C bus')
        except Exception as e:
            print('TCS34725 init error:', e)
            raise

        self._active = False
        self.integration_time(2.4)
        sensor_id = self.sensor_id()
        if sensor_id not in (0x44, 0x10):
            raise RuntimeError("wrong sensor id 0x{:x}".format(sensor_id))

        # Calibration storage
        self._cal_black = None   # (r, g, b) raw at black surface
        self._cal_white = None   # (r, g, b) raw at white surface

    # ------------------------------------------------------------------ #
    #  LOW-LEVEL REGISTER ACCESS (unchanged)
    # ------------------------------------------------------------------ #

    def _register8(self, register, value=None):
        register |= _COMMAND_BIT
        if value is None:
            return self.i2c.readfrom_mem(self.address, register, 1)[0]
        data = ustruct.pack('<B', value)
        self.i2c.writeto_mem(self.address, register, data)

    def _register16(self, register, value=None):
        register |= _COMMAND_BIT
        if value is None:
            data = self.i2c.readfrom_mem(self.address, register, 2)
            return ustruct.unpack('<H', data)[0]
        data = ustruct.pack('<H', value)
        self.i2c.writeto_mem(self.address, register, data)

    # ------------------------------------------------------------------ #
    #  CORE SENSOR CONTROL (unchanged)
    # ------------------------------------------------------------------ #

    def active(self, value=None):
        if value is None:
            return self._active
        value = bool(value)
        if self._active == value:
            return
        self._active = value
        enable = self._register8(_REGISTER_ENABLE)
        if value:
            self._register8(_REGISTER_ENABLE, enable | _ENABLE_PON)
            time.sleep_ms(3)
            self._register8(_REGISTER_ENABLE,
                enable | _ENABLE_PON | _ENABLE_AEN)
        else:
            self._register8(_REGISTER_ENABLE,
                enable & ~(_ENABLE_PON | _ENABLE_AEN))

    def sensor_id(self):
        return self._register8(_REGISTER_SENSORID)

    def integration_time(self, value=None):
        if value is None:
            return self._integration_time
        value = min(614.4, max(2.4, value))
        cycles = int(value / 2.4)
        self._integration_time = cycles * 2.4
        return self._register8(_REGISTER_ATIME, 256 - cycles)

    def gain(self, value=None):
        if value is None:
            return _GAINS[self._register8(_REGISTER_CONTROL)]
        if value not in _GAINS:
            raise ValueError("gain must be 1, 4, 16 or 60")
        return self._register8(_REGISTER_CONTROL, _GAINS.index(value))

    def _valid(self):
        return bool(self._register8(_REGISTER_STATUS) & 0x01)

    def read(self, raw=False):
        was_active = self.active()
        self.active(True)
        while not self._valid():
            time.sleep_ms(int(self._integration_time + 0.9))
        data = tuple(self._register16(register) for register in (
            _REGISTER_RDATA,
            _REGISTER_GDATA,
            _REGISTER_BDATA,
            _REGISTER_CDATA,
        ))
        self.active(was_active)
        if raw:
            return data
        return self._temperature_and_lux(data)

    def _temperature_and_lux(self, data):
        r, g, b, c = data
        x = -0.14282 * r + 1.54924 * g + -0.95641 * b
        y = -0.32466 * r + 1.57837 * g + -0.73191 * b
        z = -0.68202 * r + 0.77073 * g +  0.56332 * b
        d = x + y + z
        if d == 0:
            return 0, 0
        n = (x / d - 0.3320) / (0.1858 - y / d)
        cct = 449.0 * n**3 + 3525.0 * n**2 + 6823.3 * n + 5520.33
        return cct, y

    def threshold(self, cycles=None, min_value=None, max_value=None):
        if cycles is None and min_value is None and max_value is None:
            min_value = self._register16(_REGISTER_AILT)
            max_value = self._register16(_REGISTER_AIHT)   # bug fixed
            if self._register8(_REGISTER_ENABLE) & _ENABLE_AIEN:
                cycles = _CYCLES[self._register8(_REGISTER_APERS) & 0x0f]
            else:
                cycles = -1
            return cycles, min_value, max_value
        if min_value is not None:
            self._register16(_REGISTER_AILT, min_value)
        if max_value is not None:
            self._register16(_REGISTER_AIHT, max_value)
        if cycles is not None:
            enable = self._register8(_REGISTER_ENABLE)
            if cycles == -1:
                self._register8(_REGISTER_ENABLE, enable & ~(_ENABLE_AIEN))
            else:
                self._register8(_REGISTER_ENABLE, enable | _ENABLE_AIEN)
                if cycles not in _CYCLES:
                    raise ValueError("invalid persistence cycles")
                self._register8(_REGISTER_APERS, _CYCLES.index(cycles))

    def interrupt(self, value=None):
        if value is None:
            return bool(self._register8(_REGISTER_STATUS) & _ENABLE_AIEN)
        if value:
            raise ValueError("interrupt can only be cleared")
        self.i2c.writeto(self.address, b'\xe6')

    def html_rgb(self):
        r, g, b, c = self.read(True)
        if c == 0:
            return (0, 0, 0)
        red   = int(pow((int((r/c) * 256) / 255), 2.5) * 255)
        green = int(pow((int((g/c) * 256) / 255), 2.5) * 255)
        blue  = int(pow((int((b/c) * 256) / 255), 2.5) * 255)
        if red   > 255: red   = 255
        if green > 255: green = 255
        if blue  > 255: blue  = 255
        return (red, green, blue)

    def html_hex(self):
        r, g, b = self.html_rgb()
        return "{0:02x}{1:02x}{2:02x}".format(int(r), int(g), int(b))

    def read_color(self, color):
        return self.html_rgb()[COLOR[color]]

    def detect(self, color, limit=40):
        r, g, b = self.html_rgb()
        if max(r, g, b, limit) == r:
            return 0 == COLOR[color]
        elif max(r, g, b, limit) == g:
            return 1 == COLOR[color]
        elif max(r, g, b, limit) == b:
            return 2 == COLOR[color]
        elif max(r, g, b) < (limit / 3):
            return 3 == COLOR[color]
        elif min(r, g, b) > (limit / 3):
            return 4 == COLOR[color]
        elif ((26 < r < 36) and (14 < g < 24) and (0 < b < 8)):
            return 5 == COLOR[color]
        else:
            return False

    # ================================================================== #
    #  NEW INTERNAL HELPERS
    # ================================================================== #

    def _safe_read_raw(self, timeout_ms=1000):
        """Read raw RGBC with timeout. Returns (r,g,b,c) or None on timeout."""
        was_active = self.active()
        self.active(True)
        elapsed = 0
        interval = int(self._integration_time + 0.9)
        while not self._valid():
            time.sleep_ms(interval)
            elapsed += interval
            if elapsed >= timeout_ms:
                self.active(was_active)
                print('[TCS34725] WARNING: sensor timeout — check wiring or lighting')
                return None
        data = tuple(self._register16(reg) for reg in (
            _REGISTER_RDATA, _REGISTER_GDATA, _REGISTER_BDATA, _REGISTER_CDATA))
        self.active(was_active)
        return data

    def _read_average_raw(self, samples=5):
        """Average multiple raw RGBC readings to reduce noise."""
        results = []
        for _ in range(samples):
            d = self._safe_read_raw()
            if d is not None:
                results.append(d)
            time.sleep_ms(10)
        if not results:
            return None
        n = len(results)
        return tuple(sum(row[i] for row in results) // n for i in range(4))

    def _brightness_percent(self, c_raw=None):
        """
        Return brightness 0-100 from the Clear channel.
        Used internally to warn about extreme lighting conditions.
        """
        if c_raw is None:
            data = self._safe_read_raw()
            if data is None:
                return 0
            c_raw = data[3]
        # max count for default integration time 2.4ms * 1 cycle = 1024 counts
        # for 614.4ms = 65535. Use ratio against saturation limit.
        sat = min(65535, int(self._integration_time / 2.4) * 1024)
        if sat == 0:
            return 0
        return min(100, int(c_raw * 100 / sat))

    def _check_brightness_warning(self, brightness):
        """Print a warning if lighting conditions are too extreme."""
        #if brightness < _BRIGHTNESS_TOO_DARK:
            #print('[TCS34725] WARNING: environment too dark ({}%) — color readings may be unreliable'.format(brightness))
        #elif brightness > _BRIGHTNESS_TOO_BRIGHT:
            #print('[TCS34725] WARNING: environment too bright ({}%) — sensor may be saturated'.format(brightness))

    def _rgb_to_hsv(self, r, g, b):
        """Convert 0-255 RGB to HSV (h: 0-360, s: 0-100, v: 0-100)."""
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        diff = mx - mn
        v = mx * 100
        s = 0 if mx == 0 else (diff / mx) * 100
        if diff == 0:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / diff) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / diff) + 120) % 360
        else:
            h = (60 * ((r - g) / diff) + 240) % 360
        return h, s, v

    def _normalize_rgb_calibrated(self, r, g, b):
        """
        Normalize RGB using stored black/white calibration points.
        Returns normalized (r, g, b) in 0-255 range.
        """
        if self._cal_black is None or self._cal_white is None:
            return r, g, b
        nr, ng, nb = self._cal_black
        wr, wg, wb = self._cal_white
        def norm(val, lo, hi):
            if hi == lo:
                return 128
            return max(0, min(255, int((val - lo) * 255 / (hi - lo))))
        return norm(r, nr, wr), norm(g, ng, wg), norm(b, nb, wb)

    # ================================================================== #
    #  NEW PUBLIC API
    # ================================================================== #

    def is_ready(self):
        """
        Check if the sensor is connected and responding on the I2C bus.
        Returns True if ready, False otherwise.
        """
        try:
            found = self.i2c.scan()
            return self.address in found
        except:
            return False

    def calibrate_white(self):
        """
        Record the current surface as WHITE reference.
        Point the sensor at a plain white surface before calling this.
        Uses averaged reading for stability.
        """
        data = self._read_average_raw(samples=8)
        if data is None:
            print('[TCS34725] calibrate_white failed: no data')
            return False
        r, g, b, c = data
        brightness = self._brightness_percent(c)
        self._check_brightness_warning(brightness)
        self._cal_white = (r, g, b)
        print('[TCS34725] White calibrated: R={} G={} B={} (brightness={}%)'.format(r, g, b, brightness))
        return True

    def calibrate_black(self):
        """
        Record the current surface as BLACK reference.
        Point the sensor at a plain black (dark) surface before calling this.
        Uses averaged reading for stability.
        """
        data = self._read_average_raw(samples=8)
        if data is None:
            print('[TCS34725] calibrate_black failed: no data')
            return False
        r, g, b, c = data
        brightness = self._brightness_percent(c)
        self._check_brightness_warning(brightness)
        self._cal_black = (r, g, b)
        print('[TCS34725] Black calibrated: R={} G={} B={} (brightness={}%)'.format(r, g, b, brightness))
        return True

    def get_color_name(self):
        """
        Return the detected color as a Vietnamese string:
        'đỏ', 'cam', 'vàng', 'xanh lá', 'xanh lam', 'xanh dương', 'tím',
        'hồng', 'trắng', 'đen', 'không xác định'
        Uses HSV for light-independent classification.
        """
        data = self._read_average_raw(samples=5)
        if data is None:
            return 'không xác định'
        r_raw, g_raw, b_raw, c = data
        brightness = self._brightness_percent(c)
        self._check_brightness_warning(brightness)

        # Normalize with calibration if available
        r, g, b = self._normalize_rgb_calibrated(r_raw, g_raw, b_raw)

        # Compute a simple normalized RGB for HSV
        total = r + g + b
        if total == 0:
            return 'đen'

        scale = 255.0 / max(r, g, b) if max(r, g, b) > 0 else 1
        r_s = min(255, int(r * scale))
        g_s = min(255, int(g * scale))
        b_s = min(255, int(b * scale))

        h, s, v = self._rgb_to_hsv(r_s, g_s, b_s)

        # Achromatic: black or white
        if v < 20:
            return 'đen'
        if s < 20:
            if v > 70:
                return 'trắng'
            return 'đen'

        # Chromatic: classify by Hue
        if h < 15 or h >= 345:
            return 'đỏ'
        elif h < 36:
            return 'cam'
        elif h < 66:
            return 'vàng'
        elif h < 150:
            return 'xanh lá'
        #elif h < 186:
            #return 'xanh lam'
        elif h < 261:
            return 'xanh dương'
        elif h < 311:
            return 'tím'
        elif h < 345:
            return 'hồng'
        return 'không xác định'

    def on_dark_surface(self):
        """
        Return True if the sensor is currently over a DARK (black) line/surface.
        Requires calibrate_black() and calibrate_white() to be called first
        for best accuracy. Falls back to a fixed threshold if not calibrated.
        """
        pct = self.line_position_percent()
        return pct < 30

    def on_light_surface(self):
        """
        Return True if the sensor is currently over a LIGHT (white) surface.
        Requires calibrate_black() and calibrate_white() to be called first
        for best accuracy. Falls back to a fixed threshold if not calibrated.
        """
        pct = self.line_position_percent()
        return pct > 70

    def line_position_percent(self):
        """
        Return a value 0-100 representing how light the current surface is,
        relative to the calibrated black (0%) and white (100%) references.

        Use this for proportional (PID-style) line following:
          ~0%   = fully on dark line
          ~50%  = on the edge of the line
          ~100% = fully on white surface

        If not calibrated, uses raw Clear channel normalized to sensor max.
        Prints a warning if lighting conditions are extreme.
        """
        data = self._read_average_raw(samples=5)
        if data is None:
            return 50  # safe default

        r_raw, g_raw, b_raw, c = data
        brightness = self._brightness_percent(c)
        self._check_brightness_warning(brightness)

        if self._cal_black is not None and self._cal_white is not None:
            # Use calibrated luminance: weighted sum matching human perception
            def lum(rgb):
                return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
            lum_black = lum(self._cal_black)
            lum_white = lum(self._cal_white)
            lum_now   = 0.299 * r_raw + 0.587 * g_raw + 0.114 * b_raw
            if lum_white == lum_black:
                return 50
            pct = int((lum_now - lum_black) * 100 / (lum_white - lum_black))
            return max(0, min(100, pct))
        else:
            # Fallback: raw brightness
            return brightness
