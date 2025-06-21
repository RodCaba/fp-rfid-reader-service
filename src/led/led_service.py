class LedService:
  def __init__(self, gpio=None, pin=18):
    """
    Initializes the LedService with an optional GPIO controller.

    Args:
      gpio: An optional GPIO controller instance, used for Raspberry Pi.
      pin: The GPIO pin number to which the LED is connected (default is 18).
    """
    self.gpio = gpio
    self.pin = pin
    if self.gpio is not None:
      self.gpio.setmode(self.gpio.BCM)  # Set the GPIO mode to BCM
      self.gpio.setup(self.pin, self.gpio.OUT)

  def __del__(self):
    """
    Cleans up the GPIO settings when the LedService instance is deleted.

    This method is called when the LedService instance is about to be destroyed.
    It ensures that the GPIO pin is cleaned up properly to avoid resource leaks.
    """
    if self.gpio is not None:
      self.gpio.cleanup()  # Clean up GPIO settings
  
  def turn_on(self):
    """
    Turns on the LED by setting the GPIO pin to HIGH.

    This method is used to activate the LED connected to the specified GPIO pin.
    """
    if self.gpio is not None:
      self.gpio.output(self.pin, self.gpio.HIGH)

  def turn_off(self):
    """
    Turns off the LED by setting the GPIO pin to LOW.

    This method is used to deactivate the LED connected to the specified GPIO pin.
    """
    if self.gpio is not None:
      self.gpio.output(self.pin, self.gpio.LOW)