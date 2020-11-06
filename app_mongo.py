# import necessary module
from flask import Flask, request, session, jsonify
from flask_pymongo import PyMongo
from datetime import date

# new Flask instance
app = Flask(__name__)

# set database connection parameters here
# app.config['MONGO_DBNAME'] = 'plaschema'
app.config['MONGO_URI'] = "mongodb+srv://ritmwa0104:ritmwa0104@cluster0.cih4a.mongodb.net/plaschema?retryWrites=true&w=majority"
mongo = PyMongo(app)

# this will handle all POST request to /enrol
@app.route('/enrol', methods=["POST"])
def enrol():
    #convert request data from JSON to dictionary
    info = request.get_json()
    # get the email key from the info dictionary
    email = info['email']

    #connecting to the database
    query = mongo.db.enrollment

    
    #let's check to ensure the email doesn't exist
    account_exists = query.find({"email":email})
    for data in account_exists:
        data["_id"] = str(data["_id"])
        if data["email"] == email :
            #can't continue with registration
        #jsonify() will convert your dictionary to JSON string (opposite of get_json())
            return jsonify({
            "status": "failed",
            "message": "Email address already exists!"
            })
   

    
    #if account doesn't exist, get the other info from
    fullname = info['fullname']
    marital_status = info['marital_status']
    gender = info['gender']
    date_of_birth = info['date_of_birth']
    phone_number = info['phone_number']
    nationality = info['nationality']
    password = info['password']
    disability = info['disability'].capitalize()


    dob_list = date_of_birth.split("/")
    year_of_birth = int(dob_list[2])
    today = date.today()
    this_year = today.year
    age = this_year - year_of_birth
    is_equity = "none"
    if (age <= 5) or (age >= 60) or(disability == "Yes"):
        print("good")
        is_equity = "equity"

    #run the INSERT query to add the new user. I also used the format() method too for the same reason.
    query.insert({"fullname": fullname, "marital_status": marital_status, "gender": gender, "date_of_birth": date_of_birth, "phone_number": phone_number, "nationality": nationality, "email": email,"plan":is_equity})



   

    # since we were successful, let us return a success message
    # along with the enrolment id in a dictionary
    # remember we convert from dictionary to JSON using the jsonify() function
    # return jsonify ({
    # "status": "success",
    # "message": "User has been enrolled successfully",
    # "enrol_id": 1,
    # "equity": "is_equity"
    # })
      
    
    result = query.find({"fullname": fullname})
    b = []
    for a in result:
        a["_id"] = str(a["_id"])
        b.append(a)

    return jsonify (status=True,data = b)

#that's all... let's run our app.
app.run(debug=True)