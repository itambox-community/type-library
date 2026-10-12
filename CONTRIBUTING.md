# Contributing

Thank you for adding a model. Changes reach `main` only through a pull request that passes CI and
is merged by a maintainer. There is no automerge.

## Add a model

1. Copy `asset-types/Fairphone/Fairphone 5.yaml` to `asset-types/<Manufacturer>/<Model>.yaml`.
2. Replace the content with the data of your model. Only add values you can source from the
   manufacturer's datasheet; leave a key out when you do not know it.
3. Run `python scripts/validate.py` and `yamllint -c .yamllint.yaml .`.
4. Open a pull request, one model or one manufacturer per PR.
5. Use a conventional commit subject in English, e.g. `feat: add Fairphone 5`.

## Required fields

| Field | Notes |
|---|---|
| `manufacturer` | Official brand name. Also the folder name. |
| `model` | Official model name. Also the file name without `.yaml`. |
| `category` | One of the category slugs below. |

Optional: `description` (text), `part_number` (max 100 characters), `ean` (max 14 characters), `specs`.

The file must live at `asset-types/<manufacturer>/<model>.yaml`. The names are used verbatim,
so they must not be padded with spaces or contain `< > : " / \ | ? *`.

## The unit rule

Quantities are written as a number, a space and the vocabulary unit only, e.g. `57 Wh`.
Never convert in a different unit and never add a second one: `57000 mWh`, `0.057 kWh` and
`57Wh` all fail CI. The expected unit of every key is listed below, and the CI message names
the key and the unit it expects.

Other value kinds: integers are plain numbers (`ethernet_port_count: 8`), booleans are
`true`/`false`, choices use the listed slug (`form_factor: notebook`), lists use YAML sequences.

## Categories

- `access-points`
- `desktops`
- `firewalls`
- `laptops`
- `mobile-phones`
- `monitors`
- `printers`
- `routers`
- `servers`
- `switches`
- `tablets`
- `ups`
- `virtual-machines`

## Specification keys

Generated from `schema/generated_schema.json`.

| Key | Value |
|---|---|
| `acoustic_level` | quantity, `<number> dBA` |
| `analog_input_count` | integer |
| `apparent_power` | quantity, `<number> VA` |
| `battery_capacity` | quantity, `<number> Wh` |
| `battery_runtime` | quantity, `<number> min` |
| `battery_runtime_load` | quantity, `<number> W` |
| `camera_resolution` | quantity, `<number> MP` |
| `color_supported` | boolean |
| `core_count` | integer |
| `country_of_origin` | text |
| `digital_input_count` | integer |
| `display_resolution` | text |
| `display_size` | quantity, `<number> in` |
| `drive_bay_count` | integer |
| `duplex_supported` | boolean |
| `energy_certifications` | list of: `80plus`, `80plus_bronze`, `80plus_gold`, `80plus_platinum`, `80plus_silver`, `80plus_titanium`, `energy_star`, `epeat_bronze`, `epeat_gold`, `epeat_silver`, `other` |
| `ethernet_port_count` | integer |
| `ethernet_speeds` | list of: `100g`, `100m`, `10g`, `10m`, `1g`, `200g`, `25g`, `2_5g`, `400g`, `40g`, `50g`, `5g` |
| `firmware_version` | text |
| `form_factor` | one of: `appliance`, `blade`, `desktop`, `module`, `notebook`, `other`, `peripheral`, `phone`, `rack`, `tablet`, `tower` |
| `hostname` | text |
| `hot_swap_supported` | boolean |
| `industrial_protocols` | list of: `bacnet_ip`, `canopen`, `ethercat`, `ethernet_ip`, `modbus_rtu`, `modbus_tcp`, `opc_ua`, `other`, `profibus`, `profinet` |
| `input_voltage_max` | quantity, `<number> V` |
| `input_voltage_min` | quantity, `<number> V` |
| `ip_rating` | text |
| `management_protocols` | list of: `graphql`, `https`, `ipmi`, `other`, `redfish`, `rest`, `snmpv1`, `snmpv2c`, `snmpv3`, `ssh`, `wsman` |
| `memory_capacity` | quantity, `<number> GiB` |
| `memory_type` | one of: `ddr3`, `ddr4`, `ddr5`, `hbm2`, `hbm3`, `lpddr4x`, `lpddr5`, `lpddr5x`, `other` |
| `network_functions` | list of: `bridge`, `firewall`, `gateway`, `load_balancer`, `modem`, `router`, `switch`, `vpn_gateway`, `wlan_ap`, `wlan_controller` |
| `operating_system_family` | one of: `android`, `bsd`, `chromeos`, `embedded`, `ios`, `ipados`, `linux`, `macos`, `network_os`, `other`, `windows`, `windows_server` |
| `operating_temperature_max` | quantity, `<number> °C` |
| `operating_temperature_min` | quantity, `<number> °C` |
| `outdoor_rated` | boolean |
| `poe_budget` | quantity, `<number> W` |
| `poe_port_count` | integer |
| `power_consumption_max` | quantity, `<number> W` |
| `power_output` | quantity, `<number> W` |
| `print_speed` | quantity, `<number> pages_per_minute` |
| `print_technology` | one of: `dot_matrix`, `dye_sublimation`, `inkjet`, `laser`, `other`, `solid_ink`, `thermal` |
| `processor_model` | text |
| `rack_units` | quantity, `<number> U` |
| `regulatory_certifications` | list of: `ce`, `csa`, `eac`, `fcc`, `other`, `rcm`, `ukca`, `ul`, `vcci` |
| `rohs_compliant` | boolean |
| `sensor_types` | list of: `current`, `energy`, `flow`, `gas`, `humidity`, `level`, `light`, `motion`, `other`, `position`, `power`, `pressure`, `smoke`, `temperature`, `vibration`, `voltage` |
| `storage_capacity` | quantity, `<number> GiB` |
| `storage_interface` | one of: `emmc`, `nvme`, `other`, `sas`, `sata`, `ufs`, `usb`, `virtual` |
| `storage_medium` | one of: `flash`, `hdd`, `hybrid`, `optical`, `other`, `ssd`, `tape` |
| `switching_capacity` | quantity, `<number> Gbit/s` |
| `touch_supported` | boolean |
| `usb_port_count` | integer |
| `vcpu_count` | integer |
| `weight` | quantity, `<number> kg` |
| `wifi_standards` | list of: `802_11a`, `802_11ac`, `802_11ax`, `802_11b`, `802_11be`, `802_11g`, `802_11n` |

## Requesting a new specification key or category

The vocabulary belongs to the ITAMbox webapp, not to this repository. Open an issue in this
repository describing the key, its unit and a few example models. If accepted, it is implemented
as a pull request in the webapp, and the schema copy here is refreshed from the next webapp release.
Until then files using the key cannot be merged.

## Refreshing the schema copy (maintainers)

`schema/generated_schema.json` is copied from the webapp (`manage.py export_catalogue_schema`).
Never edit it by hand; replace the file in a dedicated PR and let CI revalidate every model.
