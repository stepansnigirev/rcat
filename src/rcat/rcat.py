from rich.console import Console, ConsoleOptions, RenderResult
from rich.measure import Measurement
from rich.style import Style
from rich.color import Color
from rich.segment import Segment
import cv2
import sys

class Image:
    def __init__(self, img):
        self.img = img

    @classmethod
    def from_file(cls, fname):
        return cls(cv2.imread(fname))

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        maxsize = ((options.max_height-1)*2, options.max_width)
        original = self.img.shape[:2]
        scale = min([sz/o for sz, o in zip(maxsize, original)])
        sznew = [round(x*scale) for x in reversed(original)]
        img = cv2.resize(self.img, dsize=sznew, interpolation=cv2.INTER_CUBIC)
        for y in range(len(img)//2):
            for x in range(len(img[0])):
                c = img[2*y][x]
                bgcolor = Color.from_rgb(c[2], c[1], c[0])
                c = img[2*y+1][x]
                color = Color.from_rgb(c[2], c[1], c[0])
                yield Segment("▄", Style(color=color, bgcolor=bgcolor))
            yield Segment("\r\n")

    def __rich_measure__(self, console: Console, options: ConsoleOptions) -> Measurement:
        return Measurement(8, options.max_width)

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <path/to/file>")
        sys.exit()
    fname = sys.argv[-1]
    c = Console()
    img = Image.from_file(fname)
    maxsize = (c.width, c.height*2)
    c.print(img)

if __name__ == "__main__":
    main()

