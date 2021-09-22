// Set the speed of growth
float GROWTH = 1;

// Set the limit for the number of timelines
int LIMIT = 100000;

// Sacred timeline and list of other timelines
Timeline sacred;
ArrayList<Timeline> timelines;

// Miss Minutes and her parameters
Clock clock;
int cx;
int cy;
float secondsRadius;
float minutesRadius;
float hoursRadius;
float clockDiameter;

// Set to fullscreen and call the same reset function on setup
void setup() {
  fullScreen(0);
  //size(900, 768);
  reset();
}

// Function to reset the timeline growth
void reset() {
  // Set a dark blue background
  background(7, 25, 49);
  background(0);

  // Create Miss Minutes and calculate her position
  int radius = min((width / 3) / 2, height) / 3;
  cx = width - radius;
  cy = height / 2;
  secondsRadius = radius * 0.72;
  minutesRadius = radius * 0.60;
  hoursRadius = radius * 0.50;
  clockDiameter = radius * 1.8;
  
  //clock = new Clock(width, height / 2, radius * 0.72, radius * 0.60, radius * 0.50, radius * 1.80);

  // Initialize the sacred timeline and the other timelines list
  //sacred = new Timeline(width - clockDiameter, height / 2);
  timelines = new ArrayList<Timeline>();
  timelines.add(new Timeline(width - clockDiameter, height / 2));
}

// Draw branching timelines randomly coming from Miss Minutes
void draw() {
  //sacred.update();
  if (timelines.size() < LIMIT) {
    for (int i = 0; i < timelines.size(); i++) {
      Timeline t = timelines.get(i);
      int random = int(random(0, 300));
      if (random == 82) {
        timelines.add(new Timeline(t.x, t.y, PI / 2, t.level + 1, int(random(1, 3))));
      }
      t.update();
    }
  }
  if (!timelines.get(0).isAlive()) {
    reset();
  }
  drawClock();
}

class Timeline {
  float x;
  float y;
  float thickness;
  float period;
  float amplitude;
  float angle;
  color lineColor;
  int red;
  int green;
  int blue;
  int initialRed;
  boolean sacred;
  int level;
  int branches;

  // Simple constructor for sacred timeline
  Timeline(float x, float y) {
    this.x = x;
    this.y = y;
    this.thickness = 8;
    this.period = 100 + random(-20, 20);
    this.amplitude = random(0.25, 1);
    this.angle = 0;
    this.red = int(random(140, 210));
    this.green = int(random(140, 210));
    this.blue = int(random(160, 220));
    this.initialRed = this.red;
    this.lineColor = color(red, green, blue);
    this.sacred = true;
    this.level = 0;
    this.branches = int(random(3, 6));
    println(period, amplitude, branches);
  }
  
  // More detailed and randomized constructor for branched timelines
  Timeline(float x, float y, float angle, int level, int branches) {
    this.x = x;
    this.y = y;
    this.angle = angle;
    this.period = 100 + random(-40, 40);
    this.amplitude = random(0.25, 2.75);
    this.red = int(random(140, 210));
    this.green = int(random(140, 210));
    this.blue = int(random(160, 220));
    this.initialRed = this.red;
    this.lineColor = color(red, green, blue);
    this.sacred = false;
    this.level = level;
    this.thickness = 8 / pow(2, level);
    this.branches = branches;
  }

  void update() {
    if (this.isAlive()) {
      stroke(lineColor);
      strokeWeight(this.thickness);
      pushMatrix();
      translate(this.x, this.y);
      rotate(this.angle);
      for (int i = 0; i < this.branches; i++) {
        if (sacred) {
          stroke(color(random(140, 210), random(140, 210), random(160, 220)));
        } else {
          //this.red += 1;
          //this.green -= 1;
          //this.blue -= 1;
          this.red = int(map(min(dist(0, this.y, 0, 0), dist(0, this.y, 0, height)), 0, height / 2, 255, initialRed));
          this.lineColor = color(this.red, this.green, this.blue);
        }
        line((20 / (level + 1)) * i, 0, (20 / (level + 1)) * i, GROWTH);
      }
      y += amplitude * sin(x / period);
      x -= GROWTH;
      popMatrix();
    }
  }

  boolean isAlive() {
    return this.y >= 0 && this.y <= height && x >= 0 && x <= width;
  }
}

class Clock {
  float x;
  float y;
  float secondsRadius;
  float minutesRadius;
  float hoursRadius;
  float diameter;

  // Simple constructor for sacred timeline
  Clock(float x, float y, float secondsRadius, float minutesRadius, float hoursRadius, float diameter) {
    this.x = x;
    this.y = y;
    this.secondsRadius = secondsRadius;
    this.minutesRadius = minutesRadius;
    this.hoursRadius = hoursRadius;
  }

  void drawClock() {
    // Draw the clock background
    fill(204, 102, 0);
    noStroke();
    ellipse(this.x, this.y, this.diameter, this.diameter);
    
    // Angles for sin() and cos() start at 3 o'clock;
    // subtract PI to make them start at 9 o'clock
    float s = map(second(), 0, 60, 0, TWO_PI) - PI;
    float m = map(minute() + norm(second(), 0, 60), 0, 60, 0, TWO_PI) - PI; 
    float h = map(hour() + norm(minute(), 0, 60), 0, 24, 0, TWO_PI * 2) - PI;
    
    // Draw the hands of the clock
    stroke(255);
    strokeWeight(1);
    line(this.x, this.y, this.x + cos(s) * secondsRadius, this.y + sin(s) * secondsRadius);
    strokeWeight(2);
    line(this.x, this.y, this.x + cos(m) * minutesRadius, this.y + sin(m) * minutesRadius);
    strokeWeight(4);
    line(this.x, this.y, this.x + cos(h) * hoursRadius, this.y + sin(h) * hoursRadius);
    
    // Draw the eyes
    fill(255);
    stroke(0);
    ellipse(this.x - (this.diameter / 12), this.y - (this.diameter / 7), this.diameter / 4, this.diameter / 8);
    ellipse(this.x - (this.diameter / 12), this.y + (this.diameter / 7), this.diameter / 4, this.diameter / 8);
    
    // Draw the pupils and nose
    fill(0);
    ellipse(this.x - (this.diameter / 12), this.y - (this.diameter / 7), this.diameter / 12, this.diameter / 24);
    ellipse(this.x - (this.diameter / 12), this.y + (this.diameter / 7), this.diameter / 12, this.diameter / 24);
    ellipse(this.x, this.y, this.diameter / 50, this.diameter / 50);
    
    // Draw the mouth
    fill(255);
    arc(this.x + this.diameter / 8, this.y, this.diameter / 8, this.diameter / 4, -PI / 2, PI / 2);
    line(this.x + this.diameter / 8, this.y - this.diameter / 8, this.x + this.diameter / 8, this.y + this.diameter / 8);
    
    // Draw the minute notches
    stroke(0);
    strokeWeight(2);
    beginShape(POINTS);
    for (int a = 0; a < 360; a+=6) {
      float angle = radians(a);
      float x = this.x + cos(angle) * secondsRadius;
      float y = this.y + sin(angle) * secondsRadius;
      vertex(x, y);
    }
    
    // End drawing
    endShape();
  }
}

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
