from flask import Flask,render_template,Response
import cv2
from YOLOv8InferenceClass import ObjectDetection 
app=Flask(__name__)
camera=cv2.VideoCapture(0)
#frame_width, frame_height = camera.get(3), camera.get(4)  # Get the frame width and height
#frame_aspect_ratio = frame_width / frame_height


def generate_frames():
    while True:
            
        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    detector = ObjectDetection(capture_index=0)
    return Response( detector(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True)
