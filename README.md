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

- press `b` to capture the background model (Remember to move your hand out of the rectangle before press `b`)
*
*
*
* press `r` and `b` to reset and re-capture the backgroud model
* press `ESC` to exit









      
      
      
      
 
















