import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector


def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost", 
            user="root",       
            password="Hernandez14",
            database="keykishop" 
        )
        if connection.is_connected():
            return connection
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        return None


def load_items():
    connection = create_connection()
    if not connection:
        return []
    cursor = connection.cursor(dictionary=True) 
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    connection.close()
    return items


def admin_login(username, password, success_callback):
    try:
        connection = create_connection()
        if not connection:
            return
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM admins WHERE username = %s AND password = %s", (username, password))
        if cursor.fetchone():
            success_callback()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials. Access denied.")
        connection.close()
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Failed to log in: {e}")


def customer_menu(root, items, previous_menu):
    # Clear previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Keyki Shop - Customer", font=("Helvetica", 20), bg='#8B4513', fg="white").pack(pady=15)
    tk.Button(root, text="Show Menu", width=25, height=2, font=("Helvetica", 16), bg='#D2B48C', command=lambda: show_menu(root, load_items(), customer_menu, previous_menu)).pack(pady=10)
    tk.Button(root, text="Order Items", width=25, height=2, font=("Helvetica", 16), bg='#D2B48C', command=lambda: order_items(root, items, customer_menu, previous_menu)).pack(pady=10)
    tk.Button(root, text="Back", width=25, height=2, font=("Helvetica", 16), bg='#D2B48C', command=lambda: main_menu(root, items)).pack(pady=10)
    tk.Button(root, text="Exit", width=25, height=2, font=("Helvetica", 16), bg='#D2B48C', command=root.quit).pack(pady=10)
    if previous_menu:
        tk.Button(root, text="Back", width=25, height=2, font=("Helvetica", 16), bg='#D2B48C', command=lambda: previous_menu(root, items)).pack(pady=10)

def save_item(name, price, item_type, items, current_menu, previous_menu, root):
    try:
        connection = create_connection()
        if not connection:
            return
        cursor = connection.cursor()
        cursor.execute("INSERT INTO items (name, price, type) VALUES (%s, %s, %s)", (name, price, item_type))
        connection.commit()
        connection.close()
        messagebox.showinfo("Item Added", f"Item '{name}' has been added successfully!")
        current_menu(root, load_items(), previous_menu)
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Failed to add item: {e}")


def delete_item(root, items, current_menu, previous_menu):
    # Clear previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Delete Item", font=("Helvetica", 20), bg='#8B4513', fg="white").pack(pady=15)

    item_id_label = tk.Label(root, text="Enter Item ID to delete", font=("Helvetica", 16), bg='#8B4513', fg="white")
    item_id_label.pack(pady=5)
    item_id_entry = tk.Entry(root, width=25, font=("Helvetica", 16))
    item_id_entry.pack(pady=10)

    tk.Button(root, text="Delete Item", width=25, height=2, font=("Helvetica", 16), bg='#D2B48C', command=lambda: perform_delete(item_id_entry.get(), items, current_menu, previous_menu, root)).pack(pady=10)
    tk.Button(root, text="Back", width=25, height=2, font=("Helvetica", 16), bg='#D2B48C', command=lambda: current_menu(root, items, previous_menu)).pack(pady=10)

def perform_delete(item_id, items, current_menu, previous_menu, root):
    try:
        connection = create_connection()
        if not connection:
            return
        cursor = connection.cursor()
        cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
        if cursor.rowcount > 0:
            connection.commit()
            messagebox.showinfo("Item Deleted", f"Item ID '{item_id}' has been deleted.")
        else:
            messagebox.showerror("Item Not Found", f"No item found with ID '{item_id}'.")
        connection.close()
        current_menu(root, load_items(), previous_menu)
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Failed to delete item: {e}")
    
