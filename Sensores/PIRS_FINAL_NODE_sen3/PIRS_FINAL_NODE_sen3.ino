// Modificar informacion de conexion a internet
// Modificar el servidor al que se enviaran los datos
// Modificar la informacion que se enviara al servidor
// SENSOR 3 
//=======================================================================
//                    Resquest sender 
//=======================================================================
// Librerias
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

// Configuracion WIFI 
const char* ssid = "mezczyzna";            /// JUSTO AQUI MODIFICAR
const char* password = "12345678";

// Direccion a donde van los post request
const char *host = "http://ide50-jbst2000.cs50.io:8080/nes"; /// JUSTO AQUI MODIFICAR

// Pir
#define pir1 D0  
#define pir2 D3  

// Const. para el pir      
int lectura1 = 0;  
int lectura2 = 0;  

// Estados para los pir
int est_pir1 = LOW;  
int est_pir2 = LOW;       

//=======================================================================
//                    Wifi and Pir
//=======================================================================

void setup() {

  // No empiece inmediatamente
  delay(1000);
  
  // Lectura pir 
  pinMode(pir1, INPUT);
  pinMode(pir2, INPUT);
  
  // Imprimiendo a serial
  Serial.begin(115200);
  Serial.print("Conectando a ");
  Serial.println(ssid);
  
  // Conectando
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(" . ");
  }

  // Imprimir que ya esta conectado
  Serial.println("");
  Serial.println("WiFi connected… Oh yeah!");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

//=======================================================================
//                    HTTP request.
//=======================================================================
void loop()
{
   lectura1 = digitalRead(pir1);
   lectura2 = digitalRead(pir2);
   
   // Cuando el Pir A es activado
   if (lectura1 == HIGH)   
   { 
      // Mandando HTTP resquest
      if (est_pir1 == LOW)  
      {
        Serial.println("Sensor activado A ");
        est_pir1 = HIGH;
        
        // Declarando http como HTTPClient
        HTTPClient http;    
        
        // Destino     
        http.begin(host);              
        http.addHeader("Content-Type", "None");  
        
        // headers con la informacion - JUSTO AQUI TAMBIEN MODIFICAR !!!
        http.addHeader("NODECMU", "3");
        http.addHeader("num", "3");
        http.addHeader("direccion", "a");
        http.addHeader("sen_n", "sen3_a");

        // JUSTO AQUI TAMBIEN MODIFICAR !!!
        int httpCode = http.POST("Sensor 3 A");
        //Serial.print("  Request response = ");
        //Serial.print(httpCode);   //Print HTTP return code

        http.end();  //Close connection

      }
   } 
   else   // Desactivando el ciclo de envio
   {
      
      if ( est_pir1 == HIGH ) 
      {
        //Serial.println("  Http resquest enviado  ");
        est_pir1 = LOW;
      }
   }

// Cuando el Pir 2 es activado
   if (lectura2 == HIGH)   
   { 
      // Mandando HTTP resquest
      if (est_pir2 == LOW)  
      {
        Serial.println("Sensor activado B ");
        est_pir2 = HIGH;
        
        // Declarando http como HTTPClient
        HTTPClient http;    
        
        // Destino     
        http.begin(host);              
        http.addHeader("Content-Type", "None");  
        
        // headers con la informacion - a modificar segun el sensor
        http.addHeader("NODECMU", "3");
        http.addHeader("num", "3");
        http.addHeader("direccion", "b");
        http.addHeader("sen_n", "sen3_b");

        // Igual esto a modificar segun el sensor
        int httpCode = http.POST("Sensor 3 B");
        //Serial.print("Request response =  ");
        //Serial.print(httpCode);   //Print HTTP return code

        http.end();  //Close connection

      }
   } 
   else   // Desactivando el ciclo de envio
   {
      
      if ( est_pir2 == HIGH ) 
      {
        //Serial.println("Http resquest enviado");
        est_pir2 = LOW;
      }
   }
}
//=======================================================================
