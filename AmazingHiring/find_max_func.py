def find_max(your_list):
    if len(your_list) == 0:
        raise ValueError("find_max() arg is an empty sequence")
    else:
        max = 0
        try:
            for element in your_list:
                if element > max:
                    max = element
        except TypeError:
            raise TypeError("Please make sure that the array contains only elements of type int.")
        return max
