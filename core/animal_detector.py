import cv2
import numpy as np
from ultralytics import YOLO

class AnimalDetector:
    def __init__(self):
        """Inicializa o detector YOLO para animais"""
        # Carrega o modelo YOLOv8 nano (rápido e leve)
        self.model = YOLO('yolov8n.pt')

        # Classes de animais do COCO dataset
        self.animal_classes = {
            14: 'passaro',
            15: 'gato',
            16: 'cachorro',
            17: 'cavalo',
            18: 'ovelha',
            19: 'vaca',
            20: 'elefante',
            21: 'urso',
            22: 'zebra',
            23: 'girafa'
        }

    def detect(self, frame, confidence_threshold=0.5):
        """
        Detecta animais no frame

        Args:
            frame: Frame da webcam (BGR)
            confidence_threshold: Confiança mínima para detecção

        Returns:
            detections: Lista de dicionários com {class, confidence, bbox}
        """
        detections = []

        # Executa a detecção
        results = self.model(frame, verbose=False)

        # Processa os resultados
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Pega a classe e confiança
                cls = int(box.cls[0])
                conf = float(box.conf[0])

                # Verifica se é um animal e se a confiança é alta o suficiente
                if cls in self.animal_classes and conf >= confidence_threshold:
                    # Pega as coordenadas da bounding box
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

                    detections.append({
                        'class': self.animal_classes[cls],
                        'confidence': round(conf * 100, 1),
                        'bbox': (int(x1), int(y1), int(x2), int(y2))
                    })

        return detections

    def draw_detections(self, frame, detections):
        """
        Desenha as detecções no frame

        Args:
            frame: Frame BGR
            detections: Lista de detecções

        Returns:
            frame: Frame com as detecções desenhadas
        """
        for det in detections:
            x1, y1, x2, y2 = det['bbox']

            # Desenha retângulo
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 107, 107), 3)

            # Prepara o texto
            label = f"{det['class']}: {det['confidence']}%"

            # Calcula o tamanho do texto
            (text_width, text_height), _ = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2
            )

            # Desenha fundo para o texto
            cv2.rectangle(
                frame,
                (x1, y1 - text_height - 10),
                (x1 + text_width + 10, y1),
                (255, 107, 107),
                -1
            )

            # Desenha o texto
            cv2.putText(
                frame,
                label,
                (x1 + 5, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )

        return frame
