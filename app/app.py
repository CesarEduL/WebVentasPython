from flask import Flask, render_template, request, jsonify
from abc import ABC, abstractmethod

app = Flask(__name__)

# Datos de ejemplo para los productos
products = [
    {"id": 1, "name": "Smartphone XYZ", "price": 299.99, "image": "https://via.placeholder.com/150"},
    {"id": 2, "name": "Laptop ABC", "price": 799.99, "image": "https://via.placeholder.com/150"},
    {"id": 3, "name": "Auriculares Inalámbricos", "price": 89.99, "image": "https://via.placeholder.com/150"},
]

# Interfaz común para todos los métodos de pago
class PaymentMethod(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> str:
        pass

# Clases concretas para cada tipo de pago
class CreditCardPayment(PaymentMethod):
    def process_payment(self, amount: float) -> str:
        return f"Pago con tarjeta de crédito procesado exitosamente por ${amount:.2f}."

class PayPalPayment(PaymentMethod):
    def process_payment(self, amount: float) -> str:
        return f"Pago con PayPal procesado exitosamente por ${amount:.2f}."

class CryptoPayment(PaymentMethod):
    def process_payment(self, amount: float) -> str:
        return f"Pago con criptomonedas procesado exitosamente por ${amount:.2f}."

# Clase Factory para decidir qué tipo de pago crear
class PaymentFactory:
    @staticmethod
    def create_payment_method(method: str) -> PaymentMethod:
        if method == 'CreditCard':
            return CreditCardPayment()
        elif method == 'PayPal':
            return PayPalPayment()
        elif method == 'Crypto':
            return CryptoPayment()
        else:
            raise ValueError(f"Método de pago '{method}' no soportado.")

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html', products=products)

# Ruta para procesar el pago
@app.route('/process_payment', methods=['POST'])
def process_payment():
    data = request.json
    method = data['payment_method']
    amount = float(data['amount'])
    
    try:
        payment = PaymentFactory.create_payment_method(method)
        result = payment.process_payment(amount)
        return jsonify({"success": True, "message": result})
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)