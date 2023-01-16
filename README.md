Payriff-Gateway
=======

Payriff Gateway for python based projects.


 ### Compatibility

Tested on Python 3.8+



### Get Started

First step: set Secret key of application as environment variables. (SEE `.example.env` file)


```bash
-> pip install requests
```

**Example (Create Order):**

```python
>>> from payriff_gateway import PayriffGateway
>>> 
>>> gateway = PayriffGateway(
>>>        merchant_id='your_merchant_id',
>>>        approve_url='https://example.com/approve',
>>>        cancel_url='https://example.com/cancel',
>>>        decline_url='https://example.com/decline',
>>>    )

>>> result = gateway.create_order(amount=100, currency="AZN" description="Lorem ipsum", direct_pay=True, language="AZ")
>>> print(result)
```

**Result:**

```python
>>> {'status_code': '00000', 'payment_url': 'https://tstpg.kapitalbank.az/index.jsp?OrderID=000000&SessionID=8EEF178F30464CED2F79176CE739E0F4', 'session_id': '8EEF178F30464CED2F79176CE739E0F4', 'order_id': '000000'}
```

**Example (Get Order Status):**

```python
>>> result = gateway.get_order_status(order_id=000000, language="AZ",session_id="8EEF178F30464CED2F79176CE739E0F4")
>>> print(result)
```

**Result:**

```python
>>> {'order_id': '000000', 'status_code': '00000', 'status': 'CREATED', 'message': 'Operation performed successfully'}
```


### Methods

**Example: get_order()**

```python
>>> order_obj = gateway.get_order()
>>> order_obj
>>> Order(amount=100, currency='AZN', status_code='00000', order_id='000000', session_id='8EEF178F30464CED2F79176CE739E0F4', payment_url='https://tstpg.kapitalbank.az/index.jsp?OrderID=000000&SessionID=8EEF178F30464CED2F79176CE739E0F4', transaction_id=123456)
```

**Example: get_order_status_instance()**

```python
>>> payment_status_obj = gateway.get_payment_status()
>>> payment_status_obj
>>> OrderStatus(order_id='00000', status_code='00000', status='CREATED', message='Operation performed successfully')
```

### Documentation
For more information, see the [Payriff Gateway Documentation](https://docs.payriff.com/).


### Credits
- <a href="https://github.com/ughurguliyev"> Ughur Guliyev </a>