def add_item(root, items, current_menu, previous_menu):
    # Clear previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Add New Item", font=("Helvetica", 20), bg='#8B4513', fg="white").pack(pady=15)
    name_label = tk.Label(root, text="Item Name", font=("Helvetica", 16), bg='#8B4513', fg="white")
    name_label.pack(pady=5)
    name_entry = tk.Entry(root, width=25, font=("Helvetica", 16))
    name_entry.pack(pady=10)

    price_label = tk.Label(root, text="Price", font=("Helvetica", 16), bg='#8B4513', fg="white")
    price_label.pack(pady=5)
    price_entry = tk.Entry(root, width=25, font=("Helvetica", 16))
    price_entry.pack(pady=10)

    type_label = tk.Label(root, text="Type (sweet or not sweet)", font=("Helvetica", 16), bg='#8B4513', fg="white")
    type_label.pack(pady=5)
    type_entry = tk.Entry(root, width=25, font=("Helvetica", 16))
    type_entry.pack(pady=10)

    tk.Button(root, text="Add Item", width=25, height=2, font=("Helvetica", 16), bg='#D2B48C', command=lambda: save_item(name_entry.get(), price_entry.get(), type_entry.get(), items, current_menu, previous_menu, root)).pack(pady=10)
    tk.Button(root, text="Back", width=25, height=2, font=("Helvetica", 16), bg='#D2B48C', command=lambda: current_menu(root, items, previous_menu)).pack(pady=10)


def view_orders(root, items, current_menu, previous_menu):
    # Clear previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="View Orders", font=("Helvetica", 20), bg='#8B4513', fg="white").pack(pady=15)

    # Connect to the database to fetch orders
    connection = create_connection()
    if not connection:
        return

    cursor = connection.cursor(dictionary=True)

    try:
        # Fetch all orders from the database
        cursor.execute("""
            SELECT o.id AS order_id, o.customer_name, o.customer_phone, o.order_type, 
                   i.name AS item_name, i.price, oi.quantity, (i.price * oi.quantity) AS item_total
            FROM customers o
            JOIN order_items oi ON o.id = oi.order_id
            JOIN items i ON oi.item_id = i.id
            ORDER BY o.id
        """)
        fetched_orders = cursor.fetchall()

        if not fetched_orders:
            tk.Label(root, text="No orders yet.", font=("Helvetica", 16), bg='#8B4513', fg="white").pack(pady=10)
        else:
            # Create Treeview
            tree = ttk.Treeview(root, columns=("Order ID", "Customer Name", "Phone", "Order Type", "Item", "Quantity", "Price", "Item Total"), show="headings", height=15)
            tree.pack(fill="both", expand=True, pady=10, padx=10)

            # Define column headings
            columns = {
                "Order ID": 100, 
                "Customer Name": 150, 
                "Phone": 120, 
                "Order Type": 100, 
                "Item": 150, 
                "Quantity": 80, 
                "Price": 80, 
                "Item Total": 100
            }

            for col, width in columns.items():
                tree.heading(col, text=col)
                tree.column(col, width=width, anchor="center")

            # Group orders by order ID and calculate totals
            grouped_orders = {}
            for row in fetched_orders:
                if row["order_id"] not in grouped_orders:
                    grouped_orders[row["order_id"]] = {
                        "customer_name": row["customer_name"],
                        "customer_phone": row["customer_phone"],
                        "order_type": row["order_type"],
                        "items": [],
                        "order_total": 0
                    }
                grouped_orders[row["order_id"]]["items"].append({
                    "item_name": row["item_name"],
                    "quantity": row["quantity"],
                    "price": row["price"],
                    "item_total": row["item_total"]
                })
                grouped_orders[row["order_id"]]["order_total"] += row["item_total"]

            # Populate Treeview
            for order_id, order_data in grouped_orders.items():
                customer_info = (
                    order_id, 
                    order_data["customer_name"], 
                    order_data["customer_phone"], 
                    order_data["order_type"], 
                    "", 
                    "", 
                    "", 
                    ""
                )
                # Insert customer row with blank item details
                tree.insert("", "end", values=customer_info, tags=("customer",))
                
                # Insert item rows
                for item in order_data["items"]:
                    item_info = (
                        "", 
                        "", 
                        "", 
                        "", 
                        item["item_name"], 
                        item["quantity"], 
                        item["price"], 
                        item["item_total"]
                    )
                    tree.insert("", "end", values=item_info, tags=("item",))

                # Insert total row
                total_info = (
                    "", 
                    "", 
                    "", 
                    "Order Total:", 
                    "", 
                    "", 
                    "", 
                    order_data["order_total"]
                )
                tree.insert("", "end", values=total_info, tags=("total",))

            # Style rows differently
            tree.tag_configure("customer", background="#f0f0f0", font=("Helvetica", 12, "bold"))
            tree.tag_configure("item", background="#ffffff", font=("Helvetica", 12))
            tree.tag_configure("total", background="#d3d3d3", font=("Helvetica", 12, "bold"))

            # Add a scrollbar for the Treeview
            scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Failed to fetch orders: {e}")
    finally:
        connection.close()

    # Back button to return to the admin menu
    tk.Button(root, text="Back", width=25, height=2, font=("Helvetica", 16), bg='#D2B48C', command=lambda: current_menu(root, items, previous_menu)).pack(pady=10)


