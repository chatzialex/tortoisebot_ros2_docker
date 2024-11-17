# tortoisebot_ros1_docker

### Simulation

To launch:
```
# cd to the repo root dir
docker-compose -f docker-compose-sim.yml up
```

### Real robot

To launch:
```
ssh -X tortoisebot@<ROBOT_IP>
# cd to the repo root dir
docker-compose -f docker-compose-real.yml up
```

If the `ssh` session is setup to forward the `X` server, this will also spawn `rviz` (though a rather laggy instance). Without `X` server forwarding, the spawning of `rviz` will silently fail. The docker is, however, connected to the host network, so `rviz` should be able to connect to it from the host computer.
