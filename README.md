# Description #

Scraper based extractor component for extraction of cost and transaction data from Zbozi.cz.

## Config ##

The settings is provided through parameters attribute. Here you can set date range through **Date_preset** of **Date_from** and **Date_to** attributes. Furthermore you can set the **Mode** parameter which allows you to geather summary or by_category.

Example configuration of parameters:

```
"parameters": {
        "Date_from": "2016-03-27",
        "Date_to": "2016-04-02",
        "Mode": "summary"
    }
```

#Parameters options#

* **Date_preset**:
	* "Yesterday" -> extracts data for yesterday only
	* "last_week" -> extracts data for last 7 days
	* "last_31_days" -> extracts data for last 31 days
	* "last_year" -> extracts data for last year


## Shop credential ##

The shop credentials are to be configured through parameters in configuration. Right now you must configure them directly to the python code. Ask administrator if editations are necessary.

## Comunication with KBC ##

The extractor is comuticating with KBC through output mapping settings, which configured by standard way (through UI just like it is in any transformation).
