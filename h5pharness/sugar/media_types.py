"""Sugar for media-centred types: image, vidéo, audio, carrousel."""
from . import adapter
from .common import IMAGE, lines_of, media_library


def _images(text, s):
    found = []
    for ln, line in lines_of(text):
        stripped = line.strip().lstrip("-*+ ").strip()
        im = IMAGE.match(stripped)
        if im:
            found.append((ln, im))
        elif stripped:
            s.error(ln, "ligne inattendue: « ![description](image ou URL) » attendu")
    return found


@adapter("H5P.Image")
def image(text, s, arg=None):
    imgs = _images(text, s)
    if len(imgs) != 1:
        s.error(None, "une image attendue: « ![description](image) »")
        return {}
    value = media_library(imgs[0][1].group(1), imgs[0][1].group(2), imgs[0][1].group(3))
    value.pop("library", None)
    return value


@adapter("H5P.Video")
def video(text, s, arg=None):
    imgs = _images(text, s)
    return {"sources": [m.group(2) for _, m in imgs]}


@adapter("H5P.Audio")
def audio(text, s, arg=None):
    imgs = _images(text, s)
    return {"files": [m.group(2) for _, m in imgs]}


@adapter("H5P.ImageSlider")
def imageslider(text, s, arg=None):
    slides = []
    for ln, m in _images(text, s):
        img = media_library(m.group(1), m.group(2), m.group(3))
        if img.get("library") != "H5P.Image":
            s.error(ln, "le carrousel n'accepte que des images")
            continue
        slides.append({"library": "H5P.ImageSlide", "image": img})
    if len(slides) < 2:
        s.error(None, "au moins 2 images « - ![description](image) »")
    return {"imageSlides": slides}
