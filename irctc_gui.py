import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import urllib.request, io
import datetime
import time

# Train image URLs
image_urls = {
    "12345": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/WAP-7_locomotive_with_Kanpur_Shatabdi_Express.jpg/640px-WAP-7_locomotive_with_Kanpur_Shatabdi_Express.jpg",
    "54321": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Indian_Railways_AC_coach.JPG/640px-Indian_Railways_AC_coach.JPG",
    "67890": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Sleeper_class_train.jpg/640px-Sleeper_class_train.jpg",
    "11223": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/WDM-3A_locomotive_with_passenger_train.jpg/640px-WDM-3A_locomotive_with_passenger_train.jpg",
    "33445": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Howrah_Duronto_Express.jpg/640px-Howrah_Duronto_Express.jpg",
    "55667": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Train_at_Bhestan_Station.jpg/640px-Train_at_Bhestan_Station.jpg"
}

trains = {
    "12345": {"name": "Rajdhani Express", "coaches": {"A1": 10, "A2": 10, "A3": 10, "AC": 20, "NON AC": 30, "SLEEPER": 40}, "image": image_urls["12345"]},
    "54321": {"name": "Shatabdi Express", "coaches": {"A1": 5, "AC": 25, "NON AC": 30, "SLEEPER": 20}, "image": image_urls["54321"]},
    "67890": {"name": "Duronto Express", "coaches": {"A1": 5, "A2": 5, "AC": 10, "SLEEPER": 25}, "image": image_urls["67890"]},
    "11223": {"name": "Garib Rath Express", "coaches": {"A1": 8, "A2": 8, "AC": 18, "NON AC": 28, "SLEEPER": 35}, "image": image_urls["11223"]},
    "33445": {"name": "Howrah Duronto", "coaches": {"A1": 6, "A2": 6, "A3": 6, "AC": 15, "SLEEPER": 30}, "image": image_urls["33445"]},
    "55667": {"name": "Ahmedabad Express", "coaches": {"A1": 7, "AC": 12, "NON AC": 22, "SLEEPER": 30}, "image": image_urls["55667"]},
}

bookings = []

root = tk.Tk()
root.title("IRCTC Reservation System")
root.geometry("1100x750")
root.configure(bg="#f2f2f2")
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

clock_label = tk.Label(root, font=('Segoe UI', 12, 'bold'), fg="blue", bg="#f2f2f2")
clock_label.pack(anchor='ne', padx=10, pady=5)

def update_clock():
    now = time.strftime("%H:%M:%S")
    clock_label.config(text=f"Live Time: {now}")
    root.after(1000, update_clock)
update_clock()

style = ttk.Style()
style.configure("Treeview", font=('Segoe UI', 10), rowheight=30)
style.configure("Treeview.Heading", font=('Segoe UI', 12, 'bold'))

# Train Schedule
schedule_tab = tk.Frame(notebook, bg="#e6f2ff")
notebook.add(schedule_tab, text="Train Schedule")

columns = ("Train Number", "Train Name", "Coaches")
tree = ttk.Treeview(schedule_tab, columns=columns, show="headings", height=8)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=300, anchor="center")
tree.pack(pady=20)

for tid, tinfo in trains.items():
    coach_summary = ", ".join([f"{k}:{v}" for k, v in tinfo["coaches"].items()])
    tree.insert("", "end", values=(tid, tinfo["name"], coach_summary))

image_label = tk.Label(schedule_tab, bg="#e6f2ff")
image_label.pack(pady=10)

def on_select(event):
    selected = tree.focus()
    if not selected:
        return
    values = tree.item(selected, 'values')
    train_id = values[0]
    image_url = trains[train_id]["image"]
    try:
        with urllib.request.urlopen(image_url) as u:
            raw_data = u.read()
        img = Image.open(io.BytesIO(raw_data)).resize((600, 250))
        img_tk = ImageTk.PhotoImage(img)
        image_label.configure(image=img_tk)
        image_label.image = img_tk
    except:
        image_label.configure(text="Image not available", image="")
        image_label.image = None

tree.bind("<<TreeviewSelect>>", on_select)

# Booking
booking_tab = tk.Frame(notebook, bg="#fff")
notebook.add(booking_tab, text="Booking")

train_var = tk.StringVar()
tk.Label(booking_tab, text="Select Train Number", bg="#fff").pack(pady=5)
train_combo = ttk.Combobox(booking_tab, textvariable=train_var, values=list(trains.keys()), state="readonly")
train_combo.pack(pady=5)

entry_name = tk.Entry(booking_tab)
tk.Label(booking_tab, text="Passenger Name", bg="#fff").pack(pady=5)
entry_name.pack(pady=5)

coach_type = ttk.Combobox(
    booking_tab,
    values=["A1", "A2", "A3", "AC", "NON AC", "SLEEPER"],
    state="readonly"
)
coach_type.set("Select Coach Type")
coach_type.pack(pady=10)

def book_ticket():
    train = train_var.get()
    name = entry_name.get()
    coach = coach_type.get()
    if not (train and name and coach and coach != "Select Coach Type"):
        messagebox.showerror("Error", "Please fill all fields")
        return
    booking = {
        "train": train,
        "name": name,
        "coach": coach,
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    bookings.append(booking)
    messagebox.showinfo("Success", f"Ticket booked for {name}")
    entry_name.delete(0, 'end')
    coach_type.set("Select Coach Type")

book_button = tk.Button(booking_tab, text="Book Ticket", command=book_ticket, bg="#0066cc", fg="white")
book_button.pack(pady=10)

# Cancellation
cancel_tab = tk.Frame(notebook, bg="#ffe6e6")
notebook.add(cancel_tab, text="Cancellation")

tk.Label(cancel_tab, text="Enter Passenger Name to Cancel", bg="#ffe6e6").pack(pady=5)
cancel_name = tk.Entry(cancel_tab)
cancel_name.pack(pady=5)

def cancel_ticket():
    name = cancel_name.get()
    global bookings
    before = len(bookings)
    bookings = [b for b in bookings if b['name'] != name]
    after = len(bookings)
    if before == after:
        messagebox.showinfo("Not Found", "No booking found")
    else:
        messagebox.showinfo("Cancelled", f"Booking cancelled for {name}")
    cancel_name.delete(0, 'end')

cancel_button = tk.Button(cancel_tab, text="Cancel Ticket", command=cancel_ticket, bg="#cc0000", fg="white")
cancel_button.pack(pady=10)

# Report
report_tab = tk.Frame(notebook, bg="#e6ffe6")
notebook.add(report_tab, text="Booking Report")

report_train_var = tk.StringVar()
tk.Label(report_tab, text="Select Train Number for Report", bg="#e6ffe6").pack(pady=5)
report_combo = ttk.Combobox(report_tab, textvariable=report_train_var, values=list(trains.keys()), state="readonly")
report_combo.pack(pady=5)

report_text = tk.Text(report_tab, width=80, height=20, bg="#f9fff9")
report_text.pack(pady=10)

def show_report():
    selected_train = report_train_var.get()
    report_text.delete(1.0, 'end')
    filtered = [b for b in bookings if b['train'] == selected_train]
    if not filtered:
        report_text.insert('end', "No bookings available for this train")
    else:
        for b in filtered:
            report_text.insert('end', f"Name: {b['name']} | Train: {b['train']} | Coach: {b['coach']} | Time: {b['time']}\n")

report_button = tk.Button(report_tab, text="Show Report", command=show_report, bg="#009933", fg="white")
report_button.pack()

root.mainloop()