def admin_menu(root, items, previous_menu):
    # Clear previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Keyki Shop - Admin", font=("Helvetica", 20), bg='#8B4513', fg="white").pack(pady=15)
    tk.Button(root, text="Show Menu", width=25, height=2, font=("Helvetica", 16), bg='#D2B48C', command=lambda: show_menu(root, items, admin_menu, previous_menu)).pack(pady=10)
    tk.Button(root, text="Add Item", width=25, height=2, font=("Helvetica", 16), bg='#D2B48C', command=lambda: add_item(root, items, admin_menu, previous_menu)).pack(pady=10)
    tk.Button(root, text="Delete Item", width=25, height=2, font=("Helvetica", 16), bg='#D2B48C', command=lambda: delete_item(root, items, admin_menu, previous_menu)).pack(pady=10)
    tk.Button(root, text="View Orders", width=25, height=2, font=("Helvetica", 16), bg='#D2B48C', command=lambda: view_orders(root, items, admin_menu, previous_menu)).pack(pady=10)
    tk.Button(root, text="Log Out", width=25, height=2, font=("Helvetica", 16), bg='#D2B48C', command=lambda: main_menu(root, items)).pack(pady=10)


def show_menu(root, items, current_menu, previous_menu):
    # Clear previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Menu", font=("Helvetica", 20), bg='#8B4513', fg="white").pack(pady=15)
    
    if not items:  # If no items exist, show a message
        tk.Label(root, text="No items available", font=("Helvetica", 16), bg='#8B4513', fg="white").pack(pady=5)
    else:
        for item in items:
            # Display each item with id, name, and price
            tk.Label(root, text=f"{item['id']}. {item['name']} - ${item['price']}", font=("Helvetica", 16), bg='#8B4513', fg="white").pack(pady=5)
    
    # Button to go back to the previous menu
    tk.Button(root, text="Back", width=25, height=2, font=("Helvetica", 16), bg='#D2B48C', command=lambda: current_menu(root, items, previous_menu)).pack(pady=15)


# Global variable to store orders (in memory for now)
orders = []


