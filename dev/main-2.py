# import library
import uvicorn
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import uvicorn.config
import platform
import pandas as pd
from openai.embeddings_utils import distances_from_embeddings
from ast import literal_eval
import numpy as np
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

# FastAPI 서버 클래스
from module import openai_generate_AnswerByQusetion as OGABQ

Game_Server_Main_Memory = {}

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: str):
        self.active_connections[room_id].remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, room_id: str):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_text(message)

manager = ConnectionManager()

class FASTAPI_SERVER:
    
    def __init__(self):
        self.OWNER_NAME = "Tyranno-Rex"
        self.openai_key = ""
        self.question_key = ""
        # FastAPI 서버 설정
        self.app = FastAPI()
        self.app.router.redirect_slashes = False
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

            # MongoDB 연결
        # RELEASE: mongodb://root:1234@mongodb-container/
        # DEBUG: localhost:27017

        # 운영 체제를 확인하여 디버그 모드와 릴리즈 모드를 설정합니다.
        self.current_os = platform.system()
        print("Environment: ", self.current_os)
        try :
            print("=====================================")
            print("MongoDB Connection")
            if self.current_os == 'Windows':
                PASSWORD = open("C:/Users/admin/project/portfolio-project/back-end/main/database/password-mongo-token.txt", "r").read().strip()
            else:
                PASSWORD = open("/app/mongo-token.txt", "r").read().strip()
            
            print("Password: ", PASSWORD)
            self.client = MongoClient("mongodb+srv://jsilvercastle:" + PASSWORD + "@portfolio.tja9u0o.mongodb.net/?retryWrites=true&w=majority&appName=portfolio")
            try:
                self.client.admin.command('ismaster')
            except ConnectionFailure:
                print('MongoDB server not available')
            # readme 데이터베이스
            self.git_repo_mongodb = self.client['github_repo']

            # portfolio 데이터베이스
            self.portfoilo = self.client['portfolio']
            self.question = self.portfoilo['question']
            print("MongoDB Connection Complete")
            print("=====================================")
        except Exception as e:
            print("MongoDB Connection Error: ", e)
            print("=====================================")

        try :
            print("=====================================")
            print("OpenAI Setting")
            if self.current_os == 'Windows':
                PASSWORD = open("C:/Users/admin/project/portfoilo-oracle/fastapi/database/password-openai-token.txt", "r").read().strip()
                QUESTION_KEY = open("C:/Users/admin/project/portfoilo-oracle/fastapi/database/password-openai-question-key.txt", "r").read().strip()
            else:
                PASSWORD = open("/app/openai-token.txt", "r").read().strip()
                QUESTION_KEY = open("/app/openai-question-key.txt", "r").read().strip()
            
            print("Password: ", PASSWORD)
            print("Question Key: ", QUESTION_KEY)
            self.openai_key = PASSWORD
            self.question_key = QUESTION_KEY
            print("OpenAI Setting Complete")
        except Exception as e:
            print("OpenAI Setting Error: ", e)
            print("=====================================")
        
        try:
            print("=====================================")
            print("processed texts Setting")
            if self.current_os == 'Windows':
                self.df = pd.read_csv('C:/Users/admin/project/portfoilo-oracle/fastapi/database/data/processed_texts_embeddings.csv')
            else:
                self.df = pd.read_csv('/app/data/processed_texts_embeddings.csv')
            self.df['embeddings'] = self.df['embeddings'].apply(literal_eval).apply(np.array)
            print("processed texts Setting Complete")
        except Exception as e:
            print("processed texts Setting Error: ", e)
            print("=====================================")


        print("=====================================")
        print("FastAPI Server Setting")
        # FastAPI 라우터 설정
        self.router = APIRouter()
        self.router.add_api_route('/local/', endpoint=self.check_local, methods=['POST'])
        self.router.add_api_route('/openai/check/password/', endpoint=self.check_password, methods=['POST'])
        self.router.add_api_route('/openai/', endpoint=self.check_server, methods=['GET'])
        self.router.add_api_route('/openai/api/send_question/', endpoint=self.send_AnswerByQuestion, methods=['POST'])
        # self.router.add_websocket_route('/openai/ws/', endpoint=self.Game_Server_Main_ws)
        self.router.add_api_websocket_route('/openai/ws/{room_id}', self.Game_Server_Main_ws)
        self.app.include_router(self.router)
        print("FastAPI Server Setting Complete")
        print("=====================================")

    async def Game_Server_Main_ws(self, websocket: WebSocket, room_id: str):
        await manager.connect(websocket, room_id)
        try:
            while True:
                data = await websocket.receive_text()
                await manager.broadcast(f"{data}", room_id)
        except WebSocketDisconnect:
            manager.disconnect(websocket, room_id)

    async def check_local(self):
        return JSONResponse(status_code=200, content={"message": "Local is running", "question": "What is the owner's name?", 
                                                        "answer": "this letter is came from the owner of this project. The owner's name is " + self.OWNER_NAME + "."})

    async def check_password(self, request: Request):
        data = await request.json()
        password = data.get('password')
        if password != self.question_key:
            return JSONResponse(status_code=401, content={"message": "Error", "data": "Password is incorrect"})
        return JSONResponse(status_code=200, content={"message": "Success", "data": "Password is correct"})

    async def check_server(self):
        return JSONResponse(status_code=200, content={"message": "Server is running"})

    async def send_AnswerByQuestion(self, request: Request):
        try:
            data = await request.json()
            question = data.get('question')
            question_key = data.get('question_key')
            # question = request.query_params.get('question')
            # question_key = request.query_params.get('question_key')
            if (self.question_key != question_key):
                return JSONResponse(status_code=401, content={"message": "Error", "data": "Invalid question key"})
            response = OGABQ.answer_question(self.df, question=question, openai_key=self.openai_key)
            self.question.insert_one({"question": question, "answer": response})
            return JSONResponse(status_code=200, content={"message": "Success", "question": question, "answer": response})
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": "Error", "data": str(e)})



fastapi_server = FASTAPI_SERVER()
app = fastapi_server.app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
