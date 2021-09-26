// Set the speed of growth
float GROWTH = 1;

// Set the limit for the number of timelines
int LIMIT = 100000;

// Set the probability for branching (P = 1 / BRANCH for each call of draw())
int BRANCH = 300;

// Set the thickness of the sacred timeline
int THICKNESS = 8;

// Create a list of timelines to be drawn
ArrayList<Timeline> timelines;

// Parameters for drawing Miss Minutes
int cx;
int cy;
float secondsRadius;
float minutesRadius;
float hoursRadius;
float clockDiameter;

// Set to fullscreen and call the same reset function on setup
void setup() {
  //fullScreen(0);
  
  // Smaller screen option for debugging
  size(900, 768);
  
  reset();
}

// Function to reset the timeline growth
void reset() {
  // Set a dark blue background
  background(7, 25, 49);

  // Create Miss Minutes and calculate her position
  int radius = min((width / 3) / 2, height) / 3;
  cx = width - radius;
  cy = height / 2;
  secondsRadius = radius * 0.72;
  minutesRadius = radius * 0.60;
  hoursRadius = radius * 0.50;
  clockDiameter = radius * 1.8;
  
  // Initialize the timelines list and add the sacred timeline
  timelines = new ArrayList<Timeline>();
  timelines.add(new Timeline(width - clockDiameter, height / 2));
}

// Draw branching timelines randomly coming from Miss Minutes
void draw() {
  // Keep allowing for branching and updating the drawing until the limit is reached
  if (timelines.size() < LIMIT) {
    // Loop through all the timelines and randomly branch off them
    for (int i = 0; i < timelines.size(); i++) {
      Timeline t = timelines.get(i);
      int random = int(random(0, BRANCH));
      if (random == 82) {
        timelines.add(new Timeline(t.x, t.y, t.level + 1, int(random(1, 3))));
      }
      t.update();
    }
  }
  
  // If the sacred timeline has died/reached the edge, reset everything (optional)
  if (!timelines.get(0).isAlive()) {
    background(255, 0, 0);
    delay(1000);
    reset();
  }
  
  // Draw Miss Minutes
  drawClock();
}

// Class for a timeline (sacred or otherwise)
class Timeline {
  float x;
  float y;
  float thickness;
  float period;
  float amplitude;
  color lineColor;
  int red;
  int green;
  int blue;
  int initialRed;
  boolean sacred;
  int level;
  int branches;
  int shift;

  // Simple constructor for sacred timeline
  Timeline(float x, float y) {
    // Set the x and y to the input values
    this.x = x;
    this.y = y;
    
    // Set the thickness of the lines to the THICKNESS constant
    this.thickness = THICKNESS;
    
    // Set the period and amplitude randomly (smallish amplitude)
    this.period = 100 + random(-20, 20);
    this.amplitude = random(0.25, 1);
    
    // Set random RGB values within the desired range while storing the initial red value
    this.red = int(random(140, 210));
    this.green = int(random(140, 210));
    this.blue = int(random(160, 220));
    this.initialRed = this.red;
    this.lineColor = color(red, green, blue);
    
    // Indicate that it is a sacred timeline on level 0 with between 3 and 5 branches
    this.sacred = true;
    this.level = 0;
    this.branches = int(random(3, 6));
  }
  
  // More detailed and randomized constructor for branched timelines
  Timeline(float x, float y, int level, int branches) {
    // Set the x and y to the input values
    this.x = x;
    this.y = y;
    
    // Set the period and amplitude randomly (largish amplitude possible)
    this.period = 100 + random(-40, 40);
    this.amplitude = random(0.25, 2.75);
    
    // Set random RGB values within the desired range while storing the initial red value
    this.red = int(random(140, 210));
    this.green = int(random(140, 210));
    this.blue = int(random(160, 220));
    this.initialRed = this.red;
    this.lineColor = color(red, green, blue);
    
    // Indicate that it is not a sacred timeline
    this.sacred = false;
    
    // Set level and branches to the input values and calculate thickness based on level
    this.level = level;
    this.thickness = THICKNESS / pow(2, level);
    this.branches = branches;
  }

