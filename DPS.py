import smbus

from time import sleep





def getTwosComplement(raw_val, length):

        """Get two's complement of `raw_val`.



        Args:

            raw_val (int): Raw value

            length (int): Max bit length



        Returns:

            int: Two's complement

        """

        val = raw_val

        if raw_val & (1 << (length - 1)):

            val = raw_val - (1 << length)

        return val



  

class DPS:

    """Class of DPS, Pressure and Temperature sensor.

    """

    __bus = smbus.SMBus(1)

    __addr = 0x77



    # Compensation Scale Factors

    # Oversampling Rate          | Scale Factor (kP or kT)

    # ---------------------------|------------------------

    #   1       (single)         |  524288

    #   2 times (Low Power)      | 1572864

    #   4 times                  | 3670016

    #   8 times                  | 7864320

    #  16 times (Standard)       |  253952

    #  32 times                  |  516096

    #  64 times (High Precision) | 1040384  <- Configured

    # 128 times                  | 2088960

    __kP = 1040384

    __kT = 1040384





    def __init__(self):

        """Initial setting.



        Execute `self.correctTemperature()` and `self.setOversamplingRate()`.

        """

        self.__correctTemperature()

        self.__setOversamplingRate()





    def __correctTemperature(self):

        """Correct temperature.



        DPS sometimes indicates a temperature over 60 degree Celsius

        although room temperature is around 20-30 degree Celsius.

        Call this function to fix.

        """

        # Correct Temp

        DPS.__bus.write_byte_data(DPS.__addr, 0x0E, 0xA5)

        DPS.__bus.write_byte_data(DPS.__addr, 0x0F, 0x96)

        DPS.__bus.write_byte_data(DPS.__addr, 0x62, 0x02)

        DPS.__bus.write_byte_data(DPS.__addr, 0x0E, 0x00)

        DPS.__bus.write_byte_data(DPS.__addr, 0x0F, 0x00)





    def __setOversamplingRate(self):

        """Set oversampling rate.



        Pressure measurement rate    :  4 Hz

        Pressure oversampling rate   : 64 times

        Temperature measurement rate :  4 Hz

        Temperature oversampling rate: 64 times

        """

        # Oversampling Rate Setting (64time)

        DPS.__bus.write_byte_data(DPS.__addr, 0x06, 0x26)

        DPS.__bus.write_byte_data(DPS.__addr, 0x07, 0xA6)

        DPS.__bus.write_byte_data(DPS.__addr, 0x08, 0x07)

        # Oversampling Rate Configuration

        DPS.__bus.write_byte_data(DPS.__addr, 0x09, 0x0C)





    def __getRawPressure(self):

        """Get raw pressure from sensor.



        Returns:

            int: Raw pressure

        """

        p1 = DPS.__bus.read_byte_data(DPS.__addr, 0x00)

        p2 = DPS.__bus.read_byte_data(DPS.__addr, 0x01)

        p3 = DPS.__bus.read_byte_data(DPS.__addr, 0x02)



        p = (p1 << 16) | (p2 << 8) | p3

        p = getTwosComplement(p, 24)

        return p





    def __getRawTemperature(self):

        """Get raw temperature from sensor.



        Returns:

            int: Raw temperature

        """

        t1 = DPS.__bus.read_byte_data(DPS.__addr, 0x03)

        t2 = DPS.__bus.read_byte_data(DPS.__addr, 0x04)

        t3 = DPS.__bus.read_byte_data(DPS.__addr, 0x05)



        t = (t1 << 16) | (t2 << 8) | t3

        t = getTwosComplement(t, 24)

        return t





    def __getPressureCalibrationCoefficients(self):

        """Get pressure calibration coefficients from sensor.



        Returns:

            int: Pressure calibration coefficient (c00)

            int: Pressure calibration coefficient (c10)

            int: Pressure calibration coefficient (c20)

            int: Pressure calibration coefficient (c30)

            int: Pressure calibration coefficient (c01)

            int: Pressure calibration coefficient (c11)

            int: Pressure calibration coefficient (c21)

        """

        src13 = DPS.__bus.read_byte_data(DPS.__addr, 0x13)

        src14 = DPS.__bus.read_byte_data(DPS.__addr, 0x14)

        src15 = DPS.__bus.read_byte_data(DPS.__addr, 0x15)

        src16 = DPS.__bus.read_byte_data(DPS.__addr, 0x16)

        src17 = DPS.__bus.read_byte_data(DPS.__addr, 0x17)

        src18 = DPS.__bus.read_byte_data(DPS.__addr, 0x18)

        src19 = DPS.__bus.read_byte_data(DPS.__addr, 0x19)

        src1A = DPS.__bus.read_byte_data(DPS.__addr, 0x1A)

        src1B = DPS.__bus.read_byte_data(DPS.__addr, 0x1B)

        src1C = DPS.__bus.read_byte_data(DPS.__addr, 0x1C)

        src1D = DPS.__bus.read_byte_data(DPS.__addr, 0x1D)

        src1E = DPS.__bus.read_byte_data(DPS.__addr, 0x1E)

        src1F = DPS.__bus.read_byte_data(DPS.__addr, 0x1F)

        src20 = DPS.__bus.read_byte_data(DPS.__addr, 0x20)

        src21 = DPS.__bus.read_byte_data(DPS.__addr, 0x21)



        c00 = (src13 << 12) | (src14 << 4) | (src15 >> 4)

        c00 = getTwosComplement(c00, 20)



        c10 = ((src15 & 0x0F) << 16) | (src16 << 8) | src17

        c10 = getTwosComplement(c10, 20)



        c20 = (src1C << 8) | src1D

        c20 = getTwosComplement(c20, 16)



        c30 = (src20 << 8) | src21

        c30 = getTwosComplement(c30, 16)



        c01 = (src18 << 8) | src19

        c01 = getTwosComplement(c01, 16)



        c11 = (src1A << 8) | src1B

        c11 = getTwosComplement(c11, 16)



        c21 = (src1E < 8) | src1F

        c21 = getTwosComplement(c21, 16)



        return c00, c10, c20, c30, c01, c11, c21





    def __getTemperatureCalibrationCoefficients(self):

        """Get temperature calibration coefficients from sensor.



        Returns:

            int: Temperature calibration coefficient (c0)

            int: Temperature calibration coefficient (c1)

        """

        src10 = DPS.__bus.read_byte_data(DPS.__addr, 0x10)

        src11 = DPS.__bus.read_byte_data(DPS.__addr, 0x11)

        src12 = DPS.__bus.read_byte_data(DPS.__addr, 0x12)



        c0 = (src10 << 4) | (src11 >> 4)

        c0 = getTwosComplement(c0, 12)



        c1 = ((src11 & 0x0F) << 8) | src12

        c1 = getTwosComplement(c1, 12)



        return c0, c1





    def calcScaledPressure(self):

        """Calculate scaled pressure.



        Returns:

            float: Scaled pressure

        """

        raw_p = self.__getRawPressure()

        scaled_p = raw_p / DPS.__kP

        return scaled_p





    def calcScaledTemperature(self):

        """Calculate scaled temperature.



        Returns:

            float: Scaled temperature

        """

        raw_t = self.__getRawTemperature()

        scaled_t = raw_t / DPS.__kT

        return scaled_t





    def calcCompTemperature(self, scaled_t):

        """Calculate compensated temperature.



        Args:

            scaled_t (float): Scaled temperature



        Returns:

            float: Compensated temperature [C]

        """

        c0, c1 = self.__getTemperatureCalibrationCoefficients()

        comp_t = c0 * 0.5 + scaled_t * c1

        return comp_t





    def calcCompPressure(self, scaled_p, scaled_t):

        """Calculate compensated pressure.



        Args:

            scaled_p (float): Scaled pressure

            scaled_t (float): Scaled temperature

        Returns:

            float: Compensated pressure [Pa]

        """

        c00, c10, c20, c30, c01, c11, c21 = self.__getPressureCalibrationCoefficients()

        comp_p = (c00 + scaled_p * (c10 + scaled_p * (c20 + scaled_p * c30))

                + scaled_t * (c01 + scaled_p * (c11 + scaled_p * c21)))

        return comp_p
    
    
    
    def measureTemperatureOnce(self):
        
        
        """Measures compensated temperature once.



        Returns:

            float:One compensated temperature value [C]

        """
        
        t= self.calcScaledTemperature()

        temperature=self.calcCompTemperature(t)
            
        return temperature
        

    def measurePressureOnce(self):
        
        
        """Measure compensated pressure once.


        Returns:

            float:One Compensated pressure value [Pa]

        """
        
        p = self.calcScaledPressure()

        t= self.calcScaledTemperature()

        pressure =self.calcCompPressure(p, t)
        
        return pressure
             
            

