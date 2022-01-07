[comment]: # "Auto-generated SOAR connector documentation"
# CRXcavator

Publisher: Splunk Community  
Connector Version: 1\.0\.1  
Product Vendor: DUO Security  
Product Name: CRXcavator  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 4\.8\.24304  

Connects to CRXCavator\.io service that provides reputation and risk scoring for Chrome Extensions

[comment]: # " File: readme.md"
[comment]: # "  Copyright (c) 2020 Splunk Inc."
[comment]: # ""
[comment]: # "  Licensed under Apache 2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)"
[comment]: # ""
App connects to CRXcavator's free API. It does not require an API key to connect.


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a CRXcavator asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**base\_url** |  required  | string | CRXcavator API endpoint

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[get metadata](#action-get-metadata) - Retrieve metadata about the extension  
[get report](#action-get-report) - Gets a report on a specific version of an extension\. If no version supplied, attempts to get the latest version of the extension  
[submit extension](#action-submit-extension) - Submit an extension ID to be scanned  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'get metadata'
Retrieve metadata about the extension

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**extension\_id** |  required  | Chrome extension id | string |  `crxcavator extension id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.extension\_id | string |  `crxcavator extension id` 
action\_result\.data\.extension\_id | string |  `\*` 
action\_result\.data\.\*\.icon | string |  `\*` 
action\_result\.data\.\*\.name | string |  `\*` 
action\_result\.data\.\*\.rating | string |  `\*` 
action\_result\.data\.\*\.rating\_users | string |  `\*` 
action\_result\.data\.\*\.short\_description | string |  `\*` 
action\_result\.data\.\*\.users | string |  `\*` 
action\_result\.data\.\*\.versions\.\*\.version | string |  `\*` 
action\_result\.status | string |  `\*` 
action\_result\.message | string |  `\*` 
action\_result\.summary\.name | string |  `\*` 
action\_result\.summary\.short\_description | string |  `\*` 
action\_result\.summary\.rating | numeric |  `crxcavator number` 
action\_result\.summary\.total\_versions | numeric |  `crxcavator number` 
action\_result\.summary\.latest\_version | string |  `crxcavator version number` 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get report'
Gets a report on a specific version of an extension\. If no version supplied, attempts to get the latest version of the extension

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**extension\_id** |  required  | Chrome extension id | string |  `crxcavator extension id` 
**version** |  optional  | Extension version number | string |  `crxcavator version number` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.extension\_id | string |  `crxcavator extension id` 
action\_result\.parameter\.version | string |  `crxcavator version number` 
action\_result\.data\.\*\.csp | string | 
action\_result\.data\.\*\.csp\.object\-src | string | 
action\_result\.data\.\*\.csp\.script\-src | string | 
action\_result\.data\.\*\.dangerousfunctions | string | 
action\_result\.data\.\*\.entrypoints | string | 
action\_result\.data\.\*\.extcalls | string | 
action\_result\.data\.\*\.manifest | string | 
action\_result\.data\.\*\.manifest\.background | string | 
action\_result\.data\.\*\.manifest\.background\.page | string | 
action\_result\.data\.\*\.manifest\.browser\_action | string | 
action\_result\.data\.\*\.manifest\.browser\_action\.default\_title | string | 
action\_result\.data\.\*\.manifest\.chrome\_url\_overrides | string | 
action\_result\.data\.\*\.manifest\.chrome\_url\_overrides\.newtab | string | 
action\_result\.data\.\*\.manifest\.content\_security\_policy | string | 
action\_result\.data\.\*\.manifest\.default\_locale | string | 
action\_result\.data\.\*\.manifest\.description | string | 
action\_result\.data\.\*\.manifest\.externally\_connectable | string | 
action\_result\.data\.\*\.manifest\.externally\_connectable\.matches | string | 
action\_result\.data\.\*\.manifest\.icons | string | 
action\_result\.data\.\*\.manifest\.manifest\_version | numeric | 
action\_result\.data\.\*\.manifest\.name | string | 
action\_result\.data\.\*\.manifest\.optional\_permissions | string | 
action\_result\.data\.\*\.manifest\.permissions | string | 
action\_result\.data\.\*\.manifest\.short\_name | string | 
action\_result\.data\.\*\.manifest\.update\_url | string | 
action\_result\.data\.\*\.manifest\.version | string | 
action\_result\.data\.\*\.manifest\.web\_accessible\_resources | string | 
action\_result\.data\.\*\.related | string | 
action\_result\.data\.\*\.risk | string | 
action\_result\.data\.\*\.risk\.csp | string | 
action\_result\.data\.\*\.risk\.csp\.child\-src | numeric | 
action\_result\.data\.\*\.risk\.csp\.connect\-src | numeric | 
action\_result\.data\.\*\.risk\.csp\.font\-src | numeric | 
action\_result\.data\.\*\.risk\.csp\.form\-action | numeric | 
action\_result\.data\.\*\.risk\.csp\.frame\-ancestors | numeric | 
action\_result\.data\.\*\.risk\.csp\.frame\-src | numeric | 
action\_result\.data\.\*\.risk\.csp\.img\-src | numeric | 
action\_result\.data\.\*\.risk\.csp\.manifest\-src | numeric | 
action\_result\.data\.\*\.risk\.csp\.media\-src | numeric | 
action\_result\.data\.\*\.risk\.csp\.object\-src | numeric | 
action\_result\.data\.\*\.risk\.csp\.plugin\-types | numeric | 
action\_result\.data\.\*\.risk\.csp\.sandbox | numeric | 
action\_result\.data\.\*\.risk\.csp\.script\-src | numeric | 
action\_result\.data\.\*\.risk\.csp\.strict\-dynamic | numeric | 
action\_result\.data\.\*\.risk\.csp\.style\-src | numeric | 
action\_result\.data\.\*\.risk\.csp\.total | numeric | 
action\_result\.data\.\*\.risk\.csp\.upgrade\-insecure\-requests | numeric | 
action\_result\.data\.\*\.risk\.csp\.worker\-src | numeric | 
action\_result\.data\.\*\.risk\.optional\_permissions | string | 
action\_result\.data\.\*\.risk\.optional\_permissions\.total | numeric | 
action\_result\.data\.\*\.risk\.permissions | string | 
action\_result\.data\.\*\.risk\.permissions\.total | numeric | 
action\_result\.data\.\*\.risk\.total | numeric | 
action\_result\.data\.\*\.risk\.webstore | string | 
action\_result\.data\.\*\.risk\.webstore\.address | numeric | 
action\_result\.data\.\*\.risk\.webstore\.last\_updated | numeric | 
action\_result\.data\.\*\.risk\.webstore\.rating\_users | numeric | 
action\_result\.data\.\*\.risk\.webstore\.support\_site | numeric | 
action\_result\.data\.\*\.risk\.webstore\.total | numeric | 
action\_result\.data\.\*\.risk\.webstore\.users | numeric | 
action\_result\.data\.\*\.risk\.webstore\.website | numeric | 
action\_result\.data\.\*\.risk\.metadata | string | 
action\_result\.data\.\*\.webstore | string | 
action\_result\.data\.\*\.webstore\.address | string | 
action\_result\.data\.\*\.webstore\.email | string | 
action\_result\.data\.\*\.webstore\.icon | string | 
action\_result\.data\.\*\.webstore\.last\_updated | string | 
action\_result\.data\.\*\.webstore\.name | string | 
action\_result\.data\.\*\.webstore\.offered\_by | string | 
action\_result\.data\.\*\.webstore\.permission\_warnings | string | 
action\_result\.data\.\*\.webstore\.privacy\_policy | string | 
action\_result\.data\.\*\.webstore\.rating | numeric | 
action\_result\.data\.\*\.webstore\.rating\_users | numeric | 
action\_result\.data\.\*\.webstore\.short\_description | string | 
action\_result\.data\.\*\.webstore\.size | string | 
action\_result\.data\.\*\.webstore\.support\_site | string | 
action\_result\.data\.\*\.webstore\.users | numeric | 
action\_result\.data\.\*\.webstore\.version | string | 
action\_result\.data\.\*\.webstore\.website | string | 
action\_result\.data\.\*\.webstore\.type | string | 
action\_result\.data\.\*\.webstore\.price | string | 
action\_result\.data\.\*\.extension\_id | string | 
action\_result\.data\.\*\.version | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.extension\_id | string |  `crxcavator extension id` 
action\_result\.summary\.version | string | 
action\_result\.summary\.total\_risk | numeric |  `crxcavator number` 
action\_result\.summary\.total\_versions | numeric |  `crxcavator number` 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'submit extension'
Submit an extension ID to be scanned

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**extension\_id** |  required  | Extension ID to be scanned | string |  `crxcavator extension id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.extension\_id | string |  `crxcavator extension id` 
action\_result\.data\.\*\.code | numeric | 
action\_result\.data\.\*\.extensionID | string |  `crxcavator extension id` 
action\_result\.data\.\*\.message | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.code | numeric | 
action\_result\.summary\.extension\_id | string | 
action\_result\.summary\.version | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 