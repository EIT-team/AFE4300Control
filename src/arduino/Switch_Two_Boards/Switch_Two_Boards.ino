/*

Code to switch two daisy chained switch networks, but with two channels open per board - four in total

User enters the channel they want to connect to the sink pin (default 2) and source pin (def 4) for the first board, and then for the second board

CHANGE TERMINATOR TO NEWLINE IN SERIAL MONITOR


Jimmy 2014/2015

*/

//#include "BreadboardPins.h" // Pins for breadboard version - used by kirill and me (testing)
#include "PCBPins.h" // Pins for PCB version - these have been altered to more logical layout for PCB


int sinkpin_A = 2; // pin that the sink is connected to
int sourcepin_A = 4;

int sinkpin_A = 2; // pin that the sink is connected to
int sourcepin_A = 4;

int sinkpin_B = 2; // pin that the sink is connected to
int sourcepin_B = 4;

const int chnmax = 199; // maximum number of channels

int NumBoard = 2;
int TotalPins = 40 * NumBoard;



// this writes the digital pin faster for due - only 2 clock cycles!
//taken from http://forum.arduino.cc/index.php?topic=129868.15
inline void digitalWriteDirect(int pin, int val) {
	if (val) g_APinDescription[pin].pPort->PIO_SODR = g_APinDescription[pin].ulPin;
	else    g_APinDescription[pin].pPort->PIO_CODR = g_APinDescription[pin].ulPin;
}



void setup() {


	Serial.begin(115200);
	Serial.println("#############################");
	Serial.println("Hello There! This is a ScouseTom Switch Test");
	Serial.print("The number of boards in the daisy chain is : ");
	Serial.println(NumBoard);
	Serial.print("The source pin for board A is : ");
	Serial.println(sourcepin_A);
	Serial.print("The sink pin for board A is : ");
	Serial.println(sinkpin_A);
	Serial.print("The source pin for board B is : ");
	Serial.println(sourcepin_B);
	Serial.print("The sink pin for board B is : ");
	Serial.println(sinkpin_B);
	Serial.println("#############################");
	Serial.println("MAKE SURE YOU HAVE SET TERMINATOR TO NEWLINE :)");

	Serial.println("The switches will be powered on, source and sink pins opened, then turned off");
	Serial.println("This is repeated before allowing the user to select a pin");
	Serial.println("#############################");
	delay(1000);

	init_pins();

	Serial.println("Pins initialised, should ALL be closed now");
	delay(1000);


	Serial.println("on");
	SwitchesPwrOn();
	delay(100);
	programswitches(sourcepin_A, sinkpin_A,sourcepin_B,sinkpin_B, TotalPins);
	digitalWriteDirect(SYNC, HIGH); // switch dat!
	delay(500);
	Serial.println("off");
	SwitchesPwrOff();
	delay(500);
	Serial.println("on");
	SwitchesPwrOn();

	delay(100);
	programswitches(sourcepin_A, sinkpin_A,sourcepin_B,sinkpin_B, TotalPins);
	digitalWriteDirect(SYNC, HIGH); // switch dat!
	delay(500);
	Serial.println("off");
	SwitchesPwrOff();
	SwitchesPwrOn();
	Serial.println("#############################");
	Serial.println("waiting for input each time give ");
	Serial.println("i.e. 32 sets source to pin 32, 132 sets sink to 32");
	Serial.println("#############################");

}

void loop() {
	// put your main code here, to run repeatedly:

	while (Serial.available() > 0) {
		int c = Serial.parseInt();

		if (Serial.read() == '\n') {
			//Serial.println(c);

			if (c < chnmax)
			{
				sourcepin = c;
			}
			else
			{
				c = c - 200;
				if (c < chnmax)
				{
					sinkpin = c;
				}
				else
				{
					Serial.println("too high channel number");
				}
			}

			Serial.print("Setting switches to source chn: ");
			Serial.print(sourcepin);
			Serial.print(" sink chn: ");
			Serial.println(sinkpin);
			programswitches(sourcepin, sinkpin,TotalPins); //program dem switches
			digitalWriteDirect(SYNC, HIGH); // switch dat!


		}
	}



}
