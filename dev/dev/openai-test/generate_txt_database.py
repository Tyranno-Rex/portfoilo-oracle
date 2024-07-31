from bson import ObjectId
from pymongo import MongoClient
import platform

def generate_txt_for_gpt():
    current_os = platform.system()
    if current_os == 'Windows':
        PASSWORD = open("C:/Users/admin/project/portfoilo-oracle/fastapi/database/password-mongo-token.txt", "r").read().strip()
    else:
        PASSWORD = open("/app/mongo-token.txt", "r").read().strip()
    
    client = MongoClient("mongodb+srv://jsilvercastle:" + PASSWORD + "@portfolio.tja9u0o.mongodb.net/?retryWrites=true&w=majority&appName=portfolio")
    
    db = client['portfolio']
    repos = db['database']


    for repo in repos.find():
        repo_name = repo["name"]
        repo_description = repo["description"]
        repo_complete_status = repo["complete_status"]
        repo_multi = repo["multi"]
        repo_category = repo["category"]
        repo_subproject = repo["subproject"]
        repo_readme = repo["readme"]
        # if repo["generate_txt_gpt"] == False:
        if 1 == 1:
            print(f"Generating txt for {repo_name}")
            with open(f"C:/Users/admin/project/portfoilo-oracle/fastapi/data/repo/{repo_name}.txt", "w", encoding="utf-8") as f:
                f.write(f"PROJECT_NAME : {repo_name}\n")
                f.write(f"PROJECT_DESCRIPTION : {repo_description}\n")
                f.write(f"PROJECT_COMPLETION_STATUS : {repo_complete_status}\n")
                f.write(f"PROJECT_MULTI : {repo_multi}\n")
                f.write(f"PROJECT_CATEGORY : {repo_category}\n")
                f.write(f"PROJECT_SUBPROJECT : {repo_subproject}\n")
                f.write(f"PROJECT_README : {repo_readme}\n")
                f.close()
            repo["generate_txt_gpt"] = True
            repos.update_one({"_id": repo["_id"]}, {"$set": repo})
        else:
            print(f"Already generated txt for {repo_name}")


generate_txt_for_gpt()