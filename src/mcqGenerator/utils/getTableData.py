import json
import traceback

def get_table_data(quiz_str):
    try:
        if not quiz_str or quiz_str.strip() == "":
            raise ValueError("Empty or invalid JSON string received")

        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " | ".join(
                [
                    f"{option}: {option_value}"
                    for option, option_value in value["options"].items()
                ]
            )
            correct = value["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices":options,"Correct":correct})
        return quiz_table_data
    except Exception as e:
        traceback.print_exception(type(e),e,e.__traceback__)
        return False