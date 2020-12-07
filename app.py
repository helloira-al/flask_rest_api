from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os 

# Initialize app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Initialize database
db = SQLAlchemy(app)
#Initialize ma
ma = Marshmallow(app)

# Contact class
class Contact(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20))
    lname = db.Column(db.String(20))
    category = db.Column(db.String(20))
    phone_number = db.Column(db.String(20))
    user_id = db.Column(db.Integer)
    
    def __init__(self, fname, lname, category, phone_number):
        self.fname = fname
        self.lname = lname
        self.category = category
        self.phone_number = phone_number
        
# Contact Schema
class ContactSchema(ma.Schema):
    class Meta:
        fields = ('fname', 'lname', 'category', 'phone_number')

        
# Initialize schema
contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)

# Add a contact
@app.route('/contact', methods=['POST'])
def add_contact():
    fname = request.json['fname']
    lname = request.json['lname']
    category = request.json['category']
    phone_number = request.json['phone_number']
    
    new_contact = Contact(fname, lname, category, phone_number)
    
    db.session.add(new_contact)
    db.session.commit()
    
    return contact_schema.jsonify(new_contact)

#Get all contacts
@app.route('/contacts', methods=['GET'])
def get_contacts():
    all_contacts = Contact.query.order_by(Contact.fname).all()
    result = contacts_schema.dump(all_contacts)
    return jsonify(result)

#Get a contact
@app.route('/contact/<id>', methods=['GET'])
def get_contact(id):
    contact = Contact.query.get(id)
    return contact_schema.jsonify(contact)

# Update a contact
@app.route('/contact/<id>', methods=['PUT'])
def update_contact(id):
    contact = Contact.query.get(id)
    
    fname = request.json['fname']
    lname = request.json['lname']
    category = request.json['category']
    phone_number = request.json['phone_number']
    
    contact.fname = fname
    contact.lname = lname
    contact.category = category
    contact.phone_number = phone_number
    
    db.session.commit()
    
    return contact_schema.jsonify(contact)


#Delete a contact
@app.route('/contact/<id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    return contact_schema.jsonify(contact)



# Run server
if __name__ == "__main__":
    app.run(debug=True)
    

