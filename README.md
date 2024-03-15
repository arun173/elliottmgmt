# elliottmgmt

**Challenge:**

1. Retrieve up to date SSL scan results for www.elliottmgmt.com from Qualys SSL Labs API documentation is available at (https://github.com/ssllabs/ssllabs-scan/blob/stable/ssllabs-api-docs.md)
2. Format relevant information into a report ready for email distribution.

**Solution:**

To get the SSL scan results for a domain SSL LABS provide an API interface to run a free scan and to retrieve those results.
Reference: https://github.com/ssllabs/ssllabs-scan/blob/master/ssllabs-api-docs-v3.md
For this solution SSL LABS API V3 is being used.

**Scripting Language used: Python V3.12.2**

This script should be compatible with any Python V3 version however it is testing only with V3.12.2 since that's what I have in my dev machine.

**High Level Design**


<img width="619" alt="image" src="https://github.com/arun173/elliottmgmt/assets/38709512/2a6947d9-17a9-4129-a19d-b4f05ff63647">

**Script Function**
1. Read an input file called inventory.txt which contains only domain names
2. Calls the SSL_CHECKER function which does the following:
   a. Get the IP address of the domain, this required for getEndpointData API of SSL labs
   b. Perform an API Get request with CacheOn option to get the recent report from cahce, else the Analyze API generates a new report
   c. Calls the API to get the analysis report
   d. Captures the output in JSON format
   e. Feeds the JSON output to a Pandas dataframe (if we intend to persist results in a database in future with run date)
   f. Prints the Dataframe output to STDOUT ( just for testing during verification)
   g. If the report is not ready it may encounter an exception and upon re-run report will be availble 
   h. Records the scan results output in CSV Format inside docker mount
   i. To present the CSV to local host, docker mount can be defined in the Dockerfile or docker run can be invoked with -v option to define mounts at runtime

   
   
