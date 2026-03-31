from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Root route for welcome message (Required by Rubric)
@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to the Events API"}), 200

# GET all events (Required by Rubric)
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200

# POST: Create a new event
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    
    # Input Validation
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400
    
    # Logic: Auto-increment ID based on last item
    new_id = events[-1].id + 1 if events else 1
    new_event = Event(new_id, data["title"])
    events.append(new_event)
    
    # Return 201 Created as per Rubric
    return jsonify(new_event.to_dict()), 201

# PATCH: Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()
    
    # Find the event
    event = next((e for e in events if e.id == event_id), None)
    
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    
    # Update title if provided
    if data and "title" in data:
        event.title = data["title"]
        return jsonify(event.to_dict()), 200
    
    return jsonify({"error": "No data provided"}), 400

# DELETE: Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    global events
    # Find event to confirm existence
    event = next((e for e in events if e.id == event_id), None)
    
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    
    # Filter list to remove the event
    events = [e for e in events if e.id != event_id]
    
    return jsonify({"message": f"Event {event_id} deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)