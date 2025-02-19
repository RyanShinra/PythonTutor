def main():
    text = "hello world"
    for vowel in find_vowels(text):
        print(vowel)

def find_vowels(source: str):
    for x in source:
        if x.lower() in "aeiou":
            yield x.upper()

def get_chunks_of(source: str, size: int) :
    i = 0
    for i in range(0, len(source), size) :
        chunk = source[i: i+size]
        yield chunk

if __name__ == "__main__":
    main()