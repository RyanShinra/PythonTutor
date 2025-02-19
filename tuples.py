def main():
    # Your code here
    print("Hello, World!")
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    my_tuples = [(x, x * x) for x in numbers if is_div_3(x)]
    
    print(my_tuples)
    
def is_div_3(num: int):
    return num % 3 == 0

if __name__ == "__main__":
    main()  