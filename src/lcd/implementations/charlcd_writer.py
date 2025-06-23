from ..base import Writer
from RPLCD.i2c import CharLCD

class CharLCDWriter(Writer):
    """
    Concrete implementation of the Writer interface for character LCD displays.
    """

    def __init__(
            self,
            i2c_expander="PCF8574",
            address=0x27,
            port=1,
            cols=16,
            rows=2,
            dotsize=8,
        ):
        super().__init__(
            i2c_expander=i2c_expander,
            address=address,
            port=port,
            cols=cols,
            rows=rows,
            dotsize=dotsize,
        )
        self.lcd = CharLCD(
            i2c_expander=i2c_expander,
            address=address,
            port=port,
            cols=cols,
            rows=rows,
            dotsize=dotsize,
        )

    def write(self, text: str):
        """
        Write text to the LCD display.

        Args:
            text (str): The text to display on the LCD.

        Raises:
            Exception: If there's an error writing to the display.
        """
        try:
            self.lcd.write_string(text)
        except Exception as e:
            raise Exception(f"Error writing to LCD: {e}")

    def clear(self):
        """
        Clear the LCD display.

        Raises:
            Exception: If there's an error clearing the display.
        """
        try:
            self.lcd.clear()
        except Exception as e:
            raise Exception(f"Error clearing LCD: {e}")