# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 12:55:23 2024

@author: lenov
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
from mysql.connector import Error
from PIL import Image, ImageTk
import os
import paramiko
from datetime import datetime

def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host='192.168.11.120',
            user='scidelo',
            password='scidelo2003',
            database='supermarket_db'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def verify_login(connection, full_name, password):
    try:
        cursor = connection.cursor()
        query = "SELECT admin_password FROM admin WHERE admin_name = %s"
        cursor.execute(query, (full_name,))
        result = cursor.fetchone()

        if result:
            db_password = result[0]
            if password == db_password:
                return 0  # Login successful
            else:
                return 1  # Wrong password
        else:
            return 2  # User not in database
    except Error as e:
        print(f"Error: {e}")
        return 3  # Database error

def on_admin_login():
    full_name = full_name_entry.get()
    password = password_entry.get()
    result = verify_login(db_connection, full_name, password)

    if result == 0:
        messagebox.showinfo("Login", "Login successful")
        open_admin_window(full_name)
    elif result == 1:
        messagebox.showwarning("Login", "You entered the wrong password")
    elif result == 2:
        messagebox.showerror("Login", "You are not in the database")
    else:
        messagebox.showerror("Login", "Database error")

def open_admin_window(admin_name):
    global action_frame

    admin_login_window.destroy()
    
    admin_window = tk.Tk()
    admin_window.title("Admin Dashboard")
    admin_window.geometry("800x600")
    admin_window.configure(bg="#2b2b2b")

    # Top Frame
    top_frame = ttk.Frame(admin_window)
    top_frame.pack(side=tk.TOP, fill=tk.X)

    user_icon = Image.open("./images/user.png")  # Replace with the path to your user icon
    user_icon = user_icon.resize((50, 50), Image.Resampling.LANCZOS)
    user_photo = ImageTk.PhotoImage(user_icon)

    user_icon_label = ttk.Label(top_frame, image=user_photo)
    user_icon_label.image = user_photo  # Keep a reference to avoid garbage collection
    user_icon_label.pack(side=tk.LEFT, padx=10, pady=10)

    admin_name_label = ttk.Label(top_frame, text=f"Admin: {admin_name}", font=("Helvetica", 16))
    admin_name_label.pack(side=tk.LEFT, padx=10, pady=10)

    # Menu Frame
    menu_frame = ttk.Frame(admin_window)
    menu_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

    def show_add_seller():
        clear_action_frame()
        add_seller_form()

    def show_add_category():
        clear_action_frame()
        add_category_form()

    add_seller_button = ttk.Button(menu_frame, text="Add Seller", command=show_add_seller)
    add_seller_button.pack(side=tk.LEFT, padx=5)

    add_category_button = ttk.Button(menu_frame, text="Add Category", command=show_add_category)
    add_category_button.pack(side=tk.LEFT, padx=5)

    # Action Frame
    action_frame = ttk.Frame(admin_window)
    action_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    admin_window.mainloop()

def clear_action_frame():
    for widget in action_frame.winfo_children():
        widget.destroy()

def add_seller_form():
    ttk.Label(action_frame, text="Add Seller", font=("Helvetica", 14)).pack(pady=10)
    
    ttk.Label(action_frame, text="Name").pack(pady=5)
    name_entry = ttk.Entry(action_frame)
    name_entry.pack(pady=5)

    ttk.Label(action_frame, text="Password").pack(pady=5)
    password_entry = ttk.Entry(action_frame, show="*")
    password_entry.pack(pady=5)

    ttk.Label(action_frame, text="Confirm Password").pack(pady=5)
    confirm_password_entry = ttk.Entry(action_frame, show="*")
    confirm_password_entry.pack(pady=5)

    def add_seller():
        name = name_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            password_entry.delete(0,tk.END)
            confirm_password_entry.delete(0,tk.END)
            return
        
        try:
            cursor = db_connection.cursor()
            query = "INSERT INTO seller (seller_name, seller_password) VALUES (%s, %s)"
            cursor.execute(query, (name, password))
            db_connection.commit()
            messagebox.showinfo("Success", "Seller added successfully")
            name_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
            confirm_password_entry.delete(0, tk.END)
        except Error as e:
            messagebox.showerror("Error", f"Failed to add seller: {e}")

    ttk.Button(action_frame, text="Add Seller", command=add_seller).pack(pady=10)
