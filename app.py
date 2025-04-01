from flask import Flask, request, jsonify, render_template
from models.user import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/student/add/', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        data = request.form
        new_student = User(name=data['name'], email=data['email'], password=data['password'])
        db.session.add(new_student)
        db.session.commit()
        return jsonify({'message': 'Student added successfully'}), 201
    return render_template('add_student.html')

@app.route('/student/lists/', methods=['GET'])
def get_students():
    students = User.query.all()
    return render_template('list_students.html', students=students)

@app.route('/student/update/', methods=['GET', 'POST'])
def update_student():
    if request.method == 'POST':
        data = request.form
        student = User.query.get(data['id'])
        if student:
            if 'name' in data:
                student.name = data['name']
            if 'email' in data:
                student.email = data['email']
            if 'password' in data:
                student.password = data['password']
            db.session.commit()
            return jsonify({'message': 'Student updated successfully'}), 200
        return jsonify({'message': 'Student not found'}), 404
    return render_template('update_student.html')

@app.route('/student/delete/', methods=['GET', 'POST'])
def delete_student():
    if request.method == 'POST':
        data = request.form
        student = User.query.get(data['id'])
        if student:
            db.session.delete(student)
            db.session.commit()
            return jsonify({'message': 'Student deleted successfully'}), 200
        return jsonify({'message': 'Student not found'}), 404
    return render_template('delete_student.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)