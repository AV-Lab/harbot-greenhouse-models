# HARBOT Greenhouse Models

A collection of greenhouse models and environment assets for agricultural robotics research within the HARBOT project.

This repository provides reusable greenhouse and crop models that can be used in **PyBullet**, **Gazebo Sim**, and **Gazebo Classic**.

## Gazebo Classic

![Gazebo Classic greenhouse preview](media/greenhouse_gazebo_classic_preview.gif)

Use this for Gazebo Classic (for example Gazebo 11).

From the repository root,set model paths:

```bash
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:$PWD/gazebo_classic/models
```

Launch the world:

```bash
gazebo gazebo_classic/greenhouse.world
```

If Gazebo hangs while loading models, disable online model fetching:

```bash
export GAZEBO_MODEL_DATABASE_URI=""
```

> **Note:**  
> To use the greenhouse environment in your own simulation workspace, copy the `gazebo_classic/` folder into your workspace. The models already include the required meshes and textures.

## Gazebo Sim

![Gazebo Sim greenhouse preview](media/greenhouse_gazebo_sim_preview.gif)

Use this for newer Gazebo releases (Ignition / Gazebo Sim, e.g. Fortress, Garden, Harmonic).

From the repository root, set the resource path:

```bash
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:$(pwd)
```

Launch the world:

```bash
gz sim gazebo_sim/greenhouse_world.sdf
```

> **Note:**  
> To use the greenhouse environment in your own simulation workspace, copy the `assets/` and `gazebo_sim/` folders into your workspace.

## PyBullet

![PyBullet greenhouse preview](media/greenhouse_pybullet_preview.gif)

Install PyBullet:

```bash
pip install pybullet
```

Run the greenhouse simulation:

```bash
python pybullet/load_greenhouse.py
```

> **Note:**  
> To use the greenhouse environment in your own workspace, copy the `assets/` folder and use the script provided in the `pybullet/` directory.
