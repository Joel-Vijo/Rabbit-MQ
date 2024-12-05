import pika 
import tkinter as tk 

bg_color = "#2F4F4F"
fg_color = "#FFA500"
font_style = "Times New Roman" 

# function to receive messages from a message queue
def receive_message(queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    
    # Retrieve a message from the specified queue
    method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=True)
    print(f"Message sent to queue '{queue_name}': {body}")
    
    # If a message was received, display it in a new window
    if method_frame:
        # Create a new window to display the message
        message_window = tk.Toplevel()
        message_window.title("Received Message")
        message_window.configure(bg=bg_color)

        # Create a frame to center align the content
        center_frame = tk.Frame(message_window, bg=bg_color)
        center_frame.pack(expand=True, padx=20, pady=20)

        # Create a label to display the received message
        message_label = tk.Label(center_frame, text=body.decode(), fg=fg_color, bg=bg_color, font=(font_style, 14))
        message_label.pack(padx=5, pady=5)
        
        # Get the number of messages remaining in the queue
        message_count = method_frame.message_count
        
        # Create a label to display the number of messages remaining in the queue
        message_count_label = tk.Label(center_frame, text="{} message(s) remaining in the queue".format(message_count), fg=fg_color, bg=bg_color, font=(font_style, 10))
        message_count_label.pack(padx=5, pady=5)

        
    else:
        # Create a new window to display the empty queue message
        message_window = tk.Toplevel()
        message_window.title("Empty Queue")
        message_window.configure(bg=bg_color)

        # Create a frame to center align the content
        center_frame = tk.Frame(message_window, bg=bg_color)
        center_frame.pack(expand=True, padx=20, pady=20)

        # Create a label to display the empty queue message
        message_label = tk.Label(center_frame, text="The specified queue is empty.", fg=fg_color, bg=bg_color, font=(font_style, 14))
        message_label.pack(padx=5, pady=5)

    # Close the connection to RabbitMQ
    connection.close()

# Create the main GUI window
root = tk.Tk()
root.title("Consumer") 
root.geometry("400x150")
root.configure(bg=bg_color) 

# Create a frame within the main window to center align the content
center_frame = tk.Frame(root, bg=bg_color)
center_frame.pack(expand=True, padx=20, pady=20)

# Add a label and an entry field for the user to specify the message queue to receive from
queue_label = tk.Label(center_frame, text="Queue:", fg=fg_color, bg=bg_color, font=(font_style, 14))
queue_label.grid(row=0, column=0, padx=5, pady=5)

queue_entry = tk.Entry(center_frame, bg=fg_color, fg=bg_color, font=(font_style, 14))
queue_entry.grid(row=0, column=1, padx=5, pady=5)

receive_button = tk.Button(center_frame, text="Receive", bg=fg_color, fg=bg_color, font=(font_style, 14), command=lambda: receive_message(queue_entry.get()))
receive_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# Center the main window on the screen
root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())

# Start the GUI event loop
root.mainloop()
