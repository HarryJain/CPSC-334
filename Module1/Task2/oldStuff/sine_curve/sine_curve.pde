float x = 0;
float y = 0;
float GROWTH = 1;
int LIMIT = 100000;
Timeline timeline;
Timeline timeline2;
ArrayList<Timeline> timelines = new ArrayList<Timeline>();

void setup() {
  size(800, 800);
  smooth();
  background(7, 25, 49);
  stroke(211, 216, 223);
  timelines.add(new Timeline(width / 2, height));
}

void reset() {
  background(7, 25, 49);
  timelines = new ArrayList<Timeline>();
  timelines.add(new Timeline(width / 2, height));
}

void draw() {
  if (timelines.size() < 100000) {
    for (int i = 0; i < timelines.size(); i++) {
      Timeline t = timelines.get(i);
      int random = int(random(0, 500));
      if (random == 82) {
        timelines.add(new Timeline(t.x, t.y));
      }
      t.update();
    }
  }
}

//void setup() {
//  size(800, 800);
//  smooth();
//  background(7, 25, 49);
//  stroke(211, 216, 223);
//  timeline = new Timeline(width / 2, height);
//  timeline2 = new Timeline(width / 2, height, timeline.period, timeline.amplitude);
//}

//void reset() {
//  background(7, 25, 49);
//  timeline = new Timeline(width /m 2, height);
//  timeline2 = new Timeline(width / 2, height, timeline.period, timeline.amplitude);
//}

//void draw() {
//  timeline.update();
//  if (timeline.y < height / 2) {
//    timeline2.update();
//  }
//}

class Timeline {
  float x;
  float y;
  float thickness;
  float period;
  float amplitude;
  float angle;
  color lineColor;

  Timeline(float x, float y) {
    this.x = x;
    this.y = y;
    this.thickness = 10;
    this.angle = -HALF_PI;
    //this.thickness = map(dist(0, this.y, 0, 0), 0, height, 0, 5);
    this.period = 100 + random(-20, 20);
    this.amplitude = random(0.25, 1.75);
    this.lineColor = color(random(140, 210), random(140, 210), random(160, 220));
  }
  
  Timeline(float x, float y, float angle) {
    this.x = x;
    this.y = y;
    this.thickness = 10;
    this.angle = angle;
    //this.thickness = map(dist(0, this.y, 0, 0), 0, height, 0, 5);
    this.period = 100 + random(-40, 40);
    this.amplitude = random(0.25, 1.75);
    this.lineColor = color(random(140, 210), random(140, 210), random(160, 220));
  }
  
  Timeline(float x, float y, float period, float amplitude) {
    this.x = x;
    this.y = y;
    this.thickness = 10;
    //this.thickness = map(dist(0, this.y, 0, 0), 0, height, 0, 5);
    this.period = period;
    this.amplitude = amplitude;
  }

  void update() {
    //this.thickness = map(dist(0, this.y, 0, 0), 0, height, 0, 5);
    if (this.isAlive()) {
      stroke(lineColor);
      strokeWeight(this.thickness);
      pushMatrix();
      translate(this.x, this.y);
      rotate(this.angle);
      stroke(color(random(140, 210), random(140, 210), random(160, 220)));
      line(0, 0, GROWTH, 0);
      stroke(color(random(140, 210), random(140, 210), random(160, 220)));
      line(0, 20, GROWTH, 20);
      stroke(color(random(140, 210), random(140, 210), random(160, 220)));
      line(0, 40, GROWTH, 40);
      stroke(color(random(140, 210), random(140, 210), random(160, 220)));
      line(0, 60, GROWTH, 60);
      x += amplitude * sin(y / period);
      y -= GROWTH;
      //float newx = x + amplitude * sin(y / period);
      //float newy = y - GROWTH;
      //x = newx * cos(this.angle) - newy * sin(this.angle);
      //y = newx * sin(this.angle) + newy * cos(this.angle);
      popMatrix();
    }
  }

  boolean isAlive() {
    return this.y > 0;
  }
}

void mouseClicked() {
  reset();
}
