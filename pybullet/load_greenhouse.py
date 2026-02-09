#!/usr/bin/env python3

import pybullet as p
import pybullet_data
import time
import os

class GreenhouseEnvironment:
    def __init__(self):
        """Initialize PyBullet environment"""
        self.physics_client = p.connect(p.GUI)
        
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
        self.urdf_path="./assets/greenhouse/urdf/"
        
                
    def load_greenhouse_structure(self):
        """Load the greenhouse floor, grass, and top structure"""
        try:
            greenhouse_id = p.loadURDF(
                os.path.join(self.urdf_path, "greenhouse.urdf"),
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
            
    
    def load_oranges(self):
        """Load orange models in a grid pattern inside the greenhouse"""
        left_urdf  = os.path.join(self.urdf_path, "orange_left.urdf")
        right_urdf = os.path.join(self.urdf_path, "orange_right.urdf")

        self.model_ids.setdefault("oranges", {})

        x_start = 0.0
        y_start = 0.0
        dx = 4.0
        dy = 3.6111

        num_rows = 4
        num_cols = 8

        for r in range(num_rows):
            x = x_start + r * dx

            for c in range(num_cols):
                y = y_start + c * dy
                pos = [x, y, 0.0]

                name_L = f"orange{r+1}.{c+1}.L"
                name_R = f"orange{r+1}.{c+1}.R"

                try:
                    oid_L = p.loadURDF(
                        left_urdf,
                        pos,
                        useFixedBase=True
                    )
                    
                    p.changeVisualShape(oid_L, -1, rgbaColor=[1.0, 1.0, 1.0, 1.0])

                    self.model_ids["oranges"][name_L] = oid_L
                except Exception as e:
                    print(f"Warning: could not load {name_L}: {e}")

                try:
                    oid_R = p.loadURDF(
                        right_urdf,
                        pos,
                        useFixedBase=True
                    )
                    
                    p.changeVisualShape(oid_R, -1, rgbaColor=[1.0, 1.0, 1.0, 1.0])
                    
                    self.model_ids["oranges"][name_R] = oid_R
                except Exception as e:
                    print(f"Warning: could not load {name_R}: {e}")

        print(f"Loaded {len(self.model_ids['oranges'])} oranges")
        
        
    def disconnect(self):
        """Disconnect from PyBullet"""
        p.disconnect()
        

def main():
    """Main function"""
    env = GreenhouseEnvironment()
    
    print("Loading greenhouse structure...")
    env.load_greenhouse_structure()
    
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
    
    