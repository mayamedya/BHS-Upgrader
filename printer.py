import usb.core
import usb.util

class PrinterKP300V:
    def __init__(self):
        #self.VENDOR_ID = 0x0fe6
        #self.PRODUCT_ID = 0x811e
        
        self.VENDOR_ID = 0x0fe6
        self.PRODUCT_ID = 0x811e

    def translate_status_code(self, code):

        status_codes = {
            -1: "Device not found or error during communication.",
            30: "Kağıt Bitmek Üzere",
            18: "İyi Durumda",
            126: "Kağıt Yok",
            114: "Rulo Var Kağıt Yok",
        }
        return status_codes.get(code, f"Unknown status code: {code}")

    def printer_kp300v(self):
        try:
            dev = usb.core.find(idVendor=self.VENDOR_ID, idProduct=self.PRODUCT_ID)

            if not dev:
                return self.translate_status_code(-1)

            dev.reset()

            if dev.is_kernel_driver_active(0):
                dev.detach_kernel_driver(0)

            dev.set_configuration()

            EP_OUT = 0x03
            EP_IN = 0x81

            #data = [0x1B, 0x76]  # Replace with specific commands from your printer's documentation
            data = [0x10, 0x04, 0x04]
            dev.write(EP_OUT, data)

            response = dev.read(EP_IN, 8, timeout=20000)
            res_code = response[0]
            
            if res_code & 0b00110000 == 0b00100000:  # Bits 5–6 == 01
                print("Error: Paper end.")
            elif res_code & 0b00001100 == 0b00000100:  # Bits 2–3 == 01
                print("Warning: Paper near-end.")
            else:
                print("Printer is ready with sufficient paper.")

            # Log and return the translated status
            print(response)
            print(f"Raw Response: {response}")
            print(f"Result Code: {res_code}")
            return self.translate_status_code(res_code)

        except usb.core.USBError as usb_err:
            print(f"[KP300V USB Error] {usb_err}")
            return self.translate_status_code(-1)
        except Exception as e:
            print(f"[KP300V General Error] {e}")
            return self.translate_status_code(-1)

# Create an instance of the PrinterKP300V class and test
if __name__ == "__main__":
    printer = PrinterKP300V()
    status_message = printer.printer_kp300v()
    print(f"Printer Status: {status_message}")

'''
import usb.core
import usb.util

class PrinterKP300V:
    def __init__(self):
        #self.VENDOR_ID = 0x0fe6
        #self.PRODUCT_ID = 0x811e
        
        self.VENDOR_ID = 0x0fe6
        self.PRODUCT_ID = 0x811e

    def translate_status_code(self, code):

        status_codes = {
            -1: "Device not found or error during communication.",
            30: "kağıt bitmek üzere",
            18: "iyi durumda",
            126: "yazıcı ağzında kağıt yok.",
            114: "yazıcıda rulo var ağzında kağıt yok.",
            4: "Paper near end.",
        }
        return status_codes.get(code, f"Unknown status code: {code}")

    def printer_kp300v(self):
        try:
            dev = usb.core.find(idVendor=self.VENDOR_ID, idProduct=self.PRODUCT_ID)

            if not dev:
                return self.translate_status_code(-1)

            dev.reset()

            if dev.is_kernel_driver_active(0):
                dev.detach_kernel_driver(0)

            dev.set_configuration()

            EP_OUT = 0x03
            EP_IN = 0x81

            #data = [0x1B, 0x76]  # Replace with specific commands from your printer's documentation
            data = [0x10, 0x04, 0x04]
            dev.write(EP_OUT, data)

            response = dev.read(EP_IN, 8, timeout=20000)
            res_code = response[0]
            
            if res_code & 0b00110000 == 0b00100000:  # Bits 5–6 == 01
                print("Error: Paper end.")
            elif res_code & 0b00001100 == 0b00000100:  # Bits 2–3 == 01
                print("Warning: Paper near-end.")
            else:
                print("Printer is ready with sufficient paper.")

            # Log and return the translated status
            print(response)
            print(f"Raw Response: {response}")
            print(f"Result Code: {res_code}")
            return self.translate_status_code(res_code)

        except usb.core.USBError as usb_err:
            print(f"[KP300V USB Error] {usb_err}")
            return self.translate_status_code(-1)
        except Exception as e:
            print(f"[KP300V General Error] {e}")
            return self.translate_status_code(-1)

# Create an instance of the PrinterKP300V class and test
if __name__ == "__main__":
    printer = PrinterKP300V()
    status_message = printer.printer_kp300v()
    print(f"Printer Status: {status_message}")'''
