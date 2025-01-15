import mysql.connector
from datetime import datetime

class DBManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        # 연결이 되어 있는지 확인
        if self.connection is None or not self.connection.is_connected():
            try:
                self.connection = mysql.connector.connect(
                    host='10.0.66.10',  # DB 호스트명
                    user='jjeong',       # DB 사용자명
                    password='001125',       # DB 비밀번호
                    database='board_db2'  # 사용할 DB
                )
                self.cursor = self.connection.cursor(dictionary=True)  # 커서를 dictionary 형식으로 설정
                print("DB 연결 성공")
            except mysql.connector.Error as error:
                print(f"데이터베이스 연결 실패: {error}")
                self.connection = None
                self.cursor = None

    def disconnect(self):
        # 연결 종료
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("DB 연결 종료")
            
    def get_all_posts(self):
        try:
            self.connect()
            if self.connection is None or self.cursor is None:
                print("데이터베이스 연결 실패")
                return []
            sql = "SELECT * FROM posts"
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(f"게시글 조회 실패: {error}")
            return []
        finally:
            self.disconnect()
    
    def add_post(self, title, content, filename=None):
        try:
            self.connect()
            if self.connection is None or self.cursor is None:
                print("데이터베이스 연결 실패")
                return False
            sql = "INSERT INTO posts (title, content, filename, created_at) values (%s, %s, %s, NOW())"
            values = (title, content, filename)  # 파일명이 없을 경우 None으로 처리
            self.cursor.execute(sql, values)
            self.connection.commit()  # 데이터베이스에 저장
            return True
        except mysql.connector.Error as error:
            self.connection.rollback()  # 실패 시 롤백
            print(f"게시글 추가 실패: {error}")
            return False
        finally:
            self.disconnect()

    def get_post_by_id(self, id):
        try:
            self.connect()
            if self.connection is None or self.cursor is None:
                print("데이터베이스 연결 실패")
                return None
            sql = "SELECT * FROM posts WHERE id = %s"
            value = (id,)  # 튜플로 값을 넘겨야 함
            self.cursor.execute(sql, value)
            return self.cursor.fetchone()
        except mysql.connector.Error as error:
            print(f"내용 조회 실패: {error}")
            return None
        finally:
            self.disconnect()

    def update_post(self, id, title, content, filename):
        try:
            self.connect()
            if self.connection is None or self.cursor is None:
                print("데이터베이스 연결 실패")
                return False
            if filename:
                sql = """UPDATE posts 
                        SET title = %s, content = %s, filename = %s 
                        WHERE id = %s"""
                values = (title, content, filename, id)
            else:
                sql = """UPDATE posts 
                        SET title = %s, content = %s 
                        WHERE id = %s"""
                values = (title, content, id)
            self.cursor.execute(sql, values)
            self.connection.commit()  # 변경사항을 DB에 반영
            return True
        except mysql.connector.Error as error:
            self.connection.rollback()
            print(f"게시글 수정 실패: {error}")
            return False
        finally:
            self.disconnect()

    def delete_post(self, id):
        try:
            self.connect()
            if self.connection is None or self.cursor is None:
                print("데이터베이스 연결 실패")
                return False
            sql = "DELETE FROM posts WHERE id = %s"
            value = (id,)  # 튜플 1개일 때
            self.cursor.execute(sql, value)
            self.connection.commit()
            return True
        except mysql.connector.Error as error:
            self.connection.rollback()
            print(f"게시글 삭제 실패: {error}")
            return False
        finally:
            self.disconnect()
