import time
import serial
import cv2
from ultralytics import YOLO
import cvzone
import pandas as pd


def setup_serial_connection(port="/dev/ttyACM0", baudrate=9600):
    """Initialize the serial connection."""
    return serial.Serial(port, baudrate)


def load_model(model_path='../models/kowalskibank_yolov8n.pt'):
    """Load the YOLO model."""
    return YOLO(model_path)


def get_class_color(class_id):
    """Assign a color to each class."""
    class_colors = {
        0: (36, 21, 24),     # billete_10k
        1: (242, 240, 206),  # billete_20k
        2: (56, 49, 13),      # billete_2k
        3: (36, 1, 57),      # billete_50k
        4: (1, 51, 56)     # billete_5k
    }
    return class_colors.get(class_id, (255, 255, 255))  # Default to white for unknown classes

def process_frame(model, frame, serial_connection):
    """Process a single frame: run prediction, annotate, and send class data over serial."""
    results = model.predict(frame, conf=0.5)[0]

    if len(results.boxes):
        boxes_data = results.boxes.data
        px = pd.DataFrame(boxes_data).astype("float")
        for index, row in px.iterrows():
            x1, y1, x2, y2, conf, class_id = row.astype(int)
            conf =  row[4]
            color = get_class_color(class_id)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cvzone.putTextRect(frame, f'{model.names[class_id]} {conf:.2f}', (x1, y1), 1, 1, colorR=color)

            class_str = f"{class_id}\n"
            class_bytes = class_str.encode('utf-8')
            serial_connection.write(class_bytes)

    return frame


def main():
    """Main function to run the video capture and processing loop."""
    ser = setup_serial_connection()
    model = load_model()

    vid = cv2.VideoCapture(0)
    time.sleep(1)  # Give the camera time to warm up

    try:
        while True:
            ret, frame = vid.read()
            frame = cv2.resize(frame,(640,640))
            if not ret:
                print("Failed to capture image")
                break

            processed_frame = process_frame(model, frame, ser)
            cv2.imshow('YOLO V8 Detection', processed_frame)

            if cv2.waitKey(1) & 0xFF == ord(' '):
                break

    except KeyboardInterrupt:
        print("\nInterrupción por teclado")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        vid.release()
        cv2.destroyAllWindows()
        ser.close()


if __name__ == "__main__":
    main()