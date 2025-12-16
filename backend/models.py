from config import db

class Contact(db.Model):
  id = db.Column(db.Integer, primary_key=True) # WE ALWAYS NEED AN ID
  # THIS IS THE KEY WE'LL INDEX THIS AND SHOULD BE UNQUIE

  first_name = db.Column(db.String(80), unique=False, nullable=False)
  last_name = db.Column(db.String(80), unique=False, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)


  def to_json(self): # TAKES ALL THE DIFFERENT FIELDS ABOVE AND CONVERT THEM INTO A PYTHON DICTIONARY WHICH WE CAN CONVERT IN JSON WHICH WE CAN PASS TO THE API
    return {
      "id": self.id,# CAMEL CASE IS BEING USED HERE FOR JSON, 
      "firstName": self.first_name,
      "lastName": self.last_name,
      "email": self.email

    }






