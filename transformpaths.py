import os

def to_abs(path):
    abs_path = os.path.abspath(path)
    return abs_path    

def main():
    with open ("paths.txt", 'r') as input_file:
        paths = [line.rstrip() for line in input_file.readlines()]
        print(paths)
    
    for path in paths:
        path = to_abs(path)
        
    print(to_abs(path))
    
    
    

if __name__ == "__main__":
    main()
         