from flask import *
import ibm_db
import ibm_boto3
from ibm_botocore.client import Config, ClientError
app = Flask(__name__)
app.secret_key = 'something'
conn =ibm_db.connect("DATABASE=bludb;HOSTNAME=19af6446-6171-4641-8aba-9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30699;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=vmk43766;PWD=udLPWZFCFmIzOQbe;", "", "")
print("DB connected")
@app.route('/')
def demo():
    return render_template('register.html')
@app.route('/home.html')
def demo1():
    return render_template('home.html')
@app.route('/home.html')
def home():
    return render_template('home.html')
@app.route('/admin.html')
def admin():
    return render_template('admin.html')
@app.route('/guide.html')
def guide():
    return render_template('guide.html')
@app.route('/register.html')
def reg():
    return render_template('register.html')
@app.route('/login.html')
def log():
    return render_template('login.html')

@app.route('/register' , methods = ['POST', 'GET'])
def reg_1():
    if request.method == 'POST':
        uname = request.form['username']
        email = request.form['email']
        password = request.form['password']
        print(uname,email,password)
        print('Register Success')
        sql = "SELECT * FROM USER WHERE USERNAME = ?"
        stmt =  ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, uname)
        ibm_db.execute(stmt)
        acc = ibm_db.fetch_assoc(stmt)
        if acc:
            msg = "USER EXIST .., REGISTER with new Credintials"
            return render_template("register.html", msg = msg)
        else:
            sql = "SELECT * FROM USER WHERE EMAIL = ? "
            stmt =  ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, email)
            ibm_db.execute(stmt)
            acc = ibm_db.fetch_assoc(stmt)
            if acc:
                msg = "EMAIL ID is already Registered .., Use Another EMAIL"
                return render_template("register.html", msg = msg)
            else:
                sql = "INSERT INTO USER VALUES ( ?, ?, ?)"
                stmt = ibm_db.prepare(conn, sql)
                ibm_db.bind_param(stmt, 1, uname)
                ibm_db.bind_param(stmt, 2, email)
                ibm_db.bind_param(stmt, 3, password)
                ibm_db.execute(stmt)
                msg = "Account Created Successfully.., LOGIN Here"
                return render_template("login.html", msg = msg)
    return  render_template('login.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    global username
    if request.method == 'POST':
        uname = request.form['username']
        password = request.form['password']
        print("The login username and password is ", uname, password)
        sql = "SELECT * FROM USER WHERE USERNAME = ? and PASSWORD = ?"
        stmt =  ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, uname)
        ibm_db.bind_param(stmt, 2,password )
        ibm_db.execute(stmt)
        acc = ibm_db.fetch_assoc(stmt)
        print("Details fetch from the DB based on the sql : " ,acc)
        if acc:
            session['Loggedin'] = True
            session['uname'] = acc['USERNAME']
            username = acc['USERNAME']
            return render_template('home.html')
        else:
            msg = "USERNAME or PASSWORD is incorrect"
            return render_template("login.html", msg = msg)
    print("Login Success!!!!")
    return render_template('login.html')
@app.route('/plants', methods = ['POST', 'GET'])
def plants1():
    if request.method == 'POST':
        pname = request.form['plant_name']
        pid = request.form['plant_id']
        pcost = request.form['cost']
        sql = "INSERT INTO PLANTS VALUES ( ?, ?, ?)"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, pname)
        ibm_db.bind_param(stmt, 2, pid)
        ibm_db.bind_param(stmt, 3, pcost)
        ibm_db.execute(stmt)
        msg = "Plant Added Successfully"
        return render_template("admin.html", msg = msg)
    else:
        msg = "Plant not added"
        return render_template("admin.html" , msg = msg)

@app.route("/plants_file", methods = ['POST', 'GET'])
def file():
    
    f = request.files["plant_image"]
    fname = f.filename
    f.save(fname)
    COS_ENDPOINT = "https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints"
    COS_API_KEY_ID = "6jA8hs8-KSR7Qd4fWOvepgacPFdOy5-jdx9YYFN_gE8K"
    COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/edcb2015a9924ed897d9d0fa9750c2da:40b098df-12b9-4fa8-a012-255436e66e7f:bucket:obj7"
    cos = ibm_boto3.client("s3", ibm_api_key_id = COS_API_KEY_ID, ibm_service_instance_id = COS_INSTANCE_CRN, endpoint_url = COS_ENDPOINT, config = Config(signature_version='oauth') )
    cos.upload_file(Filename = fname, Bucket = "obj7", Key = fname )
    msg = "file uplaod successfull"
    return render_template("admin.html" , msg = msg)

@app.route('/guide' ,  methods = ['POST', 'GET'])
def guide1():
    pn = request.form.get('indoor_plants')
    if pn == 'coral_berry':
        return redirect('https://www.houseplantsexpert.com/coral-berry-plant.html')
    elif pn == "money_tree":
        return redirect('https://www.housebeautiful.com/lifestyle/gardening/a30298787/money-tree-care/')
    elif pn == "philodendron":
        return redirect('https://www.masterclass.com/articles/philodendron-care')
    elif pn == "chinese_evergreen":
        return redirect('https://www.hgtv.com/outdoors/flowers-and-plants/houseplants/chinese-evergreen#:~:text=Chinese%20evergreen%20care%20is%20simple,but%20they%20prefer%20high%20humidity.')
    elif pn == "spider_plant":
        return redirect('https://www.hgtv.com/outdoors/flowers-and-plants/houseplants/2019/spider-plant-indoor-care#:~:text=Spider%20plant%20needs%20are%20simple,a%20bit%20more%20between%20waterings.')
    elif pn == "staghorn_fern":
        return redirect('https://hort.extension.wisc.edu/articles/staghorn-fern-platycerium-bifurcatum/#:~:text=These%20tropical%20plants%20need%20good,basal%20fronds%20and%20the%20medium.')
    elif pn == "orchid":
        return redirect('https://www.repotme.com/pages/orchid-care-10')
    elif pn == "peace_lily":
        return redirect('https://miraclegro.com/en-us/indoor-gardening/how-to-grow-and-care-for-peace-lilies.html')
    elif pn == "jade_plant":
        return redirect('https://www.masterclass.com/articles/jade-plant-care-guide')
    elif pn == "string_of_hearts":
        return redirect('https://www.masterclass.com/articles/string-of-hearts-plant-guide')
    else:
        msg = " Select any one plant"
        return render_template('guide.html' , msg=msg)
    

if __name__ == '__main__':
    app.run(debug=True)