def upload_file_to_server(local_file_path, remote_file_path, server_address, username, password):
    try:
        transport = paramiko.Transport((server_address, 22))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(local_file_path, remote_file_path)
        sftp.close()
        transport.close()
        print(f"File uploaded to {remote_file_path}")
        return True
    except Exception as e:
        print(f"Error uploading file: {e}")
        return False
def get_last_id_category():
    try:
        cursor = db_connection.cursor()
        query = "SELECT category_id FROM category ORDER BY category_id DESC LIMIT 1;"
        cursor.execute(query)
        return cursor.fetchone()[0]
    except Error as e:
        messagebox.showerror("Error", f"Failed to get the last categoy_id: {e}")
    finally:
        if cursor:
            cursor.close()

def add_category_form():
    ttk.Label(action_frame, text="Add Category", font=("Helvetica", 14)).pack(pady=10)

    ttk.Label(action_frame, text="Category Name").pack(pady=5)
    category_name_entry = ttk.Entry(action_frame)
    category_name_entry.pack(pady=5)

    ttk.Label(action_frame, text="Category Image").pack(pady=5)
    image_path_var = tk.StringVar()
    image_entry = ttk.Entry(action_frame, textvariable=image_path_var)
    image_entry.pack(pady=5)
    
    def browse_image():
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        image_path_var.set(file_path)
    
    browse_button = ttk.Button(action_frame, text="Browse", command=browse_image)
    browse_button.pack(pady=5)

    def add_category(category_name, local_image_path):
       # Define remote server details
       server_address = '192.168.11.135'  # Replace with your server's IP address
       username = 'DefaultAccount'  # Replace with your server's username
       password = '11223344'  # Replace with your server's password
       remote_directory = 'D:\\gsea1\\technologie web\\projet\\app python\\app python\\images'  # Replace with your remote directory
       id_category=get_last_id_category()
       # Generate a new image name with a timestamp
       new_image_name = f"category_{id_category}{os.path.splitext(local_image_path)[1]}"
       remote_image_path = f'{remote_directory}/{new_image_name}'

       # Upload the image file to the remote server
       if upload_file_to_server(local_image_path, remote_image_path, server_address, username, password):
           try:
               connection = create_db_connection()
               cursor = connection.cursor()
               query = "INSERT INTO category (category_name, category_photo) VALUES (%s, %s)"
               cursor.execute(query, (category_name, remote_image_path))
               connection.commit()
               print("Category added successfully")
               messagebox.showinfo("Success", "Category added successfully")
           except Error as e:
               print(f"Error: {e}")
               messagebox.showerror("Error", f"Failed to add category: {e}")
           finally:
               if connection.is_connected():
                   cursor.close()
                   connection.close()
    def submit_category():
       category_name = category_name_entry.get()
       local_image_path = image_path_var.get()

       if not category_name or not local_image_path:
           messagebox.showerror("Error", "Please fill all fields and select an image")
           return

       add_category(category_name, local_image_path)
           
    ttk.Button(action_frame, text="Add Category", command=submit_category).pack(pady=10)

# Create a database connection once
db_connection = create_db_connection()

# Initialize the main window for admin login
admin_login_window = tk.Tk()
admin_login_window.title("Admin Login")
admin_login_window.geometry("300x200")
admin_login_window.resizable(False, False)
admin_login_window.configure(bg="#2b2b2b")

# Style configuration
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#2b2b2b", foreground="#FFFFFF", font=("Helvetica", 12))
style.configure("TButton", background="#1e90ff", foreground="#FFFFFF", font=("Helvetica", 12), padding=5)
style.configure("TEntry", font=("Helvetica", 12))

# Add widgets for admin login
ttk.Label(admin_login_window, text="Admin Name:").pack(pady=5)
full_name_entry = ttk.Entry(admin_login_window)
full_name_entry.pack(pady=5)

ttk.Label(admin_login_window, text="Password:").pack(pady=5)
password_entry = ttk.Entry(admin_login_window, show="*")
password_entry.pack(pady=5)

ttk.Button(admin_login_window, text="Login", command=on_admin_login).pack(pady=10)

# Start the main event loop
admin_login_window.mainloop()
