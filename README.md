Mooshoo's EV3 Demo
==========
### Introducing 6 year olds to programming with the help of Lego EV3

This repository contains the (little) code used for an "Introduction to Software Programing" activity I created for my nephew's 6st birthday on his kindergarten. I was asked to create a short activity that relates to what I do for a living and figured nothing could be better to steal the show than a live demo of a cool looking robot.

The robot was a quick and dirty (no arms) version of [Lego Mindstorms EV3STORM](http://www.lego.com/en-us/mindstorms), running [topikachu's python-ev3](https://github.com/topikachu/python-ev3) a project that let you run python code on the EV3. based on a modefied version of the [lejos kernel](http://sourceforge.net/projects/lejos/).

![The robot](readme-resources/robot.jpg?raw=true)

The python code I run on the EV3 is a very simple HTTP server utilizing topikachu ev3 motor driver. On the client I created a little web page to allow the kids to run any one of an 8 predefined robot moves, or "record" a sequence of the move commands then send them to the robot.

![Web interface](readme-resources/web-interface.png?raw=true)

##### Great success!

![Astonished kids](readme-resources/kids.jpg?raw=true)