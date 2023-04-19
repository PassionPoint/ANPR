import cv2
import easyocr
import datetime

# Load the number plate cascade classifier
NumberPlateCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')

# Initialize the EasyOCR reader with the English language
reader = easyocr.Reader(['en'])

# Start the video capture using the default camera
cap = cv2.VideoCapture(0)

# Define a function to display the captured number plate
def displayCapturedPlate(plate):
    cv2.imshow('Taken Plate', plate)

while True:
    # Read the current frame from the video capture
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect the number plate using the cascade classifier
    NumberPlate = NumberPlateCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(25,25))

    # Display the live camera feed
    cv2.imshow('Live Camera', frame)

    # Exit the program when the 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

    # If a number plate is detected, process it
    if len(NumberPlate) > 0:
        for (x, y, w, h) in NumberPlate:
            # Crop the number plate from the frame
            plate = gray[y: y+h, x:x+w]

            # Apply a Gaussian blur to the plate to reduce noise
            blur = cv2.GaussianBlur(plate, (9,9), 1)

            # Apply an adaptive threshold to the plate to make the characters stand out
            thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

            # Display the captured number plate
            displayCapturedPlate(plate)

            # Use EasyOCR to recognize the characters on the plate
            result = reader.readtext(thresh, allowlist='ABCDEFGHJKLMNOPQRSTUVWXYZ0123456789')

            # Loop through the recognized characters and print them
            for r in result:
            	# Save the captured image to a file with a timestamp
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                filename = '/home/saj/NumberPlate-Images/NP_{}.jpg'.format(timestamp)
                cv2.imwrite(filename, frame)
                # Makes sure to output a result with 60% accuracy
                if r[2] >= 0.6:
                        print("License plate detected:", r[1])
                        print("Accuracy:", r[2])
                                
                        # Check if the plate is in the whitelist
                        with open("whitelist.txt", "r") as f:
                                whitelist = f.read().splitlines()
                        if r[1] in whitelist:
                                print("Welcome back ",r[1],". Gates are open")

                    	# Check if the plate is in the blacklist
                        with open("blacklist.txt", "r") as f:
                                blacklist = f.read().splitlines()
                        if r[1] in blacklist:
                                print("Unauthorised access.")
                                
                else:
                    continue

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
