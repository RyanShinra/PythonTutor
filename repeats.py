def main():
    input = ["apple", "banana", "cherry"]

    max_str_len = max(len(word) for word in input)
    letters = set()

    for i in range(max_str_len):
        for word in input:
            if i < len(word):
                if word[i] in letters:
                    print(word[i])
                    return word[i]
                else:
                    letters.add(word[i])

    print('none')
    return None


if __name__ == "__main__":
    main()
 