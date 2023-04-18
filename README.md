# project E-commerce Django
This is an E-commerce project created using Django 4.1.4 and Python 3.8. The database used is a PostgreSQL hosted on AWS, and the website is hosted on (https://render.com/).

## You can access the E-commerce webpage here -> https://ecommerce.alanmf.com

> **Note**
> It may take some time (less than 3 min) to access the webpage as it is hosted on a free plan at render.com

## Educational content
This repository is for learning purposes and none of the products created within the page are real. 

This project was created within the course [Python 3 - Do Básico Ao Avançado (Completo)](https://www.udemy.com/course/python-3-do-zero-ao-avancado/), and  according to [Luiz Otávio's Repository](https://github.com/luizomf/django-simple-ecommerce). 
Some functionalities and templates were added later to implement the E-commerce functionality and design, making it more complete.

You are allowed to download, copy and use the contents of this repository under the MIT license.

PROJECT UNDER DEVELOPMENT.

### This project does NOT include
Below is a list of features I haven't added yet, that are pending to be added.

- Discount coupons in the shopping cart
- Payment methods (Visa, Mastercard, PayPal, etc...)
- Wishlist

### Included features 1
Below is a list of what was added along with the course, although the entire HTML and CSS has been restructured.

- [x] Product Model
- [x] Variation Model
- [x] List and details for products and variations
- [x] Shopping Cart based on sessions
- [x] Remove products from cart
- [x] Profile Model (create and update)
- [x] User Login and Logout
- [x] Register user order
- [x] Payment and checkout page

### Included features 2
Below is a list of what was added after the course, based on various E-commerce demands.

- [x] Image Model (for multiple images on each product)
- [x] Combinations of Product Variations (one product can have multiple variations)
- [x] Unique CPF Validator
- [x] Address Model (create and update)
- [x] Address validator (Brazil Addresses only) using ```pycep_correios``` [API](https://pypi.org/project/pycep-correios/)
- [x] Shipping calculator based on selected address
- [x] Multiple addresses per profile
- [x] Order details and tracking
- [x] JS scripts to increase response time for some features (calculate shipping price, validate address, stock alert, order tracking, etc...)
- [x] Forgot password recover by email

### ./utils folder
In this folder is located some python code for implemented features.

- [x] Shipping calculator
- [x] Address generator
- [x] CPF validator

### To clone this repository

```
git clone https://github.com/VenPoisen/project-Ecommerce-Django.git
```

```
pip install -r requirements.txt
```
