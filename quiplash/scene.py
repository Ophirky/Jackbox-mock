"""
    AUTHOR: Ophir Nevo Michrowski
    DATE: 07/04/24
    DESCRIPTION: This is a class that contains everything that is needed for a scene.
"""
from abc import *


class Scene(ABC):
    """This is a Scene interface"""

    @property
    @abstractmethod
    def scene_over(self) -> bool:
        """
        Is the scene over - No Setter (variable change can be only internal.
        :return bool: Whether the scene is over or not
        """
        pass

    @abstractmethod
    def scene(self) -> None:
        """
        This is where the scene code will be contained.
        :return: None
        """
        pass
