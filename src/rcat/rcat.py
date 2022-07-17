from rich.console import Console, ConsoleOptions, RenderResult
from rich.measure import Measurement
import cv2

class Image:
    def __init__(self, img):
        self.img = img

    def __bool__(self):
        return self.img is not None

    @classmethod
    def from_file(cls, fname):
        return cls(cv2.imread(fname))

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        from rich.style import Style
        from rich.color import Color
        from rich.segment import Segment
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
    import sys
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <path/to/file>")
        sys.exit()
    fname = sys.argv[-1]
    console = Console()
    if fname.lower().endswith(".md"):
        from rich.markdown import Markdown
        with open(fname, "r") as f:
            content = Markdown(f.read())
    elif fname.startswith("camera:"):
        cam_idx = int(fname.split(":")[1] or 0)
        vid = cv2.VideoCapture(cam_idx)
        ret, frame = vid.read()
        content = Image(frame)
        vid.release()
    else:
        content = Image.from_file(fname)
        # if we failed to load an image
        # try syntax highlighting
        if not content:
            from rich.syntax import Syntax
            content = Syntax.from_path(fname)
    console.print(content)

if __name__ == "__main__":
    main()

