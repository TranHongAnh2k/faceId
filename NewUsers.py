import cv2
import sqlite3
import os

cam = cv2.VideoCapture(0)
detector = cv2.CascadeClassifier('Models/haarcascade_frontalface_default.xml')


# Hàm cập nhật tên và ID vào CSDL
def insertOrUpdate(id, name):
    conn = sqlite3.connect("Models/FaceBaseNew.db")
    cursor = conn.execute('SELECT * FROM People WHERE ID=' + str(id))
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
        break

    if isRecordExist == 1:
        cmd = "UPDATE people SET Name=' " + str(name) + " ' WHERE ID=" + str(id)
    else:
        cmd = "INSERT INTO people(ID,Name) Values(" + str(id) + ",' " + str(name) + " ' )"

    conn.execute(cmd)
    conn.commit()
    conn.close()


id = input('Nhập số thứ tự:')
name = input('Nhập tên:')


#tạo thư mục nhân viên
os.mkdir(f"./DataSet/Facedata/raw/{name}")

#đường dân tới thư mục nhân viên
folder_path = f"./DataSet/Facedata/raw/{name}"

print("Bắt đầu chụp ảnh, nhấn q để thoát!")

insertOrUpdate(id, name)

sampleNum = 0


while (True):

    ret, img = cam.read()

    # Lật ảnh cho đỡ bị ngược
    img = cv2.flip(img, 1)

    # Kẻ khung giữa màn hình để người dùng đưa mặt vào khu vực này
    centerH = img.shape[0] // 2;
    centerW = img.shape[1] // 2;
    sizeboxW = 300;
    sizeboxH = 400;
    cv2.rectangle(img, (centerW - sizeboxW // 2, centerH - sizeboxH // 2),
                  (centerW + sizeboxW // 2, centerH + sizeboxH // 2), (255, 255, 255), 5)

    # Đưa ảnh về ảnh xám
   # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Nhận diện khuôn mặt
    faces = detector.detectMultiScale(img, 1.3, 5)
    for (x, y, w, h) in faces:
        # Vẽ hình chữ nhật quanh mặt nhận được
        cv2.rectangle(img, (x-w//2, y-h//2), (x + 3*w//2, y + 3*h//2), (255, 0, 0), 2)
        sampleNum = sampleNum + 1
        # Ghi dữ liệu khuôn mặt vào thư mục DataSet
        cv2.imwrite(f"./DataSet/Facedata/raw/{name}/User{sampleNum}.jpg", img[y:y + h, x:x + w])

    cv2.imshow('frame', img)
    # Check xem có bấm q hoặc trên 100 ảnh sample thì thoát
    if cv2.waitKey(500) & 0xFF == ord('q'):
        break
    elif sampleNum >= 100:
        break

cam.release()
cv2.destroyAllWindows()