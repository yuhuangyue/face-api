const video = document.getElementById('video')

Promise.all([
    faceapi.nets.tinyFaceDetector.loadFromUri('/models'),
    faceapi.nets.faceLandmark68Net.loadFromUri('/models'),
    faceapi.nets.faceRecognitionNet.loadFromUri('/models'),
    faceapi.nets.faceExpressionNet.loadFromUri('/models')
]).then(startVideo)

function startVideo(){
    navigator.getUserMedia(
        { video:{} },
        stream => video.srcObject = stream,
        err => console.error(err)
    )
}

async function test(im){
    // 调用python函数
    const res = await eel.image_process (im)();
    console.log(res);
}

video.addEventListener('play',() => {
    const canvas = faceapi.createCanvasFromMedia(video)
    document.body.append(canvas)
    const displaySize = { width:video.width, height: video.height }


    const ctx = canvas.getContext('2d')
    faceapi.matchDimensions(canvas, displaySize)


    setInterval(async () => {

        const uint8ClampedArray = ctx.getImageData(0, 0, video.width, video.height).data
        // console.log(uint8ClampedArray)

        const detections = await faceapi.detectAllFaces(video,new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceExpressions()
        const resizeDetections = faceapi.resizeResults(detections,displaySize)

        ctx.clearRect(0,0,canvas.width,canvas.height)

        faceapi.draw.drawDetections(canvas, resizeDetections)

        faceapi.draw.drawFaceLandmarks(canvas, resizeDetections)
        faceapi.draw.drawFaceExpressions(canvas, resizeDetections)



        // ctx.drawImage(video, 0, 0, video.width, video.height)




    },100)


})