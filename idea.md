## Database Table
Customers
    id
    first_name
    last_name
    creator_id
    created_at

Users
    id
    email
    password
    role - [admin, regular]

Transactions
    id
    customer_id
    creator_id
    Amount
    currency_received - [NGN, USD]
    rate_applied
    rate_base
    created_at


## API definitions
Users
    /users/ - POST - create a new user
    /users/ - GET - get a list of all users
                /?limit=10&skip=0
    /users/{id} - GET - get a specific user by id
    /users/{id} - PUT - update a user information (Admins can update any user or a logged in user can only update his own user information)
    /users/{id} - DELETE - delete a user from the database

Customers
    /customers/ - POST - create a new customer - only logged-in user
    /customers/ - GET - get a list of all the customers created by logged-in user - only owner
        /?limit=10&skip=0
    /customers/{id} - GET - get a customer based on id - only owner
    /customers/{id} - PUT - update a customer information - only owner
    /customers/{id} - DELETE - delete a customer information - only owner

Transactions
    /transactions/ - POST - create a new transaction - only logged-in user
    /transactions/ - GET  - a list of transactions - only owner
        /?limit=10&skip=0&currency=NGN
    /transactions/customer/{id} - GET - a list of transaction by a specific customer - only owner
        /?limit=10&skip=0&currency=NGN
    /transactions/{id} - GET - get a specific transaction - only owner
    /transactions/{id} - PUT - update a specific transaction - only owner
    /transactions/{id} - DELETE - delete a specific transaction - only owner
    

    