# Module 2, Task 2: Interactive Devices


## Task Description
The second task of this Interactive Devices module aims to take the experience from Task #1 and apply it to build a "performable" device (e.g. a digital instrument or game console). As in the previous task, the device must:
- Utilize exactly the three given sensors: a momentary button, a SPST switch, and an analog joystick
- Demonstrate three different modes of operation (i.e. states of the system that alter the effect an input action has on the output) directly via user input
- Have some digital output, audio or video (monitor, mini-screen, etc.)
However, instead of requiring use of the Raspberry Pi, the device:
- Must use the ESP32 (or any other Arduino-style microcontroller) and may additionally use the Raspberry Pi
With the additional constraints that it:
- Must have an enclosure or enclosures
- May use as many LEDs as desired


## Centipede X Ellsworth Kelly: An Artistic Reinterpretation of a Classic Arcade Game
Building off the basic motions established in Task #1 for Marco Polo, I wanted to create a more interactive game for Task #2. To do so, I turned to the most classic arcade games, which seemed approachable to make and would allow for the creation of attractive visual artifacts. In the end, I decided on the Atari and arcade classic Centipede due to the abundant opportunities for colorful and persistent items.

For artistic inspiration, I wanted to replicate the simple, primary colors of modern artists like Jackson Pollack and Ellsworth Kelly. In specific, I utilized the colors from Kelly's *Colors for a Large Wall* (1951) as the basis for the obstacles and sprites in my game.

![Ellsworth Kelly](assets/marco_polo.png)

## Usage Instructions

### Running and Setup
To set up this repository for local use, you need to
- Create a replica circuit connected to an ESP32 like the one described below
- Have an installation of Python3 with the *pygame* and *serial* libraries installed
- Download the code to your local computer (either using git clone or by downloading a *.zip* folder)
- Open a terminal and move to the project directory
- Run the code using *python3 centipede.py* with no argument for a Mac installation and *--pi* for a Raspberry Pi

### Gameplay
Like the original game, the objective of this version is to shoot all the segments of the centipede. Here, you play as the navy square and aim for the green circles, which move together until divided. The obstacles, which have the aforementioned colors, will block movement and shots, while redirecting the centipede segments.
- Press the button on the main menu to start gameplay
- Flip the Centipede "nose" switch to pause/unpause (up is paused, down is unpaused)
- Continue playing until you lose all 3 lives

![Gameplay](assets/gameplay.gif)

[Full length, high quality gameplay demonstration](assets/gameplay_screen_recording.mov)


## Implementation Details

### Enclosure
As a play on the concept and title of the game, I decided to make my enclosure resemble a cartoon centipede, using the image below in specific for inspiration.

For ease of construction, I utilized a foam board, cutting six sides to form a rectangular prism that could enclose the ESP32 and Pi together. However, to enable access to the internal circuitry, I made the lefthand side a "drawer" that could slide out, as shown in the picture below.



### Circuit Design
As required, this project uses a physical control circuit connected to a ESP32 for sensor data, including:
- A momentary button for shooting
- A SPST switch for pausing
- An analog joystick for player movement

All of these components were wired to GPIO pins of the ESP32 as well as the required power/ground values in order to function as desired. Namely, the circuit used the following connections (which are fairly evident from the code):
- Button: one pin to GND from the ESP32 and the other to GPIO 33
- Switch: one pin to GND from the Pi and the other to GPIO 32
- Joystick: VRX to GPIO 25, VRY to GPIO 26, +5V to 5V from the ESP32, GND to GND from the ESP32, and SW to GPIO 27

![Circuit](assets/circuit.JPG)

### Languages and Frameworks
This project uses a basic Python installation on a Raspberry Pi running Raspian. In addition, it uses the following libraries:
- *pygame* for all the game features and logic
- *serial* to communicate with the ESP32
- *threading* to implement the multi-threading needed to constantly take ESP32 input while updating the game
- *sys* for a command-line argument to run on either the Pi or a Mac (from the serial port)
- *os* for *path* to write the files to a folder
- *random* to randomize obstacle-spawning

### File Structure
- *README.md* describes all aspects of the project and game.
- *centipede.py* contains the final Marco Polo terminal game.
- *assets* contains the images and videos used in *README.md*.
- *old_stuff* contains previous attempts at various sub-parts of the game code, as well as for several other ideas outlined below.


## Approach Analysis

### Benefits
- The game is easily playable without additional hardware and accurately represents the original vision.

### Downsides
- While conveniently-packaged, the enclosure was certainly difficult to work with while designing and debugging.

## Abandoned Ideas
While most of the original ideas were achieved in this Task,

## Future Plans
In the future, I would like to further refine the enclosure design to be more sturdy and attractive.
