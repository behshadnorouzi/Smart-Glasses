import serial
import matplotlib.pyplot as plt
import time
import keyboard

ser = serial.Serial('COM10', 115200) # Open the serial port

values = []  # Create an empty list to store the values
timestamps = []  # Create an empty list to store the timestamps

while True:
    value = ser.readline().decode('utf-8').strip()  # Read the value from serial and convert it to a string
    try:
        value = int(value)  # Convert the string value to an integer
        timestamp = time.time()  # Get the current timestamp
        values.append(value)  # Append the value to the list
        timestamps.append(timestamp)  # Append the timestamp to the list
        plt.plot(timestamps, values)  # Plot the values against the timestamps
        plt.xlabel('Time')  # Set the x-axis label
        plt.ylabel('A0 Pin')  # Set the y-axis label
        plt.title('A0 Pin vs Time')  # Set the plot title
        plt.pause(1)  # Pause for a short duration to update the plot
    except ValueError:
        print("Invalid value:", value)

    if keyboard.is_pressed('k'):  # Check if the 'k' key is pressed
        plt.close()  # Close the plot
        break

plt.show()  # Show the final plot