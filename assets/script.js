const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let ws;

// Inicia a câmera com alta qualidade
const videoConstraints = {
    video: {
        width: { ideal: 1280 },
        height: { ideal: 720 },
        frameRate: { ideal: 30, max: 60 },
        facingMode: 'user',
        aspectRatio: { ideal: 16/9 }
    }
};

navigator.mediaDevices.getUserMedia(videoConstraints)
    .then(stream => {
        video.srcObject = stream;
        video.onloadedmetadata = () => initWS();
    })
    .catch(err => {
        console.error('Erro ao acessar câmera:', err);
        // Fallback para configuração padrão
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                video.srcObject = stream;
                video.onloadedmetadata = () => initWS();
            });
    });

function initWS() {
    const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
    ws = new WebSocket(`${protocol}//${location.host}/ws`);

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        // 1. ATUALIZA LABELS E CONFIABILIDADE (O que você pediu)
        const labelsContainer = document.getElementById('labels-container');
        if (labelsContainer) {
            if (data.labels && data.labels.length > 0) {
                // Monta o texto com o nome do gesto e a confiança (%)
                labelsContainer.innerHTML = data.labels.map(l =>
                    `<span>${l.hand}: <strong>${l.gesture}</strong> (${l.confidence}%)</span>`
                ).join('');
            } else {
                labelsContainer.innerHTML = "Nenhum gesto detectado";
            }
        }

        // 2. ATUALIZA IMAGEM DO GESTO (JOINHA, PAZ, ETC)
        const gestureImg = document.getElementById('gesture-img');
        if (gestureImg) {
            if (data.gesture_image) {
                gestureImg.src = `/assets/images/gestures/${data.gesture_image}`;
                gestureImg.style.visibility = 'visible';
                gestureImg.style.opacity = '1';
            } else {
                gestureImg.style.visibility = 'hidden';
                gestureImg.style.opacity = '0';
            }
        }

        // 3. ATUALIZA ANIMAIS DETECTADOS
        const animalsContainer = document.getElementById('animals-container');
        if (animalsContainer) {
            if (data.animals && data.animals.length > 0) {
                animalsContainer.innerHTML = data.animals.map(a =>
                    `<div class="animal-item">🐾 <strong>${a.animal}</strong> (${a.confidence}%)</div>`
                ).join('');
            } else {
                animalsContainer.innerHTML = "Nenhum animal detectado";
            }
        }

        // 4. ATUALIZA FPS
        const fpsCounter = document.getElementById('fps-counter');
        if (fpsCounter) fpsCounter.innerText = data.fps;

        // 5. DESENHA O VÍDEO PROCESSADO
        const img = new Image();
        img.onload = () => {
            // Interpolação de alta qualidade
            ctx.imageSmoothingEnabled = true;
            ctx.imageSmoothingQuality = 'high';

            // Limpa e desenha
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0);

            setTimeout(sendFrame, 30);
        };
        img.src = data.image;
    };

    ws.onopen = () => sendFrame();
    ws.onerror = (error) => console.error('Erro no WebSocket:', error);
    ws.onclose = () => setTimeout(initWS, 1000);
}

function sendFrame() {
    if (ws && ws.readyState === WebSocket.OPEN && video.videoWidth > 0) {
        const qualitySlider = document.getElementById('quality-slider');
        const qualityVal = document.getElementById('quality-val');
        const landmarkCheckbox = document.getElementById('show-landmarks-check');
        const animalsCheckbox = document.getElementById('detect-animals-check');

        // Atualiza o texto da qualidade na tela (ex: 50%)
        if (qualitySlider && qualityVal && !qualitySlider.hasAttribute('data-listener')) {
            qualitySlider.setAttribute('data-listener', 'true');
            qualitySlider.addEventListener('input', (e) => {
                qualityVal.innerText = `${Math.round(parseFloat(e.target.value) * 100)}%`;
            });
        }

        const quality = qualitySlider ? parseFloat(qualitySlider.value) : 0.5;
        // Pega o estado dos checkboxes
        const showLandmarks = landmarkCheckbox ? landmarkCheckbox.checked : true;
        const detectAnimals = animalsCheckbox ? animalsCheckbox.checked : true;

        const tempCanvas = document.createElement('canvas');
        tempCanvas.width = canvas.width;
        tempCanvas.height = canvas.height;
        const tempCtx = tempCanvas.getContext('2d');

        // Melhora a qualidade do downscaling (HD → 640x480)
        tempCtx.imageSmoothingEnabled = true;
        tempCtx.imageSmoothingQuality = 'high';
        tempCtx.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Envia o pacote completo para o Python
        const payload = {
            msg: tempCanvas.toDataURL('image/jpeg', quality),
            quality: quality,
            show_landmarks: showLandmarks,
            detect_animals: detectAnimals
        };
        ws.send(JSON.stringify(payload));
    }
}