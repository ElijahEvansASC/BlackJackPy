class InputValidateAndSanitize:

    @staticmethod
    def is_num_input(user_input):
        user_input = user_input.strip()
        try:
            number = int(user_input)
            return number
        except ValueError:
            print("Invalid Input: Please enter a numeric value.")
            return None
        except Exception as e:
            print(f"An error occured: {e}")

    @staticmethod
    def is_string_input(user_input):
        cleaned_input = user_input.strip().lower()
        return cleaned_input
        
