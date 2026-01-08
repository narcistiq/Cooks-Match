"""
Code to find barcodes in data
"""


def is_valid_upc_barcode(text : str) -> bool:
    """
    Takes in a string and returns if it is a valid UPC barcode
    """
    if (len(text) != 12):
        return False

    for character in text:
        try:
            int(character)
        except:
            return False
    
    # Source implementation: https://boxshot.com/barcode/tutorials/upc-a-calculator/
    number = [int(digit) for digit in text]

    odd_sum  = sum(number[i] for i in range(0, 11, 2)) * 3
    even_sum = sum(number[i] for i in range(1, 11, 2))

    total = odd_sum + even_sum
    remainder = total % 10

    if (remainder != 0):
        remainder = 10 - remainder

    return text[-1] == str(remainder)

def get_barcode(text : List[str]) -> List[int]:
    """
    Returns a list of UPC barcodes given text input
    """

    for word in text:
        pass
    pass