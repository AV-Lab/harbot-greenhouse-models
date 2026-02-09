# HARBOT Agri Simulation

A collection of simulation environments, models, and assets for agricultural
robotics research within the **HARBOT** project.


This repository currently contains a greenhouse environment used for simulation
experiments in PyBullet and Gazebo.



## PyBullet
![PyBullet greenhouse preview](media/greenhouse_pybullet_preview.gif)

Install PyBullet:

```bash
pip install pybullet
````

Run the greenhouse simulation:

```bash
python pybullet/run_greenhouse.py
```


## Gazebo
![Gazebo greenhouse preview](media/greenhouse_gazebo_preview.gif)


A Gazebo world file is provided as an SDF.
The SDF references the greenhouse URDF and adds basic world elements such as
lighting.

The world file can be copied into an existing Gazebo project and used directly
as a simulation world.


## Project

This work is part of the **HARBOT** project and is intended for research and
experimentation in agricultural robotics.

