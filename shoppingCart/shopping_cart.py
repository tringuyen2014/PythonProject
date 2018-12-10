import db
from business import Product, LineItem, Cart

def show_title():
    print("The Shopping Cart program")
    print()
    
def show_menu_admin():
    print("COMMAND MENU")
    print("show     - Show items in the Inventory")
    print("addDB    - Add an item to the Inventory")
    print("delDB    - Delete an item in the Inventory")
    print("modDB    - Modify an item in the Inventory")
    print("exit     - Exit program")
    print()

def show_menu_reg():
    print("COMMAND MENU")
    print("cart     - Show the cart")
    print("add      - Add an item to the cart")
    print("del      - Delete an item from cart")
    print("mod      - Modify an item in your cart")
    print("check    - Checkout")
    print("exit     - Exit program")
    print()

def show_products(products):
    print("PRODUCTS")
    line_format1 = "{:<5s} {:<25s} {:>10s} {:>10s} {:>12s}"
    line_format2 = "{:<5d} {:<25s} {:>10.2f} {:>10s} {:>12.2f}"
    print(line_format1.format("Item", "Name", "Price",
                              "Discount", "Your Price"))
    for i in range(len(products)):
        product = products[i]
        print(line_format2.format(i+1,
              product.name,
              product.price,
              str(product.discountPercent) + "%",
              product.getDiscountPrice()))
    print()

def show_cart(username):
    if db.getItemCount(username) == 0:
        print("There are no items in your cart.\n")
    else:
        line_format1 = "{:<5s} {:<20s} {:>12s} {:>10s} {:>10s}"
        line_format2 = "{:<5d} {:<20s} {:>12.2f} {:>10d} {:>10.2f}"
        print(line_format1.format("Item", "Name", "Your Price",
                                  "Quantity", "Total"))
        i = 0
        total = 0
        
        cart = Cart(username)
        detail = Product()
        
        for item in cart:
            detail = db.getProductDetail(item.product)
            total += item.getTotalItem(detail.getDiscountPrice())
            
            print(line_format2.format(i+1,
                  detail.name,
                  detail.getDiscountPrice(),
                  item.quantity,
                  item.getTotalItem(detail.getDiscountPrice())
                  ))
            i += 1
        print("{:>66.2f}".format(total))
        print()

def add_item(products, username):
    number = int(input("Item number: "))
    quantity = int(input("Quantity: "))
    if number < 1 or number > len(products):
        print("No product has that number.\n")
    else:
        cart = Cart(username)
        product = products[number-1]
        item = LineItem(product, quantity)
        cart.addItem(item)
        
        #put in db
        db.addItemtoCart(username, product.name, quantity)
        
        print(product.name + " was added.\n")

def remove_item(username):
    number = int(input("Item number: "))
    
    if number < 1 or number > db.getItemCount(username):
        print("The cart does not contain an item " +
              "with that number.\n")
    else:
        cart = Cart(username)
        item = []
        item = cart.removeItem(number-1)
        
        #delete in db
        db.deleteItemCart(username,item[0].product,item[0].quantity)
        
        print("Item" + number + "was deleted.\n")


def modItem(username):
    number = int(input("Item number: "))
    cart = Cart(username)
    
    if number < 1 or number > db.getItemCount(username):
        print("The cart does not contain an item " +
              "with that number.\n")
    else:
        mod = int(input("Change the quantity to: "))
        if mod > 0:
            item = []
            item = cart.modItem(number-1)

            #modify in db
            db.modifyItemCart(username, item[0].product, item[0].quantity, mod)

        else:
            print("Invalid number.\n")

def checkOut(username):
    show_cart(username)
    db.checkOut(username)
    print("Thank you for your order\n")
            

def showDB():
    products = db.showItem()
    show_products(products)
    
def addItemDB():
    name                = input("Name: ")
    price               = float(input("Price: "))
    discountPercent     = float(input("Discount: "))
          
    item = Product(name=name, price=price, discountPercent=discountPercent)
    db.addItemtoDB(item)    
    print(name + " was added to database.\n")

def deleteItemDB():
    item = input("Item Name: ")
    db.deleteIteminDB(item)
    print(item + " was deleted from database.\n")


def modifyItemDB():
    name                = input("Name: ")
    
    print("Enter new infomation")
    newName             = input("New Name: ")
    newPrice            = float(input("New Price: "))
    newDiscountPercent  = float(input("New Discount: "))
    
    db.modifyItemDB(name, newName, newPrice, newDiscountPercent)
    print(name + " was modified database.\n")

def show_loginregister():
    print("reg      - Register an account")
    print("log      - Login to your account")
    print("exit     - Exit program\n")
    print("To login as an admin, please use:")
    print("username is admin, password is admin123\n")

def register():
    username            = input("Username: ")
    password            = input("Password: ")

    if db.register(username,password) == 1:
        print("Account create sucessfully!\n")
        print("Please choose command 'log' to login into your account")
    else:
        print("Username already exists, please try a different username or login.\n")
    
def login():
    username            = input("Username: ")
    password            = input("Password: ")

    status = db.login(username,password)
    returnValue = ""
    
    if status == 0:
        print("User does not exist!\n")
    elif status == 1:
        print("Wrong password!\n")
    else:
        print("\n\nWELCOME "  + status + " user\n")
        returnValue = username
    return returnValue



def main():
    db.connect()
    username = ""
    show_loginregister()
    
    while username == "":
        command = input("Command: ")
        if command == "reg":
            register()
        elif command == "log":
            username = login()
        elif command == "exit":
            print("Bye!")
            break
        else:
            print("Not a valid command. Please try again.\n") 


    if username != "":
        show_title()

        # get a list of Product objects and display them
        products = db.showItem()
        show_products(products)
    
        role = db.getUserRole(username)
        
        if role == "admin":
            show_menu_admin()
            while True:
                command = input("Command: ")
                if command == "show":
                    showDB()
                elif command == "addDB":
                    addItemDB()
                elif command == "delDB":
                    deleteItemDB()
                elif command == "modDB":
                    modifyItemDB()
                elif command == "exit":
                    print("Bye!")
                    break
                else:
                   print("Not a valid command. Please try again.\n")
        else:
            show_menu_reg()
            while True:        
                command = input("Command: ")
                if command == "cart":
                    show_cart(username)
                elif command == "add":
                    add_item(products, username)
                elif command == "del":
                    remove_item(username)
                elif command == "mod":
                    modItem(username)
                elif command == "show":
                    showDB()
                elif command == "check":
                    checkOut(username)
                elif command == "exit":
                    print("Bye!")
                    break
                else:
                   print("Not a valid command. Please try again.\n") 

if __name__ == "__main__":
    main()
