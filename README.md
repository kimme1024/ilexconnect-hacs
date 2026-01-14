# I-LexConnect Water Softener

Home Assistant integration for SYR / I-LexConnect water softeners.

## Features
- Water consumption (daily / weekly / monthly / yearly)
- Salt level monitoring
- Water pressure
- Regeneration statistics
- Energy dashboard compatible (water)

## Installation

1. Install via HACS (Custom Repositories → Add repository) or manually copy `custom_components/ilexconnect` to your Home Assistant `custom_components` folder.
2. Restart Home Assistant.
3. Add the integration via **Settings → Devices & Services → Add Integration → I-LexConnect**.
4. Enter your `username`, `password`, and `device_id`.
5. All sensors will appear automatically.

### Manual
Copy `custom_components/ilexconnect` to your Home Assistant config folder.

## Configuration
Configured via UI (Settings → Devices & Services)

## Sensors

| Sensor | Unit | Description |
|--------|------|-------------|
| Today's Water Usage | L | Total water used today |
| Yesterday's Water Usage | L | Total water used yesterday |
| Water Flow | L/min | Current flow rate |
| Salt Content | kg | Current salt level |
| Water Reserve | % | Remaining water reserve |
| Normal Regenerations | — | Number of normal regenerations |
| Service Regenerations | — | Number of service regenerations |
| Incomplete Regenerations | — | Number of incomplete regenerations |
| Total Regenerations | — | Total number of regenerations |
| Salt Dose | g/L | Current salt dosing setting |
| Water Pressure | bar | Current water pressure |
| Current Week Usage | L | Water usage for this week |
| Previous Week Usage | L | Water usage for last week |
| Yearly Water Usage | m³ | Water usage this year |
| Lifetime Water Usage | m³ | Total water usage since installation |
| Salt Usage Total | kg | Total salt used |
| Monthly Water Usage | m³ | Water usage per month |
| Salt Usage Monthly | kg | Salt used per month |

### Device Information

| Field | Description |
|-------|-------------|
| Device Type | Device model/type |
| Firmware | Installed firmware version |
| System Date/Time | Current date and time of the system |
| Mac Address | Device MAC address |
| Serial Number | Device serial number |
| Status | Online/offline |

## Energy Dashboard
Use the provided `today_s_water_usage` sensor together with a Utility Meter.

## Disclaimer
This integration is not affiliated with SYR or I-LexConnect.

This integration was developed with the assistance of AI tools.
I will do my best to maintain and support it, but please note that
support may be limited and community contributions are welcome.