def order_items(root, items, current_menu, previous_menu):
    # Clear previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Order Items", font=("Helvetica", 20), bg='#8B4513', fg="white").pack(pady=15)

    # Collect customer information
    name_label = tk.Label(root, text="Your Name", font=("Helvetica", 16), bg='#8B4513', fg="white")
    name_label.pack(pady=5)
    name_entry = tk.Entry(root, width=25, font=("Helvetica", 16))
    name_entry.pack(pady=10)

    phone_label = tk.Label(root, text="Phone Number", font=("Helvetica", 16), bg='#8B4513', fg="white")
    phone_label.pack(pady=5)
    phone_entry = tk.Entry(root, width=25, font=("Helvetica", 16))
    phone_entry.pack(pady=10)

    order_type_label = tk.Label(root, text="Order Type (dine in/pick up)", font=("Helvetica", 16), bg='#8B4513', fg="white")
    order_type_label.pack(pady=5)
    order_type_entry = tk.Entry(root, width=25, font=("Helvetica", 16))
    order_type_entry.pack(pady=10)

    item_label = tk.Label(root, text="Enter Item Names and Quantities (e.g., item1:2, item2:3)", font=("Helvetica", 16), bg='#8B4513', fg="white")
    item_label.pack(pady=5)
    item_entry = tk.Entry(root, width=50, font=("Helvetica", 16))
    item_entry.pack(pady=10)

    def submit_order():
        # Collect customer and order details
        customer_name = name_entry.get()
        customer_phone = phone_entry.get()
        order_type = order_type_entry.get()
        item_details = item_entry.get()

        if not customer_name or not customer_phone or not order_type or not item_details:
            messagebox.showerror("Missing Information", "Please fill all fields and enter item names with quantities.")
            return

        # Parse items and quantities from input
        try:
            item_quantity_pairs = [
                pair.strip().split(":") for pair in item_details.split(",")
            ]
            item_quantities = {
                name.strip().lower(): int(quantity.strip())
                for name, quantity in item_quantity_pairs
            }
        except ValueError:
            messagebox.showerror("Invalid Format", "Please use the format 'item1:2, item2:3' for items and quantities.")
            return

        # Validate items and quantities
        selected_items = []
        for item_name, quantity in item_quantities.items():
            item = next((item for item in items if item['name'].lower() == item_name), None)
            if not item:
                messagebox.showerror("Invalid Item", f"Item '{item_name}' is not available.")
                return
            if quantity <= 0:
                messagebox.showerror("Invalid Quantity", f"Quantity for '{item_name}' must be greater than 0.")
                return
            selected_items.append((item, quantity))

        # Connect to the database
        connection = create_connection()
        if not connection:
            return

        try:
            cursor = connection.cursor()

            # Insert the order into the 'orders' table
            cursor.execute("""
                INSERT INTO customers (customer_name, customer_phone, order_type, total_bill)
                VALUES (%s, %s, %s, 0)
            """, (customer_name, customer_phone, order_type))

            order_id = cursor.lastrowid  # Get the ID of the inserted order

            total_price = 0

            # Insert each selected item into the 'order_items' table
            for item, quantity in selected_items:
                cursor.execute("""
                    INSERT INTO order_items (order_id, item_id, quantity)
                    VALUES (%s, %s, %s)
                """, (order_id, item['id'], quantity))
                total_price += item['price'] * quantity

            # Update the total bill in the 'orders' table
            cursor.execute("""
                UPDATE customers
                SET total_bill = %s
                WHERE id = %s
            """, (total_price, order_id))

            # Commit changes
            connection.commit()

            messagebox.showinfo("Order Successful", f"Order placed successfully! Order ID: {order_id}")
            # Go back to the previous menu or clear the form
            current_menu(root, items, previous_menu)

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to place order: {e}")
        finally:
            connection.close()

    # Submit button to place the order
    submit_button = tk.Button(root, text="Place Order", font=("Helvetica", 16), bg='#D2B48C', command=submit_order)
    submit_button.pack(pady=10)

    # Back button to return to the previous menu
    back_button = tk.Button(root, text="Back", font=("Helvetica", 16), bg='#D2B48C', command=lambda: current_menu(root, items, previous_menu))
    back_button.pack(pady=10)

    # def submit_order():
    #     if selected_item.get() == '':
    #         messagebox.showerror("Error", "Please select an item to order.")
    #         return
    #     item = next(item for item in items if item['id'] == int(selected_item.get()))
        
    #     # Save order data
    #     order = {
    #         "item": item['name'],
    #         "customer": name_entry.get(),
    #         "phone": phone_entry.get(),
    #         "order_type": order_type_entry.get(),
    #         "price": item['price']
    #     }
    #     orders.append(order)  # Add the order to the orders list
        
    #     # Confirm the order submission
    #     messagebox.showinfo("Order Confirmed", f"Order for {item['name']} has been placed.")
        
    #     # Redirect to admin dashboard
    #     admin_dashboard(root)

    # tk.Button(root, text="Submit Order", width=25, height=2, font=("Helvetica", 16), bg='#D2B48C', command=submit_order).pack(pady=10)
    # tk.Button(root, text="Back", width=25, height=2, font=("Helvetica", 16), bg='#D2B48C', command=lambda: current_menu(root, items, previous_menu)).pack(pady=10)


