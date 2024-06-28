from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)


@app.route("/")
def welcome():
    return render_template("index.html")


import os
import numpy as np
from PIL import Image

app.config["UPLOAD_FOLDER"] = "uploads"

@app.route("/submit_image", methods=["POST","GET"])
def submit_image():
    if request.method=="POST":
        image=request.files["imageFile"]
        client_image_file = image.filename
        uploads_directory = "static/uploads/"
        client_img_path = os.path.join(uploads_directory,"client_img.jpg")
        image.save(client_img_path)
    return render_template("display_img_with_coord.html",client_img_path=client_img_path)

@app.route("/submit", methods=["POST", "GET"])
def submit():
    if request.method == "POST":
        # getting data from the web application.
        # the image entered by the client
        # image = request.files["imageFile"]
        # the marker pixels entered by the client
        client_img_path="static/uploads/client_img.jpg"
        client_image=Image.open(client_img_path)
        img_width,img_height=client_image.size  

        x1_list = request.form.getlist("x1[]")
        y1_list = request.form.getlist("y1[]")
        x2_list = request.form.getlist("x2[]")
        y2_list = request.form.getlist("y2[]")
        markers = []
        for x1, y1, x2, y2 in zip(x1_list, y1_list, x2_list, y2_list):
            x1=int(x1)
            y1=int(y1)
            x2=int(x2)
            y2=int(y2)
            x1=(x1*img_width)/450
            x2=(x2*img_width)/450
            y1=(y1*img_height)/450
            y2=(y2*img_height)/450
            x1=int(x1)
            y1=int(y1)
            x2=int(x2)
            y2=int(y2)

            markers.append(np.array([y1,x1,y2,x2]))
        markers=np.array(markers)

        # saving the image entered by the client on to the server
        # client_image_file = image.filename
        # uploads_directory = "static/uploads/"
        # client_img_path = os.path.join(uploads_directory, client_image_file)
        # image.save(client_img_path)

        # Image_Segmentation is the python program containing the image_segmentation implemented class
        import Image_Segmentation
        # import numpy as np
        obj=Image_Segmentation.Image_Seg(client_img_path,markers)
        # seg() is the method of Image_Seg Class
        segmented_img=obj.seg()
        save_seg_img=Image.fromarray(segmented_img)

        
        save_path="static/uploads/client_segmented.jpg"
        # the segmented image obtained is saveed in the folder statics/uploads
        save_seg_img.save(save_path)
        
    return render_template("result.html", path=save_path)


if __name__ == "__main__":
    app.run(debug=True)
