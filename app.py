from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    important = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Note {self.id} - Important: {self.important}>'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        note_text = request.form.get('note_text')
        important = 'important' in request.form
        new_note = Note(text=note_text, important=important)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('index'))

    notes = Note.query.all()
    return render_template('notes.html', notes=notes)

@app.route('/clear_notes', methods=['POST'])
def clear_notes():
    # Очищаем все заметки из базы данных
    db.session.query(Note).delete()
    db.session.commit()
    return '', 204  # Возвращаем пустой ответ с кодом 204 (No Content)



if __name__ == '__main__':
    with app.app_context():  # Создаем контекст приложения
        db.create_all()  # Создание базы данных и таблицы
    app.run(debug=True)