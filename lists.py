def main():
    # Your code here
    print("Hello, World!")
    words = ["apple", "banana", "egg", "ice", "orange", "cat", "elephant", "at"]
    answer = [first_letter_upper(x) for x in words if meets_criteria(x)]
    print(answer)

def meets_criteria(source: str):
    if len(source) < 3:
        return False
    if source[0].upper() not in "AEIOU":
        return False
    
    return True

def first_letter_upper(source: str):
    return source[0].upper() + source[1:]

if __name__ == "__main__":
    main()