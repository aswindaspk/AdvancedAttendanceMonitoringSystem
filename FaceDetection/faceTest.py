import cv2
import face_recognition

from DBConnection import Database


db=Database()
# Create your views here.

qry="SELECT * FROM `myapp_student`"
res= db.select(qry)


print(res)



knownimage=[]
knownids=[]
studentcourse=[]
studentcoursesem=[]


for i in res:
    s=i["student_photo"]
    s=s.replace("/media/","")
    pth="C:\\Users\\aswin\\PycharmProjects\\AdvancedAttendanceTrackingSystem\\media\\"+ s
    # pth="C:\\Users\\shahana kp\\PycharmProjects\\college_violence\\media\\"+ s
    picture_of_me = face_recognition.load_image_file(pth)
    print(pth)
    my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]
    print(my_face_encoding)
    knownimage.append(my_face_encoding)
    knownids.append(i['id'])
    studentcourse.append(i['COURSE_id'])
    studentcoursesem.append(i['sem'])








# define a video capture object
vid = cv2.VideoCapture(0)



firsthour= (9.00,10.00)
secondhour= (10.00,11.00)
thirdhour= (11.00,12.00)
fourthhour= (12.00,13.00)
fifthhour= (13.00,14.00)
lasthour= (14.00,16.00)





while(True):

    ret, frame = vid.read()

    cv2.imwrite(r"C:\Users\aswin\PycharmProjects\AdvancedAttendanceTrackingSystem\media\tests\a.jpg",frame)
    # cv2.imwrite(r"C:\Users\shahana kp\PycharmProjects\college_violence\media\tests\a.jpg",frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    picture_of_others = face_recognition.load_image_file(r"C:\Users\aswin\PycharmProjects\AdvancedAttendanceTrackingSystem\media\tests\a.jpg")
    # picture_of_others = face_recognition.load_image_file(r"C:\Users\shahana kp\PycharmProjects\college_violence\media\tests\a.jpg")
    # print(pth)
    others_face_encoding = face_recognition.face_encodings(picture_of_others)


    totface=len(others_face_encoding)


    print("aaaaa", totface)

    from datetime import datetime

    curh = float(str(datetime.now().time().hour) + "." + str(datetime.now().time().minute))

    print(curh, "hgfhhgfgfghfghfgh")
    period=0
    if firsthour[0]<  curh <= firsthour[1]:
        period=1
    elif secondhour[0]< curh <= secondhour[1]:
        period=2
    elif thirdhour[0]< curh <= thirdhour[1]:
        period=3
    elif fourthhour[0]< curh <= fourthhour[1]:
        period=4
    elif fifthhour[0]< curh <= fifthhour[1]:
        period=5
    elif lasthour[0] < curh <= lasthour[1]:
        period = 6
    else:
        period = 1

    for i in range(0,totface):


        print("inside check")
        res=face_recognition.compare_faces(knownimage,others_face_encoding[i],tolerance=0.4)
        print(res,"helllo")
        l=0
        for j in res:
            if j==True:

                qry="SELECT * FROM `myapp_attendance` WHERE `date`=CURDATE() and `period`='"+str(period)+"' and status='Present' and STUDENT_id='"+str(knownids[l])+"'"
                print(qry)
                resa=db.select(qry)

                if len(resa)>0:

                    resa= resa[0]


                    # qry="update myapp_attendance set  status='Check out' where STUDENT_id='"+str(knownids[l])+"'"
                    qry="update myapp_attendance set  status='Present' where id='"+str(resa['id'])+"'"
                    db.update(qry)
                else:
                    d=str(datetime.now().strftime('%A'))
                    qry="select * from `myapp_timetable` where `COURSE_id`='"+str(studentcourse[l])+"' and `sem`='"+str(studentcoursesem[l])+"' and Day='"+d+"'"
                    print(qry)
                    ressubject= db.select(qry)
                    if len(ressubject) >0:
                        resa1= ressubject[0]
                        sid=""
                        if  period==1:
                            sid= resa1['SUBJECT_1_id']
                        elif period==2:
                            sid= resa1['SUBJECT_2_id']
                        elif period==3:
                            sid= resa1['SUBJECT_3_id']
                        elif period==4:
                            sid= resa1['SUBJECT_4_id']
                        elif period==5:
                            sid= resa1['SUBJECT_5_id']
                        else:
                            sid= resa1['SUBJECT_6_id']


                    # qry="INSERT INTO `myapp_attendance` (`status`,`date`,`STUDENT_id`,`hour`,`period`) VALUES ('Check in',CURDATE(),'"+str(knownids[l])+"',CURTIME(),'"+str(period)+"')"
                        qry="INSERT INTO `myapp_attendance` (`status`,`date`,`STUDENT_id`,`hour`,`period`,`SUBJECT_id`) VALUES ('Present',CURDATE(),'"+str(knownids[l])+"',CURTIME(),'"+str(period)+"','"+str(sid)+"')"

                        print(qry)
                        db.insert(qry)
            l=l+1
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()