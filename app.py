import cv2 as cv
from werkzeug.utils import secure_filename
from playsound import playsound
from flask import Flask,render_template,request,url_for,Response,stream_with_context,session,flash,make_response
app = Flask(__name__, instance_relative_config=True, template_folder='template')
app.secret_key="hello"
filenames=""
filenamess=""
message=""
path=""
capacity=0
capacity1=0
capacity2=0
@app.route('/')
def hellos():
    return render_template('home.html')
@app.route('/through_image')
def through_image():
    return render_template('image.html')
def gen1(image,capacity):
    img=cv.cvtColor(image,cv.COLOR_RGB2GRAY)
    face_cascade=cv.CascadeClassifier(cv.data.haarcascades+'haarcascade_frontalface_alt2.xml')
    detect=face_cascade.detectMultiScale(img,scaleFactor=1.1,minNeighbors=5)
    i=0
    for x,y,w,h in detect:
        rectangle=cv.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        i=i+1
        if i<=capacity:
            rectangle=cv.putText(rectangle,'face num'+str(i),(x-20,y-10),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),1)
        else:
            rectangle=cv.putText(rectangle,'exceeded',(50,50),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),1)
            playsound("/static/sai.mp3")
    imjpeg=cv.imencode('.jpg',rectangle)[1].tobytes()
    yield(b'--frame\r\n'+b'Content-Type: image/jpeg\r\n\r\n' + imjpeg + b'\r\n\r\n')
@app.route('/through_images',methods=['GET','POST'])
def through_images():
    if request.method=='POST':
        f=request.files['image[]']
        global filenames
        filenames=""
        global capacity1
        capacity1=0
        f1=request.form['Capacity']
        capacity1=int(f1)
        l=0
        filenames+=secure_filename(f.filename)
        l=len(filenames)
        f.save('Upload_Folder/'+secure_filename(f.filename))
        print(filenames)
    return render_template('imageoutput.html')
@app.route('/through_imagess')
def through_imagess():
    img=cv.imread('/Upload_Folder/'+filenames) 
    return Response(stream_with_context(gen1(img,capacity1)),mimetype='multipart/x-mixed-replace; boundary=frame')
def gen2(path,capacity):
    print(path)
    global capacity2
    global message
    face_cascade=cv.CascadeClassifier(cv.data.haarcascades+'haarcascade_frontalface_default.xml')
    eyes_cascade=cv.CascadeClassifier(cv.data.haarcascades+'haarcascade_eye.xml')
    #cap=cv.VideoCapture('path')
    '''d=cap.isOpened()
    if d==1:
        pass
    else:
        cap.Open()'''
    cap=cv.VideoCapture(path)
    count_img=0
    while (count_img<=100):
        ret,img =cap.read()
        count_img+=1
        #img = cv.resize(image, (0,0), fx=0.5, fy=0.5) 
        faces=face_cascade.detectMultiScale(img,scaleFactor=1.1,minNeighbors=5)
        i=0                   
        for(x,y,w,h) in faces:
            rectangle=cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            i=i+1
            if i<=capacity:
                rectangle=cv.putText(rectangle,'face num'+str(i),(x-10,y-10),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
            else:
                rectangle=cv.putText(rectangle,'exceeded',(50,50),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
                playsound("/static/sai.mp3")            
            jpegs = cv.imencode('.jpg', rectangle)[1].tobytes()
            yield (b'--frame\r\n'+b'Content-Type: image/jpeg\r\n\r\n' + jpegs + b'\r\n\r\n')
    cap.release()
    cv.destroyAllWindows()
@app.route('/through_imagerec')
def through_imagerec():
    return render_template('imagerec.html')
@app.route('/through_imagesrec',methods=['GET','POST'])
def through_imagesrec():
    if request.method=='POST':
        f=request.files['image[]']
        global filenamess
        filenamess=""
        global path
        path=""
        global capacity2
        capacity2=0
        f1=request.form['Capacity']
        capacity2=int(f1)
        l=0
        filenamess+=secure_filename(f.filename)
        l=len(filenamess)
        print(l)
        print(filenamess)
        print(capacity2)
        f.save('Upload_Folder/'+secure_filename(f.filename))
        path+='/Upload_Folder/'+filenamess
        #print(path)
    return render_template('imagerecoutput.html',capacity=capacity2)
@app.route('/through_imagessrec')
def through_imagessrec():
    #img=cv.VideoCapture(path) 
    #print(path)
    return Response(stream_with_context(gen2(path,capacity2)),mimetype='multipart/x-mixed-replace; boundary=frame')
def gen():
    global capacity
    global message
    face_cascade=cv.CascadeClassifier(cv.data.haarcascades+'haarcascade_frontalface_default.xml')
    eyes_cascade=cv.CascadeClassifier(cv.data.haarcascades+'haarcascade_eye.xml')
    cap=cv.VideoCapture(0)
    '''d=cap.isOpened()
    if d==1:
        pass
    else:
        cap.Open()'''
    cap=cv.VideoCapture(0)
    count_img=0
    while (cap.isOpened() and count_img<=100):
        ret,img =cap.read()
        count_img+=1
        img = cv.resize(img, (0,0), fx=0.5, fy=0.5) 
        faces=face_cascade.detectMultiScale(img,scaleFactor=1.1,minNeighbors=5)
        i=0                   
        for(x,y,w,h) in faces:
            rectangle=cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            i=i+1
            if i<=capacity:
                rectangle=cv.putText(rectangle,'face num'+str(i),(x-10,y-10),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
            else:
                rectangle=cv.putText(rectangle,'exceeded',(50,50),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
                playsound("/static/sai.mp3")            
            jpegs = cv.imencode('.jpg', rectangle)[1].tobytes()
            yield (b'--frame\r\n'+b'Content-Type: image/jpeg\r\n\r\n' + jpegs + b'\r\n\r\n')
            if(cv.waitKey(1) & 0xFF ==ord('q')):
                break
    cap.release()
    cv.destroyAllWindows()
@app.route('/through_video')
def through_video():
    return render_template('video.html')   
@app.route('/through_videos',methods=['GET','POST'])
def through_videos():
    global capacity
    if request.method=="POST":
        f=request.form['text']
        f=int(f)
        capacity=f
    return render_template('outputvideo.html',capacity=f)
@app.route('/detecting')
def detecting():
    return Response(stream_with_context(gen()),mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__=='__main__':
    app.run(debug="True")