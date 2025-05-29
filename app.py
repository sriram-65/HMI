from flask import Flask , redirect , request , session , url_for , render_template 
from pymongo import MongoClient
from bson.objectid import ObjectId
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

client = MongoClient("mongodb+srv://sriram65raja:1324sriram@cluster0.dejys.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
data_base = client["ai"]
TEMPLATES_DB = data_base["TEMPLATES_DB"]
COUSTOMERS_DB = data_base["COUSTOMERS_DB"]

cloudinary.config(
     cloud_name="dbrmvywb0",
    api_key="799647841433247",
    api_secret="XLtCOYXxRTnjZqwaF2oFnQ0AK7k"
)


@app.route("/")
def home():
    get_templates = TEMPLATES_DB.find({}).sort("_id" , -1)
    return render_template("index.html" , templates = get_templates)



@app.route("/upload-Template" , methods=["POST" , "GET"])
def upload():
    if(request.method=="POST"):
        title = request.form.get("title")
        category = request.form.get("category")
        img = request.files.get("img")
        des = request.files.get("des")
        live_previwe_link = request.form.get("link")
        
        if(not title and not category and not img and live_previwe_link):
            return "Unable to Upload"
        
        upload_to_cloud = cloudinary.uploader.upload(img , resource_type="auto")
        img_url = upload_to_cloud["secure_url"]
        data={
            "title":title,
            "category":category,
            "img":img_url,
            "descption":des,
             "Links":live_previwe_link
        }
        
        TEMPLATES_DB.insert_one(data)
        return redirect("/")
    get_templates = TEMPLATES_DB.find({}).sort("_id" , -1)
    get_cousterms_details_info = COUSTOMERS_DB.find({}).sort("_id" , -1)
    return render_template("admin.html" , templates = get_templates , deatils = get_cousterms_details_info )
        
        

@app.route("/del/<template_id>" , methods=["POST"])
def delete_post(template_id):
    try:
        TEMPLATES_DB.delete_one({"_id":ObjectId(template_id)})
        return redirect("/")
    except:
        return "Server : Unable handle Your request"
    

@app.route("/upload-information-about-shops" , methods=["POST"])
def shops():
    shop_owner_name = request.form.get("soname")
    phone_no = request.form.get("phoneno")
    shop_adress = request.form.get("address")
    shop_name = request.form.get("shop_name")
    business_type = request.form.get("business_type")
    shop_logo = request.form.get('logo')
    description = request.form.get('description')
    products = request.form.get('products')
    website_type= request.form.get("website_type")
    advance_payment = request.form.get("advance")
    img_upload = request.files.getlist("img-upload")
    payment_mode = request.form.get("payment_mode")
    
    
    upload_img_url = []
    
    for files in img_upload:
        result = cloudinary.uploader.upload(files , resource_type="auto" )
        upload_img_url.append(result["secure_url"])
    
    data = {
        "shop_owner_name":shop_owner_name,
        "phone_no":phone_no,
        "shop_adress":shop_adress,
        "shop_name":shop_name,
        "business_type":business_type, 
        "shop_logo":shop_logo,
        "description":description,
        "products":products,
        "website_type":website_type,
        "advance_payment":advance_payment,
        "payment_mode":payment_mode,
        "imgs":upload_img_url
    }
    
    COUSTOMERS_DB.insert_one(data)
    return redirect("/")
    
    
@app.route("/delelet/<coustomers_id>" , methods=["POST"])
def Dc(coustomers_id):
    try:
        COUSTOMERS_DB.delete_one({"_id":ObjectId(coustomers_id)}) 
        return redirect("/upload-Template") 
    except:
        return "Server : Unable handle Your request"

    
if __name__ == "__main__":
    app.run(debug=True)
