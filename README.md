# GIFT - A Github Finder Tool

_GIFT_ is a web application designed to help users to search and visualize information about github users and repositories. It supports different types of search: search for a _specific user_; search for _users_ based on their _login_ or _fullnames_; search for _repositories_ based on their names or in specific information that might be present in their _descriptions_ or _readme_ files. Search results can be sorted with respect to several qualifiers. Moreover, search queries can be constrained using the advanced search panel, that support constraining the search with respect to the number of _stars_, _forks_, _followers_, _repositories_ and dates of _creation_ and most recent _update_ of repositories. These modes of search are implemented with the help of the [GitHub REST API v3](https://developer.github.com/v3/). The visualization of a user profile in _GIFT_ includes a list of all his/her public repositories. A visual account of the total number of searches are presented by charts created with the library [Chart.js](https://www.chartjs.org/docs/latest/). We also use the REST API pagination facilities to implement page navigation whenever the number of results returned exceeds what is predetermined for that particular search mode. This application is implemented with _HTML_, _CSS_, _Bootstrap_, _JavaScript_, _Python_, _Django_ and the _SQLite_ database. You can see it live [here](https://gift-gh.herokuapp.com/).
This application satisfy all the requirements in the specification of the final project, especially in the use of Django, JavaScript, models and responsiveness (see video). Also, it is rather different from all the other project assignments defined in this course. Moreover, it is particulary useful for the community of programmers in general, because it allows developers to have a quick overview of a GitHub profile and supports very complex and sophisticated queries using a considerable subset of the Github search API. Most important, the complexity of the search API language is hidden through the use of pre-defined templates and the rather sophisticated panel for advanced search.

## Source Code - Comments

- /gift:

  - models.py: contains the models for plotting charts and for controling the advanced search panel.
  - urls.py: all the urls supported by the application.
  - utils.py: a number of helper functions, especially the ones that access the Github REST API.
  - views.py: definition of all functions that implement the behaviour for each url in 'urls.py'.
  - /static/gift:
    - styles.css: contains all definitions for styling the whole app.
    - getCookie.js: return the csrf token needed to make fetch calls in Django.
    - source.js: used to insert the template of a query in the navbar search box.
    - charts.js: code to generate the bar charts associated to the search queries.
    - adv.search: code that controls the advanced search panel.
    - sort_repos.js: controls the dropdown menu for sorting repositories.
    - sort_uers.js: controls the dropdown menu for sorting users.
    - sort_user_reps.js:controls the dropdown menu for sorting user repositories.
  - /templates/gift:
    - layout.html: generates markup that is contained in every page.
    - error.html: used to present error messages to the user (when nothing is found).
    - index_adv.html: markup to represent both the advanced search and examples panel.
    - index.html: markup that displays only the examples panel.
    - readme.html: shows a simplified version of this file inside the application.
    - repos.html: markup used to display the repositories returned by a search query.
    - users.html: markup used to display the users returned by a search query.
    - user.html: markup used to display the user profile and his/her public repositories.
  - /templatetags:
    - gift_extras.py: declares a new filter to replace 'normal spaces' by 'non-breaking spaces'.

- requirements.txt: programs and libraries that must be installed for a successful deployment.
- ProcFile: configuration file for deployment at Heroku.
- runtime.txt: configuration file for deployment at Heroku.

### Some data about me

- Alfio Ricardo de Brito Martini
- Porto Alegre - RS - Brazil
- alfio.martini@gmail.com
