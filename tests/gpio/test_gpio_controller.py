from unittest.mock import Mock, patch
from src.gpio.gpio_controller import GPIOController

class TestGPIOController:
  """
  TestGPIOController class for testing the GPIOController functionality.
  This test suite validates the behavior of the GPIOController class which is responsible
  for controlling GPIO (General Purpose Input/Output) pins on a device, typically used 
  for controlling components like LEDs or buzzers.
  The tests verify:
  - Proper initialization with default and custom values
  - Handling of missing GPIO implementation
  - Turning components on and off
  - Toggling component states
  - Proper cleanup in destructor
  """
  def setup_method(self):
    self.mock_gpio = Mock()
    
  def test_init(self):
    """
    Test the initialization of GPIOController with default values.
    """
    controller = GPIOController(gpio=self.mock_gpio)
    assert controller.pin == 18
    assert controller.component_type == "LED"
    assert controller.gpio == self.mock_gpio
    # Verify that GPIO setup is called correctly
    self.mock_gpio.setmode.assert_called_once_with(self.mock_gpio.BCM)
    self.mock_gpio.setup.assert_called_once_with(18, self.mock_gpio.OUT)
    
  def test_init_custom_values(self):
    """
    Test the initialization of GPIOController with custom pin and component type.
    """
    controller = GPIOController(gpio=self.mock_gpio, pin=22, component_type="BUZZER")
    assert controller.pin == 22
    assert controller.component_type == "BUZZER"
    self.mock_gpio.setmode.assert_called_once_with(self.mock_gpio.BCM)
    self.mock_gpio.setup.assert_called_once_with(22, self.mock_gpio.OUT)
  
  def test_init_no_gpio(self):
    """
    Test the initialization of GPIOController with no GPIO implementation.
    This simulates a scenario where GPIO is not available, such as in a unit test environment
    """
    controller = GPIOController(gpio=None)
    assert controller.pin == 18
    assert controller.component_type == "LED"
    assert controller.gpio is None
  
  def test_turn_on(self):
    """
    Test the turn_on method of GPIOController.
    This method should set the GPIO pin to HIGH, indicating that the component is turned on.
    """
    controller = GPIOController(gpio=self.mock_gpio)
    controller.turn_on()
    self.mock_gpio.output.assert_called_once_with(18, self.mock_gpio.HIGH)
  
  def test_turn_off(self):
    """
    Test the turn_off method of GPIOController.
    This method should set the GPIO pin to LOW, indicating that the component is turned off.
    """
    controller = GPIOController(gpio=self.mock_gpio)
    controller.turn_off()
    self.mock_gpio.output.assert_called_once_with(18, self.mock_gpio.LOW)
  
  def test_toggle_on_to_off(self):
    """
    Test the toggle method of GPIOController when the component is currently ON.
    This method should turn the component OFF by setting the GPIO pin to LOW.
    """
    self.mock_gpio.input.return_value = True
    controller = GPIOController(gpio=self.mock_gpio)
    controller.toggle()
    self.mock_gpio.input.assert_called_once_with(18)
    self.mock_gpio.output.assert_called_once_with(18, False)
  
  def test_toggle_off_to_on(self):
    """
    Test the toggle method of GPIOController when the component is currently OFF.
    This method should turn the component ON by setting the GPIO pin to HIGH.
    """
    self.mock_gpio.input.return_value = False
    controller = GPIOController(gpio=self.mock_gpio)
    controller.toggle()
    self.mock_gpio.input.assert_called_once_with(18)
    self.mock_gpio.output.assert_called_once_with(18, True)
  
  def test_no_gpio_methods(self):
    """
    Test the GPIOController methods when no GPIO implementation is provided.
    The calls to turn_on, turn_off, and toggle should not raise any exceptions
    """
    controller = GPIOController(gpio=None)
    controller.turn_on()  # Should not raise any exception
    controller.turn_off()  # Should not raise any exception
    controller.toggle()  # Should not raise any exception
  
  def test_del(self):
    """
    Test the __del__ method of GPIOController.
    This method should clean up the GPIO settings when the controller is deleted.
    """
    controller = GPIOController(gpio=self.mock_gpio)
    
    # Reset mock to clear previous setup calls
    self.mock_gpio.reset_mock()
    
    # Call __del__ explicitly (normally Python would do this)
    controller.__del__()
    
    self.mock_gpio.setmode.assert_called_once_with(self.mock_gpio.BCM)
    self.mock_gpio.setup.assert_called_once_with(18, self.mock_gpio.OUT)
    self.mock_gpio.output.assert_called_once_with(18, self.mock_gpio.LOW)