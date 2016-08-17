// TMS Hyperloop display
// increase of 2 x 2  pos XY5 counter as a result of passing a car
// 
// Arduino Due
// rs485 brakout 
// connections:
// Breakout - Arduino
// GND  -   GND 
// RTS  -   3V3
//TX-O  -   not connected
//RX-I  -   TX (pin 1 digital)
//3-5V  -   5V
// radar switch#1
// between  pin 3 and GND
// radar switch@2
// between pin4 and GND
//
// deboucing of a trigger button every  5s
// dipswitches settings of the lsb controller
// 3 positions: speed of communication:
//
// 0:1200
// 1:2400
// 2:4800
// 3:9600 <--- this should be set, means 1-ON 2-ON 3-OFF
// 4:19200 
// 5:38200 <-- do not use, most probably wrong speed programmed
// 6: 9600
// 7: 9600
// 8: 9600
//
// 5 positions: order.
// digit 1: 1
// digit 2: 2
// digit 3: 3
// ... etc digit 9: 9

// switch#1 is shown on digit 1 and 2 / switch #2 is shown on digit 3 and 4




// pin 2 digital connected through 10kohm res to 5V and through a radar to GND - Interrupt 0 is on DIGITAL PIN 2!
// pin 3 digitial connected though 10 kohm res to 5V and through a radar to GND - Interr 1 is on digital pin 3


// 0x80 beginning 
//___________________
// 0x81 - 112 bytes / no refresh / C+3E
// 0x82 - refresh
// 0x83 - 28 bytes of data / refresh / 2C
// 0x84 - 28 bytes of data / no refresh / 2C
// 0x85 - 56 bytes of data / refresh / C+E
// 0x86 - 56 bytes of data / no refresh / C+E
// ---------------------------------------
// address or 0xFF for all
// data ... 1 to nuber of data buytes
// 0x8F end




volatile int state = LOW;      // The input state toggle
 


byte numbers[]={
   62,   65,  65,  62,  0, //0
    0,   66,  127, 64,  0, //1
   98,   81,  73,  70,  0, //2
   34,   65,  73,  54,  0, //3
   56,   36,  34, 127, 32, //4
   79,   73,  73,  49,  0, //5
   62,   73,  73,  50,  0, //6
    3,    1,   1, 127,  0, //7
   54,   73,  73,  54,  0, //8
   38,   73,  73,  62,  0, //9
   24,  126, 126,  24,  0, // +
   24,   24,  24,  24,  0 //-
};


byte transmission[]= {
  0x80, //header
  0x83, // 28 bytes, refresh
  0x00, //adres
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  // 28 data
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x8F}; //EOT







byte all_bright[]={
  0x80,  //header
  0x83,  // 28 bytes refresh
  0xFF, // adres
  0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, //data
  0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F,
  0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F,
  0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 
   0x8F}; // EOT


byte all_dark[]={
  0x80,  //header
  0x83,  // 28 bytes refresh
  0xFF, // adres
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, //data
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
   0x8F}; // EOT



 
int pin1 = 2;
int pin2 = 3;

volatile unsigned long int counter1 = 0x00; 
volatile unsigned long int counter2 = 0x00; 

int n;
long int x=111111111;         
         


void show_number(byte panel_adres, int number_to_show)
{

int cyfra1=0;
int cyfra2=0;

cyfra1=number_to_show/10;
cyfra2=number_to_show-(cyfra1*10);


transmission[2]=panel_adres;
for (int t=0;t<5;t++)  transmission[10+3+t]= numbers[(cyfra1*5)+t];
for (int t=0;t<5;t++)  transmission[15+3+t]= numbers[(cyfra2*5)+t];


for (int t=0;t<5;t++)  transmission[3+t]= numbers[((9+panel_adres)*5)+t]; // +

Serial.write(transmission,32);


  
}    






void my_interrupt_handler1()
{
  static unsigned long last_interrupt_time = 0;
  unsigned long interrupt_time = millis();
  // If interrupts come faster than 100ms, assume it's a bounce and ignore
 if (interrupt_time - last_interrupt_time > 500) 
  {
   counter1++;
if (counter1>99) counter1=0;  // Question: what if counter is above 99 it changes to 0;
                                   // what if power is off?

//Serial.println("Przerwanie!");

//Serial.println(counter);
show_number(1,counter1);
 
    
  }
  last_interrupt_time = interrupt_time;
}



void my_interrupt_handler2()
{
  static unsigned long last_interrupt_time = 0;
  unsigned long interrupt_time = millis();
  // If interrupts come faster than 100ms, assume it's a bounce and ignore
 if (interrupt_time - last_interrupt_time > 500) 
  {
   counter2=counter2+1;
if (counter2>99) counter2=0;  // Question: what if counter is above 999999999 it changes to 0;
                                   // what if power is off?

//Serial.println("Przerwanie!2");

//Serial.println(counter);


show_number(2,counter2);

  
  }
  last_interrupt_time = interrupt_time;
}



                  
                  
void setup() {

Serial.begin(57600);  

Serial.write(all_bright,32); 
delay (250);
Serial.write(all_dark,32); 
delay (250);

attachInterrupt(0, my_interrupt_handler1, LOW);
attachInterrupt(1, my_interrupt_handler2, LOW);

show_number(1,counter1);
show_number(2,counter2);

}





void loop()                     
{
  //Simulate a long running process or complex task
  for (int i = 0; i < 100; i++)
  {
    // do nothing but waste some time
//    send_number(i); // or send some numbers over rs485
    delay(10); 
  }
}








