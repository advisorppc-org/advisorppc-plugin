{
  "count": 3,
  "managers": [
    "1112223334"
  ],
  "accounts": [
    {
      "id": "1112223334",
      "name": "Harbor Group (example manager)",
      "currency": "GBP",
      "timezone": "Europe/London",
      "manager": true,
      "status": "ENABLED",
      "level": 0,
      "via_manager": null,
      "source": "hierarchy"
    },
    {
      "id": "4455667788",
      "name": "Harbor Bakery (example)",
      "currency": "GBP",
      "timezone": "Europe/London",
      "manager": false,
      "status": "ENABLED",
      "level": 1,
      "via_manager": "1112223334",
      "source": "via_mcc"
    },
    {
      "id": "5566778899",
      "name": "Harbor Cafe (example)",
      "currency": "EUR",
      "timezone": "Europe/Dublin",
      "manager": false,
      "status": "ENABLED",
      "level": 1,
      "via_manager": "1112223334",
      "source": "via_mcc"
    }
  ],
  "mcc_accounts": {
    "1112223334": [
      "4455667788",
      "5566778899"
    ]
  },
  "customer_ids": [
    "1112223334",
    "4455667788",
    "5566778899"
  ],
  "direct_customer_ids": [
    "1112223334"
  ],
  "inventory_complete": true,
  "metadata_complete": true
}
