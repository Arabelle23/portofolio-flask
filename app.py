from flask import Flask, render_template, session, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'supersecretkey123'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'portofolio_db'

mysql = MySQL(app)

@app.route('/')
def portfolio():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name, level, icon FROM skills")
        skills = cur.fetchall()
        cur.execute("SELECT id, title, description, image, link FROM projects")
        projects = cur.fetchall()
        cur.close()
        return render_template('portofolio.html', skills= skills, projects=projects)

    except Exception as e:
        return f"Error koneksi database: {e}"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()
        cur.close()
        if user:
            session['is_logged_in'] = True
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error='Username atau password salah!')
    return render_template('login.html')

@app.route('/admin')
def admin():
    if 'is_logged_in' not in session:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM skills")
    total_skills = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM projects")
    total_projects = cur.fetchone()[0]
    cur.close()
    return render_template('admin.html', username=session['username'],
                           total_users=total_users, total_skills=total_skills, total_projects=total_projects)


def logout():
    session.clear()
    return redirect(url_for('portfolio'))

@app.route('/admin/users')
def manage_users():
    if 'is_logged_in' not in session:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, name, bio, foto FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template('manage_user.html', users=users)

@app.route('/admin/users/add', methods=['GET', 'POST'])
def add_user():
    if 'is_logged_in' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        bio = request.form['bio']
        foto = request.form['foto']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password, name, bio, foto) VALUES (%s,%s,%s,%s,%s)",
                    (username, password, name, bio, foto))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('manage_users'))
    return render_template('add_user.html')

@app.route('/admin/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'is_logged_in' not in session:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        bio = request.form['bio']
        foto = request.form['foto']
        cur.execute("UPDATE users SET username=%s, password=%s, name=%s, bio=%s, foto=%s WHERE id=%s",
                    (username, password, name, bio, foto, user_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('manage_users'))
    cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cur.fetchone()
    cur.close()
    return render_template('edit_user.html', user=user)

@app.route('/admin/users/delete/<int:user_id>')
def delete_user(user_id):
    if 'is_logged_in' not in session:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('manage_users'))

@app.route('/admin/skills')
def manage_skills():
    if 'is_logged_in' not in session:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, level, icon FROM skills")
    skills = cur.fetchall()
    cur.close()
    return render_template('manage_skills.html', skills=skills)

@app.route('/admin/skills/add', methods=['GET', 'POST'])
def add_skill():
    if 'is_logged_in' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        level = request.form['level']
        icon = request.form['icon']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO skills (name, level, icon) VALUES (%s,%s,%s)",
                    (name, level, icon))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('manage_skills'))
    return render_template('add_skills.html')

@app.route('/admin/skills/edit/<int:skill_id>', methods=['GET', 'POST'])
def edit_skill(skill_id):
    if 'is_logged_in' not in session:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        level = request.form['level']
        icon = request.form['icon']
        cur.execute("UPDATE skills SET name=%s, level=%s, icon=%s WHERE id=%s",
                    (name, level, icon, skill_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('manage_skills'))
    cur.execute("SELECT * FROM skills WHERE id=%s", (skill_id,))
    skill = cur.fetchone()
    cur.close()
    return render_template('edit_skills.html', skill=skill)

@app.route('/admin/skills/delete/<int:skill_id>')
def delete_skill(skill_id):
    if 'is_logged_in' not in session:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM skills WHERE id=%s", (skill_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('manage_skills'))

@app.route('/admin/projects')
def manage_projects():
    if 'is_logged_in' not in session:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, title, description, image, link FROM projects")
    projects = cur.fetchall()
    cur.close()
    return render_template('manage_projects.html', projects=projects)

@app.route('/admin/projects/add', methods=['GET', 'POST'])
def add_project():
    if 'is_logged_in' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        image = request.form['image']
        link = request.form['link']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO projects (title, description, image, link) VALUES (%s,%s,%s,%s)",
                    (title, description, image, link))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('manage_projects'))
    return render_template('add_projrcts.html')

@app.route('/admin/projects/edit/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    if 'is_logged_in' not in session:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        image = request.form['image']
        link = request.form['link']
        cur.execute("UPDATE projects SET title=%s, description=%s, image=%s, link=%s WHERE id=%s",
                    (title, description, image, link, project_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('manage_projects'))
    cur.execute("SELECT * FROM projects WHERE id=%s", (project_id,))
    project = cur.fetchone()
    cur.close()
    return render_template('edit_projects.html', project=project)

@app.route('/admin/projects/delete/<int:project_id>')
def delete_project(project_id):
    if 'is_logged_in' not in session:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM projects WHERE id=%s", (project_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('manage_projects'))

if __name__ == '__main__':
    app.run(debug=True)
