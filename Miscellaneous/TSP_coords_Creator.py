import numpy as np

def generate_unique_coordinates(num_coordinates, x_range, y_range):
    coordinates = [(0, 0)]
    coordinates_set = set(coordinates)

    while len(coordinates_set) < num_coordinates + 1:
        x = np.random.randint(x_range[0], x_range[1] + 1)
        y = np.random.randint(y_range[0], y_range[1] + 1)
        new_coord = (x, y)
        if new_coord not in coordinates_set:
            coordinates_set.add(new_coord)
            coordinates.append(new_coord)

    return coordinates

def save_coordinates_to_file(coordinates, file_name="coordinates.txt"):
    with open(file_name, 'w') as f:
        for coord in coordinates:
            f.write(f"{coord[0]}, {coord[1]}\n")
    print(f"Coordinates saved to {file_name}")

def main():
    num_coordinates = int(input("Enter the number of coordinates (excluding the origin): "))
    x_min, x_max = map(int, input("Enter the x range (min max): ").split())
    y_min, y_max = map(int, input("Enter the y range (min max): ").split())

    coordinates = generate_unique_coordinates(num_coordinates, (x_min, x_max), (y_min, y_max))
    save_coordinates_to_file(coordinates)

if __name__ == "__main__":
    main()
