#import numpy as np
import cv2 as cv
#import os
#import pyttsx3
from werkzeug.utils import secure_filename
#from camera import VideoCamera
from playsound import playsound
from flask import Flask,render_template,request,url_for,Response,stream_with_context,session,flash,make_response
app = Flask(__name__, instance_relative_config=True, template_folder='template')
app.secret_key="hello"
filenames=""
message=""
capacity=0
capacity1=0
@app.route('/')
def hellos():
    return render_template('home.html')
    #app.debug="TRUE"
    #return app
@app.route('/through_image')
def through_image():
    return render_template('image.html')
def gen1(image,capacity):
    #img=cv.resize(image,(0,0),fx=0.5,fy=0.5)
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
            playsound("/Users/saikscbs/Documents/project2/proj3/sai.mp3")
            #engine = pyttsx3.init()
            #engine.say('Limit Exceeded.')
            #engine.runAndWait()
            #engine.startLoop(True)
            #engine.stop()
            # engine.iterate() must be called inside Server_Up.start()
            #Server_Up = threading.Thread(target = Comm_Connection)
            #Server_Up.start()
            #engine.endLoop()
            #if engine._inLoop:
            #engine.endLoop()
            #file = "w.wav"
            #print('playing sound using native player')
            #os.system("afplay " + file)
            #os.system("afplay sound.wav&")
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
        if l>0:
            print(1)
        f.save('/Users/saikscbs/Documents/project2/proj3/Upload_Folder/'+secure_filename(f.filename))
    return render_template('imageoutput.html')
@app.route('/through_imagess')
def through_imagess():
    img=cv.imread('/Users/saikscbs/Documents/project2/proj3/Upload_Folder/'+filenames)
    print(filenames)
    #Response(gen1(img),mimetype='multipart/x-mixed-replace; boundary=frame')  
    return Response(stream_with_context(gen1(img,capacity1)),mimetype='multipart/x-mixed-replace; boundary=frame')
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
        #session["capacity"]=f
    #cap.release()
    #cv.destroyALLWindows()
    #return Response(f,mimetype='multipart/x-mixed-replace; boundary=frame')
    #return Response(cv.imshow('ractangled image',rectangle),mimetype='multipart/x-mixed-replace; boundary=frame')
    #return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')
    return render_template('outputvideo.html',capacity=f)
def gen():
    global capacity
    global message
    #capacity=0
    face_cascade=cv.CascadeClassifier(cv.data.haarcascades+'haarcascade_frontalface_default.xml')
    eyes_cascade=cv.CascadeClassifier(cv.data.haarcascades+'haarcascade_eye.xml')
    #img=cv.imread('/Users/saikscbs/Desktop/proj3/i.jpg')
    cap=cv.VideoCapture(0)
    d=cap.isOpened()
    if d==1:
        pass
    else:
        cap.Open()
    cap=cv.VideoCapture(0)
    count_img=0
    while (cap.isOpened() and count_img<=100):
        ret,img =cap.read()
        count_img+=1
        #print(img)
        #cv.imshow('boxer',img)
        img = cv.resize(img, (0,0), fx=0.5, fy=0.5) 
        faces=face_cascade.detectMultiScale(img,scaleFactor=1.1,minNeighbors=5)
        #print(faces)
        i=0                   
        for(x,y,w,h) in faces:
            #print("drawing rectangles")
            rectangle=cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            i=i+1
            
            '''if 'capacity' in session:
                session["capacities"]=i'''
            '''if i<=capacity:
                yield str("capacity is in limit")
            else:
                yield str("capacity limit exceeded")'''
            if i<=capacity:
                rectangle=cv.putText(rectangle,'face num'+str(i),(x-10,y-10),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
            else:
                rectangle=cv.putText(rectangle,'exceeded',(50,50),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
                playsound("/Users/saikscbs/Documents/project2/proj3/sai.mp3")
                #engine = pyttsx3.init()
                #engine.say('Limit Exceeded.')
                #engine.runAndWait()
            '''if i<=capacity:
                message+=str("capacity is in limit")
            else:
                message+=str("capacity limit exceeded")'''
            '''if i<=capacity:
                Response("capacity is in limit")
            else:
                Response("capacity limit exceeded")'''
            '''if i<=capacity:
                return render_template('outputvideo.html',x=str("capacity is in limit"))
            else:
                return render_template('outputvideo.html',x=str("capacity limit exceeded"))'''
            
            #print(img,i)
            #cv.imshow('boxer',rectangle)
            #height=int(cap.get(4))
            #width=int(cap.get(3))
            #fps=cap.get(cv.CAP_PROP_FPS)
            #fourcc=cv.VideoWriter_fourcc(*'mp4v')
            #PATH='Users/saikscbs/Documents/project2/proj3/static/demo.webm'
            #frameSize=[]
            #out=cv.VideoWriter('rectangle.mp4',fourcc,20.0,(640,480))
            #out.write(rectangle)
            #jpegs = cv.resize(jpegs, (0,0), fx=0.5, fy=0.5)
            jpegs = cv.imencode('.jpg', rectangle)[1].tobytes()
            yield (b'--frame\r\n'+b'Content-Type: image/jpeg\r\n\r\n' + jpegs + b'\r\n\r\n')
            if(cv.waitKey(1) & 0xFF ==ord('q')):
                break
    cap.release()
    cv.destroyAllWindows()
@app.route('/detecting')
def detecting():
    #return Response(f,mimetype='multipart/x-mixed-replace; boundary=frame')
    #return Response(cv.imshow('ractangled image',rectangle),mimetype='multipart/x-mixed-replace; boundary=frame')
    #return Response(stream_with_context(gen()))
    return Response(stream_with_context(gen()),mimetype='multipart/x-mixed-replace; boundary=frame')
    #return Response(stream_with_context(gen()),mimetype='multipart/x-mixed-replace; boundary=frame')
    #return {"image":temp[0],"message":temp[1]}
'''@app.route('/detecting')
def detecting():
    #return Response(f,mimetype='multipart/x-mixed-replace; boundary=frame')
    #return Response(cv.imshow('ractangled image',rectangle),mimetype='multipart/x-mixed-replace; boundary=frame')
    #return Response(stream_with_context(gen()))
    resp=make_response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')
    resp.set_cookie(session["capacities"])
    return resp'''
if __name__=='__main__':
    app.run(debug="True")