  // Function to update timeline with new coordinates
  void update() {
    // Only keep drawing if it is alive
    if (this.isAlive()) {
      // Draw a line of the designated color
      stroke(lineColor);
      strokeWeight(this.thickness);
      pushMatrix();
      translate(this.x, this.y);
      
      // Loop through the branches of the timeline and draw a new part of the line
      for (int i = 0; i < this.branches; i++) {
        // If it's the sacred timeline, set the stroke randomly within range
        if (sacred) {
          stroke(color(random(140, 210), random(140, 210), random(160, 220)));
        // Otherwise make it redder the closer you are to the edge
        } else {
          this.red = int(map(min(dist(0, this.y, 0, 0), dist(0, this.y, 0, height)), 0, height / 2, 255, initialRed));
          this.lineColor = color(this.red, this.green, this.blue);
        }
        
        // Draw a part of the line for the given branch
        line((20 / (level + 1)) * i, 0, (20 / (level + 1)) * i, GROWTH);
      }
      
      // Change the y by the corresponding sine function and the x by GROWTH
      y += amplitude * sin(x / period);
      x -= GROWTH;
      popMatrix();
    }
  }

  // Return true/alive if the x and y are within the boundaries
  boolean isAlive() {
    return this.y >= 0 && this.y <= height && x >= 0 && x <= width;
  }
}

// Function to draw Miss Minutes
void drawClock() {
  // Draw the clock background
  fill(204, 102, 0);
  noStroke();
  ellipse(cx, cy, clockDiameter, clockDiameter);
  
  // Angles for sin() and cos() start at 3 o'clock;
  // subtract PI to make them start at 9 o'clock
  float s = map(second(), 0, 60, 0, TWO_PI) - PI;
  float m = map(minute() + norm(second(), 0, 60), 0, 60, 0, TWO_PI) - PI; 
  float h = map(hour() + norm(minute(), 0, 60), 0, 24, 0, TWO_PI * 2) - PI;
  
  // Draw the hands of the clock
  stroke(255);
  strokeWeight(1);
  line(cx, cy, cx + cos(s) * secondsRadius, cy + sin(s) * secondsRadius);
  strokeWeight(2);
  line(cx, cy, cx + cos(m) * minutesRadius, cy + sin(m) * minutesRadius);
  strokeWeight(4);
  line(cx, cy, cx + cos(h) * hoursRadius, cy + sin(h) * hoursRadius);
  
  // Draw the eyes
  fill(255);
  stroke(0);
  ellipse(cx - (clockDiameter / 12), cy - (clockDiameter / 7), clockDiameter / 4, clockDiameter / 8);
  ellipse(cx - (clockDiameter / 12), cy + (clockDiameter / 7), clockDiameter / 4, clockDiameter / 8);
  
  // Draw the pupils and nose
  fill(0);
  ellipse(cx - (clockDiameter / 12), cy - (clockDiameter / 7), clockDiameter / 12, clockDiameter / 24);
  ellipse(cx - (clockDiameter / 12), cy + (clockDiameter / 7), clockDiameter / 12, clockDiameter / 24);
  ellipse(cx, cy, clockDiameter / 50, clockDiameter / 50);
  
  // Draw the mouth
  fill(255);
  arc(cx + clockDiameter / 8, cy, clockDiameter / 8, clockDiameter / 4, -PI / 2, PI / 2);
  line(cx + clockDiameter / 8, cy - clockDiameter / 8, cx + clockDiameter / 8, cy + clockDiameter / 8);
  
  // Draw the minute notches
  stroke(0);
  strokeWeight(2);
  beginShape(POINTS);
  for (int a = 0; a < 360; a+=6) {
    float angle = radians(a);
    float x = cx + cos(angle) * secondsRadius;
    float y = cy + sin(angle) * secondsRadius;
    vertex(x, y);
  }
   endShape();
}

// Reset the growth when the mouse is clicked
void mouseClicked() {
  reset();
}
