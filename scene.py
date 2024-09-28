from classes_with_method import *
from datetime import datetime
import json

product_cat.add_product("Jelly Tint", 259, "#02", 11, "Magic Lib Tint", "This is detail\nThis lib made by angle that came from heaven\nHave been sell For 10 year","Lips")
product_cat.add_product("Logitect MX MASTER 3", 3500, "white", 11, "dsdasda", "dsafdsfsdfsfsdsfdsfsdf", "gadget")
product_cat.add_product("Jelly Tint", 259, "#01", 22, "Magic Lib Tint", "This is detail\nThis lib made by angle that came from heaven\nHave been sell For 10 year","Lips")
product_cat.add_product("Jelly Tint", 259, "#07", 9, "Magic Lib Tint", "This is detail\nThis lib made by angle that came from heaven\nHave been sell For 10 year","Lips")
product_cat.add_product("EST. HARDDER 2", 229, "#31", 1, "nothing here", "This is another detaikl", "Lips")
product_cat.add_product("Keychorn Q1", 6790, "Blue", 12, "First Keychron custom keyboard","This is magic thing, just buy it and typing 300wpm","keyboard,gadget")

admin1 = Admin("Krittithee Tuncharoen",10000,"admin1","admin1@gmail.com","pass1")
# admin2 = Admin("Jirapat Treesuwan",10000,"admin2","admin2@gmail.com","pass2")

shop.admins.append(admin1)

guest = Guest()
customer = guest.register("user","maikittitee@gmail.com","pass")
if (customer.login("user","pass")):
	print("login Sucess")

shop.add_promotion("1,3", datetime(2004,4,9), datetime(2025,4,9), 50)

customer.shopping_cart.add_to_cart(product_cat.get_inst_product_by_id("1"), 2)
customer.shopping_cart.add_to_cart(product_cat.get_inst_product_by_id("2"), 1)
addr = ShippingAddress("Krittihee Tuncharoen", "ECC-999", "0951018285")
customer.address.append(addr)

customer.make_purchase(addr)

print(shop.admins)
