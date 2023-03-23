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
    * ~~move scoreboard to its own object~~
    * address updateEnemies function (add an enemy manager object?)
    * organize initialization between init and onStart
    * (new) main's self.render_scale does not use the constant value
    * (new) re-organize level generation so it's out of main
  * ~~make code more pythonic and easier to read~~
  * "enemy" class shouldn't be changing player, camera, or anything else
  * stop "enemy" from using a function from "player" class
  * ~~make game over work gracefully (this was implemented but bugged, fixed bug)~~
  * implement main menu
    * implement map selection from main menu
  * game over takes player to main menu where the game can be restarted
  * create an input handler and add controller support
