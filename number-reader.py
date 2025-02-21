import os
from typing import Callable, Literal

StatTypes = Literal['average', 'sum', 'max']
class FileAnalyzer:
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.numbers: list[int] = []
        # maybe self.stats or some such
        pass

    def __enter__(self):
        try:
            with open(self.file_path) as file:
                for line in file:
                    for word in line.split(' '):
                        try:
                            self.numbers.append(float(word))
                        except ValueError:
                            continue
        except FileNotFoundError as e:
            print(f'File does not exist: {self.file_path}')
            raise e
        
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        # Cleanup code if needed
        pass

    def __getitem__(self, action: StatTypes) -> float:
        match action:
            case 'average':
                return sum(self.numbers) / len(self.numbers)
            case 'sum':
                return sum(self.numbers)
            case 'max':
                return max(self.numbers)
            case _:
                raise KeyError(f"Unknown statistic: {action}")
            
    def get_number(self):
        for num in self.numbers:
            yield num
            
    def process_with_function(self, your_fn: Callable[[int], int]):
        for num in self.numbers:
            yield your_fn(num)


def main():
    with open('dummy.txt', 'w') as file:
        file.write("Here are numbers: 12.5 45 78.333\n")
        file.write("More numbers: 90.1 34.7 21\n")
        file.write("And more: 56 89.999 23.456")
        
    
    
    with FileAnalyzer('dummy.txt') as helper:
        print('\n Original Numbers: ')
        for num in helper.get_number():
            print(num)
        
        print('\n Squared Numbers: ')
        for num_x in helper.process_with_function(lambda x: x**2):
            print(num_x)
           
        print('\nStatistics')
        print(f'\n Average: {helper['average']}')
        print(f'\n Sum: {helper['sum']}')
        print(f'\n Maximum: {helper['max']}')
            
if __name__ == "__main__":
    main()