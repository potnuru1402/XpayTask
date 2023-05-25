from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import uvicorn
from pymongo import MongoClient


class MyApp:
    def __init__(self):
        app = FastAPI()
        self.hostname = "localhost"
        self.database = 'test'
        self.username = 'postgres'
        self.password = 'Priya@1999'
        self.port_id = '5432'
        self.db = MongoClient("localhost", 27017)['test']['users']

        class User(BaseModel):
            full_name: str
            email: str
            password: str
            phone: str
            profile_picture: str

        @app.get("/")
        def root():
            return {"message": "Hello, World!"}

        @app.post("/users/")
        def create_user(user: User):
            conn = psycopg2.connect(
                host=self.hostname,
                dbname=self.database,
                user=self.username,
                password=self.password,
                port=self.port_id
            )
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM users WHERE email = %s", (user.email,))
            if cur.fetchone()[0] > 0:
                raise HTTPException(status_code=400, detail="Email already exists")
            cur.execute(
                "INSERT INTO users (full_name, email, password, phone, profile_picture) VALUES (%s, %s, %s, %s, %s)",
                (user.full_name, user.email, user.password, user.phone, user.profile_picture)
            )
            conn.commit()
            cur.execute("SELECT * FROM users WHERE email = %s AND phone = %s", (user.email, user.phone))
            result = cur.fetchone()
            if result is None:
                raise HTTPException(status_code=404, detail="User not found")
            user_id, full_name, email, password, phone, profile_picture = result
            self.db.insert_one({
                "user_id": str(user_id),
                "full_name": str(full_name),
                "email": str(email),
                "password": str(password),
                "phone": str(phone),
                "profile_picture": str(profile_picture)
            })
            return {"message": "User created successfully."}

        @app.get("/users/{user_id}")
        def get_user(user_id: str):
            conn = psycopg2.connect(
                host=self.hostname,
                dbname=self.database,
                user=self.username,
                password=self.password,
                port=self.port_id
            )
            cur = conn.cursor()
            cur.execute("SELECT full_name, email, phone, profile_picture FROM users WHERE id = %s", (user_id,))
            row = cur.fetchone()
            print("")
            mongo_doc = self.db.find_one({"_id": user_id})
            if row is None:
                raise HTTPException(status_code=404, detail="User not found")
            sql_doc = {
                "full_name": row[0],
                "email": row[1],
                "phone": row[2],
                "profile_picture": row[3]
            }
            response_content = {"sql_doc": sql_doc, "mongo_doc": mongo_doc}
            return response_content
        self.app = app

    def run(self):
        uvicorn.run(self.app, host="127.0.0.1", port=6451, log_level="info")


if __name__ == "__main__":
    my_app = MyApp()
    my_app.run()