class DPS422:

    """Class of DPS422, Pressure and Temperature sensor.

    """

    __bus = smbus.SMBus(1)

    __addr = 0x77



    # Compensation Scale Factors

    # Oversampling Rate          | Scale Factor (kP or kT)

    # ---------------------------|------------------------

    #   1       (single)         |  524288

    #   2 times (Low Power)      | 1572864

    #   4 times                  | 3670016

    #   8 times                  | 7864320

    #  16 times (Standard)       |  253952

    #  32 times                  |  516096

    #  64 times (High Precision) | 1040384  <- Configured

    # 128 times                  | 2088960

    __kP = 1040384

    __kT = 1040384
    
    DPS422_A_0 = 5030

    DPS422_T_REF = 27

    DPS422_T_C_VBE = -1.735e-3

    DPS422_V_BE_TARGET = 0.687027

    DPS422_K_PTAT_CORNER = -0.8

    DPS422_K_PTAT_CURVATURE = 0.039

    DPS422_ALPHA = 9.45




    def __init__(self):

        """Initial setting.



        Execute `self.correctTemperature()` and `self.setOversamplingRate()`.

        """

        self.__correctTemperature()

        self.__setOversamplingRate()





    def __correctTemperature(self):

        """Correct temperature.



        DPS422 sometimes indicates a temperature over 60 degree Celsius

        although room temperature is around 20-30 degree Celsius.

        Call this function to fix.

        """

        # Correct Temp

        DPS422.__bus.write_byte_data(DPS422.__addr, 0x0E, 0xA5)

        DPS422.__bus.write_byte_data(DPS422.__addr, 0x0F, 0x96)

        DPS422.__bus.write_byte_data(DPS422.__addr, 0x62, 0x02)

        DPS422.__bus.write_byte_data(DPS422.__addr, 0x0E, 0x00)

        DPS422.__bus.write_byte_data(DPS422.__addr, 0x0F, 0x00)





    def __setOversamplingRate(self):

        """Set oversampling rate.



        Pressure measurement rate    :  4 Hz

        Pressure oversampling rate   : 64 times

        Temperature measurement rate :  4 Hz

        Temperature oversampling rate: 64 times

        """

        # Oversampling Rate Setting (64time)

        DPS422.__bus.write_byte_data(DPS422.__addr, 0x06, 0x26)

        DPS422.__bus.write_byte_data(DPS422.__addr, 0x07, 0xA6)

        DPS422.__bus.write_byte_data(DPS422.__addr, 0x08, 0x07)

        # Oversampling Rate Configuration

        DPS422.__bus.write_byte_data(DPS422.__addr, 0x09, 0x0C)





    def __getRawPressure(self):

        """Get raw pressure from sensor.



        Returns:

            int: Raw pressure

        """

        p1 = DPS422.__bus.read_byte_data(DPS422.__addr, 0x00)

        p2 = DPS422.__bus.read_byte_data(DPS422.__addr, 0x01)

        p3 = DPS422.__bus.read_byte_data(DPS422.__addr, 0x02)



        p = (p1 << 16) | (p2 << 8) | p3

        p = getTwosComplement(p, 24)

        return p





    def __getRawTemperature(self):

        """Get raw temperature from sensor.



        Returns:

            int: Raw temperature

        """

        t1 = DPS422.__bus.read_byte_data(DPS422.__addr, 0x03)

        t2 = DPS422.__bus.read_byte_data(DPS422.__addr, 0x04)

        t3 = DPS422.__bus.read_byte_data(DPS422.__addr, 0x05)



        t = (t1 << 16) | (t2 << 8) | t3

        t = getTwosComplement(t, 24)

        return t





    def __getPressureCalibrationCoefficients(self):

        """Get pressure calibration coefficients from sensor.



        Returns:

            int: Pressure calibration coefficient (c00)

            int: Pressure calibration coefficient (c10)

            int: Pressure calibration coefficient (c01)

            int: Pressure calibration coefficient (c02)

            int: Pressure calibration coefficient (c20)

            int: Pressure calibration coefficient (c30)

            int: Pressure calibration coefficient (c11)

            int: Pressure calibration coefficient (c12)

            int: Pressure calibration coefficient (c21)

        """
        
        src26 = DPS422.__bus.read_byte_data(DPS422.__addr, 0x26)

        src27 = DPS422.__bus.read_byte_data(DPS422.__addr, 0x27)

        src28 = DPS422.__bus.read_byte_data(DPS422.__addr, 0x28)

        src29 = DPS422.__bus.read_byte_data(DPS422.__addr, 0x29)

        src2A = DPS422.__bus.read_byte_data(DPS422.__addr, 0x2A)

        src2B = DPS422.__bus.read_byte_data(DPS422.__addr, 0x2B)

        src2C = DPS422.__bus.read_byte_data(DPS422.__addr, 0x2C)

        src2D = DPS422.__bus.read_byte_data(DPS422.__addr, 0x2D)

        src2E = DPS422.__bus.read_byte_data(DPS422.__addr, 0x2E)

        src2F = DPS422.__bus.read_byte_data(DPS422.__addr, 0x2F)

        src30 = DPS422.__bus.read_byte_data(DPS422.__addr, 0x30)

        src31 = DPS422.__bus.read_byte_data(DPS422.__addr, 0x31)

        src32 = DPS422.__bus.read_byte_data(DPS422.__addr, 0x32)

        src33 = DPS422.__bus.read_byte_data(DPS422.__addr, 0x33)

        src34 = DPS422.__bus.read_byte_data(DPS422.__addr, 0x34)
        
        src35 = DPS422.__bus.read_byte_data(DPS422.__addr, 0x35)

        src36 = DPS422.__bus.read_byte_data(DPS422.__addr, 0x36)

        src37 = DPS422.__bus.read_byte_data(DPS422.__addr, 0x37)

        src38 = DPS422.__bus.read_byte_data(DPS422.__addr, 0x38)

        src39 = DPS422.__bus.read_byte_data(DPS422.__addr, 0x39)



        c00 = (src26 << 12) | (src27 << 4) | (src28 >> 4)

        c10 = ((src28 & 0x0F) << 16) | (src29 <<8) | src2A

        c01 = (src2B << 12) | (src2C << 4) | ((src2D & 0xF0) >> 4)

        c02 = ((src2D & 0x0F) << 16) | (src2E <<8) | src2F

        c20 = ((src30 & 0x7F) << 8) | src34

        c30 = ((src32 & 0x0F) << 8) | src33

        c11 = (src34 << 9) | (src35 << 1) | ((src36 & 0x80) >>7)

        c12 = ((src36 & 0x7F) << 10) | (src37 << 2) | ((src38 & 0xC0) >> 6)

        c21 = ((src38 & 0x7F) << 8) | src39


        c00 = getTwosComplement(c00, 20)

        c01 = getTwosComplement(c01, 20)

        c02 = getTwosComplement(c02, 20)
        
        c10 = getTwosComplement(c10, 20)

        c11 = getTwosComplement(c11, 17)

        c12 = getTwosComplement(c12, 17)

        c20 = getTwosComplement(c20, 15)
        
        c21 = getTwosComplement(c21, 14)        

        c30 = getTwosComplement(c30, 12)                


        return c00, c01, c02, c10, c11, c12, c20, c21, c30





    def __getTemperatureCalibrationCoefficients(self):

        """Get temperature calibration coefficients from sensor.



        Returns:

            float : Temperature calibration coefficient (a_prime)

            float : Temperature calibration coefficient (a_prime)

        """
        #read T_Gain, T_Vbe and T_dVbe
        T_Gain = DPS422.__bus.read_byte_data(DPS422.__addr, 0x20)

        T_dVBE_Coeff = DPS422.__bus.read_byte_data(DPS422.__addr, 0x21)

        T_VBE_Coeff = DPS422.__bus.read_byte_data(DPS422.__addr, 0x22)

        T_dVbe = T_dVBE_Coeff >> 1

        T_Vbe = (T_dVBE_Coeff & 0x01) | (T_VBE_Coeff << 1)
    
        T_Gain = getTwosComplement(T_Gain, 8)
    
        T_dVbe = getTwosComplement(T_dVbe, 7)

        T_Vbe = getTwosComplement(T_Vbe, 9)

        #Vbe, dVbe and Aadc
        Vbe = T_Vbe * 1.05031e-4 + 0.463232422
        dVbe = T_dVbe * 1.25885e-5 + 0.04027621
        Aadc = T_Gain * 8.4375e-5 + 0.675
        #Vbe_cal and dVbe_cal
        Vbe_cal = Vbe / Aadc
        dVbe_cal = dVbe / Aadc
        #T_calib
        T_calib = DPS422.DPS422_A_0 * dVbe_cal - 273.15
        #Vbe_cal(T_ref): Vbe value at reference temperature
        Vbe_cal_tref = Vbe_cal - (T_calib - DPS422.DPS422_T_REF) * DPS422.DPS422_T_C_VBE
        #calculate PTAT correction coefficient
        k_ptat = (DPS422.DPS422_V_BE_TARGET - Vbe_cal_tref) * DPS422.DPS422_K_PTAT_CORNER + DPS422.DPS422_K_PTAT_CURVATURE
        #calculate A_Prime and B_Prime
        a_prime = DPS422.DPS422_A_0 * (Vbe_cal + DPS422.DPS422_ALPHA * dVbe_cal) * (1 + k_ptat)
        b_prime = -273.15 * (1 + k_ptat) - k_ptat * T_calib



        return a_prime, b_prime





    def calcScaledPressure(self):

        """Calculate scaled pressure.



        Returns:

            float: Scaled pressure

        """

        raw_p = self.__getRawPressure()

        scaled_p = raw_p / DPS422.__kP

        return scaled_p





    def calcScaledTemperature(self):

        """Calculate scaled temperature.



        Returns:

            float: Scaled temperature

        """

        raw_t = self.__getRawTemperature()

        scaled_t = raw_t / DPS422.__kT

        return scaled_t





    def calcCompTemperature(self, scaled_t):

        """Calculate compensated temperature.



        Args:

            scaled_t (float): Scaled temperature



        Returns:

            float: Compensated temperature [C]

        """

        a_prime, b_prime = self.__getTemperatureCalibrationCoefficients()

        u = scaled_t / (1 + DPS422.DPS422_ALPHA * scaled_t)

        return (a_prime * u + b_prime)





    def calcCompPressure(self, scaled_p, scaled_t):

        """Calculate compensated pressure.



        Args:

            scaled_p (float): Scaled pressure

            scaled_t (float): Scaled temperature



        Returns:

            float: Compensated pressure [Pa]

        """

        c00, c01, c02, c10, c11, c12, c20, c21, c30 = self.__getPressureCalibrationCoefficients()

        temp = (8.5 * scaled_t) / (1 + 8.8 * scaled_t)

        comp_p = c00 +(c10 *scaled_p) + (c01 * temp )+ (c20 * scaled_p *scaled_p) + (c02 *temp *temp) + (c30 *scaled_p *scaled_p * scaled_p) + (c11 *temp * scaled_p) + (c12 * scaled_p *temp *temp) + (c21 * scaled_p *scaled_p *temp)


        return comp_p
    
    def measureBothOnce(self):

        """ measures compensated temperature and compensated pressure once

        Returns:
            
            float: Compensated Temperature 

            float: Compensated Pressure

        """
        t = self.calcScaledTemperature()
        
        temp = self.calcCompTemperature(t)
        
        p = self.calcScaledPressure()
        
        pressure = self.calcCompPressure(p, t)
        
        return temp, pressure
    


   





 