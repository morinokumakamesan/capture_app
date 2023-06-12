// device_idの発行
var deviceId = "";
if(!localStorage.getItem('deviceId')) {
    var deviceId = Math.random().toString(32).substring(2);
    localStorage.setItem('deviceId', deviceId);
}
deviceId = localStorage.getItem('deviceId');
document.getElementById("device_id").innerHTML = deviceId;

var video = document.getElementById('video');
// getUserMedia()でカメラ映像の取得
var media = navigator.mediaDevices.getUserMedia({ video: {facingMode: "environment"} });

//リアルタイム再生（ストリーミング）を行うためにビデオタグに流し込む
media.then((stream) => {
    video.srcObject = stream;
});

var canvas = document.getElementById('canvas');
canvas.setAttribute('width', video.width);
canvas.setAttribute('height', video.height);

video.addEventListener(
    'timeupdate',
    function () {
        var context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, video.width, video.height);
    },
    true
);

var intervalId = null;
function startCam(){
    context = canvas.getContext('2d');
    var img_base64 = canvas.toDataURL('image/jpeg').replace(/^.*,/, '')
    captureImg(img_base64);
}

var xhr = new XMLHttpRequest();

// キャプチャ画像データ(base64)をPOST
function captureImg(img_base64) {
    const body = new FormData();
    body.append('img', img_base64);
    body.append('deviceId', deviceId);

    // Render
    xhr.open('POST', 'https://capture-app.onrender.com/capture_img', true);
    // ローカル
    // xhr.open('POST', 'http://localhost:10000/capture_img', true);

    xhr.onload = () => {
        console.log(xhr.responseText)
    };
    xhr.send(body);
}

// LINE_APIのイベント発火による画像の撮影
var socket = io();
console.log(socket)
socket.on('connect', () => {
    const initialData = {
    socketId: socket.id,
    deviceId: deviceId
    };
    socket.emit('initial_data', initialData);
});

socket.on('img_event', (msg) => {
    startCam();
});