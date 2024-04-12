"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 07/04/24
    DESCRIPTION: This is a class that contains everything that is needed for a scene.
"""


class Scene:
    """This is a Scene interface"""
    def __init__(self, background_color=(255, 255, 255)):
        """
        The interface constructor
        :param background_color: The background color of the scene
        """
        self.background_color = background_color

    def scene(self) -> None:
        """
        This is where the scene code will be contained.
        :return: None
        """
        pass
