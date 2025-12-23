# V1
## Issues
* Holes disappeared from SSS slide pwr switch footprint for some reason
* Silk On(|) and Off(O) are backwards
* Buttons not actually connected to pins
* SW1 stopped working on one unit for 5mins, then started working again. Power wouldnt turn off.
* R28 silk in wrong spot
* DS1307Z+ needs 5v not 3.3V oof, need to desolder, remove pin, flush cut or tape, then wire over 5v0, i2c Vih is fine at 3v3
* D1 D4 too bright
* Soldering an OLED sucks, should use FFC Connector in the future
* Needs a schematic note that ext switch only works when PCB switch if off or not GND, this could be better
* Ext conns like the LDR should have a second fuse just in case
* Silk on WS2812B-2020 got cut in fab for some reason, never got to test this part, fet may be to slow after simulation.
* Add extended property or basic to BOM jlc_status
* Adjust silk on CR2032 holder +/- 
* put rtc address on schematic 110 1000 R/W 0x68
* Make oled addr 0x3C clearer 011 1100 R/W 0x3C
* RTC built was DS1302 not DS1307Z , select a cheap non 5V part

## Add
* Red PBAD LED
* LDR THT Holes
* different logic level shifter and RGBW LED?

Extended Parts
Fix these
U2 SRV05-4-P-T7 ESD Diode, bom = 0 this one
R31 20 ohms?
Select new 0603 leds that are basic, run them off 5v for good green

Unselected Parts because I had them?
D2 Zener and D5 WS2812B-2020

Consider
SW1 SSSS811101
U3 RT9080-33GJ5
DS1307 RTC and Y2 and CR2032 holder
J4 5 6, SM02B-SRSS-TB(LF)(SN)


Need
USBC
RP2040
J3 FFC and 1.25 expensive 

#V2 notes
look at impedance control for free?
Make mtg holes plated?
Make 

Gerber Review
Verify holes on SSSS811101
Silk on 