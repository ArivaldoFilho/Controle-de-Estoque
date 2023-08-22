import pyodbc

connection_data = (
    "Driver={SQL SERVER};"
    "Server=Dell-Arivaldo;"
    "Database=Loja_Eletronicos;"
)


connection = pyodbc.connect(connection_data)
print("Connection successful")


cursor = connection.cursor()

def add_product(code, name, price, quantity):
    command = f"""INSERT INTO PRODUCTS (CODIGO, DESCRITOR, PRECO, ESTOQUE) VALUES ({code}, '{name}', {price}, {quantity})"""
    cursor.execute(command)
    connection.commit()
    return True

def add_product_inventory():
    code = int(input("Enter the product code to be added: "))
    name = input("Enter the product name: ")
    price = float(input("Enter the product price: "))
    quantity = int(input("Enter the quantity to be added: "))
    add_product(code, name, price, quantity)
    print("Product added to inventory successfully!")
    
def remove_product(code, quantity):
    command = f"SELECT ESTOQUE FROM PRODUTOS WHERE CODIGO = {code}"
    cursor.execute(command)
    result = cursor.fetchone()
    
    if result:
        current_quantity = result[0]
        if current_quantity >= quantity:
            command = f"UPDATE PRODUCTS SET ESTOQUE = ESTOQUE - {quantity} WHERE CODIGO = {code}"
            cursor.execute(command)
            connection.commit()
            return f"Products removed from inventory successfully."
        else:
            return "Insufficient quantity in stock for removal."
    else:
        return "Product not found."
    
def remove_product_inventory():
    code = int(input("Enter the product code to be removed: "))
    quantity = int(input("Enter the quantity to be removed: "))
    removal_result = remove_product(code, quantity)
    print(removal_result)
    
    
def display_inventory():
    cursor.execute("SELECT CODIGO, DESCRITOR, PRECO, ESTOQUE FROM PRODUTOS")
    products = cursor.fetchall()
    print("\nInventory:")
    for product in products:
        print(f"Code: {product[0]}, Name: {product[1]}, Price: $ {product[2]:.2f}, Quantity: {product[3]}")
        
def process_purchase(code, quantity):
    cursor.execute(f"SELECT DESCRITOR, PRECO, ESTOQUE FROM PRODUCTS WHERE CODE = {code}")
    result = cursor.fetchone()
    
    if result:
        name, price, stock_quantity = result
        if stock_quantity >= quantity:
            total = price * quantity
            cursor.execute(f"UPDATE PRODUTOS SET ESTOQUE = ESTOQUE - {quantity} WHERE CODIGO = {code}")
            connection.commit()
            return f"Purchase successful. Total: $ {total:.2f}"
        else:
            return "Insufficient quantity in stock."
    else:
        return "Product not found."
    
while True:
    print("\nOptions:")
    print("1. Display inventory")
    print("2. Process purchase")
    print("3. Add product to inventory")
    print("4. Remove product from inventory")
    print("5. Exit")
    
    option = input("Choose an option: ")

    if option == "1":
        display_inventory()
    elif option == "2":
        code = int(input("Enter the product code to be purchased: "))
        quantity = int(input("Enter the quantity to be purchased: "))
        purchase_result = process_purchase(code, quantity)
        print(purchase_result)
    elif option == "3":
        add_product_inventory()
    elif option == "4":
        remove_product_inventory()
    elif option == "5":
        break
    else:
        print("Invalid option. Please try again.")

