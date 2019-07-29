int accel_vals[15] = {};
int i = 0;
long start_time = millis();
int pulseX;
int accelerationX;
int highest;
int second_highest;
int lowest;
int second_lowest;
int highest_index=0;
int second_highest_index=0;
int lowest_index=0;
int second_lowest_index=0;
long peak_time;
int threshold = 3000;
int avg_high = 0;
int peak_time_1;
int peak_time_2;
int peak_time_3;
int peak_num = 0;

void setup() {
  // initialize serial communications:
  Serial.begin(9600);
  Serial.println("Program Started");
  pinMode(4,OUTPUT);
  pinMode(7, INPUT);
  digitalWrite(4,HIGH);
}

void loop() {
  //collect data every 20 millis, 50 readings per second
  if (millis()-start_time >=20){
    start_time = millis();
    pulseX = pulseIn(7, HIGH);
    accelerationX = ((((pulseX / 10) - 500) * 8)+1024);
    accel_vals[14] = accelerationX;

    //running list of most recent 50 data points (1 seconds worth)
    //also calculates best and second best values
    for(int k=0; k<14;k++){
      accel_vals[k]=accel_vals[k+1];
      if (k==0){
        highest = max(accel_vals[0],accel_vals[1]);
        second_highest = min(accel_vals[0],accel_vals[1]);
        lowest = second_highest;
        second_lowest = highest;
      }
      else{
        if (accel_vals[k] > highest){
          second_highest = highest;
          second_highest_index = highest_index;
          highest = accel_vals[k];
          highest_index = k;
        }
        if (accel_vals[k] < lowest){
          second_lowest = lowest;
          second_lowest_index = lowest_index;
          lowest = accel_vals[k];
          lowest_index = k;
        }
      }
      avg_high = (highest+second_highest/2);
    }

    if (5 < highest_index && highest_index < 8){
      if (5 < lowest_index && lowest_index < 8){
        if (highest > second_highest*1.5){
          if (lowest < second_lowest*1.5){
            if (avg_high > 200){
            
            Serial.println("singular peak");
            Serial.println("Data:");
            Serial.println(highest);
            Serial.println(highest_index);
            Serial.println(second_highest);
            Serial.println(second_highest_index);
            Serial.println(second_lowest);
            Serial.println(second_lowest_index);
            Serial.println(lowest);
            Serial.println(lowest_index);
            
            //FIX THE FACT THAT IT ITERATES THROUGH ALL 3
            if (peak_num==0){
              peak_time_1 = millis();
              peak_num=1;
              Serial.println("peak 1");
              }
            else if (peak_num ==1){
              peak_time_2 = millis();
              peak_num = 2;
              Serial.println("peak 2");
              }
            else if (peak_num==2){
              peak_time_3 = millis();
              Serial.println("peak 3");
              Serial.println(peak_time_2-peak_time_1);
              Serial.println(peak_time_3 - peak_time_2);
              if (200 < (peak_time_2-peak_time_1)&&(peak_time_2-peak_time_1) < 4000){
                if (200 < (peak_time_3 - peak_time_2)&& (peak_time_3 - peak_time_2) < 4000){
                  Serial.println("sidewalk");
                  digitalWrite(4,LOW);
                  delay(5000);
                  digitalWrite(4,HIGH);
                }
              }
              peak_num = 0;
            }
          }
        }
      }
    }
    }

    

    
    
    /*
    if(accel_vals[25] > second*3){
      Serial.println("PEAK PEAK PEAK");
      Serial.println(millis()-peak_time);
      Serial.println(best);
      Serial.println(second);
      if (millis()-peak_time < threshold){
        Serial.println("Peak Threshold Met");
        digitalWrite(4,LOW);
        Serial.println("HIGH");
        delay(5000);
        digitalWrite(4,HIGH);
        Serial.println("LOW");
        for(int k = 0; k<50;k++){
          accel_vals[k]=2000;
        }
      }
      peak_time = millis();


      
    }
    */
  }
}
