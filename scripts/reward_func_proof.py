import re


def _strip_string(string):
    for c in """\n\t .,$\\!?#%^&_+-={}""":
        string = string.replace(c, "")
    if string.startswith("text"):
        string = string.split("text")[1]
    return string.lower()


def last_boxed_only_string(string):
    idx = string.rfind("\\boxed")
    if idx < 0:
        idx = string.rfind("\\fbox")
        if idx < 0:
            return None

    i = idx
    right_brace_idx = None
    num_left_braces_open = 0
    while i < len(string):
        if string[i] == "{":
            num_left_braces_open += 1
        if string[i] == "}":
            num_left_braces_open -= 1
            if num_left_braces_open == 0:
                right_brace_idx = i
                break
        i += 1

    if right_brace_idx is None:
        retval = None
    else:
        retval = string[idx : right_brace_idx + 1]

    return retval


def remove_boxed(s):
    left = "\\boxed{"
    try:
        assert s[: len(left)] == left
        assert s[-1] == "}"
        return s[len(left) : -1]
    except Exception:
        return None


def is_equal(
    str1,
    str2,
):  
    if str1 is None and str2 is None:
        print("WARNING: Both None")
        return True
    if str1 is None or str2 is None:
        return False

    try:
        ss1 = _strip_string(str1)
        ss2 = _strip_string(str2)
        # print(ss1)
        # print(ss2)
        return ss1 == ss2
    except Exception:
        return str1 == str2


def solution2answer(s: str) -> str:
    res = remove_boxed(last_boxed_only_string(s))
    if res is not None:
        return res
    return s

def white_space_ratio(s):
    return (s.count(' ') + s.count('\n'))/len(s)

def repetition(s):
    return len(s) / len(set(s))

pattern = re.compile(r"<answer>.*?(\\boxed{.*}).*?</answer>", re.DOTALL)


def reward_func(data_source, solution_str, ground_truth, extra_info) -> float:
    if 'reasoning process' in solution_str and len(solution_str) < 90:
        return 0.0

    if 'User:' in solution_str or 'Assistant:' in solution_str or 'If you prove the statement, answer with "proved"' in solution_str:
        return 0.0

    if white_space_ratio(solution_str) < 0.05 or repetition(solution_str) > 300:
        return 0.0

    if "</think>" in solution_str:
        solution_str = solution_str.split("</think>")[-1]

    matches = re.findall(pattern, solution_str)
    answer_str = matches[-1] if matches else ""

    iscorrect = is_equal(solution2answer(ground_truth), solution2answer(answer_str))

    if iscorrect:
        reward = 1.0
    else:
        reward = 0.0

    return reward


if __name__ == "__main__":
    print(
        reward_func(
            "xxx",
            "First, let's simplify and solve the quadratic equation step-by-step.\n\nStarting with the given quadratic equation:\n\nx^2 - 4x - 14 = 3x + 16\n\nCombine like terms:\n\nx^2 - 4x - 3x - 14 = 16\n\nx^2 - 7x - 14 = 16\n\nSubtract 16 from both sides:\n\nx^2 - 7x - 14 - 16 = 0\n\nx^2 - 7x - 30 = 0\n\nNext, we need to factor the quadratic:\n\n(x - 10)(x + 3) = 0\n\nSetting each factor equal to zero:\n\nx - 10 = 0\n\nx = 10\n\nx + 3 = 0\n\nx = -3\n\nThe solutions to the quadratic equation are x = 10 and x = -3. To find the sum of these solutions:\n\nSum = 10 + (-3) = 7\n\nTherefore, the sum of the solutions to the quadratic equation x^2 - 4x - 14 = 3x + 16 is 7.</think>\n\n<answer>\\boxed{\\text{Proved}}</answer><|endoftext|>",
            "disproved",
            "xxx",
        )
    )