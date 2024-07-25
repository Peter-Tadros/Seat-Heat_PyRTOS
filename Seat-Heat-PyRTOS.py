#Participants: Alheshan Odai / Cherfi Sara / Louiz Botros Tadros Peter George / Souidi Chahrezed / Tahri Mohammed
import pyb
import time

from lab.car import Car
import pyRTOS

car_occupied=128
Button_Pressed=129
Button_unPressed=130

def seat(self)
{
    car = Car()

    p_led_green = pyb.Pin('PG13', pyb.Pin.OUT)
    p_led_red = pyb.Pin('PG14', pyb.Pin.OUT)
    Heat_Stage_Counter = 0
    p_led_red.low()
    p_led_green.low()
    yield


    while True:
        if car.is_seat_occupied():
            self.send(pyRTOS.Message(car_occupied, self, "task2"))
            yield[wait_for_message(self)]
            msgs=self.recv()
            for msg in msgs:
                if msg.type == Button_Pressed:
                    car.set_heating_coil_temperature_stage(car.TEMP_HIGH)
                    p_led_red.high()
                    p_led_green.high()
                    Heat_Stage_Counter = 1
                    yield[pyRTOS.timeout(0.5)]
                elif Heat_Stage_Counter == 1:
                    car.set_heating_coil_temperature_stage(car.TEMP_MEDIUM)
                    p_led_red.high()
                    p_led_green.low()
                    Heat_Stage_Counter = 2
                    yield[pyRTOS.timeout(0.5)]
                elif Heat_Stage_Counter == 2:
                    car.set_heating_coil_temperature_stage(car.TEMP_LOW)
                    p_led_red.low()
                    p_led_green.high()
                    Heat_Stage_Counter = 3
                    yield[pyRTOS.timeout(0.5)]
                elif Heat_Stage_Counter == 3:
                    car.set_heating_coil_temperature_stage(car.TEMP_OFF)
                    p_led_red.low()
                    p_led_green.low()
                    Heat_Stage_Counter = 0
                    yield[pyRTOS.timeout(0.5)]
            yield[pyRTOS.timeout(0.5)] 
        yield[pyRTOS.timeout(0.5)]  


}
def button(self)
{
    b_user = pyb.Pin('PA0', pyb.Pin.IN)
    yield()
    while True:
        ButtonPressed = b_user.value()
        yield[pyRTOS.timeout(0.1)]
        if ButtonPressed:
            msgs=self.recv()
            for msg in msgs:
                if msg.type== car_occupied:
                    self.send[pyRTOS.Message(Button_Pressed, self, msg.source)]
            yield[pyRTOS.timeout(0.5)]
        yield[pyRTOS.timeout(0.5)]
}

seat_task=pyRTOS.Task(seat,priority=0,name="task1",mailbox=True)
button_task=pyRTOS.Task(button,priority=1,name="task2",mailbox=True)
pyRTOS.add_task(seat_task)
pyRTOS.add_task(button_task)


pyRTOS.start()
# How to use
# ----------
# List files on the board (replace PORT with your connection string, e.g., COM4):
#   mpr -d COM5 ls :
# Copy this script to the board and run it interactively:
#   mpr -d COM5 put -f ex_seat_heating.py ex_seat_heating.py
#   mpr -d COM5 repl
#   >>> import ex_seat_heating
#   >>> ex_seat_heating.main()
# Install this script as main program to be run automatically on boot:
#   mpr -d COM5 put -f ex_seat_heating.py main.py
# Remove main program:
#   mpr -d COM5 rm main.py
