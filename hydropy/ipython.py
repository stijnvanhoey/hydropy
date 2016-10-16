# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 11:44:13 2016

@author: Marty

ipython.py

This module is for holding convenience functions for working with IPython.
"""
import pandas as pd
from IPython.display import HTML
# import hydropy as hp


def startsession():
    """This doesn't work. The hope was to create a function that a user could
    call that would take care of all of the imports and whatnot. Not a big
    convenience, but that was the idea.

    You can't import inside of a function and have it affect the main
    namespace. Instead, try the following:
        - create a ipython_config.py file. http://ipython.org/ipython-doc/stable/config/intro.html#setting-configurable-options

    take care of all of the imports and other things that need to be done
    at the start of a session.

    TODO: wrap the imports in a try clause, and create a special import Error
    if the import fails. This Error will include a message about how to use pip
    or conda to install pandas and numpy.


    # Import the libraries that we'll be using
    print('import numpy as np')
    import numpy as np
    print('import pandas as pd')
    import pandas as pd
    print('hydropy as hp')
    # Note to self: hey dummy!  How can you use startsession() if you haven't
    # already imported hydropy?
    import hydropy as hp
    # Set the notebook to plot graphs in the output cells.
    print('%matplotlib inline')
    # %matplotlib inline
    """
    pass


def draw_map(width=700, height=400):
    """Draw an interactive map from hydrocloud.org.

    Places a map of USGS stream gauges from hydrocloud.org into an IFrame and
    displays it in an IPython interactive session.  To use the map, click on
    the red dots to display information about each USGS stream gauge.

    Args:
    -----
        width (int): The width of the map iframe.
        height (int): The height of the map iframe.

    Returns:
    --------
        HTML display object.

    Example:
    --------
        >>> import hydropy as hp
        >>> hp.draw_map()
        A map is drawn.

        >>> hp.draw_map(width=900, height=600)
        A big map is drawn!

    TODO:
    -----
        - use ipywidgets to allow users to click on the map, and this will
            return a value that can be used in another IPython cell. This
            feature would allow the map to act as an interactive site selection
            tool.
"""
    output = HTML('<p>Use <a href="http://hydrocloud.org" target="_blank">'
                  'HydroCloud.org</a> to find a stream gauge. '
                  'Click on the red dots to learn more about a site.</p>'
                  '<iframe src=http://hydrocloud.org/ width={} height={}>'
                  '</iframe>'.format(width, height))

    return output


# inject this function into HydroPy classes that would benefit from Pandas'
# excellent __str__() functions.  Inject like this::
# self.__str__ = hydro_df_to_str
def hydro_df_to_str(self):
    return str(self.data)


def hydro_df_to_repr(self):
    return repr(self.data)


def hydro_df_to_repr_html(self):
        """return the data formatted as html in an IPython notebook.
        """
        if self.data is None:
            return str(self.data)
        return pd.DataFrame._repr_html_(self.data)
