/**
 * Clock. 
 * 
 * The current time can be read with the second(), minute(), 
 * and hour() functions. In this example, sin() and cos() values
 * are used to set the position of the hands.
 */

int[] cxa;
int cy;
float secondsRadius;
float minutesRadius;
float hoursRadius;
float clockDiameter;

void setup() {
  fullScreen(0);
  
  stroke(255);
  
  int radius = min((width / 3) / 2, height) / 2;
  secondsRadius = radius * 0.72;
  minutesRadius = radius * 0.60;
  hoursRadius = radius * 0.50;
  clockDiameter = radius * 1.8;
  
  cxa = new int[]{(width / 3) / 2 + width / 12, 3 * (width / 3) / 2 + width / 12, 5 * (width / 3) / 2 + width / 12};
  cy = height / 2;
}

void drawClock(int num) {
  // Draw the clock background
  fill(204, 102, 0);
  noStroke();
  ellipse(cxa[num], cy, clockDiameter, clockDiameter);
  
  // Angles for sin() and cos() start at 3 o'clock;
  // subtract HALF_PI to make them start at the top
  float s = map(second(), 0, 60, 0, TWO_PI) - PI;
  float m = map(minute() + norm(second(), 0, 60), 0, 60, 0, TWO_PI) - PI; 
  float h = map(hour() + norm(minute(), 0, 60), 0, 24, 0, TWO_PI * 2) - PI;
  
  // Draw the hands of the clock
  stroke(255);
  strokeWeight(1);
  line(cxa[num], cy, cxa[num] + cos(s) * secondsRadius, cy + sin(s) * secondsRadius);
  strokeWeight(2);
  line(cxa[num], cy, cxa[num] + cos(m) * minutesRadius, cy + sin(m) * minutesRadius);
  strokeWeight(4);
  line(cxa[num], cy, cxa[num] + cos(h) * hoursRadius, cy + sin(h) * hoursRadius);
  
  // Draw the eyes
  fill(255);
  stroke(0);
  ellipse(cxa[num] - (clockDiameter / 12), cy - (clockDiameter / 7), clockDiameter / 4, clockDiameter / 8);
  ellipse(cxa[num] - (clockDiameter / 12), cy + (clockDiameter / 7), clockDiameter / 4, clockDiameter / 8);
  
  // Draw the pupils and nose
  fill(0);
  ellipse(cxa[num] - (clockDiameter / 12), cy - (clockDiameter / 7), clockDiameter / 12, clockDiameter / 24);
  ellipse(cxa[num] - (clockDiameter / 12), cy + (clockDiameter / 7), clockDiameter / 12, clockDiameter / 24);
  ellipse(cxa[num], cy, clockDiameter / 50, clockDiameter / 50);
  
  // Draw the mouth
  fill(255);
  arc(cxa[num] + clockDiameter / 8, cy, clockDiameter / 8, clockDiameter / 4, -PI / 2, PI / 2);
  line(cxa[num] + clockDiameter / 8, cy - clockDiameter / 8, cxa[num] + clockDiameter / 8, cy + clockDiameter / 8);
  //arc(cx, cy + 20, 80, 50, 0, 3.14);
  //line(cx - 40, cy + 20, cx + 40, cy + 20);
  
  // Draw the minute notches
  stroke(0);
  strokeWeight(2);
  beginShape(POINTS);
  for (int a = 0; a < 360; a+=6) {
    float angle = radians(a);
    float x = cxa[num] + cos(angle) * secondsRadius;
    float y = cy + sin(angle) * secondsRadius;
    vertex(x, y);
  }
  //rotate(PI / 3.0);
  endShape();
}

void draw() {
  background(0);
  
  for (int i = 0; i < 3; i++) {
    drawClock(i);
  }
}
