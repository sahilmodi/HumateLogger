def get_input(query, valid_responses=[]):
    print(query)
    response = input()
    if len(valid_responses):
        return response if response.lower() in valid_responses else ""
    return response