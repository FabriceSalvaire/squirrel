.. _how-to-refer-page:

===========================
 How to Refer to Babel ?
===========================

Up to now, the official url for Babel is @project_url@

*A permanent redirection will be implemented if the domain change in the future.*

On Github, you can use the **Babel** `topic <https://github.com/search?q=topic%3ABabel&type=Repositories>`_ for repository related to Babel.

A typical `BibTeX <https://en.wikipedia.org/wiki/BibTeX>`_ citation would be, for example:

.. code:: bibtex

    @software{Babel,
      author = {Fabrice Salvaire}, % actual author and maintainer
      title = {Babel},
      url = {@project_url@},
      version = {x.y},
      date = {yyyy-mm-dd}, % set to the release date
    }

    @Misc{Babel,
      author = {Fabrice Salvaire},
      title = {Babel},
      howpublished = {\url{@project_url@}},
      year = {yyyy}
    }
