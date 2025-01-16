from flask import Flask, render_template, request, redirect, url_for, session
import os
from datetime import datetime
from model import DBManager

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')

#디렉토리 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.secret_key = 'your_secret_key'  # 이 값은 안전하게 관리해야 합니다.

manager = DBManager()

# 로그인 페이지
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 로그인 인증 (여기선 생략)
        session['user'] = username  # 로그인 성공 시 세션에 사용자 이름 저장
        return redirect(url_for('index'))  # 로그인 후 게시글 목록 페이지로 리디렉션
    return render_template('login.html')

# 로그아웃 처리
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

# 게시글 목록 보기
@app.route('/')
def index():
    posts = manager.get_all_posts()
    return render_template('index.html', posts=posts)

# 게시글 상세 보기
@app.route('/post/<int:id>')
def view_post(id):
    post = manager.get_post_by_id(id)
    return render_template('view.html', post=post)

# 게시글 추가
@app.route('/post/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        # 파일 처리
        file = request.files.get('file')  # 파일이 있을 경우
        filename = None
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # 서버에 저장

        # 게시글 추가
        if manager.add_post(title, content, filename):  # 게시글 추가 함수 호출
            return redirect(url_for('index'))  # 게시글 목록 페이지로 리디렉션
        else:
            return "게시글 추가 실패", 400  # 실패 시 메시지 표시
        
    return render_template('add.html')  # GET 요청 시 게시글 작성 폼


# 게시글 수정
@app.route('/post/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = manager.get_post_by_id(id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        file = request.files.get('file')  # 파일 업로드
        filename = file.filename if file else None
        
        if filename:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # 파일 저장
        
        if manager.update_post(id, title, content, filename):
            return redirect(url_for('index'))  # 게시글 목록 페이지로 리디렉션
        return "게시글 수정 실패", 400
        
    return render_template('edit.html', post=post)  # 수정할 게시글 정보 전달


# 게시글 삭제
@app.route('/post/delete/<int:id>')
def delete_post(id):
    if manager.delete_post(id):
        return redirect(url_for('index'))
    return "게시글 삭제 실패", 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
