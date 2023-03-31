

class LevelGenerator:
  def __init__(self) -> None:
    pass

  def new(self):
    level_map = [
      '            ',
      '            ',
      '            ',
      '            ',
      '         .  ',
      '      .  #  ',
      '  . . #  .  ',
      '  # # #  #  ',
      '  ..# ...#. ',
      '  ### ##### ',
      '  ##. ### . ',
      '  ###.....# ',
      '  ######### '
    ]
    return level_map

  def get_map_classic(self):
    level_map = [
      '            ',
      '            ',
      '            ',
      '            ',
      '         .  ',
      '      .  #  ',
      '  . . #  .  ',
      '  # # #  #  ',
      '  ..#....#. ',
      '  ######### ',
      '  ######### ',
      '  ######### ',
      '  ######### '
    ]
    return level_map