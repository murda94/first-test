# Hand Sound Control

## Goal
The main purpose of this project is to create an interactive music instrument that can be controlled using hand geasture and color/object tracking.
Once choose the preferred rythm and melody, the musician could play the instrument using left hand as a pick and the right hand as a tool that can modify the note played.

## Environment

OS: MacOS Mojave

Platform: Python 3.6

## Requirements

* Install Super Collider: https://supercollider.github.io/download

* Install Anaconda: https://www.anaconda.com/distribution/#download-section

#### Open terminal

* Create a virtual environment: 

```
conda create -n myenv python=3.6
```

- Activate the new environment: 

```
conda activate myenv
```

- Install dependencies:

```
conda install numpy
conda install opencv
conda install pythonosc
```

## How to run it

### Super Collider

Open the script  ''ciao bello'' in Super Collider and follow the procedure below:

1. Compile first only `s.boot` line using `cmd + enter` in order to initialize the server
2. Compile separately (using `cmd + enter`) the following part:

   - Synth initalization
    - Communication initalization
     - Tempo clock initalization
      - Tempo function
      
### Python

1. Open terminal and activate virtual environment:

```
conda activate myenv
```

2. Open Jupyer Lab

```
jupyter-lab
```

3. Create new terminal window on Jupyter and run the 'ciao bello' script


## How to play instrument 

<img src="https://github.com/murda94/first-test/blob/master/images/Schermata%202019-07-26%20alle%2012.08.37.png" align="left" width="250">

<br /><br /><br /><br /><br /><br /><br /><br />

Place green pencil in box 4/4 or 6/8 in order to choose two different types of rythms

<img src="https://github.com/murda94/first-test/blob/master/images/Schermata%202019-07-25%20alle%2016.21.35.png" align="center" width="200">


Place blue pencil in box 4/4 or 6/8 in order to choose two different types of melodies

<img src="https://github.com/murda94/first-test/blob/master/images/Schermata%202019-07-25%20alle%2016.21.44.png" align="center" width="200">


Press `b` to capture the background model (remember to move your hand out of the rectangle before press `b`)

Move your hand in the rectangle and set the optimal threshold in order to isolate completely the hand from background

<img src="https://github.com/murda94/first-test/blob/master/images/Schermata%202019-07-25%20alle%2016.04.17.png" align="left" width="200">

<img src="https://github.com/murda94/first-test/blob/master/images/Schermata%202019-07-25%20alle%2016.04.32.png" align="left" width="200">

<img src="https://github.com/murda94/first-test/blob/master/images/Schermata%202019-07-25%20alle%2016.04.58.png" align="left" width="240">

<br /><br /><br /><br />
<img src="https://github.com/murda94/first-test/blob/master/images/Schermata%202019-07-25%20alle%2016.04.43.png" align="left" width="140"><br /><br />

<br /><br /><br /><br /><br /><br/>

#### Play instrument

1. Use middle finger as a guitar peak (each transition beetween one and two finger (and viceversa) correspond to an exciation)

<img src="https://github.com/murda94/first-test/blob/master/images/Schermata%202019-07-26%20alle%2010.34.30.png" align="left" width="200">
<img src="https://github.com/murda94/first-test/blob/master/images/Schermata%202019-07-26%20alle%2010.34.58.png" align="left" width="200">

<br /><br /><br /><br/><br /><br /><br /><br/><br /><br />

2. Place green pencil in the note boxs to play the associate notes

<img src="https://github.com/murda94/first-test/blob/master/images/Schermata%202019-07-26%20alle%2010.33.52.png" align="left" width="200">

<br /><br /><br /><br/><br /><br /><br /><br/>

#### Utilities

- Due to the sensibility of background subtraction algorithm, if there is any changes in background press `r` and `b` to reset and re-capture the backgroud model

- Press `ESC` to exit

- Press `q` to stop sound and restart


## Extension Javascript











      
      
      
      
 
















