class Car:


    
    type = "High class car"

    def __init__(self, color, engine_displacement, distance):
        self.color = color
        self.engine_displacement = engine_displacement
        self.distance = distance

    def reset_counter(self):
        self.distance = 0

    def increase_counter(self, distance):
        self.distance += distance


mercides26 = Car("black", 2000, 100000)
mercides25 = Car("black", 2000, 100000)

mercides26.reset_counter()
mercides25.increase_counter(-85000)

print(f"Car Type: {mercides26.type} 2026")
print(f"Details: Color: {mercides26.color}, Engine: {mercides26.engine_displacement}cc, Distance: {mercides26.distance}km")

print(f"Car Type: {mercides25.type} 2025")
print(f"Details: Color: {mercides25.color}, Engine: {mercides25.engine_displacement}cc, Distance: {mercides25.distance}km")

