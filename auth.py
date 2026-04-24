
NAV = {
    "public": [
        {"name": "Home",      "url": "/"},
        {"name": "About",     "url": "/about"},
        {"name": "Shop",      "url": "/shop"},
        {"name": "Producers", "url": "/producers"},
        {"name": "Contact",   "url": "/contact-us"},
    ],
    "login": [
        {"name": "Home",     "url": "/"},
        {"name": "About",    "url": "/about"},
        {"name": "Shop",     "url": "/shop"},
        {"name": "Register", "url": "/register"},
    ],
    "register": [
        {"name": "Home",  "url": "/"},
        {"name": "About", "url": "/about"},
        {"name": "Shop",  "url": "/shop"},
        {"name": "Login", "url": "/login"},
    ],
    "customer": [
        {"name": "Home",      "url": "/"},
        {"name": "Shop",      "url": "/shop"},
        {"name": "My Orders", "url": "/orders"},
        {"name": "Dashboard", "url": "/dashboard"},
        {"name": "Logout",    "url": "/logout"},
    ],
    "producer": [
        {"name": "Home",         "url": "/"},
        {"name": "Dashboard",    "url": "/producer/dashboard"},
        {"name": "Manage Stock", "url": "/producer/manage-stock"},
        {"name": "Settings",     "url": "/producer/settings"},
        {"name": "Logout",       "url": "/logout"},
    ],
    "admin": [
        {"name": "Home",             "url": "/"},
        {"name": "Admin Dashboard",  "url": "/admin/dashboard"},
        {"name": "Manage Accounts",  "url": "/admin/manage-accounts"},
        {"name": "Manage Products",  "url": "/admin/manage-products"},
        {"name": "All Orders",       "url": "/admin/orders"},
        {"name": "Settings",         "url": "/account-settings"},
        {"name": "Logout",           "url": "/logout"},
    ],
}


def nav_for(user) -> list:
    """Return the correct nav link set for the given user."""
    if user.role == "producer":
        return NAV["producer"]
    if user.role == "admin":
        return NAV["admin"]
    return NAV["customer"]


