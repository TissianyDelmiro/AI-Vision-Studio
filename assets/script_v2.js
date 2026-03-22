const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let ws;

navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
    video.srcObject = stream;
    video.onloadedmetadata = () => initWS();
});

function initWS() {
    const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
    ws = new WebSocket(`${protocol}//${location.host}/ws`);
    
    ws.onmessage = (event) => {
        console.log("Recebido:", event.data.substring(0, 100) + "...");
        const data = JSON.parse(event.data);
        
        // Atualiza os labels
        const labelsContainer = document.getElementById('labels-container');
        if (labelsContainer) {
            if (data.labels.length > 0) {
                labelsContainer.innerHTML = data.labels.map(l => 
                    `<span>${l.hand}: ${l.gesture} (${l.confidence}%)</span>`
                ).join(' | ');
            } else {
                labelsContainer.innerHTML = "Nenhum gesto detectado";
            }
        }

        // Atualiza a imagem do gesto
        const gestureImg = document.getElementById('gesture-img');
        if (gestureImg) {
            if (data.gesture_image) {
                gestureImg.src = `/assets/images/gestures/${data.gesture_image}`;
                gestureImg.style.visibility = 'visible';
                gestureImg.style.opacity = '1';
                gestureImg.style.transform = 'scale(1)';
            } else {
                gestureImg.style.visibility = 'hidden';
                gestureImg.style.opacity = '0';
                gestureImg.style.transform = 'scale(0.9)';
            }
        }

        // Atualiza o FPS
        const fpsCounter = document.getElementById('fps-counter');
        if (fpsCounter && data.fps !== undefined) {
            fpsCounter.innerText = data.fps;
        }
        
        const img = new Image();
        img.onload = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0);
            setTimeout(sendFrame, 30);
        };
        img.onerror = () => console.error("Erro ao carregar imagem:", img.src.substring(0, 100));
        img.src = data.image;
    };

    ws.onopen = () => sendFrame();
    ws.onclose = () => setTimeout(initWS, 1000);
}

function sendFrame() {
    if (ws && ws.readyState === WebSocket.OPEN && video.videoWidth > 0) {
        const qualitySlider = document.getElementById('quality-slider');
        const qualityVal = document.getElementById('quality-val');
        
        if (qualitySlider && qualityVal && !qualitySlider.hasAttribute('data-listener')) {
            qualitySlider.setAttribute('data-listener', 'true');
            qualitySlider.addEventListener('input', (e) => {
                const percent = Math.round(parseFloat(e.target.value) * 100);
                qualityVal.innerText = `${percent}%`;
            });
        }

        const quality = qualitySlider ? parseFloat(qualitySlider.value) : 0.5;
        const landmarksCheckbox = document.getElementById('toggle-landmarks');
        const showLandmarks = landmarksCheckbox ? landmarksCheckbox.checked : true;

        // Captura o frame do vídeo e envia
        const tempCanvas = document.createElement('canvas');
        tempCanvas.width = canvas.width;
        tempCanvas.height = canvas.height;
        const tempCtx = tempCanvas.getContext('2d');
        tempCtx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        const data = tempCanvas.toDataURL('image/jpeg', quality);
        const payload = {
            msg: data,
            quality: quality,
            show_landmarks: showLandmarks
        };
        console.log("Enviando JSON. Landmarks:", showLandmarks);
        ws.send(JSON.stringify(payload));
    }
}

// Helper to match Python's json_stringify if needed, 
// though standard JSON.stringify is usually what's meant.
function json_stringify(obj) {
    return JSON.stringify(obj);
}
