# SF Base Election Data (SFBED)

SFBED is an open data project to provide baseline information
about San Francisco elections.

To permit a higher guarantee of quality and accuracy, the focus of the
project is on the information that tends to remain the same from election
to election (or that changes infrequently).

See [here][SFBED_gh_page] for a sample web page created from this data.
If you notice any issues or have a suggestion, please file an issue in the
[issue tracker][issue_tracker].

SFBED is a project of the [SF Elections Data][sf_elections_data] group
of [Code for San Francisco][code_for_sf].


## Overview

The data is provided as a single JSON file included in this repository:
[`data/sf.json`](data/sf.json).

Examples of the type of information that the project aims to provide include--

* all local, state, and federal offices that appear on San Francisco ballots,
* links to the official web site of each office or office body,
* the lengths of the terms of each office, and
* district information for each office (e.g. list of precincts).

The project focus is on the information that tends to remain the
same from election to election.  Thus, the project does not provide
information about candidates, election results, or current office holders.


## Languages

The project has partially support for [internationalization][i18n] (aka "i18n"),
which means support for multiple languages.  The data contains translations
of some phrases in the following languages:

* Chinese
* Spanish
* Filipino/Tagalog (limited)

The [San Francisco Department of Elections][SFDOE] currently prints official
ballots in English, Chinese, and Spanish.  In November 2015, the
Department will begin printing official ballots in Filipino (see
[here](http://www.sfmayor.org/index.aspx?recordid=543&page=998) for
information on the San Francisco
[Language Access Ordinance](http://sfgsa.org/index.aspx?page=4450]), or LAO).

The project would like to add translations in the following languages--

* Japanese
* Korean
* Vietnamese

In the November 2014 election, the Department of Elections also made
translations of election materials available in the three languages
above, along with Filipino.  The materials included ballots and related
instructions, State Voter Information Guides, and Voter Bill of Rights
posters.


## Use Cases

Possible uses of the data include
"[mashing up](http://en.wikipedia.org/wiki/Mashup_%28web_application_hybrid%29)"
with or otherwise supplementing presentations of--

* what is on the ballot,
* election results, or
* campaign finance information.


## The Data

For how to interpret the JSON file, see [this page](docs/json.md).


## Sources

See Article XIII: ELECTIONS, SEC. 13.101. TERMS OF ELECTIVE OFFICE. of the
San Francisco Charter for information about terms of offices, etc.

Resources:

* [List of Local Elected Officials](http://www.sfgov2.org/index.aspx?page=832)
* [List of State Elected Officials](http://www.sfgov2.org/index.aspx?page=833)


## Contributors

Contributors should refer to the [contributor documentation](docs/develop.md)
for additional information.


## License

This project is licensed under the BSD 3-clause license.  See the
[`LICENSE`](LICENSE) file for details.


## Author

Chris Jerdonek (<chris.jerdonek@gmail.com>)


[code_for_sf]: http://codeforsanfrancisco.org/
[i18n]: http://en.wikipedia.org/wiki/Internationalization_and_localization
[issue_tracker]: https://github.com/cjerdonek/sf-base-election-data/issues
[sf_elections_data]: http://cjerdonek.github.io/sf-elections-data/
[SFBED_gh_page]: http://cjerdonek.github.io/sf-base-election-data
[SFDOE]: sfelections.org
