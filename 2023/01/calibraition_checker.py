from typing import List 

def load_file(name: str) -> List[str]:
    with open(name, "r") as file:
        lines = file.readlines()
    return lines

word_numbers = {"one":1, "two":2, "three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8, "nine":9}
def get_number(line, i, reverse=False, advanced=False):
    if line[i].isdigit():
        return line[i]
    
    if not advanced: return None

    segment = line[i:min(i+5,len(line))] if not reverse else line[max(i-5,0):i]

    for k in [3, 4, 5]:
        segment = line[i:min(i+k,len(line))] if not reverse else line[max(i+1-k,0):i+1]
        # print(segment)
        if segment in word_numbers: return str(word_numbers[segment])

    return None

def calibration_checker(lines, advanced=False) -> int:
    total = 0
    for line in lines:
        line = line.strip()
        l, r = 0, len(line) - 1
        ld, rd = None, None

        while l <= r:
            n = get_number(line, l, advanced=advanced)
            if n:
                ld = n
                break
            l += 1

        while r >= l: 
            n = get_number(line, r, reverse=True, advanced=advanced)
            if n:
                rd = n
                break
            r -= 1

        # print(line.strip(), int(ld+rd))
        total += int(ld + rd)
    return total

# test_custom = ["two19", "onetwo99", "2one5a", "26two"]
print(calibration_checker(load_file("calibration_document.txt")))
print(calibration_checker(load_file("advanced_calibration_document.txt"), advanced=True))
# print(calibration_checker(test_custom, advanced=True))
