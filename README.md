# Minimum viable Elasticsearch Graphite

Inspired by dlutzy's excellent [mvredisgraphite](https://github.com/dlutzy/mvredisgraphite) here is mveg.

Hopefully pretty simple to use, make sure `mveg.py` and `mveg.sh` are in the same folder and set the following environment variables:

* `ENVIRONMENT` - basically a prefix
* `APP_NAME` - varies the application name used
* `HOSTNAME` - the name of the host being queries (defaults to the output of `hostname`)
* `ES_HOST` - the host on which Elasticsearch is running
* `ES_PORT` - the port on which Elasticsearch is running
* `CARBON_HOST` - the host on which Carbon is running
* `CARBON_PORT` - the port on which Carbon is receiving metrics

Then run `mveg.sh` from wherever you've put it. It'll gather the metrics from Elasticsearch and fire them over to Carbon.

This will start creating metrics with a prefix of `$ENVIRONMENT.$APP_NAME.$HOSTNAME`. It's a bit specific to my use-case, any customisations are more than welcome.
