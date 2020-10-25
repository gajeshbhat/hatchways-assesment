from json import dumps

# Errors
no_tag_error = dumps({"error": "Tags parameter is required"})
wrong_sortby_input_error = dumps({"error": "sortBy parameter is invalid"})
sorting_order_error = dumps({"error": "direction parameter is invalid"})
external_server_error = dumps({"error": "External Server did not respond. Try Again later."})