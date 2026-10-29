import io

from PIL import Image, ImageDraw, ImageFont

from .analysis import limit_display_confidence


def safe_font(size=28):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        return ImageFont.load_default()


def make_report_image(original_image, heatmap_image, predicted_class, confidence, timestamp_text):
    display_confidence = limit_display_confidence(confidence)
    width = 1600
    height = 980
    bg = (239, 230, 216)
    accent = (192, 6, 70)
    green = (48, 57, 31)
    white = (255, 252, 247)
    text = (48, 57, 31)
    soft = (115, 94, 87)

    canvas = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(canvas)

    title_font = safe_font(54)
    subtitle_font = safe_font(28)
    text_font = safe_font(34)
    small_font = safe_font(24)

    draw.rounded_rectangle((40, 35, 1560, 170), radius=30, fill=accent)
    draw.text((70, 60), "Relatório de análise - Mobo IA Lichia", fill=white, font=title_font)
    draw.text((70, 122), f"Gerado em: {timestamp_text}", fill=white, font=subtitle_font)

    result_color = green if confidence >= 0.90 else accent
    draw.rounded_rectangle((40, 205, 1560, 355), radius=26, fill=white, outline=accent, width=6)
    draw.text((70, 235), f"Classe prevista: {predicted_class}", fill=text, font=text_font)
    draw.text((70, 285), f"Confiança: {display_confidence:.2%}", fill=result_color, font=text_font)

    img_w, img_h = 650, 520
    original_resized = original_image.resize((img_w, img_h))
    heatmap_resized = heatmap_image.resize((img_w, img_h))

    canvas.paste(original_resized, (70, 400))
    canvas.paste(heatmap_resized, (880, 400))

    draw.rounded_rectangle((60, 390, 730, 930), radius=18, outline=accent, width=6)
    draw.rounded_rectangle((870, 390, 1540, 930), radius=18, outline=accent, width=6)

    draw.text((280, 935), "Imagem original", fill=soft, font=small_font)
    draw.text((1060, 935), "Heatmap da atenção da IA", fill=soft, font=small_font)

    return canvas


def pil_to_png_bytes(image):
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


def pil_to_pdf_bytes(image):
    buffer = io.BytesIO()
    image_rgb = image.convert("RGB")
    image_rgb.save(buffer, format="PDF")
    buffer.seek(0)
    return buffer
