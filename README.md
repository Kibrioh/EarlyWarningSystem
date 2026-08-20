# EarlyWarningSystem
Location-Based Early Warning System for Flooding via SMS
Overview
This system is designed to provide early warnings for flooding based on the user's location. It utilizes geographical data to identify flood-prone areas and sends SMS alerts to registered users within those areas.

Features
Geolocation Integration: The system integrates with OSM Nominatim services to determine the user's location based on their input.

SMS Alerts: When a user is located within a flood-prone area, they receive SMS alerts notifying them of the potential danger. It uses Twilio API for sms

User Registration: Users can register their information, including their name, phone number, and location, to receive alerts tailored to their specific area.

Requirements
Python 3.x
Django web framework
Geocoding service (OSM Nominatim)
SMS service provider ( Twilio)

Clone the repository:
git clone https://github.com/kibrioh/EarlyWarningSystem.git

Set up the database: Postgres/PostGIS

Set up environment variables for your geocoding service API key and SMS service provider credentials.
Run the development server:

Access the web application through your browser:

http://localhost:8000/

Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

