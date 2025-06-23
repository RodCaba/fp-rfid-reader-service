class GPIOController:
  def __init__(self, gpio=None, pin=18, component_type="LED"):
    """
    Initializes the GPIOController for handling various output components.

    Args:
      gpio: An optional GPIO controller instance, used for Raspberry Pi.
      pin: The GPIO pin number to which the component is connected (default is 18).
      component_type: Type of component connected (e.g., "LED", "BUZZER"). For logging/identification.
    """
    self.gpio = gpio
    self.pin = pin
    self.component_type = component_type
    if self.gpio is not None:
      self.gpio.setmode(self.gpio.BCM)  # Set the GPIO mode to BCM
      self.gpio.setup(self.pin, self.gpio.OUT)

  def __del__(self):
    """
    Cleans up the GPIO settings when the GPIOController instance is deleted.

    This method is called when the GPIOController instance is about to be destroyed.
    It ensures that the GPIO pin is cleaned up properly to avoid resource leaks.
    """
    if self.gpio is not None:
      self.turn_off()

  def turn_on(self):
    """
    Turns on the component by setting the GPIO pin to HIGH.

    This method activates the component connected to the specified GPIO pin.
    """
    if self.gpio is not None:
      self.gpio.output(self.pin, self.gpio.HIGH)

  def turn_off(self):
    """
    Turns off the component by setting the GPIO pin to LOW.

    This method deactivates the component connected to the specified GPIO pin.
    """
    if self.gpio is not None:
      self.gpio.output(self.pin, self.gpio.LOW)

  def toggle(self):
    """
    Toggles the state of the component (ON to OFF or OFF to ON).
    
    This method is useful for blinking or alternating states.
    """
    if self.gpio is not None:
      current_state = self.gpio.input(self.pin)
      self.gpio.output(self.pin, not current_state)