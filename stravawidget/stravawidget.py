from queue import Queue, Empty
from threading import Thread

from libqtile.widget import base
from libqtile import bar
from libqtile.log_utils import logger
from libqtile.popup import Popup

from .stravadata import get_strava_data


class StravaWidget(base._Widget, base.MarginMixin):

    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ("font", "sans", "Default font"),
        ("fontsize", None, "Font size"),
        ("font_colour", "ffffff", "Text colour"),
        ("text", "{CA:%b} {CD:.1f}km", "Widget text"),
        ("refresh_interval", 1800, "Time to update data"),
        ("startup_delay", 10, "Time before sending first web request"),
        ("popup_display_timeout", 15, "Time to display extended info")
    ]

    format_map = {
        "CD": ("current", "distance"),
        "CC": ("current", "count"),
        "CT": ("current", "formatTime"),
        "CP": ("current", "formatPace"),
        "CN": ("current", "name"),
        "CA": ("current", "date"),
        "YD": ("year", "distance"),
        "YC": ("year", "count"),
        "YT": ("year", "formatTime"),
        "YP": ("year", "formatPace"),
        "YN": ("year", "name"),
        "YA": ("year", "date"),
        "AD": ("alltime", "distance"),
        "AC": ("alltime", "count"),
        "AT": ("alltime", "formatTime"),
        "AP": ("alltime", "formatPace"),
        "AN": ("alltime", "name"),
        "AA": ("alltime", "date"),
    }

    def __init__(self, **config):
        base._Widget.__init__(self, bar.CALCULATED, **config)
        self.add_defaults(StravaWidget.defaults)
        self.add_defaults(base.MarginMixin.defaults)
        self.data = None

    def _configure(self, qtile, bar):
        base._Widget._configure(self, qtile, bar)
        self.timeout_add(self.startup_delay, self.refresh)

    def _get_data(self, queue=None):
        result, data = get_strava_data()

        if result:
            queue.put(data)

        else:
            logger.warning(data)

    def _wait_for_data(self):
        try:
            data = self._queue.get(False)
            self._read_data(data)
        except Empty:
            self.timeout_add(1, self._wait_for_data)

    def _read_data(self, data):
        self.data = data
        self.formatted_data = {}
        for k, v in self.format_map.items():
            obj = self.data
            for attr in v:
                obj = getattr(obj, attr)

            self.formatted_data[k] = obj

        self.timeout_add(1, self.update)
        self.timeout_add(self.refresh_interval, self.refresh)

    def refresh(self):
        self._queue = Queue()
        kwargs = {"queue": self._queue}
        self.worker = Thread(target=self._get_data, kwargs=kwargs)
        self.worker.daemon = True
        self.worker.start()
        self._wait_for_data()

    def set_refresh_timer(self):
        pass

    def calculate_length(self):

        total = 0

        if self.data is not None:

            text = self.formatText(self.text)

            width, _ = self.drawer.max_layout_size(
                [text],
                self.font,
                self.fontsize)

            total += (width + 2 * self.margin)

        total += self.height

        return total

    def draw_icon(self):
        scale = self.height / 24.0
        self.drawer.set_source_rgb("ffffff")
        self.drawer.ctx.set_line_width(2)
        self.drawer.ctx.move_to(8 * scale, 14 * scale)
        self.drawer.ctx.line_to(12 * scale, 6 * scale)
        self.drawer.ctx.line_to(16 * scale, 14 * scale)
        self.drawer.ctx.stroke()

        self.drawer.ctx.set_line_width(1)
        self.drawer.ctx.move_to(13 * scale, 14 * scale)
        self.drawer.ctx.line_to(16 * scale, 20 * scale)
        self.drawer.ctx.line_to(19 * scale, 14 * scale)
        self.drawer.ctx.stroke()

    def update(self):
        # Remove background
        self.drawer.clear(self.background or self.bar.background)

        x_offset = 0

        self.draw_icon()
        x_offset += self.height

        if self.data is None:
            text = ""

        else:
            text = self.formatText(self.text)

        # Create a text box
        layout = self.drawer.textlayout(text,
                                        self.font_colour,
                                        self.font,
                                        self.fontsize,
                                        None,
                                        wrap=False)

        # We want to centre this vertically
        y_offset = (self.bar.height - layout.height) / 2

        # Draw it
        layout.draw(x_offset + self.margin_x, y_offset)

        # Redraw the bar
        self.bar.draw()

    def draw(self):
        self.drawer.draw(offsetx=self.offset, width=self.length)

    def button_press(self, x, y, button):
        self.show_popup_summary()

    def hide(self):
        self.hidden = True
        self.update()

    def mouse_enter(self, x, y):
        pass

    def formatText(self, text):
        try:
            return text.format(**self.formatted_data)
        except Exception as e:
            logger.warning(e)
            return "Error"

    def show_popup_summary(self):
        if not self.data:
            return False

        lines = []

        heading = ("{:^6} {:^20} {:^8} {:^10} {:^6}".format("Date",
                                                            "Title",
                                                            "km",
                                                            "time",
                                                            "pace"))
        lines.append(heading)

        for act in self.data.current.children:
            line = ("{a.date:%d %b}: {a.name:<20.20} {a.distance:7,.1f} "
                    "{a.formatTime:>10} {a.formatPace:>6}").format(a=act)
            lines.append(line)

        sub = ("\n{a.date:%b %y}: {a.name:<20.20} {a.distance:7,.1f} "
               "{a.formatTime:>10} "
               "{a.formatPace:>6}").format(a=self.data.current)
        lines.append(sub)

        for month in self.data.previous:
            line = ("{a.groupdate:%b %y}: {a.name:<20.20} {a.distance:7,.1f} "
                    "{a.formatTime:>10} {a.formatPace:>6}").format(a=month)
            lines.append(line)

        year = ("\n{a.groupdate:%Y}  : {a.name:<20.20} {a.distance:7,.1f} "
                "{a.formatTime:>10} "
                "{a.formatPace:>6}").format(a=self.data.year)
        lines.append(year)

        alltime = ("\nTOTAL : {a.name:<20.20} {a.distance:7,.1f} "
                   "{a.formatTime:>10} "
                   "{a.formatPace:>6}").format(a=self.data.alltime)
        lines.append(alltime)

        self.popup = Popup(self.qtile,
                           y=self.bar.height,
                           width=900,
                           height=900,
                           font="monospace",
                           horizontal_padding=10,
                           vertical_padding=10,
                           opacity=0.8)
        self.popup.text = "\n".join(lines)
        self.popup.height = (self.popup.layout.height +
                             (2 * self.popup.vertical_padding))
        self.popup.width = (self.popup.layout.width +
                            (2 * self.popup.horizontal_padding))
        self.popup.x = min(self.offsetx, self.bar.width - self.popup.width)
        self.popup.place()
        self.popup.draw_text()
        self.popup.unhide()
        self.popup.draw()
        self.timeout_add(self.popup_display_timeout, self.popup.kill)
