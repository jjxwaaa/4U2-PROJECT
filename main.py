from classes_with_method import *
from datetime import datetime
from classes_with_method import shop
from fastapi import FastAPI, APIRouter
from typing import Optional
from scene import *
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# class UserPass(BaseModel):
# 	username: str
# 	password: str
	
# 	class Config:
# 		schema_extra = {
#             "example": {
#                 "username": "username",
# 				"password": "password",
#             }
#         }


app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

customer = APIRouter()
admin = APIRouter()

# example 127.0.0.1:58742/Products?name=Keychron
# example 127.0.0.1:58742/Products?in_type=Lips
@app.get("/Products") # j
async def	products(name:Optional[str] = None, in_type:Optional[str] = None):
	return (product_cat.browse_product(name, in_type))

@app.get("/Products/{product_id}") # j
async def	view_product(product_id : str):
	return (product_cat.view_product(product_id))

@app.get("/Users/{username}") # j
async def	view_user_detail(username : str):
	print(shop.users)
	if (shop.get_user_by_username(username)):
		return (shop.get_user_by_username(username).get_user_detail())
	return ("KO")

@app.get("/Products/{product_id}/add_to_fav") # j
async def	add_to_fav(username, product_id): 
	user = shop.get_user_by_username(username)
	user.add_to_favorite(product_id)
	return ("OK")

@app.post("/Auth/login") # n
async def	login(data:dict):
	user = User(0)
	if (user.login(data["username"], data["password"])):
		return (data["username"])
	return ("KO")

@app.post("/Auth/register") # i
async def	register(data:dict):
	guest = Guest()
	new = guest.register(data["username"], data["email"], data["password"]) 
	if (new):
		shop.users.append(new)
		return (new.name)
	return ("KO")

@app.post("/Auth/logout") #n
async def	logout(data:dict):
	if (shop.get_user_by_username(data["username"]).logout()):
		return ("OK")
	return ("KO")


# system feat

@app.get("/Users/{username}/confirm_payment") #n
async def	confirm_payment(order_id, username, amount:int):
	order = shop.get_user_by_username(username).get_order_by_id(order_id)
	if (not order):
		return ("KO")
	if (order.confirm_payment(amount)):
		return ("OK")
	return ("KO")

@app.get("/feat/orders") # i
async def	view_order(email, order_id):
	ret = shop.get_user_by_email(email).get_order_by_id(order_id).get_order_detail()
	if (ret):
		return (ret)
	return ("KO")

# info feat

@app.get("/Users/{username}/orders")
async def	get_user_orders(username):
	print(shop.get_user_by_username(username).order)
	return (shop.get_user_by_username(username).get_user_order())

@app.post("/users/{username}/editinfo") # i
async def	change_info(username, data:dict):
	user = shop.get_user_by_username(username)
	user.name = data["new_name"]
	user.tel = data["new_tel"]


@app.delete("/users/{username}/del_address") # i
async def	del_address(address_index:int, username):
	user = shop.get_user_by_username(username)
	user.address.pop(address_index)
	return ("OK")


@app.get("/users/{username}/favorite") #n
async def get_fav(username):
	user = shop.get_user_by_username(username)
	return (user.favorite)

## cart feat

@app.post("/cart/checkout")
async def	checkout(data:dict):
	user = shop.get_user_by_username(data["username"])
	new_order = user.make_purchase(user.address[data["address_index"]]) 
	if (new_order):
		return (new_order.order_id)
	return ("KO")

@app.get("/Users/{username}/cart")
async def	view_cart(username : str):
	# need to check searching name is a guy who search or not ... but how? -> im won't do this one neither.
	return (shop.get_user_by_username(username).shopping_cart.show_cart())

@app.get("/Products/{product_id}/add_to_cart") # i
async def	add_to_cart(username:str, product_id:str, quantity:int):
	ret = shop.get_user_by_username(username).shopping_cart.add_to_cart(product_cat.get_inst_product_by_id(product_id), quantity)
	if (ret):
		return (ret)
	return ("KO")

# ADMIN SIDE API 

@app.post("/admin/login")
async def	admin_login(data:dict):
	print(data["username"])
	print(data["password"])
	user = User(0)
	if (user.login(data["username"], data["password"], 1)):
		return (data["username"])
	return ("KO")

@app.post("/admin/add_product") # j
async def	add_product(data: dict): #p_type example : "Lips,Eye" (NO SPACE, ONLY COMMA(,))
	product_cat.add_product(data["name"], data["price"], data["specify"], data["stock"], data["description"], data["detail"], data["p_type"])
	return ("OK")

@app.post("/admin/modify_product/{target_product_id}")
async def	modify_product(target_product_id, data:dict):
	if (product_cat.modify_product(target_product_id, data["product_name"], int(data["product_price"]), data["product_description"], data["product_detail"], data["product_type"], int(data["product_stock"]), data["product_specify"])):
		return ("OK")
	return ("KO")

@app.post("/admin/add_promotion") # n
async def	add_promotion(data:dict):
	if (shop.add_promotion(str(data["product_ids"]), datetime(int(data["year_start"]), int(data["month_start"]), int(data["month_end"])), datetime(int(data["year_end"]), int(data["month_end"]), int(data["day_end"])), int(data["discount"]))):
		return (data["product_ids"])
	return ("KO")

@app.delete("/admin/del_product/{product_id}")
async def	del_product(product_id:str):
	target_product = product_cat.get_inst_product_by_id(product_id)
	if (target_product == None):
		return ("KO")
	product_cat.products.remove(target_product)
	return ("OK")

@app.get("/admin/products") # i
async def	admin_browse_products(name:Optional[str] = None, in_type:Optional[str] = None):
	return (product_cat.browse_product(name, in_type, all = True))

@app.get("/admin/promotions")
async def	browse_promotions():
	return (shop.promotions)
