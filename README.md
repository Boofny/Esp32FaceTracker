# ESP32 Face Tracker

**A real-time computer vision system that physically moves servos to follow your face.**

Python captures webcam frames, detects your face with MediaPipe, and streams position data over serial to an ESP32. The ESP32 firmware, written in C++ with PlatformIO, drives servos to track the face in real time. The project spans computer vision, serial communication, embedded firmware, and hardware wiring.

`Python` `OpenCV` `MediaPipe` `PySerial` `C++` `ESP32` `PlatformIO` `uv`

## How It Works

```
Webcam -> OpenCV -> MediaPipe -> PySerial ---(USB serial)---> ESP32 -> Servo(s)
```

1. **OpenCV** captures frames from the webcam.
2. **MediaPipe** detects the face and returns its position in the frame.
3. The Python script maps the tracked position to servo angles.
4. **PySerial** sends those angles to the ESP32 over USB serial.
5. The **ESP32** firmware (C++, Arduino framework, `ESP32Servo` library) parses the incoming data and moves the servos.

## Wiring

| Component         | ESP32 Pin | Notes                                               |
| ----------------- | --------- | --------------------------------------------------- |
| Pan servo signal  | `GPIO 19` | Update to match your build                          |
| Tilt servo signal | `GPIO 18` | Update to match your build                          |
| Servo VCC         | `5V`      | Use an external supply if servos draw heavy current |
| Servo GND         | `GND`     | Share a common ground with the ESP32                |

> Servos can draw more current than the USB port provides. If you see brownouts or resets, power them from a separate 5V supply and tie the grounds together.

## Tech Stack

**(Python)**
- [uv](https://github.com/astral-sh/uv) for package and Python version management
- OpenCV
- MediaPipe
- PySerial

**(C++)**
- ESP32
- [PlatformIO](https://platformio.org/)
- Arduino framework with the `ESP32Servo` library

## Getting Started

### Prerequisites

- An ESP32 dev board and one or more hobby servos
- A webcam
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [PlatformIO](https://platformio.org/install) (CLI or the VS Code extension)

### Why uv?

MediaPipe and OpenCV only publish wheels for certain Python versions, so the newest Python is often not supported. `uv` makes this painless by fetching and using a compatible interpreter automatically, so you don't have to manage versions yourself.

### 1. Flash the ESP32

Open the PlatformIO project and upload it to the board:

```bash
pio run --target upload
```

Optionally open the serial monitor to confirm it's alive:

```bash
pio device monitor
```

### 2. Run the tracker

Update the serial port in `track.py` to match your system (for example `COM3` on Windows, `/dev/ttyUSB0` on Linux, or `/dev/cu.usbserial-*` on macOS), then:

```bash
uv run track.py
```

`uv` will create the environment, install dependencies, and run the script with a compatible Python version.

> Close the PlatformIO serial monitor before running `track.py`, since only one program can hold the serial port at a time.

## Configuration

| Setting      | Where      | Description                              |
| ------------ | ---------- | ---------------------------------------- |
| Serial port  | `track.py` | Port the ESP32 is connected to           |
| Baud rate    | Both       | Must match on the Python and ESP32 sides |
| Servo pins   | `main.cpp` | GPIO pins for the servo signal lines     |
| Angle limits | `main.cpp` | Min/max travel to protect your hardware  |
| Camera index | `track.py` | Change if you have multiple cameras      |

## License

Distributed under the MIT License. See `LICENSE` for details.
