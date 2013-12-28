Mooshoo's EV3 Demo
==========
### Introducing 6 year olds to programming with the help of Lego EV3

This repository contains the (little) code used for an "Introduction to Software Programing" activity I created for my nephew's 6st birthday on his kindergarten. I was asked to create a short activity that relates to what I do for a living. I figured nothing could be better to steal the show than a live demo of a cool looking robot.

The robot was a quick and dirty (no arms) version of [Lego Mindstorms EV3STORM](http://www.lego.com/en-us/mindstorms). Running [topikachu's python-ev3](https://github.com/topikachu/python-ev3), a project that let you run python code on the EV3. [Python-ev3](https://github.com/topikachu/python-ev3) is based on a modefied version of the [leJOS kernel](http://sourceforge.net/projects/lejos/).

The python code I run on the EV3 is a very simple HTTP server, utilizing [topikachu's](https://github.com/topikachu) ev3 motor driver. On the client I created a little web page allowing the kids to run any one of 8 predefined robot moves. Or "record" a sequence of the move commands, then send them to the robot.
