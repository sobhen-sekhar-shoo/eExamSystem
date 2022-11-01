from math import e
from sre_constants import SUCCESS
from tkinter import Image
from flask import Flask, flash, request,url_for,render_template,redirect,session
from markupsafe import escape
import pymongo
from pymongo import MongoClient
import datetime
import os
from werkzeug.utils import secure_filename
import frender



UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config["SECRET_KEY"] = "a1nbskdgksdgak697auskkdbakjfa8s7f08ajsfbjabsfljf08a7f0asfal"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 *1024
client = MongoClient("mongodb+srv://eExamSystem:8yUZvK6Z95HNOeJs@eexam-system.f07qvqu.mongodb.net/test")
db = client["Exam_system"]
UserDb = db["Users"]
LeftMenuDb = db["LeftMenu"]


@app.context_processor
def context_processor():
    Mdata = []
    if "userroll" in session :
       if  session["userroll"] == "Admin":
           AdMenu = LeftMenuDb.find()
           for item in AdMenu :
               Mdata.append(item)
       elif  session["userroll"] == "Faculty":
             AdMenu = LeftMenuDb.find()
             FJson =['Setting',"Faculty List","Subjects","Papers"]
             for item in AdMenu :
                if item["PageTitel"] not in FJson :
                   Mdata.append(item)
       else :
         AdMenu = LeftMenuDb.find()
         FJson =['Setting',"Faculty List","Subjects","Papers","Student List","Add Subject","Add Exam"]
         for item in AdMenu :
             if item["PageTitel"] not in FJson :
                Mdata.append(item)
    return dict(LeftDt = Mdata)

def LogStatus() :
    return session["LogStatus"]

def DateFormat(x):
    fDate = f"{x.strftime('%d')}/{x.strftime('%m')}/{x.strftime('%Y')}"
    return fDate

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

 
@app.route('/', methods=['GET','POST']) 
def Index():
     return redirect("/login", code=302)
 
@app.route('/logout', methods=['GET','POST']) 
def Logout():
     session.clear()
     session["LogStatus"] = False
     return redirect("/login", code=302)
     
@app.route('/login',  methods=['GET','POST'])
def Login():
    error = None
    if request.method == 'POST':
         user_id = request.form["userid"]
         password = request.form["password"]
         UserData = UserDb.find_one({"user_id": user_id, "password":password})
         if  UserData :
           session["LogStatus"] = True
           session["username"] = UserData["name"]
           session["userid"] = UserData["user_id"]
           session["userroll"] = UserData["roll"]
           session["useremail"] = UserData["email"]
           session["logtime"] = f"{datetime.datetime.utcnow()}"
           session["gender"] = UserData["gender"]
           session["image"] = f'uploads/{UserData["image"]}'
           return redirect("/home",code=302)
         else :
            error = 'Invalid user id/password'
    return render_template("login.html" ,error = error)


    
@app.route('/signup',  methods=['GET','POST'])
def Signup():
    error = None
    if request.method == 'POST':
         user_id = request.form["userid"]
         email = request.form["email"]
         name = request.form["username"]
         roll = "Student"
         password = request.form["password"]
         gender = request.form["gender"]
         if 'file' in request.files:
            image = request.files["file"]
            if image and allowed_file(image.filename):
               filename = secure_filename(image.filename)
              
         if UserDb.find_one({"user_id": user_id}) :
             error = 'User Id alredy exist'
         else :
            post = {"name": name,
                   "email": email,
                   "password": password,
                   "roll": roll,
                   "user_id": user_id,
                   "date": datetime.datetime.utcnow(),
                   "gender": gender,
                   "image": filename
                   }
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))      
            UserDb.insert_one(post)
            return redirect("/login", code=302)
          
    return render_template("signup.html", error = error)


@app.route('/home')
def Home():
     if request.method == 'GET':
      if LogStatus() :
        return render_template("home.html",name = session["username"])
      return redirect("logout")
    
@app.route('/student/students')
def Students():
    if request.method == 'POST':
      pass
      
    return render_template("/student/students.html")

@app.route('/student/add_student')
def AddStudent():
    if request.method == 'POST':
      pass
      
    return render_template("/student/add_student.html")

