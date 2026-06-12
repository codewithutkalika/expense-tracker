from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('expense.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
              (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              amount REAL NOT NULL,
              category TEXT NOT NULL,
              date TEXT NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('expense.db')
    c = conn.cursor()
    c.execute('SELECT * FROM expenses ORDER by date DESC')
    expenses = c.fetchall()
    total = round(sum(row[2] for row in expenses), 2)
    conn.close()
    return render_template('index.html', expenses=expenses, total=total)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    amount = request.form['amount']
    category = request.form['category']
    date = request.form['date']
    conn =sqlite3.connect('expense.db')
    c = conn.cursor()
    c.execute('INSERT INTO expenses (name, amount, category, date) VALUES (?, ?, ?, ?)', (name, amount, category, date))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('expense.db')
    c = conn.cursor()
    c.execute('DELETE FROM expenses WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)


