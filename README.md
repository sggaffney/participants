# participants

A clinical trial participant registry microservice.


## Installing the package

- Clone the repository; create and activate a fresh Python virtual environment using
  [venv](https://docs.python.org/3/tutorial/venv.html) or [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html);
  then install the package using `python setup.py develop` (development mode)
  or `python setup.py install`.

- Dependencies will be installed automatically:
  - Flask
  - SQLAlchemy
  - Flask-SQLAlchemy
  - python-dotenv
  - gunicorn (optional)
  - gevent (optional)

## Starting the server

The WSGI server executables `gunicorn` (Mac, *nix only) and `flask` are available after installing
the package and dependencies as above and activating the `participants` virtual environment.
Either executable can be used to serve the application. `gunicorn` is the recommended,
more production-ready option, while `flask` is a 'development' server, best suited
to testing code changes.

 **GUNICORN**:

To serve using `gunicorn`, run the following :
```shell script
gunicorn -w 1 -k gevent participants.registry:app
```
- Note that you can add [command arguments](https://docs.gunicorn.org/en/stable/run.html#commonly-used-arguments)
to further customize the application server, to modify e.g. listening port and
number of worker processes. The command above uses a single 'gevent' worker.

**FLASK**:

To serve using `flask`, run the following:
```shell script
FLASK_APP=participants.registry flask run
```

Additional environment variables can be used to configure the app, either by
prepending to the flask/gunicorn command, or via .env file
(with path set in ENV_PATH):

- `DATA_DIR`: set the directory used to store the sqlite database.
- `SECRET_KEY`: for data encryption.
- `SERVER_NAME`: for custom domains.
- `{DEV_,TEST_,}DATABASE_URL`: set URI for development, testing and production
  databases.


## API

All requests should be directed to `/participant/<reference_id>`
- a GET request retrieves metadata for an existing participant
- a POST request adds metadata for a new participant
- a PUT request modifies metadata for an existing participant
- a DELETE request removes a participant record

The following metadata fields are available:
- `firstname`
- `lastname`
- `dob` (in YYYY-mm-dd format)
- `phone`
- `address1`
- `address2`
- `address3`
- `town`
- `postcode`
- `country`

Participants can be added and modified by supplying a JSON object with the above
fields as keys, and string values. GET, POST, and PUT requests return the
corresponding participant's metadata in the response.


## Design choices and trade-offs

### The model

- Name is stored using first and last name only -- no title or initials.
- All fields can be null. This allows metadata to be entered in stages.
- Date of birth can be any date. No validation is performed, though this would
  be easy to add. Dates are supplied in YYYY-mm-dd format. A user interacting
  directly with the API could conceivably mix up the month and day if not used
  to this format, but I assume inputs will generally come from an intuitive/foolproof GUI.
- Phone number is not validated, though this could be added easily using a
  third-party package, such as `phonenumbers`.
- Address is stored as up to 3 initial lines (address{1,2,3}), then town,
  postcode, country. The term 'postcode' is UK-specific, but could hold ZIP codes.
  There is no validation of address, and this would ideally be populated via an
  address-lookup API in the entry interface.

### Other choices

- Pyscaffold was used to conveniently generate a PyPI-compatible package structure
  with tox and pre-commit hook configuration. A more minimal structure would have
  been possible, with two scripts: one for app, routes and model; another for testing.
  Splitting things up so the app factory, model, and api routes are in separate files
  keeps modules easier to read and maintain. Store the api in its own blueprint
  makes it easier to extend the app with e.g. a web interface in a separate blueprint.
- (Flask-)SQLAlchemy handles database interactions, providing an easy-to-use,
  easy-to-read ORM, and permitting a straightforward switch to other database
  engines.
- SQLite is used for storing data. This format has limitations in data types and
  SQL features, but should work out of the box without having to run and separate
  database service. In-memory sqlite would have been adequate where data persistence
  is not needed, but this app uses on-disk sqlite files to retain data.
- The sqlite files are stored by default in the current working directory (and
  can be stored elsewhere using the DATA_DIR environment variable). Similarly,
  the app checks the working directory for a .env configuration file. This keeps
  things simple for both writing and usage, but a better long-term solution might
  be to use a package like `appdirs` to pick an app-specific directory appropriate
  to the OS.
- GET, POST, and PUT requests return the raw metadata for corresponding
  participant in the response. An alternative would be to combine fields into a
  more readable format, e.g. combining address fields and dropping nulls; combining
  first and last names into a 'full name'.
