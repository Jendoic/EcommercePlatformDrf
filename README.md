## E-commerce Platform API

This project is a comprehensive **E-commerce Platform API** built using **Django** and **Django REST Framework** (DRF). It provides a robust backend solution for managing products, orders, and payments, with full functionality for carts, payment integration, and order management. The API is designed with scalability and performance in mind, and follows Object-Oriented Programming (OOP) principles to ensure clean, maintainable code.

### Features

- **User Authentication**: Secure login and registration functionality.
- **Product Management**: Add, update, and delete products with comprehensive product details.
- **Cart Management**: Add and remove items from the cart, and manage cart functionality.
- **Order System**: Users can place orders, with a status system to track order progress.
- **Payment Integration**: Integrated with **Paystack** for seamless payment processing.
- **Email Notifications**: Automated order confirmation emails upon successful purchases.
- **Celery Integration**: Background tasks for sending order confirmation emails and other asynchronous tasks.
- **Redis for Celery**: Redis as a message broker for Celery task management.

### Technologies Used

- **Django**: Web framework for Python used to build the API.
- **Django REST Framework**: For building a powerful and flexible API.
- **PostgreSQL**: Database for storing product, cart, and order information.
- **Celery**: For asynchronous task management.
- **Redis**: As a message broker for Celery.
- **Paystack API**: Integrated for payment handling.

  
### Project Structure

```
.
├── accounts/            # User authentication and profiles
├── products/            # Product management functionality
├── carts/               # Cart functionality
├── orders/              # Order and payment logic
├── payments/            # Payment integration logic
└── README.md            # Project documentation
```

### Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/ecommerce-platform-api.git
   cd ecommerce-platform-api
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the environment variables:**

   Create a `.env` file in the root directory and add the following:

   ```
   SECRET_KEY=<your-secret-key>
   DEBUG=True
   DATABASE_URL=<your-database-url>
   PAYSTACK_PUBLIC_KEY=<your-paystack-public-key>
   PAYSTACK_SECRET_KEY=<your-paystack-secret-key>
   EMAIL_HOST_USER=<your-email>
   EMAIL_HOST_PASSWORD=<your-email-password>
   ```

5. **Run the migrations:**

   ```bash
   python manage.py migrate
   ```

6. **Run Redis for Celery:**

   ```bash
   redis-server
   ```

7. **Run the Celery worker:**

   ```bash
   celery -A ecommerce worker -l info
   ```

8. **Run the Django development server:**

   ```bash
   python manage.py runserver
   ```

### API Endpoints

- **User Authentication**:
  - `POST /api/v1/auth/register/`: Register a new user.
  - `POST /api/v1/auth/login/`: Login a user.

- **Products**:
  - `GET /api/v1/products/`: List all products.
  - `POST /api/v1/products/`: Create a new product (admin only).

- **Cart**:
  - `POST /api/v1/cart/add/`: Add an item to the cart.
  - `POST /api/v1/cart/remove/`: Remove an item from the cart.

- **Orders**:
  - `POST /api/v1/orders/create/`: Create a new order.
  - `GET /api/v1/orders/`: View user’s order history.

- **Payments**:
  - `POST /api/v1/payments/verify/`: Verify a payment after Paystack processing.

### Contribution

Feel free to fork the project and submit a pull request if you'd like to contribute. You can also submit issues to help improve the API.

### License

This project is licensed under the MIT License.

