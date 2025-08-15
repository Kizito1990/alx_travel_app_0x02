# ALX Travel App 0x02 - Chapa Payment Integration

## Overview
This project integrates Chapa API for secure booking payments.

### Features
- Initiate payments via Chapa API
- Verify payment status
- Store payment details in Django model
- Send confirmation on successful payment

## Endpoints
### Initiate Payment
`POST /api/payments/initiate/`
```json
{
  "booking_reference": "BOOK123",
  "amount": 2000
}
