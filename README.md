# Gameplay
Embiggen your shadow to a cromulent size! This game plays like a SHMUP (shoot'em up). Shadow barriers will hurt your shadow if they come in contact so blast them away! You win when you embiggen to 100%. Collect power ups to embiggen and if your shadow is hit by too many barriers, you lose!


[Screenshots](/screenshots)
=
![Alt text](/screenshots/v0-5-0_1.png?raw=true "Gameplay")


Changelog
=
v0.6.0 (04-01-23)
-
-Power ups now only travel to the center of the screen and will fade away if not collected in time.

-Energy blasts now despawn when hitting a barrier

-Fixed a bug where game activity would happen behind the title screen

-Changed shadow scaling behavior to make hit detection more accurate (is still not as perfect as hoped)

-Updated victory screen to show how many times you were hit and how long you took, in addition to the final score.

-Added Python version check (requires 3.7 or higher)

v0.5.0 (03-29-23)
-
-Re-added power ups which embiggen your shadow

-Removed time limit and time loss, now scoring is based on how long you take to embiggen to 100% and how many times your shadow gets hit.

-Changed background sprite. All sprites and sounds are probably final at this point

v0.4.0 (03-28-23)
-
-Scoring changed to hitting shadows barriers with your energy blasts makes your shadow bigger, shadow getting hit makes it smaller.

-Implemented a title screen

-Optimized some code in some places

-Updated readme/license

-Added some sound effects using stock Arcade sounds

-Gameplay has been changed up to be more SHMUP (shoot'em up) style so you know have free movement and now instead of collecting energy, you shoot energy! Your shadow embiggens organically so you need to blast the neutrinos that are chipping away at your shadow.

v0.3.0 (03-27-23)
-
-Added a crude player sprite and an even cruder background

-Gameplay has been changed up to be more SHMUP (shoot'em up) style so you know have free movement and now instead of collecting energy, you shoot energy! Your shadow embiggens organically so you need to blast the neutrinos that are chipping away at your shadow.

v0.2.1 (03-26-23)
-
-Scoring system now implemented. You want to embiggen your shadow to a certain size to win! If time runs out, your shadow will leave, and if it shrinks to much from the shadow rays it will die!

v0.2.0 (03-26-23)
-
-Added energy and shadowray cubes, that will increase or decrease the shadow size respectively. The player interacts with energy and the shadow with shadowrays.


v0.1.0 (03-26-23)
-
-Initial release, simple script using Arcade to move a sprite left to right and jumping

-Player's shadow is implemented. It follows the player position and gets bigger/smaller, lighter/darker based on the players Y position.


Road Map
=
This game was created for PyWeek 35 which occured from March 26th to April 1st. As the challenge draws to an end, there are currently no plans to develop the game further as of this time.


Credits
=
Programmed by Lanecrest Tech © 2023

This program is free software released under the MIT License and is submitted as a PyWeek 35 challenge entry in acccordance with their [rules](https://pyweek.readthedocs.io/en/latest/rules.html).
