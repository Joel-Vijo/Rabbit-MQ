import pika
import tkinter as tk

bg_color = "#000000"  
fg_color = "#FFA500"
font_style = ("Times", 12)

def send_message(queue_name, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    # channel to communicate with the queue
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    # Publish the message to the queue
    channel.basic_publish(exchange='', routing_key=queue_name, body=message)
    print(f"Message sent to queue '{queue_name}': {message}")
    connection.close()

def send_message_from_entry(queue_entry, message_entry):
    queue_name = queue_entry.get()
    # Get the message from the message entry field
    message = message_entry.get()
    send_message(queue_name, message)

root = tk.Tk()
root.title("Producer")
root.geometry("400x150")
root.configure(bg=bg_color)

# Frame to center align the content
center_frame = tk.Frame(root, bg=bg_color)
center_frame.pack(expand=True, padx=20, pady=20)

# Create label for queue entry field
queue_label = tk.Label(center_frame, text="Queue:", fg=fg_color, bg=bg_color, font=font_style)
queue_label.grid(row=0, column=0, padx=5, pady=5)

# Create entry field for queue name
queue_entry = tk.Entry(center_frame, bg=fg_color, fg=bg_color, font=font_style)
queue_entry.grid(row=0, column=1, padx=5, pady=5)

# Create label for message entry field
message_label = tk.Label(center_frame, text="Message:", fg=fg_color, bg=bg_color, font=font_style)
message_label.grid(row=1, column=0, padx=5, pady=5)

# Create entry field for message
message_entry = tk.Entry(center_frame, bg=fg_color, fg=bg_color, font=font_style)
message_entry.grid(row=1, column=1, padx=5, pady=5)

send_button = tk.Button(center_frame, text="Send", bg=fg_color, fg=bg_color, font=font_style, command=lambda: send_message_from_entry(queue_entry, message_entry))
send_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Center align the window
root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())

# Start the GUI event loop
root.mainloop()
