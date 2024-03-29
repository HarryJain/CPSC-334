# Module 1, Task 2: Generative Art

## Task Description

![Leeds Setup](./images/leads-projectors.jpg)

- Use the physical layout discovered in Task 1 to greate a generative art installation for the CCAM Leeds Studio Projector array.
- Embrace the challenges of the physical space and setup to "specialize" the installation for this particular multi-projector canvas.

## *Again and Again and Again*: An Homage to Marvel Studios's *Loki*
Even as a die-hard fan of Marvel, I was especially surprised and impressed at the visual storytelling in their series *Loki*, in which the titular character finds himself thrown into the world of multiverses, timelines, and more. In particular, I was struck by the images of the "Sacred Timeline" branching out of control in the final episode, as shown in the image below.

![Loki Branching Timelines](./images/branchingTimelines.jpg)

Taking this imagery as inspiration, *Again and Again and Again* (a title inspired by the words of Time Variance Authority agent Mobius), aims to create a generative art installation of branching timelines. To establish this connection to the show, it incorporates important aspects of plot, such as the "Sacred Timeline" running down the center of the displays, "Miss Minutes" serving as the source of the timelines, a red color shift near the borders of the displays, and the Time Variance Authority theme in the background. Additionally, the constant "rebirth" of the installation represents the circular nature of time in *Loki*, while also demonstrating the destructive power of the uncontrollable branching in the finale.

![Again and Again and Again](./images/IMG_3208.JPG)

[Link to YouTube video demonstration](https://youtu.be/lurt8L2SHBo)

**Note:** the video was taken before adjusting for the disordered screens - see [this video](https://drive.google.com/file/d/1A6kfnWYGWetvha9P2aVcn8j6SxgXjgjS/view?usp=sharing) for the new functionality filmed less elegantly).

## Implementation Details

### Languages
This project uses the graphics software Processing, with the code written in the default Java installation. Everything used is from the base installation, except for the Sound libarary, which plays the optional soundtrack alonside the visual art.

### File Structure
- *README.md* describes all aspects, creative and technical, of the art installation.
- *againAndAgainAndAgain* contains the main Processing program as well as the *.wav* music file.
  - *againAndAgainAndAgain.pde* is the code file for running the installation (open in Processing to run).
  - *tva.wav* is the audio file containing a copy of Natalie Holt's "TVA" from the official *Loki* soundtrack (taken from this [YouTube video](https://youtu.be/SRWSfXdlNPc)).
- *oldStuff* contains previous and partial attempts at this installation (defunct).

## Usage Instructions
As outlined in the task description, this project is customized to the physical space of the CCAM Leeds Studio Projector array, so running it on other computers requires some modifications. To run it in the studio, utilize the following instructions:
- Turn on the MSI Omen computer and the 6 projectors.
- Download the code to your local computer (either using *git clone* or by downloading a *.zip* folder).
- Open *againAndAgainAndAgain/againAndAgainAndAgain.pde* in Processing.
- Press the *Run* button and let the program run on the projectors.
- Click the mouse on the Canvas at any time to restart.

To run the installation on other systems, consider modifying the following variables and functions:
- Install the Sound library by going to *Sketch* -> *Import Library...* -> *Add Library...*, searching for *Sound* from *The Processing Foundation*, and pressing the *Install* button.
- Remove lines 3 and 4, along with lines 47 and 48, to avoid using sound or having to download the sound library.
- Decrease the BRANCH variable to increase branching speed/frequency and increase it to decrease branching.
- Remove lines 76 to 92 if the screens are ordered properly, as these lines shift the coordinates of the timelines to account for the misordered projectors in the Leeds Studio.
- Set MAINSCREEN to 0 if your window spans only on the displays you desire and not an additional "main display" or alternately change its value to match the width of your "main display" you want to skip.
- Change other variables like THICKNESS and DELAY to mix up the parameters if desired (see code comments for all parameters and explanations of their function).

## Future Improvements
While the installation meets many of the initial goals, there are still some improvements that could be made to function better and more accurately represent the original artistic vision, some of which are outlined below.
- Rather than exclusively vary the amplitude and period of the sine curves, modify their initial angle relative to the "Sacred Timeline" as well. This idea was sidelined due to the mathematical complexity in the given time, but it should be achievable and would result in more varied and show-accurate branching. Namely, all branches would no longer move together along the same y-value as they do now.
- The installation could be tuned even further to the space by moving horizontally across screens rather than vertically one at a time, along with possibilities like branching specifically between screens, though this would lessen the amount of pixels available for branching.
- To further tie into the show, certain timelines could be "pruned" or collide with each other, causing the visuals to change to represent a "Nexus Event" or apocalypse. Another possibility would be apocalypse events and some representation of Sylvie and Loki's travels. Finally, some sort of "Big Bang" could visually represent the restart rather than just the disappearance of the previous timelines. These interactions would lead to even more randomized and visually complex results, as well as better represent the relationship to the series *Loki*.

## References
As this was my first time working in Processing, I used the official [Processing documentation](https://processing.org) extensively, along with the following open-source examples:
- [Growing Tree](https://openprocessing.org/sketch/155415/) by Martin Hartl was used as inspiration for the branching process and the basis of the Timeline class.
- The official Processing [clock example](https://processing.org/examples/clock.html) was used in combination with this Happy Coding [smiley face](https://happycoding.io/examples/processing/calling-functions/smiley-face) to create Miss Minutes.
