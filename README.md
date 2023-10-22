# WindiX - API-based Weather Reporting Web Application - 
#### Video Demo:  <https://youtu.be/2HRVx4BCW6U>
#### Description: WindiX is a web application designed to provide users with comprehensive weather information for cities around the world. Leveraging a range of cutting-edge technologies and APIs, WindiX offers real-time weather data, interactive maps, geolocation services, and the convenience of saving favorite cities for quick access.

#### Techologies Used: Python FrameWork Flask, JavaScript, Html and CSS, Bootstrap, AJAX(Basics) and SQLite.

#### API's Used:
- [weatherapi](https://www.weatherapi.com/weather/): weatherapi.com is weather and geolocation API provider that provides extensive APIs that gives info about realtime and forecasted weather, Air Quality data, Historical weather data, Astronomcial data and Geolocation.

- [Leaflet](https://leafletjs.com/index.html): Leaflet.com is open-source JavaScript library which provides interactive lightweight maps.

#### Features: 
- **Realtime Weather information**: Provide Realtime and forecast Weather data on the user Entered City using API's Provided by [weatherapi.com](https://www.weatherapi.com/weather/)

- **Interactive Maps**: Provide a Interactive Map in which you can click anywhere to access its current weather information.

- **Geolocation Services**: WindiX can detect user's longitude and latitude, which enable WindiX to report weather of user's location. 

- **Favourite Cities**: Users can store names of their favourite cities making it easier to access frequently visited places.

- **Email Verification**: During the registration process, users receive a verification code via email, ensuring secure and validated accounts. Password resets are also facilitated through email.

- **Google Charts (Basic)**: Used a Google chart to display some weather infomation.

- **AJAX (Basic)**: Used AJAX on city seachbar to display city names on the basis of what user type.

#### Setting Up Environment Variables

1. Create a `.env` file in your project's root directory.

2. Add the following variables to the `.env` file:

   - `API_KEY`: Replace `<api-key>` with your WeatherAPI.Chrome API key.
   - `MAIL_DEFAULT_SENDER`: Set this to your bot's email for sending user emails.
   - `MAIL_USERNAME`: Use your bot's email address again.
   - `MAIL_PASSWORD`: Enter your bot's email app password.

3. Save the `.env` file in the same directory as your code files.

You're now ready to work with the project.
#### Executing the program: 
   Use `flask run` in projects root directory To execute the program.
   