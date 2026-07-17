# CRXcavator

Publisher: Splunk Community <br>
Connector Version: 1.0.0 <br>
Product Vendor: DUO Security <br>
Product Name: CRXcavator <br>
Minimum Product Version: 4.8.24304

Connects to CRXCavator.io service that provides reputation and risk scoring for Chrome Extensions

### Configuration variables

This table lists the configuration variables required to operate CRXcavator. These variables are specified when configuring a CRXcavator asset in Splunk SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**verify_server_cert** | optional | boolean | Verify server certificate |
**base_url** | required | string | CRXcavator API endpoint |

### Supported Actions

[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration <br>
[get metadata](#action-get-metadata) - Retrieve metadata about the extension <br>
[get report](#action-get-report) - Gets a report on a specific version of an extension. If no version supplied, attempts to get the latest version of the extension <br>
[submit extension](#action-submit-extension) - Submit an extension ID to be scanned

## action: 'test connectivity'

Validate the asset configuration for connectivity using supplied configuration

Type: **test** <br>
Read only: **True**

#### Action Parameters

No parameters are required for this action

#### Action Output

No Output

## action: 'get metadata'

Retrieve metadata about the extension

Type: **investigate** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**extension_id** | required | Chrome extension id | string | `crxcavator extension id` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.extension_id | string | `crxcavator extension id` | |
action_result.data.extension_id | string | `\*` | |
action_result.data.\*.icon | string | `\*` | |
action_result.data.\*.name | string | `\*` | |
action_result.data.\*.rating | string | `\*` | |
action_result.data.\*.rating_users | string | `\*` | |
action_result.data.\*.short_description | string | `\*` | |
action_result.data.\*.users | string | `\*` | |
action_result.data.\*.versions.\*.version | string | `\*` | |
action_result.status | string | `\*` | success failed |
action_result.message | string | `\*` | |
action_result.summary.name | string | `\*` | |
action_result.summary.short_description | string | `\*` | |
action_result.summary.rating | numeric | `crxcavator number` | |
action_result.summary.total_versions | numeric | `crxcavator number` | |
action_result.summary.latest_version | string | `crxcavator version number` | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get report'

Gets a report on a specific version of an extension. If no version supplied, attempts to get the latest version of the extension

Type: **investigate** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**extension_id** | required | Chrome extension id | string | `crxcavator extension id` |
**version** | optional | Extension version number | string | `crxcavator version number` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.extension_id | string | `crxcavator extension id` | |
action_result.parameter.version | string | `crxcavator version number` | |
action_result.data.\*.csp | string | | |
action_result.data.\*.csp.object-src | string | | |
action_result.data.\*.csp.script-src | string | | |
action_result.data.\*.dangerousfunctions | string | | |
action_result.data.\*.entrypoints | string | | |
action_result.data.\*.extcalls | string | | |
action_result.data.\*.manifest | string | | |
action_result.data.\*.manifest.background | string | | |
action_result.data.\*.manifest.background.page | string | | |
action_result.data.\*.manifest.browser_action | string | | |
action_result.data.\*.manifest.browser_action.default_title | string | | |
action_result.data.\*.manifest.chrome_url_overrides | string | | |
action_result.data.\*.manifest.chrome_url_overrides.newtab | string | | |
action_result.data.\*.manifest.content_security_policy | string | | |
action_result.data.\*.manifest.default_locale | string | | |
action_result.data.\*.manifest.description | string | | |
action_result.data.\*.manifest.externally_connectable | string | | |
action_result.data.\*.manifest.externally_connectable.matches | string | | |
action_result.data.\*.manifest.icons | string | | |
action_result.data.\*.manifest.manifest_version | numeric | | |
action_result.data.\*.manifest.name | string | | |
action_result.data.\*.manifest.optional_permissions | string | | |
action_result.data.\*.manifest.permissions | string | | |
action_result.data.\*.manifest.short_name | string | | |
action_result.data.\*.manifest.update_url | string | | |
action_result.data.\*.manifest.version | string | | |
action_result.data.\*.manifest.web_accessible_resources | string | | |
action_result.data.\*.related | string | | |
action_result.data.\*.risk | string | | |
action_result.data.\*.risk.csp | string | | |
action_result.data.\*.risk.csp.child-src | numeric | | |
action_result.data.\*.risk.csp.connect-src | numeric | | |
action_result.data.\*.risk.csp.font-src | numeric | | |
action_result.data.\*.risk.csp.form-action | numeric | | |
action_result.data.\*.risk.csp.frame-ancestors | numeric | | |
action_result.data.\*.risk.csp.frame-src | numeric | | |
action_result.data.\*.risk.csp.img-src | numeric | | |
action_result.data.\*.risk.csp.manifest-src | numeric | | |
action_result.data.\*.risk.csp.media-src | numeric | | |
action_result.data.\*.risk.csp.object-src | numeric | | |
action_result.data.\*.risk.csp.plugin-types | numeric | | |
action_result.data.\*.risk.csp.sandbox | numeric | | |
action_result.data.\*.risk.csp.script-src | numeric | | |
action_result.data.\*.risk.csp.strict-dynamic | numeric | | |
action_result.data.\*.risk.csp.style-src | numeric | | |
action_result.data.\*.risk.csp.total | numeric | | |
action_result.data.\*.risk.csp.upgrade-insecure-requests | numeric | | |
action_result.data.\*.risk.csp.worker-src | numeric | | |
action_result.data.\*.risk.optional_permissions | string | | |
action_result.data.\*.risk.optional_permissions.total | numeric | | |
action_result.data.\*.risk.permissions | string | | |
action_result.data.\*.risk.permissions.total | numeric | | |
action_result.data.\*.risk.total | numeric | | |
action_result.data.\*.risk.webstore | string | | |
action_result.data.\*.risk.webstore.address | numeric | | |
action_result.data.\*.risk.webstore.last_updated | numeric | | |
action_result.data.\*.risk.webstore.rating_users | numeric | | |
action_result.data.\*.risk.webstore.support_site | numeric | | |
action_result.data.\*.risk.webstore.total | numeric | | |
action_result.data.\*.risk.webstore.users | numeric | | |
action_result.data.\*.risk.webstore.website | numeric | | |
action_result.data.\*.risk.metadata | string | | |
action_result.data.\*.webstore | string | | |
action_result.data.\*.webstore.address | string | | |
action_result.data.\*.webstore.email | string | | |
action_result.data.\*.webstore.icon | string | | |
action_result.data.\*.webstore.last_updated | string | | |
action_result.data.\*.webstore.name | string | | |
action_result.data.\*.webstore.offered_by | string | | |
action_result.data.\*.webstore.permission_warnings | string | | |
action_result.data.\*.webstore.privacy_policy | string | | |
action_result.data.\*.webstore.rating | numeric | | |
action_result.data.\*.webstore.rating_users | numeric | | |
action_result.data.\*.webstore.short_description | string | | |
action_result.data.\*.webstore.size | string | | |
action_result.data.\*.webstore.support_site | string | | |
action_result.data.\*.webstore.users | numeric | | |
action_result.data.\*.webstore.version | string | | |
action_result.data.\*.webstore.website | string | | |
action_result.data.\*.webstore.type | string | | |
action_result.data.\*.webstore.price | string | | |
action_result.data.\*.extension_id | string | | |
action_result.data.\*.version | string | | |
action_result.status | string | | success failed |
action_result.message | string | | |
action_result.summary.extension_id | string | `crxcavator extension id` | |
action_result.summary.version | string | | |
action_result.summary.total_risk | numeric | `crxcavator number` | |
action_result.summary.total_versions | numeric | `crxcavator number` | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'submit extension'

Submit an extension ID to be scanned

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**extension_id** | required | Extension ID to be scanned | string | `crxcavator extension id` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.extension_id | string | `crxcavator extension id` | |
action_result.data.\*.code | numeric | | |
action_result.data.\*.extensionID | string | `crxcavator extension id` | |
action_result.data.\*.message | string | | |
action_result.status | string | | success failed |
action_result.message | string | | |
action_result.summary.code | numeric | | |
action_result.summary.extension_id | string | | |
action_result.summary.version | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

______________________________________________________________________

Auto-generated Splunk SOAR Connector documentation.

Copyright 2026 Splunk Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
