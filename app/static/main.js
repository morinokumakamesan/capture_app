var video = document.getElementById('video');
// getUserMedia()でカメラ映像の取得
var media = navigator.mediaDevices.getUserMedia({ video: true });
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

var button = document.getElementById('cam');
button.addEventListener('click', (event) => {
    context = canvas.getContext('2d');
    // 取得したbase64データのヘッドを取り除く
    var img_base64 = canvas.toDataURL('image/jpeg').replace(/^.*,/, '')
    captureImg(img_base64);
    // }
});

var xhr = new XMLHttpRequest();

// キャプチャ画像データ(base64)をPOST
function captureImg(img_base64) {
    const body = new FormData();
    body.append('img', img_base64);
    // Render
    xhr.open('POST', 'https://capture-app.onrender.com/capture_img', true);
    // ローカル
    // xhr.open('POST', 'http://localhost:10000/capture_img', true);
    xhr.onload = () => {
        console.log(xhr.responseText)
    };
    xhr.send(body);
}