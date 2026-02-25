"""
database.py - إدارة قاعدة البيانات JSON
"""

import json
import os
import threading
from datetime import datetime


class Database:
    """قاعدة بيانات JSON بسيطة"""
    
    def __init__(self, db_file="delivery_db.json"):
        self.db_file = db_file
        self._lock = threading.Lock()
        self._ensure_db()
    
    def _default_data(self):
        """البيانات الافتراضية"""
        return {
            "restaurants": {},
            "drivers": {},
            "customers": {},
            "orders": {},
            "profit": 0.0,
            "completed": 0,
            "cancelled": 0,
            "created": datetime.now().isoformat(),
            "version": "6.0-web"
        }
    
    def _ensure_db(self):
        """إنشاء قاعدة البيانات إذا لم تكن موجودة"""
        if not os.path.exists(self.db_file):
            self._write(self._default_data())
    
    def _read(self):
        """قراءة قاعدة البيانات"""
        try:
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return self._default_data()
    
    def _write(self, data):
        """كتابة قاعدة البيانات"""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load(self):
        """تحميل البيانات"""
        with self._lock:
            return self._read()
    
    def save(self, data):
        """حفظ البيانات"""
        with self._lock:
            self._write(data)
    
    def add_order(self, order):
        """إضافة طلب جديد"""
        data = self.load()
        if 'orders' not in data:
            data['orders'] = {}
        data['orders'][order['id']] = order
        self.save(data)
        return order
    
    def get_order(self, order_id):
        """الحصول على طلب"""
        data = self.load()
        return data.get('orders', {}).get(order_id)
    
    def update_order(self, order_id, updates):
        """تحديث طلب"""
        data = self.load()
        if order_id in data.get('orders', {}):
            data['orders'][order_id].update(updates)
            self.save(data)
            return True
        return False
    
    def get_pending_orders(self):
        """الحصول على الطلبات المعلقة"""
        data = self.load()
        return [o for o in data.get('orders', {}).values() if o['status'] == 'pending']
    
    def get_driver_orders(self, driver_id):
        """الحصول على طلبات السائق"""
        data = self.load()
        return [o for o in data.get('orders', {}).values() 
                if o.get('driver_id') == driver_id and o['status'] in ['accepted', 'pending']]
