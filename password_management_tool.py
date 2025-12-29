import tkinter as tk
from tkinter import messagebox
import random
import string
import math


# Common Passwords
common_passwords = [
    "0000", "00000", "000000", "0000000", "00000000",
    "1111", "11111", "111111", "1111111", "11111111",
    "1234", "12345", "123456", "1234567", "12345678", "123456789",
    "987654321", "password", "qwerty", "abc123", "letmein", "welcome",
    "123", "123123", "1q2w3e4r", "admin", "monkey", "dragon", "sunshine",
    "princess", "iloveyou", "football", "baseball", "login", "starwars",
    "passw0rd", "trustno1", "hello", "freedom", "whatever", "qazwsx",
    "654321", "superman", "jordan", "shadow", "master", "killer",
    "hottie", "loveme", "zaq1zaq1", "password1", "123qwe", "letmein123",
    "batman", "696969", "7777777", "1qaz2wsx", "qwerty123", "charlie",
    "donald", "michael", "pokemon", "6969", "1q2w3e", "asdfgh",
    "zxcvbnm", "test", "computer", "welcome1", "q1w2e3r4", "abcd1234",
    "qwer1234", "121212", "888888", "qwe123", "1q2w3e4r5t", "123abc",
    "qwertyuiop", "password123", "mypass", "letmeinnow", "omg123",
    "myspace1", "football1", "babygirl", "hannah", "loveyou", "jesus",
    "ninja", "password!", "admin123", "pass123", "69696969", "michelle",
    "tigger", "pepper", "cheese", "banana", "bailey", "welcome123",
    "soccer", "ashley", "andrew", "purple", "george", "summer",
    "biteme", "jessica", "pepper123", "maggie", "taylor", "secret",
    "samantha", "silver", "cookie", "matrix", "orange", "buster",
    "nicole", "hello123", "12341234", "hello1", "daniel"
]


# Helpers
def calculate_entropy(password):
    pool = 0
    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(c in string.punctuation for c in password):
        pool += len(string.punctuation)
    return math.log2(pool) * len(password) if pool else 0

def is_common_password(password):
    return password in common_passwords

def generate_password(length=12):
    char_sets = [string.ascii_lowercase, string.ascii_uppercase,
                 string.digits, string.punctuation]
    password = [random.choice(cs) for cs in char_sets]
    all_chars = ''.join(char_sets)
    password += [random.choice(all_chars) for _ in range(length - len(password))]
    random.shuffle(password)
    return ''.join(password)


# Actions
def check_password():
    password = check_entry.get()
    if not password:
        messagebox.showwarning("Input Required", "Please enter a password to check.")
        return

    if is_common_password(password):
        result_label.config(text="❌ This is a common password!", fg="red")
    else:
        entropy = calculate_entropy(password)
        if entropy < 40:
            result_label.config(
                text=f"⚠️ Entropy: {entropy:.2f} - Not strong enough.",
                fg="orange"
            )
        else:
            result_label.config(
                text=f"✅ Strong password! Entropy: {entropy:.2f}",
                fg="green"
            )

def generate_new_password():
    try:
        length = length_slider.get()  # get the value from slider
        password = generate_password(length)
        gen_entry.delete(0, tk.END)
        gen_entry.insert(0, password)
        result_label.config(text="🔐 New password generated!", fg="blue")
        update_strength_bar(password)
    except ValueError:
        messagebox.showerror("Invalid Input", "Enter a valid number for password length.")

def copy_to_clipboard():
    password = gen_entry.get()
    if password:
        app.clipboard_clear()
        app.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

def show_info():
    messagebox.showinfo(
        "How It Works",
        "🔐 This tool helps you check the strength of a password and generate secure ones.\n\n"
        "🧠 Entropy is used to measure password strength. It's calculated based on character variety and length.\n"
        "Higher entropy = more unpredictability = stronger password.\n\n"
        "🛡️ Passwords are checked against a list of common/weak passwords.\n\n"
        "💡 Use a mix of uppercase, lowercase, digits, and symbols for better security."
    )


