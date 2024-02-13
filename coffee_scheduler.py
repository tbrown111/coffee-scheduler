import tkinter as tk

people_list = []
schedule_already_generated = False
names = set()
error_message_count = 0

class Person:
    def __init__(self, name, coffee, cost):
        self.name = name
        self.coffee = coffee
        self.cost = cost
        self.amount_paid = 0
        self.running_diff = 0

def add_person():
    global error_message_count
    result_text.config(state=tk.NORMAL)

    name = name_entry.get()
    if (name == "Enter Name"):
        result_text.insert(tk.END, f"Please enter a valid name\n", "red")
        error_message_count += 1
        return
    coffee = coffee_entry.get()
    if (coffee == "Enter Coffee"):
        result_text.insert(tk.END, f"Please enter a valid coffee type\n", "red")
        error_message_count += 1
        return
    try:
        cost = float(cost_entry.get())
    except ValueError as e:
        result_text.insert(tk.END, f"Please enter a number for Cost\n", "red")
        error_message_count += 1
        return

    if name in names:
        result_text.insert(tk.END, f"{name} is already in the group\n", "red")
        error_message_count += 1
    else:
        names.add(name)
        new_person = Person(name, coffee, cost)
        people_list.append(new_person)
        if error_message_count > 0:
            result_text.delete(float(len(people_list)), float(len(people_list)) + float(error_message_count))
            error_message_count = 0
        result_text.insert(tk.END, f"{name} drinks a {coffee}. The cost is ${cost:.2f}\n", "green")
        result_text.config(state=tk.DISABLED)

    # Clear the input fields
    name_entry.delete(0, tk.END)
    if name_entry != root.focus_get():
        name_entry.insert(tk.END, "Enter Name")
        name_entry.config(fg="grey")

    coffee_entry.delete(0, tk.END)
    if coffee_entry != root.focus_get():
        coffee_entry.insert(tk.END, "Enter Coffee")
        coffee_entry.config(fg="grey")

    cost_entry.delete(0, tk.END)
    if cost_entry != root.focus_get():
        cost_entry.insert(tk.END, "Enter Cost as Number")
        cost_entry.config(fg="grey")
    
def generate_payment_schedule(days):
    schedule = []
    total_cost = sum(person.cost for person in people_list)
    
    day_num = 1
    for person in people_list:
        person.amount_paid += total_cost
        update_running_diff(people_list, day_num)
        print_running_diffs(people_list, day_num)
        schedule.append(f"Day {day_num}: {person.name} pays ${total_cost:.2f} for everyone\n")
        day_num += 1

    for day in range(len(people_list) + 1, days + 1):
        next_person = max(people_list, key=lambda person: person.running_diff)
        next_person.amount_paid += total_cost
        update_running_diff(people_list, day)
        print_running_diffs(people_list, day)
        schedule.append(f"Day {day}: {next_person.name} pays ${total_cost:.2f} for everyone\n")

    print("Stats:")
    for person in people_list:
        print(f"{person.name}:")
        print(f"  Amount Paid: ${person.amount_paid:.2f}")
        print(f"  Expected Amount: ${(person.cost * days ):.2f}")
        print()
    return schedule

def show_schedule():
    global schedule_already_generated
    global error_message_count
    if schedule_already_generated:
        return
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    error_message_count = 0
    schedule = []
    if len(people_list) > 0:
        schedule = generate_payment_schedule(int(days_entry.get()))
        schedule_already_generated = True
        result_text.insert(tk.END, "".join(schedule), "green")
    else:
        result_text.config(state=tk.NORMAL, fg="red")
        schedule = ["Cannot generate payment schedule.\nPlease add a person.\n"]
        error_message_count += 2
        result_text.insert(tk.END, "".join(schedule), "red")
    result_text.config(state=tk.DISABLED)

def update_running_diff(people_list, day_num):
    for i, person in enumerate(people_list, start=1):
        person.running_diff = (day_num * person.cost) - person.amount_paid

def print_running_diffs(people_list, day):
    if day == 1:
        print("Day\tPerson\tAmount Paid\tAmount if bought alone\tRunning difference")
    for person in people_list:
        print(f"{day}\t{person.name}\t{person.amount_paid}\t\t{person.cost*day}\t\t\t{person.running_diff}")

def on_name_entry_click(event):
    if name_entry.get() == "Enter Name":
        name_entry.delete(0, tk.END)
        name_entry.config(fg="black")  # Change text color to black when user starts typing

def on_name_entry_focus_out(event):
    if not name_entry.get():
        name_entry.insert(tk.END, "Enter Name")
        name_entry.config(fg="grey")  # Set text color back to grey