@app.route('/setting/pages', methods=['GET'])
def Pages():
    if request.method == 'GET':
        if LogStatus() :
          LmData = []
          for menu in LeftMenuDb.find() :
              menu['date'] = DateFormat(menu['date'])
              LmData.append(menu)
          return render_template("/setting/pages.html", MenuJson = LmData)
        return redirect("/logout")
    if request.method == 'POST':
        return render_template("/setting/pages.html",code=302)


@app.route('/setting/add_pages', methods=['GET','POST'])
def AddPages():
    if request.method == 'GET':
        if LogStatus() :
         return render_template("/setting/add_pages.html")
        return redirect("/logout")
    if request.method == 'POST':
       PageOrder = request.form["PageOrder"]
       PageTitel = request.form["PageTitel"]
       PageIcon = request.form["PageIcon"]
       PageStatus = request.form["PageStatus"]
       PageUrl = request.form["PageUrl"]
       Pages = {
                "PageOrder": PageOrder,
                "PageTitel": PageTitel,
                "PageIcon": PageIcon,
                "PageStatus": PageStatus,
                "PageUrl": PageUrl,
                "PageType": "First",
                "date": datetime.datetime.utcnow()
               }
       LeftMenuDb.insert_one(Pages)
       return redirect("/setting/pages",code=302) 
       
@app.route('/setting/sub_page', methods=['GET'])
def SubPage():
    if request.method == 'GET':
        if LogStatus() :
          ParentPage = request.args.get("parent_page")
          LmSubData = []
          for menu in LeftMenuDb.find() :
             if 'ParentPage' in menu and menu['ParentPage'] == ParentPage :
                menu['date'] = DateFormat(menu['date'])
                LmSubData.append(menu)
          return render_template("/setting/sub_page.html", SubMenuJson = LmSubData,PaPage = ParentPage)
        return redirect("/logout")
    

@app.route('/setting/add_subpage', methods=['GET','POST'])
def AddSubPages():
    if request.method == 'GET':
        if LogStatus() :
           ParPage = request.args.get("parent_page")
           return render_template("/setting/add_subpage.html",PPage = ParPage) 
        return redirect("/logout")
    if request.method == 'POST':
       ParentPage = request.form["Parentpage"]
       PageOrder = request.form["PageOrder"]
       PageTitel = request.form["PageTitel"]
       PageIcon = request.form["PageIcon"]
       PageStatus = request.form["PageStatus"]
       PageUrl = request.form["PageUrl"]
       Pages = {
                "PageOrder": PageOrder,
                "ParentPage": ParentPage,
                "PageTitel": PageTitel,
                "PageIcon": PageIcon,
                "PageStatus": PageStatus,
                "PageUrl": PageUrl,
                "PageType": "Second",
                "date": datetime.datetime.utcnow()
               }
       LeftMenuDb.insert_one(Pages)
       return redirect(f"/setting/sub_page?parent_page={request.args.get('parent_page')}",code=302) 
       
@app.route('/faculty/faculty', methods=['GET'])
def Faculty():
    if request.method == 'GET':
        if LogStatus() :
          FacData = []
          for item in UserDb.find({"roll": "Faculty"}) :
              item['date'] = DateFormat(item['date'])
              FacData.append(item)
          return render_template("/faculty/faculty.html", FacultyJson = FacData)
        return redirect("/logout")

@app.route('/faculty/add_faculty', methods=['GET','POST'])
def AddFaculty():
    error = None
    if request.method == 'GET':
        if LogStatus() :
           return render_template("/faculty/add_faculty.html") 
        return redirect("/logout")
    if request.method == 'POST':
         user_id = request.form["fid"]
         email = request.form["femail"]
         name = request.form["fname"]
         roll = "Faculty"
         password = request.form["fpassword"]
         gender = request.form["fgender"]
         if 'fimage' in request.files:
            image = request.files["fimage"]
            if image and allowed_file(image.filename):
               filename = secure_filename(image.filename)
              
         if UserDb.find_one({"user_id": user_id}) :
             error = 'User Id alredy exist'
         else :
            post = {"name": name,
                   "email": email,
                   "password": password,
                   "roll": roll,
                   "user_id": user_id,
                   "date": datetime.datetime.utcnow(),
                   "gender": gender,
                   "image": filename
                   }
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))      
            UserDb.insert_one(post)
            return redirect("/faculty/faculty", code=302)     
    





if __name__ == "__main__":
   app.run(port="3000",debug=True)