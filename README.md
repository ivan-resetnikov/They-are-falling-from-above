# They-are-falling-from-above


Forked from: https://github.com/ivan-resetnikov-a/They-are-falling-from-above

Just wanted to add a couple of features that looked fun (randomly generated levels and blocks that disappear), but saw some code issues. 
Planning on fixing some things up, adding the features, and then handing this back to the author if they want it. 

TODO:
  * ~~Change how sound works (objects play their own sounds)~~
  * Add procedurally generated levels
  * Add different types of tiles that disappear.
  * Clean up Main
    * ~~move background to its own object~~
    * move scoreboard to its own object
  * make code more pythonic and easier to read
  * "enemy" class shouldn't be changing player, camera, or anything else
  * stop "enemy" from using a function from "player" class
  * ~~make game over work gracefully (this was implemented but bugged, fixed bug)~~
  * start game menu
  * game over menu 
  * create an input handler and add controller support (due to some player movement being state based, this isn't happening)