def on_coffee_entry_click(event):
    if coffee_entry.get() == "Enter Coffee":
        coffee_entry.delete(0, tk.END)
        coffee_entry.config(fg="black")

def on_coffee_entry_focus_out(event):
    if not coffee_entry.get():
        coffee_entry.insert(tk.END, "Enter Coffee")
        coffee_entry.config(fg="grey")

def on_cost_entry_click(event):
    if cost_entry.get() == "Enter Cost as Number":
        cost_entry.delete(0, tk.END)
        cost_entry.config(fg="black")

def on_cost_entry_focus_out(event):
    if not cost_entry.get():
        cost_entry.insert(tk.END, "Enter Cost as Number")
        cost_entry.config(fg="grey")

def on_days_entry_click(event):
    days_entry.config(fg="black")  # Change text color to black when user starts typing

def on_days_entry_focus_out(event):
    days_entry.config(fg="grey")  # Set text color back to grey
    

# Create and configure the main window
root = tk.Tk()
root.title("Who's paying?")
root.geometry("410x600")  # Set window size
root.config(bg="#f2f2f2")  # Set background color

# Create and place widgets in the main window using the grid geometry manager
instructions_message = "Instructions: Enter info and click 'Add Person' to add people\nto the group. Then click 'Generate Payment Schedule.'"
instructions_label = tk.Label(root, text=instructions_message, bg="#f2f2f2", justify="left", anchor="w")
instructions_label.grid(row=0, column=0, columnspan=2, pady=5, padx=20, sticky=tk.W)

name_entry_label = tk.Label(root, text="Name:", bg="#f2f2f2")
name_entry_label.grid(row=1, column=0, sticky=tk.W, pady=5, padx=20)

name_entry = tk.Entry(root, fg="grey")
name_entry.insert(tk.END, "Enter Name")
name_entry.bind("<FocusIn>", on_name_entry_click)
name_entry.bind("<FocusOut>", on_name_entry_focus_out)
name_entry.grid(row=1, column=1, sticky=tk.W, pady=5)

coffee_entry_label = tk.Label(root, text="Favorite Coffee:", bg="#f2f2f2")
coffee_entry_label.grid(row=2, column=0, sticky=tk.W, pady=5, padx=20)

coffee_entry = tk.Entry(root, fg="grey")
coffee_entry.insert(tk.END, "Enter Coffee")
coffee_entry.bind("<FocusIn>", on_coffee_entry_click)
coffee_entry.bind("<FocusOut>", on_coffee_entry_focus_out)
coffee_entry.grid(row=2, column=1, sticky=tk.W, pady=5)

cost_entry_label = tk.Label(root, text="Cost:", bg="#f2f2f2")
cost_entry_label.grid(row=3, column=0, sticky=tk.W, pady=5, padx=20)

cost_entry = tk.Entry(root, fg="grey")
cost_entry.insert(tk.END, "Enter Cost as Number")
cost_entry.bind("<FocusIn>", on_cost_entry_click)
cost_entry.bind("<FocusOut>", on_cost_entry_focus_out)
cost_entry.grid(row=3, column=1, sticky=tk.W, pady=5)

add_button = tk.Button(root, text="Add Person", command=add_person, fg="black", highlightbackground="#f2f2f2")
add_button.grid(row=4, column=0, columnspan=2, pady=10)

result_text = tk.Text(root, height=20, width=50, state=tk.DISABLED, bg="#e6e6e6")  # Set text area background color
result_text.grid(row=5, column=0, columnspan=2, pady=10, padx=20)
result_text.tag_config("red", foreground="red")
result_text.tag_config("green", foreground="green")

generate_button = tk.Button(root, text="Generate Payment Schedule", fg="black", command=lambda: show_schedule(), highlightbackground="#f2f2f2")
generate_button.grid(row=6, column=0, columnspan=2, pady=10)

days_label = tk.Label(root, text="for", bg="#f2f2f2")
days_label.grid(row=7, column=0, sticky=tk.W, padx=95, columnspan=2)

days_entry = tk.Entry(root, fg="grey", width=5)
days_entry.insert(tk.END, "100")
days_entry.bind("<FocusIn>", on_days_entry_click)
days_entry.bind("<FocusOut>", on_days_entry_focus_out)
days_entry.grid(row=7, column=0, sticky=tk.W, padx=120, columnspan=2)

days_label = tk.Label(root, text="days into the future", bg="#f2f2f2")
days_label.grid(row=7, column=1, sticky=tk.W, padx=5)

# Start the main event loop
root.mainloop()
