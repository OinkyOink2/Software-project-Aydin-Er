from flask import Flask, render_template, request
from PIL import Image
import io
import base64

app = Flask(__name__)

CHARSETS = {
    "classic": "@%#*+=-:. ",
    "dense": "@$B%8&WM#*oahkbdpqwmZ0OQLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
    "blocks": "█▓▒░ .",
    "minimal": "#=:.- "
}

LABELS = {
    "classic": "Classic (@%#*... )",
    "dense": "Dense (ascii-more)",
    "blocks": "Blocks",
    "minimal": "Minimal"
}


def image_to_ascii(img: Image.Image, width: int = 120, charset_key: str = "classic") -> str:
    """                                        """
    img = img.convert("L") 

    aspect_correction = 0.5
    w, h = img.size
    new_height = max(1, int(h * (width / float(w)) * aspect_correction))
    img = img.resize((width, new_height), Image.BILINEAR)

    pixels = img.getdata()
    ramp = CHARSETS.get(charset_key, CHARSETS["classic"])
    n = len(ramp) - 1

    def px_to_char(px):
        idx = int((255 - px) / 255 * n)
        return ramp[idx]

    chars = [px_to_char(px) for px in pixels]
    lines = ["".join(chars[i:i+width]) for i in range(0, len(chars), width)]
    return "\n".join(lines)


def encode_image_to_base64(image_bytes: bytes) -> tuple[str, str]:
    """                                                        """
    try:
        im = Image.open(io.BytesIO(image_bytes))
        fmt = (im.format or 'PNG').lower()
        buf = io.BytesIO()
        im.save(buf, format=im.format or 'PNG')
        return base64.b64encode(buf.getvalue()).decode('ascii'), fmt
    except Exception:
        return base64.b64encode(image_bytes).decode('ascii'), 'png'


@app.route('/', methods=['GET', 'POST'])
def index():
    ascii_art = ''
    img_b64 = None
    img_ext = None

    width = 120
    ramp_key = 'classic'

    if request.method == 'POST':
        try:
            width = int(request.form.get('width', width))
            width = max(40, min(300, width))
        except ValueError:
            width = 120
        ramp_key = request.form.get('ramp', ramp_key)

        file = request.files.get('image')
        if file and file.filename:
            data = file.read()
            try:
                im = Image.open(io.BytesIO(data))
                ascii_art = image_to_ascii(im, width=width, charset_key=ramp_key)
                img_b64, img_ext = encode_image_to_base64(data)
            except Exception as e:
                ascii_art = f"Error: could not process the image. ({e})"
        else:
            ascii_art = "Error: please choose an image file first."

    return render_template(
        "index.html",
        ascii=ascii_art,
        img_data=img_b64,
        img_ext=img_ext or 'png',
        width=width,
        ramp=ramp_key,
        ramps=[(k, LABELS[k]) for k in CHARSETS.keys()]
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)