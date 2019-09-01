from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink

import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D
ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')

left_arm_chain = Chain(name='left_arm', links=[
    OriginLink(),
    URDFLink(
      name="shoulder",
      translation_vector=[-10, 0, 5],
      orientation=[0, 1.57, 0],
      rotation=[0, 1, 0],
    ),
    URDFLink(
      name="elbow",
      translation_vector=[25, 0, 0],
      orientation=[0, 0, 0],
      rotation=[0, 1, 0],
    ),
    URDFLink(
      name="wrist",
      translation_vector=[22, 0, 0],
      orientation=[0, 0, 0],
      rotation=[0, 1, 0],
    )
])


left_arm_chain.plot(left_arm_chain.joints, ax)


# left_arm_chain.plot(left_arm_chain.inverse_kinematics([
#     [1, 0, 0, 2],
#     [0, 1, 0, 2],
#     [0, 0, 1, 2],
#     [0, 0, 0, 1]
#     ]), ax)

matplotlib.pyplot.show()
