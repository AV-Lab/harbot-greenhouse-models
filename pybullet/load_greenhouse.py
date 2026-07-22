#!/usr/bin/env python3

import pybullet as p
import pybullet_data
import time
import os
import math

class GreenhouseEnvironment:
    def __init__(self, connection_mode=p.GUI):
        """Initialize PyBullet environment"""
        if connection_mode == p.GUI:
            self.physics_client = p.connect(
                connection_mode,
                options="--width=1920 --height=1080",
            )
        else:
            self.physics_client = p.connect(connection_mode)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)
        p.loadURDF("plane.urdf", [0, 0, -0.1])
        
        p.resetDebugVisualizerCamera(
            cameraDistance=28.40,
            cameraYaw=28.40,
            cameraPitch=-12.20,
            cameraTargetPosition=[-3.37, 1.03, 2.86],
        )
        
        p.configureDebugVisualizer(p.COV_ENABLE_SHADOWS, 0)
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 1)
        
        self.model_ids = {}
        self.repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.greenhouse_urdf = os.path.join(
            self.repo_root, "assets", "greenhouse", "greenhouse.urdf"
        )
        self.green_floor_mesh = os.path.join(
            self.repo_root,
            "assets",
            "greenhouse",
            "meshes",
            "greenhouse_green.obj",
        )
        self.unloading_station_mesh = os.path.join(
            self.repo_root,
            "assets",
            "greenhouse",
            "meshes",
            "unloading_station.obj",
        )
        self.ripe_orange_mesh = os.path.join(
            self.repo_root,
            "assets",
            "oranges",
            "orange",
            "meshes",
            "orange.obj",
        )
        self.unripe_orange_mesh = os.path.join(
            self.repo_root,
            "assets",
            "oranges",
            "unripe_orange",
            "meshes",
            "unripe_orange.obj",
        )
        
                
    def load_greenhouse_structure(self):
        """Load the greenhouse floor, grass, and top structure"""
        try:
            greenhouse_id = p.loadURDF(
                self.greenhouse_urdf,
                [0, 0, 0],
                useFixedBase=True,
            )
            self.model_ids['greenhouse_id'] = greenhouse_id
            
            # Define colors for specific links
            link_colors = {
                'curve_top_link': [1.0, 1.0, 1.0, 0.4],
                'front_link': [1.0, 1.0, 1.0, 0.4],
                'back_link': [1.0, 1.0, 1.0, 0.4],
                'top_support_link': [0.0, 0.0, 0.0, 1.0],
                'door_link': [0.0, 0.0, 0.0, 1.0],
                'orange_stem': [0.0, 0.0, 0.0, 1.0],
                
            }
            default_color = [1.0, 1.0, 1.0, 1.0]
            
            # Apply white material to base link
            p.changeVisualShape(greenhouse_id, -1, rgbaColor=default_color)
            
            # Apply materials to all child links
            num_joints = p.getNumJoints(greenhouse_id)
            
            for link_idx in range(num_joints):
                joint_info = p.getJointInfo(greenhouse_id, link_idx)
                link_name = joint_info[12].decode('utf-8')
                
                color = link_colors.get(link_name, default_color)
                
                p.changeVisualShape(greenhouse_id, link_idx, rgbaColor=color)
            
            print(f"Loaded greenhouse structure with {num_joints + 1} links")
            
        except Exception as e:
            print(f"Warning: Could not load greenhouse structure: {e}")


    def load_green_floor(self):
        """Load the green floor mesh as a fixed visual and collision body."""
        try:
            mesh_orientation = p.getQuaternionFromEuler([math.pi / 2.0, 0, 0])
            visual_shape = p.createVisualShape(
                shapeType=p.GEOM_MESH,
                fileName=self.green_floor_mesh,
                meshScale=[1, 1, 1],
                visualFrameOrientation=mesh_orientation,
            )
            collision_shape = p.createCollisionShape(
                shapeType=p.GEOM_MESH,
                fileName=self.green_floor_mesh,
                meshScale=[1, 1, 1],
                collisionFrameOrientation=mesh_orientation,
            )
            floor_id = p.createMultiBody(
                baseMass=0,
                baseCollisionShapeIndex=collision_shape,
                baseVisualShapeIndex=visual_shape,
                basePosition=[0, 0, 0],
            )
            self.model_ids["green_floor_id"] = floor_id
            print("Loaded green floor")
        except Exception as e:
            print(f"Warning: Could not load green floor: {e}")


    def load_unloading_stations(self):
        """Load the two fixed unloading stations from greenhouse.world."""
        self.model_ids.setdefault("unloading_stations", {})

        try:
            mesh_orientation = p.getQuaternionFromEuler([math.pi / 2.0, 0, 0])
            visual_shape = p.createVisualShape(
                shapeType=p.GEOM_MESH,
                fileName=self.unloading_station_mesh,
                meshScale=[1, 1, 1],
                visualFrameOrientation=mesh_orientation,
            )
            collision_shape = p.createCollisionShape(
                shapeType=p.GEOM_MESH,
                fileName=self.unloading_station_mesh,
                meshScale=[1, 1, 1],
                collisionFrameOrientation=mesh_orientation,
            )

            station_poses = {
                "unloading_station_b": [7.5, 14.4, 0.11],
                "unloading_station_a": [-7.5, -14.4, 0.11],
            }

            for name, position in station_poses.items():
                station_id = p.createMultiBody(
                    baseMass=0,
                    baseCollisionShapeIndex=collision_shape,
                    baseVisualShapeIndex=visual_shape,
                    basePosition=position,
                )
                p.changeDynamics(station_id, -1, lateralFriction=2.0)
                self.model_ids["unloading_stations"][name] = station_id

            print("Loaded 2 unloading stations")
        except Exception as e:
            print(f"Warning: Could not load unloading stations: {e}")


    def load_oranges(self):
        """Load the updated ripe and unripe orange layout without supports."""
        self.model_ids.setdefault("oranges", {})

        # orange1.1.L.T is the starting pose from greenhouse.world. The other
        # three fruit positions on each plant are fixed offsets from it.
        start_pose = (-7.01416, -11.8646, 1.44646)
        plant_offsets = {
            "L.T": (0.0, 0.0, 0.0),
            "L.B": (0.06761, -0.5358, -0.40465),
            "R.T": (2.00535, -0.5625, 0.0),
            "R.B": (1.93775, -0.0248, -0.40465),
        }
        row_spacing = 4.0
        column_spacing = 3.440571

        unripe_names = {
            "orange1.2.L.T",
            "orange1.7.L.B",
            "orange1.4.R.B",
            "orange2.1.L.T",
            "orange2.7.L.T",
            "orange2.5.R.T",
            "orange3.4.L.B",
            "orange3.1.R.T",
            "orange3.7.R.B",
            "orange4.4.L.T",
            "orange4.2.R.T",
            "orange4.8.R.B",
        }

        mesh_orientation = p.getQuaternionFromEuler([math.pi / 2.0, 0, 0])
        ripe_visual = p.createVisualShape(
            shapeType=p.GEOM_MESH,
            fileName=self.ripe_orange_mesh,
            meshScale=[1, 1, 1],
            visualFrameOrientation=mesh_orientation,
        )
        unripe_visual = p.createVisualShape(
            shapeType=p.GEOM_MESH,
            fileName=self.unripe_orange_mesh,
            meshScale=[1, 1, 1],
            visualFrameOrientation=mesh_orientation,
        )

        for row in range(1, 5):
            for column in range(1, 9):
                for location, offset in plant_offsets.items():
                    name = f"orange{row}.{column}.{location}"
                    position = [
                        start_pose[0] + offset[0] + (row - 1) * row_spacing,
                        start_pose[1]
                        + offset[1]
                        + (column - 1) * column_spacing,
                        start_pose[2] + offset[2],
                    ]
                    visual_shape = (
                        unripe_visual if name in unripe_names else ripe_visual
                    )

                    try:
                        # A zero-mass body with no collision shape is unaffected
                        # by gravity and cannot generate contacts.
                        orange_id = p.createMultiBody(
                            baseMass=0,
                            baseCollisionShapeIndex=-1,
                            baseVisualShapeIndex=visual_shape,
                            basePosition=position,
                        )
                        self.model_ids["oranges"][name] = orange_id
                    except Exception as e:
                        print(f"Warning: could not load {name}: {e}")

        print(f"Loaded {len(self.model_ids['oranges'])} oranges")
        
        
    def disconnect(self):
        """Disconnect from PyBullet"""
        p.disconnect()
        

def main():
    """Main function"""
    env = GreenhouseEnvironment()
    
    print("Loading greenhouse structure...")
    env.load_greenhouse_structure()

    print("Loading green floor...")
    env.load_green_floor()

    print("Loading unloading stations...")
    env.load_unloading_stations()
    
    print("Loading oranges...")
    env.load_oranges()
    
    print(f"\nEnvironment loaded successfully!")
    print("\nPress Ctrl+C to quit")
    
    try:
        while True:
            p.stepSimulation()
            time.sleep(1./240.)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        env.disconnect()


if __name__ == "__main__":
    main()
