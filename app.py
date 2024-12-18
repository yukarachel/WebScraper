from flask import Flask, g, render_template, request
import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('base.html')

def get_message_db():
  # write some helpful comments here
  try:
      return g.message_db
  except AttributeError:
      g.message_db = sqlite3.connect("message_db.sqlite")
      cmd = \
      """
          CREATE TABLE IF NOT EXISTS messages (
              handle TEXT,
              message TEXT
          )
      """
      cursor = g.message_db.cursor()
      cursor.execute(cmd)
      g.message_db.commit()
      return g.message_db

def insert_message(request):
    message = request.form.get('message')
    handle = request.form.get('handle')
    
    # Get the database connection
    db = get_message_db()
    
    # Create a cursor object to execute SQL commands
    cursor = db.cursor()
    
    # SQL query to insert the message into the 'messages' table
    insert_query = "INSERT INTO messages (handle, message) VALUES (?, ?)"
    
    # Execute the SQL query with the handle and message as parameters
    cursor.execute(insert_query, (handle, message))
    
    # Commit the changes to the database
    db.commit()
    
def random_messages(n): 
    db = get_message_db()
    cursor = db.cursor()
    cursor.execute('''SELECT handle, message FROM messages ORDER BY RANDOM() LIMIT ?''', (n,))
    messages = cursor.fetchall()
    db.close()
    return messages
    
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        insert_message(request)
        # Add a small note thanking the user for their submission
        submission_note = "Thank you for your submission!"
        return render_template('submit.html', submission_note=submission_note)
    else:
        return render_template('submit.html')
    
@app.route('/view')
def view():
    messages = random_messages(5)
    return render_template('view.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)

    
    

