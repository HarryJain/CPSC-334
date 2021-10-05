// constants won't change. They're used here to set pin numbers:
const int buttonPin = 34;     // the number of the pushbutton pin

// variables will change:
int buttonState = 0;         // variable for reading the pushbutton status

int printState = 0;

void setup() {
  Serial.begin(115200);
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT);
  Serial.println("Setting up...");
}

void loop() {
  // read the state of the pushbutton value:
  buttonState = digitalRead(buttonPin);

  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  if (buttonState == HIGH) {
    if (printState == 0 || printState == -1) {
      Serial.println("I'm soooo high");
    }
    printState = 1;
  } else {
    if (printState == 0 || printState == 1) {
      Serial.println("I'm feeling down");
    }
    printState = -1;
  }
}
