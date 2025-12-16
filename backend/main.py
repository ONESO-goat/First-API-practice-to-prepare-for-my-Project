# -----------------------------
# Imports
# -----------------------------

from flask import request, jsonify
from config import app, db
from models import Contact


# -----------------------------
# GET: Retrieve all contacts
# -----------------------------
@app.route("/contacts", methods=["GET"])
def get_contacts():
    """
    Fetch all contacts from the database and return them as JSON.
    """

    # Query the database for all Contact records
    contacts = Contact.query.all()

    # Convert each Contact object into a JSON-serializable dictionary
    json_contacts = [contact.to_json() for contact in contacts]

    # Return the list wrapped in a JSON response
    return jsonify({"contacts": json_contacts}), 200


# -----------------------------
# POST: Create a new contact
# -----------------------------
@app.route("/create_contact", methods=["POST"])
def create_contact():
    """
    Create a new contact using JSON data sent from the client.
    """

    # Extract data from the incoming JSON request
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    # Validate required fields
    if not first_name or not last_name or not email:
        return jsonify({
            "message": "First name, last name, and email are required."
        }), 400

    # Create a new Contact object
    new_contact = Contact(
        first_name=first_name,
        last_name=last_name,
        email=email
    )

    # Attempt to save the new contact to the database
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        # Roll back if something goes wrong
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

    # Successful creation
    return jsonify({"message": "User created"}), 201


# -----------------------------
# PATCH: Update an existing contact
# -----------------------------
@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    """
    Update an existing contact using partial JSON data.
    """

    # Look up the contact by ID
    contact = Contact.query.get(user_id)

    # If the contact does not exist, return an error
    if not contact:
        return jsonify({"message": "User not found"}), 404

    # Get the incoming update data
    data = request.json

    # Update fields only if new values are provided
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)

    # Save changes to the database
    db.session.commit()

    return jsonify({"message": "User updated"}), 200


# -----------------------------
# DELETE: Remove a contact
# -----------------------------
@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    """
    Delete a contact by ID.
    """

    # Find the contact in the database
    contact = Contact.query.get(user_id)

    # If contact does not exist, return an error
    if not contact:
        return jsonify({"message": "User not found"}), 404

    # Delete the contact and commit the change
    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "User deleted"}), 200


# -----------------------------
# Application Entry Point
# -----------------------------
if __name__ == "__main__":
    # Ensure database tables are created before running the app
    with app.app_context():
        db.create_all()

    # Start the Flask development server
    app.run(debug=True)
