from flask import Flask, render_template, request
from abc import ABC, abstractmethod

app = Flask(__name__)

# Interfaz común para todos los métodos de pago
class PaymentMethod(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> str:
        pass

# Clases concretas para cada tipo de pago
class CreditCardPayment(PaymentMethod):
    def process_payment(self, amount: float) -> str:
        return f"Pago con tarjeta de crédito procesado exitosamente por ${amount}."

class PayPalPayment(PaymentMethod):
    def process_payment(self, amount: float) -> str:
        return f"Pago con PayPal procesado exitosamente por ${amount}."

class CryptoPayment(PaymentMethod):
    def process_payment(self, amount: float) -> str:
        return f"Pago con criptomonedas procesado exitosamente por ${amount}."

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

# Controlador para procesar la orden
def process_order(payment_method: str, amount: float) -> str:
    try:
        payment = PaymentFactory.create_payment_method(payment_method)
        return payment.process_payment(amount)
    except ValueError as e:
        return f"Error: {e}"

# Ruta para la página principal (Formulario de pago)
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para procesar el pago
@app.route('/process_payment', methods=['POST'])
def process_payment():
    method = request.form['payment_method']
    amount = float(request.form['amount'])
    result = process_order(method, amount)
    return render_template('index.html', result=result)

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
