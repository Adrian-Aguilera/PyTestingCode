from distutils.command import upload
import random
import token
from locust import HttpUser, task, between
import json
import pandas as pd

code_id = ["JD123","JS456","MJ789","EW101","RM202","AB303","WJ404","OD505","CG606","SR707","DH808","IL909","AM101","MJ202","LB303","EW404","LM505","GH606","NY707","CG808","EM909","AC101","MW202","SF303","ON404","EA505","LH606","AW707","AW808","JF909","LS101","LS202","ST303","WH404","EW505","AH606","AM707","LC808","MR909","NB101","CW202","EM303","IS404","AC505","SY606","LK707","OC808","JW909","EH101","LF202","JD123","JS456","MJ789","EW101","RM202","AB303","WJ404","OD505","CG606","SR707","DH808","IL909","AM101","MJ202","LB303","EW404","LM505","GH606","NY707","CG808","EM909","AC101","MW202","SF303","ON404","EA505","LH606","AW707","AW808","JF909","LS101","LS202","ST303","WH404","EW505","AH606","AM707","LC808","MR909","NB101","CW202","EM303","IS404","AC505","SY606","LK707","OC808","JW909","EH101","LF202","JT123","SH456","EJ789","EW101","AM202","LB303","OJ404","ND505","IG606","AR707","DH808","IL909","AM101","MJ202","LB303","EW404","LM505","GH606","NY707","CG808","EM909","AC101","MW202","SF303","ON404","EA505","LH606","AW707","AW808","JF909","LS101","LS202","ST303","WH404","EW505","AH606","AM707","LC808","MR909","NB101","CW202","EM303","IS404","AC505","SY606","LK707","OC808","JW909","EH101","LF202"]
token_id = []

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)
    #host = "http://44.228.39.101:8080"
    host = input("Enter host: ")
    #upload_json = json.
    def on_start(self):
        if code_id:  # Check if there are still codes left
            self.codigo = random.choice(code_id)
            code_id.remove(self.codigo)  # Remove the used code_id
        else:
            print("No more codes left to use.")
            return
 
        response = self.client.get(f"/api/app/App/match/{self.codigo}")
        if response.ok:
            response_data = response.json()
            result_data = response_data.get('result', {})
            self.id_member = result_data.get('id')
            self.token = result_data.get('token')
            print(result_data.get('token'))
            token_id.append([result_data.get('token'), result_data.get('id') ])

    def headers(self):
        return {"Authorization": f"Bearer {self.token}"} if hasattr(self, 'token') else {}

    def json_data(self):
        minimo = 10.0
        maximo = 20.0

        json_alert = {
            "member_id": self.id_member,
            "latitude": random.uniform(minimo, maximo),
            "longitude": random.uniform(minimo, maximo),
        }

        json_alertPoint = {
            "member_id": self.id_member,
            "latitude": random.uniform(minimo, maximo),
            "longitude": random.uniform(minimo, maximo)
        }
        return json_alert, json_alertPoint

    @task
    def test_routes_alert(self):
        if hasattr(self, 'id_member'):
            json_alert, json_alertPoint = self.json_data()
            #self.client.post("/api/app/App/alert", json=json_alert, headers=self.headers())
            #self.client.post("/api/app/App/alertPoint", json=json_alertPoint, headers=self.headers())
            self.client.get(f"/api/app/App/deleteMatch/{self.codigo}")
            self.save_token()

    def save_token(self):
        df = pd.DataFrame(token_id, columns = ["token", "id"])
        df.to_csv("tokens.csv")