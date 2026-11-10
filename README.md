# Midea Gas Water Heater & Dishwasher

Home Assistant custom integration for Midea cloud devices.

This maintained fork is intentionally focused on two device types:

- `T0xE1`: dishwasher
- `T0xE3`: gas water heater

## Installation

Copy `custom_components/midea_auto_cloud` into the Home Assistant `custom_components` directory, restart Home Assistant, and add the integration from **Settings → Devices & services**.

The integration uses the Midea cloud service and requires `lupa>=2.0`.

## Notes

The existing integration domain is kept as `midea_auto_cloud` so existing Home Assistant configuration and cached device data can continue to work. Only the dishwasher and gas water heater mappings are included in this project.

Device-specific Lua and plugin files are downloaded by the integration and stored under `.storage/midea_auto_cloud/`.

## License

This project is distributed under the Apache License 2.0. It is a maintained derivative work; see [LICENSE](./LICENSE) for the license terms.
