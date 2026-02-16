# التمرين الأول باستخدام الجملة الشرطية و دالة التحقق من الأرقام
# : If, and the function: isdigit()

score_input = input("Please enter a score (0-100): ")

if not score_input.isdigit():
    print("Error: Invalid input. Please enter a positive whole number.")
else:
    score = int(score_input)
    if score > 100:
        print("Error: The score must be between 0 and 100")
    elif score >= 91:
        print("Grade: A")
    elif score >= 81:
        print("Grade: B")
    elif score >= 71:
        print("Grade: C")
    elif score >= 61:
        print("Grade: D")
    elif score >= 51:
        print("Grade: E")
    else:
        print("Grade: F")


print("\n----------------\n")

# التمرين الثاني باستخدام الجملة الشرطية للمطابقة
# : Match

score_input = input("Please enter a score (0--100): ")

if not score_input.isdigit():
    print("Error: Invalid input.")
else:
    score = int(score_input)
    
    if score > 100:
        print("Error: Score must be 0 -- 100")
    else:
        adjusted_score = (score - 1) // 10
        
        match adjusted_score:
            case 9:
                print("Grade: A")
            case 8:
                print("Grade: B")
            case 7:
                print("Grade: C")
            case 6:
                print("Grade: D")
            case 5:
                print("Grade: E")
            case _:
                print("Grade: F")
