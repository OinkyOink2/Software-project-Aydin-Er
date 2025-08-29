from flask import Flask, render_template, request
from PIL import Image

app = Flask(__name__)

CHARSETS = {
    "classic": "@%#*+=-:. ",
    "dense": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
}

def image_to_ascii(image, new_width=100, charset="classic"):
    CHARS = CHARSETS[charset]
    width, height = image.size
    ratio = height / width / 1.65
    new_height = int(new_width * ratio)
    image = image.resize((new_width, new_height))
    image = image.convert("L")
    pixels = image.getdata()
    ascii_str = "".join([CHARS[pixel * len(CHARS) // 256] for pixel in pixels])
    ascii_lines = [ascii_str[i:i+new_width] for i in range(0, len(ascii_str), new_width)]
    return "\n".join(ascii_lines)

@app.route("/", methods=["GET", "POST"])
def home():
    ascii_art = None
    if request.method == "POST":
        file = request.files["file"]
        width = int(request.form.get("width", 100))
        charset = request.form.get("charset", "classic")
        img = Image.open(file.stream)
        ascii_art = image_to_ascii(img, width, charset)
    return render_template("index.html", ascii_art=ascii_art)

if __name__ == "__main__":
    app.run(debug=True)
