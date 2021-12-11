FROM ros:melodic
RUN apt-get update && apt-get install -y ros-melodic-joy ros-melodic-teleop-twist-joy \
  ros-melodic-teleop-twist-keyboard ros-melodic-laser-proc \
  ros-melodic-rgbd-launch ros-melodic-depthimage-to-laserscan \
  ros-melodic-rosserial-arduino ros-melodic-rosserial-python \
  ros-melodic-rosserial-server ros-melodic-rosserial-client \
  ros-melodic-rosserial-msgs ros-melodic-amcl ros-melodic-map-server \
  ros-melodic-move-base ros-melodic-urdf ros-melodic-xacro \
  ros-melodic-compressed-image-transport ros-melodic-rqt* \
  ros-melodic-gmapping ros-melodic-navigation ros-melodic-interactive-markers

COPY ./httpserver.py /root/
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN source /opt/ros/melodic/setup.bash
ENV PYTHONPATH /opt/ros/melodic/lib/python2.7/dist-packages
ENTRYPOINT ["python2.7", "/root/httpserver.py"]