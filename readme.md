# unhidden

---
## Overview
unhidden is a tool to de-anonymize [Onion Services](https://community.torproject.org/onion-services/)

Broadly, it runs on a [Tor Guard Relay](https://community.torproject.org/relay/) and collects data which can be later analyzed to correlate IP addresses with .onion addresses.

Specifically, unhidden performs opportunistic de-anonymization of Onion Services through traffic correlation with control of a single Guard Relay.

**Note: This is not a bug, a hack, nor a flaw being exploited.** This is only meant as a proof-of-concept to show that opportunistic de-anonymization of Onion Services is much easier than commonly believed.

**Tor is still quite Safe and Effective.** It is my hope not to cast doubt on its usefulness but simply to further the discussion toward making Tor even better! 

## Premise
Using a single Guard Relay, enough onion links, and enough time it should be possible to de-anonymize some (non-targeted) Onion Services through traffic correlation.

The Tor client will select a small number of Guard Relays and persist them for a long time. This means our Guard Relay will be one of only a few relays that handle connections FROM a specific, non-targeted Tor client TO the Tor network for some duration of time. 

During this time, we can expect outside connections TO the Tor client (where such a client is operating as an Onion Service) to cause the Tor client to establish a new connection to our relay (perhaps establishing a connection to a new rendezvous point). 

Using this mechanism we can attempt to correlate connections TO our relay (non-relay IPs) with outside connections TO the Tor client (by way of its onion address)

unhidden only focuses on collecting this information and will leave analysis of the produced data(base) for manual review. 

## Requirements
- Python 3
- stem (pip package)
- urllib3[socks] (pip package)
- Tor Relay with Guard flag
- links.txt
  - File in the base directory with one base onion address per line
  - Can use the output of [spelunkTor](https://github.com/christopherbugg/spelunktor)
  - Ex:
<pre>
links.txt
---
darkfailenbsdla5mal2mxn2uz66od5vtzd5qozslagrfzachha3f3id
bbcnewsd73hkzno2ini43t4gblxvycyac5aw4gnv7t2rccijh7745uqd
protonmailrmez3lotccipshtkleegetolb73fuirgj7r4o4vfu7ozyd
</pre>

## Usage
`python3 unhidden.py`

- This will create `database.db` in the base directory (if none exists)
- `database.db` is the output file and contains the collected data

## Structure
### main controller (`unhidden.py`)
- main looper that runs everything else
- gets the list of links to run in a batch
- spawns new processes for visitor and logger
- kicks off the logger
- kicks off visitor, and waits for completion
- stops logger and gathers found IPs
- sends all data (links and IPs) to db handler

### visitor (`visitor.py`)
- given a link, will attempt http connection through tor
- returns when connection was established (or error)

### logger (`logger.py`)
- keeps watch for all non-relay connections that are established
- submits connections (as IPs) to queue shared with main controller

### database handler (`dbmanager.py`)
- handles interaction to the db from the main controller
- has wrappers for all common functions for ease-of-use

## Contributing
Contributions are welcome! Please open an issue to discuss!

## License
See [license](./license.md)