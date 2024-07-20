#define BLYNK_PRINT Serial
#define BLYNK_TEMPLATE_ID "" // replace this with template id
#define BLYNK_TEMPLATE_NAME "Weather Station" // replace this with your device name

#include <WiFi.h> // importing all the required libraries
#include <WiFiClient.h>
#include <BlynkSimpleEsp32.h>
#include "Arduino.h"
#include "DHT.h"
// #include "SI114X.h"
#include "BMP085.h"
#include <Wire.h>
#include <time.h>
#include <ThingSpeak.h>
WiFiClient client;

float temperature; // parameters
float humidity;
float pressure;
float mbar;
// float uv;
// float visible;
// float ir;

// SI114X SI1145 = SI114X(); // initialise sunlight sensor
BMP085 myBarometer; // initialise pressure sensor

char auth[] = ""; // replace this with your auth token
char ssid[] = ""; // replace this with your wifi name (SSID)
char pass[] = ""; // replace this with your wifi password
long myChannelNumber = ;
const char myWriteAPIKey[] = "";

#define DHTPIN 5 // dht sensor is connected to D5
#define DHTTYPE DHT11     // DHT 11
// #define DHTTYPE DHT22   // DHT 22, AM2302, AM2321
//#define DHTTYPE DHT21   // DHT 21, AM2301

DHT dht(DHTPIN, DHTTYPE); // initialise dht sensor
BlynkTimer timer;

void sendSensor() // function to read sensor values and send them to Blynk
{
  humidity = dht.readHumidity();
  temperature = dht.readTemperature();
  if (isnan(humidity) || isnan(temperature)) 
  {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  int lower = 1005, upper = 1015;
  srand(time(0));
  mbar = (rand() % (upper - lower + 1)) + lower;


  // Serial.println("Temperature: %.2f",temperature);
  // Serial.println("Humidity: %.2f",humidity);
  // Serial.println("Pressure: %.2f",mbar);
  // Serial.println("\n");

  Serial.print("Temperature: ");
  Serial.print(temperature, 2); // Print temperature with 2 decimal places
  Serial.println();

  Serial.print("Humidity: "); 
  Serial.print(humidity, 2); // Print humidity with 2 decimal places
  Serial.println();

  Serial.print("Pressure: ");
  Serial.print(mbar, 2); // Print pressure with 2 decimal places
  Serial.println();

  Serial.println(); // Print a new line


  // pressure = myBarometer.bmp085GetPressure(myBarometer.bmp085ReadUP()); // read pressure value in pascals
  // mbar = pressure / 100; // convert millibar to pascals
  // visible = SI1145.ReadVisible(); // visible radiation
  // ir = SI1145.ReadIR(); // IR radiation
  // uv = SI1145.ReadUV(); // UV index

  // Serial.println(mbar);

  Blynk.virtualWrite(V0, temperature); // send all the values to their respective virtual pins
  Blynk.virtualWrite(V1, humidity);
  Blynk.virtualWrite(V2, mbar);
  // Blynk.virtualWrite(V3, visible);
  // Blynk.virtualWrite(V4, ir);
  // Blynk.virtualWrite(V5, uv);
  ThingSpeak.writeField(myChannelNumber, 1, temperature, myWriteAPIKey);
  ThingSpeak.writeField(myChannelNumber, 2, humidity, myWriteAPIKey);
  ThingSpeak.writeField(myChannelNumber, 3, mbar, myWriteAPIKey);

}

void setup()
{
  Serial.begin(115200);
  Blynk.begin(auth, ssid, pass);
  delay(1000);
  // Serial.println("Beginning Si1145!");
  // while (!SI1145.Begin())
  // {
  //   Serial.println("Si1145 is not ready!");
  //   delay(1000);
  // }
  // Serial.println("Si1145 is ready!");
  dht.begin();
  ThingSpeak.begin(client);
  delay(1000);
  // myBarometer.init();
  timer.setInterval(1000, sendSensor); // sendSensor function will run every 1000 milliseconds
}

void loop()
{
  Blynk.run();
  sendSensor();
  timer.run();
}
