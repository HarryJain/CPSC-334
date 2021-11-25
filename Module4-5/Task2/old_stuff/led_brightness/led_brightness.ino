// The pin connections for the LEDs
#define RED 26
#define YELLOW 25
#define GREEN 33
#define BLUE 32

// The PWM channel (0 to 15)
#define CHANNEL 0

// The PWM signal frequency for LED
#define FREQ 5000

// The signal's duty cycle resolution (1 to 16-bit)
//  8-bit for 0 to 255 LED brightness values
#define RESOLUTION 8
#define MIN 0
#define MAX 255

void setup() {
  // Configure LED PWM functionalities
  ledcSetup(CHANNEL, FREQ, RESOLUTION);

  // Attach the channel to the GPIO pins to be controlled
  ledcAttachPin(RED, CHANNEL);
  ledcAttachPin(YELLOW, CHANNEL);
  ledcAttachPin(GREEN, CHANNEL);
  ledcAttachPin(BLUE, CHANNEL);
}

void loop() {
  // Increase the LED brightness to the max
  for (int duty = MIN; duty <= MAX; duty++) {
    ledcWrite(CHANNEL, duty);
    delay(10);
  }

  // Decrease the LED brightness to the min
  for (int duty = MAX; duty >= MIN; duty--) {
    ledcWrite(CHANNEL, duty);
    delay(10);
  }
}
