import cv2
import mediapipe as mp
import numpy as np
from .models import get_mediapipe_options, load_custom_models
from .animal_detector import AnimalDetector

class GestureProcessor:
    def __init__(self):
        self.clf, self.label_encoder = load_custom_models()
        self.options = get_mediapipe_options()
        self.recognizer = mp.tasks.vision.GestureRecognizer.create_from_options(self.options)

        # Conexões com cores para cada parte da mão
        # Formato: (ponto1, ponto2, cor_BGR)
        self.CONNECTIONS = [
            # Polegar - Vermelho
            ((0,1), (0, 0, 255)),
            ((1,2), (0, 0, 255)),
            ((2,3), (0, 0, 255)),
            ((3,4), (0, 0, 255)),

            # Indicador - Verde
            ((0,5), (0, 255, 0)),
            ((5,6), (0, 255, 0)),
            ((6,7), (0, 255, 0)),
            ((7,8), (0, 255, 0)),

            # Médio - Azul
            ((9,10), (255, 0, 0)),
            ((10,11), (255, 0, 0)),
            ((11,12), (255, 0, 0)),

            # Anelar - Amarelo
            ((13,14), (0, 255, 255)),
            ((14,15), (0, 255, 255)),
            ((15,16), (0, 255, 255)),

            # Mindinho - Magenta
            ((0,17), (255, 0, 255)),
            ((17,18), (255, 0, 255)),
            ((18,19), (255, 0, 255)),
            ((19,20), (255, 0, 255)),

            # Palma - Ciano
            ((5,9), (255, 255, 0)),
            ((9,13), (255, 255, 0)),
            ((13,17), (255, 255, 0))
        ]

        # Inicializa o detector de animais
        try:
            self.animal_detector = AnimalDetector()
            self.animals_enabled = True
        except Exception as e:
            print(f"Aviso: Detector de animais não disponível: {e}")
            self.animal_detector = None
            self.animals_enabled = False

    def process_frame(self, frame, draw_landmarks=True, detect_animals=True):
        labels = []
        animals = []
        gesture_image = None
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detecção de animais (antes de desenhar as landmarks)
        if detect_animals and self.animals_enabled and self.animal_detector:
            try:
                animal_detections = self.animal_detector.detect(rgb_frame, confidence_threshold=0.4)
                if animal_detections:
                    frame = self.animal_detector.draw_detections(frame, animal_detections)
                    animals = [
                        {
                            'animal': det['class'],
                            'confidence': det['confidence']
                        }
                        for det in animal_detections
                    ]
            except Exception as e:
                print(f"Erro na detecção de animais: {e}")

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        timestamp_ms = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)
        recognition_result = self.recognizer.recognize_for_video(mp_image, timestamp_ms)

        if recognition_result.hand_landmarks:
            for i, hand_landmarks in enumerate(recognition_result.hand_landmarks):
                # 1. Desenho condicional
                if draw_landmarks:
                    # Linhas coloridas por parte da mão
                    for (conn, color) in self.CONNECTIONS:
                        p1, p2 = hand_landmarks[conn[0]], hand_landmarks[conn[1]]
                        cv2.line(frame, (int(p1.x*w), int(p1.y*h)), (int(p2.x*w), int(p2.y*h)), color, 2, cv2.LINE_AA)
                    # Pontos Brancos
                    for lm in hand_landmarks:
                        cv2.circle(frame, (int(lm.x*w), int(lm.y*h)), 4, (255, 255, 255), -1, cv2.LINE_AA)

                # 2. Predição (Sempre roda)
               # --- PREDIÇÃO (Sempre ativa) ---
                try:
                    hand_label = recognition_result.handedness[i][0].category_name
                    h_val = 0 if hand_label == 'Left' else 1
                    
                    # Monta o vetor de características
                    feat = [h_val]
                    for lm in hand_landmarks: feat.extend([lm.x, lm.y, lm.z])
                    
                    features = np.array(feat).reshape(1, -1)
                    
                    # PEGA A PROBABILIDADE REAL DO MODELO
                    probabilities = self.clf.predict_proba(features)[0]
                    prediction_idx = np.argmax(probabilities)
                    
                    # CALCULA A CONFIANÇA REAL (0.0 a 1.0)
                    confidence_raw = float(probabilities[prediction_idx])
                    gesture_name = self.label_encoder.inverse_transform([prediction_idx])[0]
                    
                    labels.append({
                        "hand": hand_label, 
                        "gesture": gesture_name, 
                        # FORMATA PARA EXIBIR 1 CASA DECIMAL (ex: 98.5)
                        "confidence": round(confidence_raw * 100, 1)
                    })
                except Exception as e:
                    print(f"Erro na predição: {e}")

        if len(labels) == 2 and labels[0]['gesture'] == labels[1]['gesture']:
            gesture_image = f"{labels[0]['gesture']}.png"

        return frame, labels, gesture_image, animals