def admin_dashboard(root):
    # Clear previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Admin Dashboard", font=("Helvetica", 20), bg='#8B4513', fg="white").pack(pady=15)

    # Show orders placed
    if orders:
        for order in orders:
            tk.Label(root, text=f"{order['item']} ordered by {order['customer']} (Phone: {order['phone']}, Type: {order['order_type']}, ${order['price']})",
                     font=("Helvetica", 16), bg='#8B4513', fg="white").pack(pady=5)
    else:
        tk.Label(root, text="No orders yet.", font=("Helvetica", 16), bg='#8B4513', fg="white").pack(pady=5)

    # Back to admin menu button
    tk.Button(root, text="Back", width=25, height=2, font=("Helvetica", 16), bg='#D2B48C', command=lambda: admin_menu(root, [], None)).pack(pady=15)


def main_menu(root, items):
    # Clear previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Keyki Shop", font=("Helvetica", 20), bg='#8B4513', fg="white").pack(pady=15)
    
    # Option buttons
    tk.Button(root, text="Admin Login", width=25, height=2, font=("Helvetica", 16), bg='#D2B48C', command=lambda: login_window(root, items)).pack(pady=10)
    tk.Button(root, text="Customer Menu", width=25, height=2, font=("Helvetica", 16), bg='#D2B48C', command=lambda: customer_menu(root, items, None)).pack(pady=10)
    tk.Button(root, text="Exit", width=25, height=2, font=("Helvetica", 16), bg='#D2B48C', command=root.quit).pack(pady=10)


def login_window(root, items):
    def login_attempt():
        username = username_entry.get()
        password = password_entry.get()
        admin_login(username, password, lambda: admin_menu(root, items, None))

    # Clear previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Admin Login", font=("Helvetica", 20), bg='#8B4513', fg="white").pack(pady=15)
    tk.Label(root, text="Username", font=("Helvetica", 16), bg='#8B4513', fg="white").pack(pady=5)
    username_entry = tk.Entry(root, width=25, font=("Helvetica", 16))
    username_entry.pack(pady=10)
    tk.Label(root, text="Password", font=("Helvetica", 16), bg='#8B4513', fg="white").pack(pady=5)
    password_entry = tk.Entry(root, width=25, font=("Helvetica", 16), show="*")
    password_entry.pack(pady=10)
    
    tk.Button(root, text="Login", width=25, height=2, font=("Helvetica", 16), bg='#D2B48C', command=login_attempt).pack(pady=10)
    tk.Button(root, text="Back", width=25, height=2, font=("Helvetica", 16), bg='#D2B48C', command=lambda: main_menu(root, items)).pack(pady=10)


def main():
    # Create Tkinter window
    root = tk.Tk()
    root.geometry("600x700")
    root.configure(bg='#8B4513')
    root.title("Keyki Shop")

    # Start with the main menu
    main_menu(root, load_items())

    root.mainloop()


if __name__ == "__main__":
    main()
