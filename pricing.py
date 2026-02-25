"""
pricing.py - محرك التسعير v5.1
"""

class PricingEngine:
    """محرك التسعير"""
    
    # الثوابت
    DRIVER_BASE = 4.00
    DRIVER_PER_KM = 0.80
    DRIVER_PER_MIN = 0.12
    
    STRIPE_PERCENT = 0.029
    STRIPE_FLAT = 0.30
    
    @classmethod
    def delivery_fee(cls, km):
        """رسوم التوصيل"""
        if km < 2: return 4.49
        elif km < 3: return 5.99
        elif km < 4: return 7.49
        elif km < 5: return 8.49
        elif km < 7: return 10.49
        else: return round(12.49 + (km - 7) * 0.50, 2)
    
    @classmethod
    def service_fee(cls, food_price):
        """رسوم الخدمة"""
        if food_price < 20:
            return 4.99
        base = food_price * 0.12
        return round(max(3.49, min(7.49, base)), 2)
    
    @classmethod
    def commission(cls, food_price):
        """عمولة المطعم"""
        if food_price < 20: return round(food_price * 0.18, 2)
        elif food_price < 40: return round(food_price * 0.15, 2)
        elif food_price < 80: return round(food_price * 0.12, 2)
        else: return round(food_price * 0.10, 2)
    
    @classmethod
    def driver_pay(cls, km, minutes):
        """أجر السائق"""
        return round(cls.DRIVER_BASE + (km * cls.DRIVER_PER_KM) + (minutes * cls.DRIVER_PER_MIN), 2)
    
    @classmethod
    def stripe_fee(cls, total):
        """رسوم Stripe"""
        return round(total * cls.STRIPE_PERCENT + cls.STRIPE_FLAT, 2)
    
    @classmethod
    def calculate(cls, food_price, km, minutes):
        """الحساب الكامل"""
        delivery = cls.delivery_fee(km)
        service = cls.service_fee(food_price)
        customer_total = round(food_price + delivery + service, 2)
        
        stripe = cls.stripe_fee(customer_total)
        net_received = round(customer_total - stripe, 2)
        
        comm = cls.commission(food_price)
        restaurant_gets = round(food_price - comm, 2)
        driver = cls.driver_pay(km, minutes)
        
        platform_profit = round(net_received - restaurant_gets - driver - 0.25, 2)
        
        return {
            "food_price": food_price,
            "distance_km": km,
            "duration_min": minutes,
            "delivery_fee": delivery,
            "service_fee": service,
            "customer_total": customer_total,
            "stripe_fee": stripe,
            "net_received": net_received,
            "commission": comm,
            "restaurant_gets": restaurant_gets,
            "driver_pay": driver,
            "platform_profit": platform_profit,
            "profitable": platform_profit >= 4.0
        }
