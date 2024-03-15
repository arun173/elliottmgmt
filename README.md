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
1. Read a configuration file called inventory.txt which contains only domain names <br>
2. Calls the SSL_CHECKER function which does the following:<br>
   a. Get the IP address of the domain, this required for getEndpointData API of SSL labs<br>
   b. Perform an API Get request with CacheOn option to get the recent report from cahce, else the Analyze API generates a new report<br>
   c. Calls the API to get the analysis report<br>
   d. Captures the output in JSON format<br>
   e. Feeds the JSON output to a Pandas dataframe (if we intend to persist results in a database in future with run date)<br>
   f. Prints the Dataframe output to STDOUT ( just for testing during verification)<br>
   g. If the report is not ready it may encounter an exception and upon re-run report will be availble <br>
   h. Records the scan results output in CSV Format inside docker mount<br>
   i. To present the CSV to local host, docker mount can be defined in the Dockerfile or docker run can be invoked with -v option to define mounts at runtime<br>

   
**Exceuting Script from Command line**
1. Download the github report elliottmgmt <br>
2. Install Python V 3.x, tested with V3.12.2 <br>
3. Install the required python libraries <br>
      **pip install -r requirements.txt**
4. Run the following <br>
      **python ssl_api.py**
5. This should generate an on-screen output and a CSV file to verify <br>

**Generating a Docker file**
1. Download the report elliottmgmt <br>
2. Run the Dockerfile to create a new local image at your environment <br>
      cd to repo directory <br>
      **docker build . -t ssl-api**

**Executing the docker Image**
Generate a local docker image if any changes needed in configuration files to suit your envrionemnt or download the use the **ssl-api** package to run as is.<br>
      **docker run -it ssl-api:latest**


**Known Issues**

During the first run, due to use of Pandas we may see this exception since there was no cache data and report is just triggered. This can be enhanced with a sleep(300) in the script and READY status check in the API.<br>
Given a 3-hour window haven't coded those aspects and it may involve little more test cycles.<br>

**First run - exception message is expected as below** <br>
*Exception encountered:If using all scalar values, you must pass an index*<br>

**Subsequent run will produce report with status immediately** <br>

                          ipAddress statusMessage  ... delegation        details<br>
hostStartTime            23.185.0.2   In progress  ...          2  1710538892959<br>
**certChains**               23.185.0.2   In progress  ...          2             []<br>
protocols                23.185.0.2   In progress  ...          2             [] <br>
prefixDelegation         23.185.0.2   In progress  ...          2           True<br>
nonPrefixDelegation      23.185.0.2   In progress  ...          2          False<br>
zeroRTTEnabled           23.185.0.2   In progress  ...          2             -1 <br>
zombiePoodle             23.185.0.2   In progress  ...          2              0 <br>
goldenDoodle             23.185.0.2   In progress  ...          2              0 <br>
zeroLengthPaddingOracle  23.185.0.2   In progress  ...          2              0 <br>
sleepingPoodle           23.185.0.2   In progress  ...          2              0 <br>

**Consideration for Next Phase of Development**

**How would you scale this script and run it with resiliency to e.g. handle 1000s of domains?**
The script has been containerized. It can handle a lot of domains. For this use case I have used only elliott's domain but test with other domains like google.com, microsoft.com etc. Python will loop through the input file and trigger the report generation.<br>
Strategic method to handle this would be:<br>

1. Keep the domain list in a database table with scan_status column (pick hosts that meet the filter criteria scan_status = "N") <br>
2. Enhance the python script to read from a database table instead of a flat file <br>
3. When each domain is picked up for scanning update the scan_status column with "Y" which implies the job has been triggered<br>
4. If there are tens of thousands of domain to be scanned then deploy this container image in Kubernetes with Horizontal Pod Autoscaling option based on cpu-usage<br>
     **e.g. kubectl autoscale deployment ssl-api --cpu-percent=50 --min=1 --max=10**<br>
   

**How would you monitor/alert on this service?**

Prometheus, Grafana & Alertmanager will be monitoring tool of choice to configure timely alerts.

**What would you do to handle adding new domains to scan or certificate expiry events from your service?**

Based on response to question #1, strategic way to be adding more records to the table with domain name. <br>
**certChains** will be fitlered out and any status other than "A" will be reported for certificated issues.<br>

**After some time, your report requires more enhancements requested by the Tech team of the company. How would you handle these "continuous" requirement changes in a sustainable manner?**

All enhancement requests will be recorded in the Jira, and feature priotization will be done based on business urgency.<br>
Scan results are produced in dataframes we can port to database for periodic analysis.
Since the results are persisted it is easy to analyze, filter and enhancements can be made quickly.
In the current build there is no database backend, only a CSV file is generated. However in an enterpise setup reporting capabilities can be enhanced with structured backend database & using state of the art reporting tools.
