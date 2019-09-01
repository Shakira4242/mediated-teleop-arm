import pybullet
import time
import pybullet_data

pybullet.connect(pybullet.GUI)#or p.DIRECT for non-graphical version
pybullet.resetSimulation()

pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())
plane = pybullet.loadURDF("plane.urdf")
robot = pybullet.loadURDF("urdf/starwars.urdf", [0.0,0.0,0.0], useFixedBase=1)
position, orientation = pybullet.getBasePositionAndOrientation(robot)

print(pybullet.getNumJoints(robot))
# joint_positions = [j[0] for j in pybullet.getJointStates(robot, range(3))]

# limits for joints
joint_index = 0
print(pybullet.getJointInfo(robot, joint_index))


joint_index = 1
print(pybullet.getJointInfo(robot, joint_index))


joint_index = 2
print(pybullet.getJointInfo(robot, joint_index))


# animate

pybullet.setGravity(0, 0, -9.81)   # everything should fall down
pybullet.setTimeStep(0.0001)       # this slows everything down, but let's be accurate...
pybullet.setRealTimeSimulation(0)  # we want to be faster than real time :)

pybullet.setJointMotorControlArray(
    robot, range(3), pybullet.POSITION_CONTROL,
    targetPositions=[0.1,0.1,0.1])

for _ in range(10000):
    pybullet.stepSimulation()
    time.sleep(0.01)

pybullet.disconnect()