# GUI Setup
app = tk.Tk()
app.title("Password Management Tool")
app.geometry("550x390")
app.resizable(False, False)


# Top-right Info Button
info_btn = tk.Button(app, text="ℹ", font=("Arial", 10, "bold"), width=2, command=show_info)
info_btn.place(x=520, y=10)


# Password Checker
tk.Label(app, text="Check Password Strength:", font=("Arial", 12, "bold")).pack(pady=(15, 5))

check_frame = tk.Frame(app)
check_frame.pack()

check_entry = tk.Entry(check_frame, width=40, font=('Arial', 12), show="*")
check_entry.pack(side="left")


# Visibility Toggle
def toggle_visibility():
    if check_entry.cget('show') == "":
        check_entry.config(show="*")
        toggle_btn.config(text="Show")
    else:
        check_entry.config(show="")
        toggle_btn.config(text="Hide")

toggle_btn = tk.Button(check_frame, text="Show", width=6, command=toggle_visibility)
toggle_btn.pack(side="left", padx=5)

check_button = tk.Button(app, text="Check Strength", command=check_password)
check_button.pack(pady=10)


# Strength Bar
strength_frame = tk.Frame(app)
strength_frame.pack(pady=2)

strength_canvas = tk.Canvas(strength_frame, width=300, height=20, bg="lightgray", highlightthickness=0)
strength_canvas.pack(side="left")

strength_bar = strength_canvas.create_rectangle(0, 0, 0, 20, fill="red")
strength_text = strength_canvas.create_text(150, 10, text="Very Weak", fill="white", font=("Arial", 10, "bold"))

def update_strength_bar(password=None):
    password = password if password is not None else check_entry.get()
    entropy = calculate_entropy(password)
    width = min(300, int(entropy * 5))

    if is_common_password(password) or len(password) == 0:
        color = "red"
        width = 30
        label = "Very Weak"
    elif entropy < 28:
        color = "red"
        label = "Very Weak"
    elif entropy < 40:
        color = "orange"
        label = "Weak"
    elif entropy < 55:
        color = "yellow"
        label = "Moderate"
    elif entropy < 70:
        color = "lightgreen"
        label = "Good"
    else:
        color = "green"
        label = "Strong"

    strength_canvas.coords(strength_bar, 0, 0, width, 20)
    strength_canvas.itemconfig(strength_bar, fill=color)
    strength_canvas.itemconfig(strength_text, text=label, fill="black" if color in ["yellow", "lightgreen"] else "white")

check_entry.bind("<KeyRelease>", lambda e: update_strength_bar())


# Password Generator
tk.Label(app, text="Generate Strong Password:", font=("Arial", 12, "bold")).pack(pady=(20, 5))
length_frame = tk.Frame(app)
length_frame.pack()

# Label for slider
tk.Label(length_frame, text="Length: ").pack(side="left")

# Password length slider from 4 to 15, default 12
length_slider = tk.Scale(length_frame, from_=4, to=15, orient=tk.HORIZONTAL, length=150)
length_slider.set(12)  # default value
length_slider.pack(side="left")

generate_button = tk.Button(length_frame, text="Generate", command=generate_new_password)
generate_button.pack(side="left", padx=10)


# Generated password + Copy button
gen_frame = tk.Frame(app)
gen_frame.pack(pady=(10, 0))

gen_entry = tk.Entry(gen_frame, width=40, font=('Arial', 12))
gen_entry.pack(side="left")

copy_btn = tk.Button(gen_frame, text="Copy", width=6, command=copy_to_clipboard)
copy_btn.pack(side="left", padx=5)


# Result
result_label = tk.Label(app, text="", font=("Arial", 12))
result_label.pack(pady=15)

app.mainloop()
