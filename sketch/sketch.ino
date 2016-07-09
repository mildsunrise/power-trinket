/**
 * Copyright (c) 2016 Alba Mendez
 * All rights reserved.
 * This file is part of power-trinket.
 *
 * power-trinket is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * power-trinket is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with power-trinket.  If not, see <http://gnu.org/licenses/>
 **/

#include <TinyWireM.h>
#include <TrinketFakeUsbSerial.h>
#include "_Adafruit_INA219.h"

#define SYNC_STRING "S              E"
#define SYNC_LENGTH (sizeof(SYNC_STRING)-1)
Adafruit_INA219 ina219;

void setup() {
  TFUSerial.begin();
  
  ina219.begin();
  // To use a slightly lower 32V, 1A range (higher precision on amps):
  //ina219.setCalibration_32V_1A();
  // Or to use a lower 16V, 400mA range (higher precision on volts and amps):
  //ina219.setCalibration_16V_400mA();
}

void loop() {
  float values [3];
  values[0] = ina219.getShuntVoltage_mV();
  values[1] = ina219.getBusVoltage_V();
  values[2] = ina219.getCurrent_mA();
  uint8_t buffer [SYNC_LENGTH + sizeof(values)];
  memcpy(buffer, SYNC_STRING, SYNC_LENGTH);
  memcpy(buffer + SYNC_LENGTH, values, sizeof(values));
  TFUSerial.write(buffer, sizeof(buffer));
}
