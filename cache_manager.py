import functools


class CacheManager:
    """
    The goal of this class is to provide some useful functools cache compatible tricks
    """

    def clear_cached_properties(self, properties: list[str] = None):
        """
        Any property that has functools.cached_property decorator will be forced to refresh its data
        by settings it to None.
        """
        attributes = [i for i in dir(type(self))]
        if properties is not None:
            attributes = [i for i in attributes if i in properties]

        for _attribute in attributes:
            if isinstance(
                    getattr(type(self), _attribute), functools.cached_property
            ):  # <- check if is a cached_property
                vars(self).pop(_attribute, None)  # <- Then delete the actual value
