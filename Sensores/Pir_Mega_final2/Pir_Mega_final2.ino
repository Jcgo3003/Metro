/* Solo modificar la direccion de envio y colocar de nuevo el delay de 30 segundos*/
#include <Ethernet.h>
#include <SPI.h>

// Confingurando mac e IP
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ip(192, 168, 100, 50);

// name address for Google (using DNS)
char server[] = "ide50-jbst2000.cs50.io";  ////  MODIFICAR JUSTO AQUI!!! 

// Inicia Ethernet client
EthernetClient client;

// Pir
#define pir1 7  
#define pir2 8

// Const. para el pir      
int lectura1 = 0;  
int lectura2 = 0;  

// Estados para los pir
int est_pir1 = LOW;  
int est_pir2 = LOW;  

// =============== conectando a Internet =============== //

void setup() {
  // Tiempo de que se calibren los pir
//  delay(30000);

  pinMode(pir1, INPUT);
  pinMode(pir2, INPUT);
  
  // wait for serial port to connect. Needed for native USB port only
  Serial.begin(9600);
  while (!Serial) {
    ; 
  }

  // Conetando a internet:
  if (Ethernet.begin (mac) == 0) {
   Serial.println("No se puedo configurar via DHCP");
    // try to congifure using IP address instead of DHCP:
    Ethernet.begin(mac, ip);
    Serial.println(" Conectando con IP Fija ");
  }
  
//  Ethernet.begin(mac, ip);
//    Serial.println(" Conectando con IP Fija");


  // give the Ethernet shield a second to initialize:
  Serial.print ("Conectando con IP ");
  Serial.println(Ethernet.localIP());

}

////////////// Enviando Post request /////////////

void loop() {

  lectura1 = digitalRead(pir1);
  lectura2 = digitalRead(pir2);

  if (lectura1 == HIGH)   
   { 
      // Mandando HTTP resquest
      if (est_pir1 == LOW)  
      {
        Serial.println("Sensor activado PIR A");
        est_pir1 = HIGH;
        if (client.connect(server, 80)) { 
          client.println("POST /nes HTTP/1.0");                ////  --------------
          client.println("Host: ide50-jbst2000.cs50.io"); // SERVER ADDRESS HERE TOO
          client.println("User-Agent: Arduino/1.0");
          client.println("Connection: close");
          client.println("Content-Length: 0");        
          client.println("Content-Type: application/x-www-form-urlencoded"); 
          client.println("num: 1");
          client.println("direccion: a");
          client.println("sen_n: sen1_a");
          client.println(""); 
          
          if (client.available()) {
            Serial.print("Respuesta del servidor");
            char c = client.read();
            Serial.print(c);
          }
          
          if (client.connected()) { 
            Serial.println("Desconectando del servidor");
            client.stop();  // DISCONNECT FROM THE SERVER
          }
          
        } 
        else {
          // if you didn't get a connection to the server:
          Serial.println("No se establecion conexion con el servidor");
        }
      
      }
   }
  else   // Desactivando el ciclo de envio
   {
      if ( est_pir1 == HIGH ) 
      {
        est_pir1 = LOW;
      }
   }

  if (lectura2 == HIGH)   
   { 
      // Mandando HTTP resquest
      if (est_pir2 == LOW)  
      {
        Serial.println("Sensor activado PIR B");
        est_pir2 = HIGH;

       if (client.connect(server, 80)) { 
          client.println("POST /nes HTTP/1.0");                ////  --------------
          client.println("Host: ide50-jbst2000.cs50.io"); // SERVER ADDRESS HERE TOO
          client.println("User-Agent: Arduino/1.0");
          client.println("Connection: close");
          client.println("Content-Length: 0");         
          client.println("Content-Type: application/x-www-form-urlencoded"); 
          client.println("num: 1");
          client.println("direccion: b");
          client.println("sen_n: sen1_b");
          client.println(""); 
          
          Serial.println("enviando POST");

          // if there are incoming bytes available
          // from the server, read them and print them:
          if (client.available()) {
            Serial.print("Respuesta del servidor");
            char c = client.read();
            Serial.print(c);
         }
          
          if (client.connected()) { 
          Serial.println("Desconectando del servidor");
          client.stop();  // DISCONNECT FROM THE SERVER
         }
         
        } 
        else {
          // if you didn't get a connection to the server:
          Serial.println("No se establecion conexion con el servidor");
        }
      
      }
   }
   else   // Desactivando el ciclo de envio
   {
      if ( est_pir2 == HIGH ) 
      {
        est_pir2 = LOW;
      }
   }
  
}
