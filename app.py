from fasthtml.common import *
from core.processor import GestureProcessor
from core.utils import decode_image, encode_image
import json
import warnings
import time

warnings.filterwarnings("ignore", category=UserWarning)

app, rt = fast_app(exts='ws')
processor = GestureProcessor()

@rt("/")
def get():
    return (
        Title("AI Vision Studio - Gesture & Animal Detection"),
        Link(rel="stylesheet", href="/assets/style.css?v=clean-quality"),
        Main(
            Div(H1("AI Vision Studio"), cls="title-bar"),
            Div(
                # Layout em duas colunas
                Div(
                    # Coluna 1: Webcam
                    Div(
                        Video(id="video", autoplay=True, playsinline=True, style="display:none"),
                        Canvas(id="canvas", width="640", height="480"),
                        Div(Span("0.0", id="fps-counter"), Span(" FPS"), cls="fps-badge"),
                        cls="card video-card"
                    ),
                    # Coluna 2: Controles + Detecções (vertical)
                    Div(
                        # Controles em cima
                        Div(
                            Div(
                                Span("⚙️ Configurações", cls="controls-title"),
                                cls="controls-header"
                            ),
                            Div(
                                Label(
                                    Input(type="checkbox", id="show-landmarks-check", checked=True),
                                    Span(" Hand Landmarks"),
                                    cls="label-with-value"
                                ),
                                cls="control-item"
                            ),
                            Div(
                                Label(
                                    Input(type="checkbox", id="detect-animals-check", checked=True),
                                    Span(" Detectar Animais"),
                                    cls="label-with-value"
                                ),
                                cls="control-item"
                            ),
                            Div(
                                Label(
                                    Span("Qualidade"),
                                    Span("80%", id="quality-val", cls="quality-badge"),
                                    _for="quality-slider", cls="label-with-value"
                                ),
                                Input(type="range", id="quality-slider", min="0.1", max="1.0", step="0.1", value="0.8"),
                                cls="control-item"
                            ),
                            cls="controls-panel card"
                        ),
                        # Detecções embaixo
                        Div(
                            Div(
                                Div(
                                    Span("👋 Gestos", cls="section-title"),
                                    cls="section-header"
                                ),
                                Div("Nenhum gesto detectado", id="labels-container"),
                                Img(id="gesture-img"),
                                cls="gesture-info"
                            ),
                            Div(
                                Div(
                                    Span("🐾 Animais", cls="section-title"),
                                    cls="section-header"
                                ),
                                Div("Nenhum animal detectado", id="animals-container"),
                                cls="animals-info"
                            ),
                            cls="detections-panel card"
                        ),
                        cls="right-column"
                    ),
                    cls="main-row"
                ),
                cls="main-container"
            ),
            Script(src="/assets/script.js?v=8-clean-quality")
        )
    )

@app.ws("/ws")
async def ws(data: dict, send):
    try:
        t0 = time.time()
        show_landmarks = data.get('show_landmarks', True)
        detect_animals = data.get('detect_animals', True)
        quality = data.get('quality', 0.5)
        msg_data = data.get('msg', '')

        img = decode_image(msg_data)
        if img is not None:
            # Passamos show_landmarks e detect_animals para o processador
            processed_img, labels, gesture_image, animals = processor.process_frame(
                img,
                draw_landmarks=show_landmarks,
                detect_animals=detect_animals
            )

            response = {
                "image": encode_image(processed_img, quality=int(quality * 100)),
                "labels": labels,
                "gesture_image": gesture_image,
                "animals": animals,
                "fps": round(1.0 / (time.time() - t0 + 0.001), 1)
            }
            await send(json.dumps(response))
    except Exception as e:
        print(f"Erro no WebSocket: {e}")

if __name__ == "__main__":
    serve(port=7860, host='0.0.0.0')