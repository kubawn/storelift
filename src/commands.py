import requests

def enter(id: int):
    r = requests.post("http://localhost:5000/enter", data={"id": id})
    print(r.text)
    return
    
def create(id: int, credits: float):
    r = requests.post("http://localhost:5000/register_customer", data={"id": id, "credits": credits})
    print(r.text)
    return

def take(id: int, item: int):
    r = requests.post("http://localhost:5000/take", data={"id": id, "item": item})
    print(r.text)
    return

def put(id: int, item: int):
    r = requests.post("http://localhost:5000/put", data={"id": id, "item": item})
    print(r.text)
    return

def exit_(id: int):
    r = requests.post("http://localhost:5000/leave", data={"id": id})
    print(r.text)
    return

def state():
    r = requests.get("http://localhost:5000/state")
    print(r.text)
    return

def item(item: int, price: float):
    r = requests.post("http://localhost:5000/register_item", data={"item": item, "price": price})
    print(r.text)
    return