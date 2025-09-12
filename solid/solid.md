Absolutely! Let’s learn the **SOLID principles** — five foundational design principles in object-oriented programming (OOP) that help you write clean, maintainable, and scalable code. We’ll go through each one with clear **Python examples**.

---

## ✅ What is SOLID?

SOLID is an acronym for:

- **S**ingle Responsibility Principle
- **O**pen/Closed Principle
- **L**iskov Substitution Principle
- **I**nterface Segregation Principle
- **D**ependency Inversion Principle

Let’s break them down one by one.

---

## 1️⃣ Single Responsibility Principle (SRP)

> **A class should have only one reason to change.**

That means: **One class = One job.**

### ❌ Bad Example (Violates SRP)

```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def save_to_db(self):  # 👈 This is a database responsibility!
        print(f"Saving {self.name} to database...")

    def send_email(self):  # 👈 This is an email responsibility!
        print(f"Sending email to {self.email}")
```

Here, `User` handles user data, saving to DB, AND sending emails → **3 responsibilities!**

### ✅ Good Example (Follows SRP)

```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email


class UserRepository:
    def save(self, user: User):
        print(f"Saving {user.name} to database...")


class EmailService:
    def send_welcome_email(self, user: User):
        print(f"Sending welcome email to {user.email}")


# Usage
user = User("Alice", "alice@example.com")
repo = UserRepository()
email_service = EmailService()

repo.save(user)
email_service.send_welcome_email(user)
```

✅ Each class has **one clear responsibility**.

---

## 2️⃣ Open/Closed Principle (OCP)

> **Software entities (classes, modules, functions) should be open for extension, but closed for modification.**

You should be able to add new features **without changing existing code**.

### ❌ Bad Example

```python
class AreaCalculator:
    def calculate_area(self, shape):
        if shape.type == "rectangle":
            return shape.width * shape.height
        elif shape.type == "circle":  # 👈 Adding a new shape requires modifying this!
            return 3.14 * shape.radius ** 2
        elif shape.type == "triangle":  # 👈 Again, modifying!
            return 0.5 * shape.base * shape.height
```

Every time we add a new shape, we must edit this class → violates OCP!

### ✅ Good Example

```python
from abc import ABC, abstractmethod
import math

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2


class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height


class AreaCalculator:
    def calculate_area(self, shapes: list[Shape]):
        total = 0
        for shape in shapes:
            total += shape.area()  # 👈 No conditionals! Just call .area()
        return total


# Usage
shapes = [
    Rectangle(5, 4),
    Circle(3),
    Triangle(6, 8)
]

calc = AreaCalculator()
print(calc.calculate_area(shapes))  # Works with ANY Shape subclass!
```

✅ New shapes? Just create a new class inheriting `Shape`. **No need to touch `AreaCalculator`.**

---

## 3️⃣ Liskov Substitution Principle (LSP)

> **Objects of a superclass should be replaceable with objects of its subclasses without breaking the application.**

Subclasses must behave like their parent — they shouldn’t break expectations.

### ❌ Bad Example

```python
class Bird:
    def fly(self):
        print("Flying...")


class Penguin(Bird):
    def fly(self):  # 🚫 Penguins can't fly!
        raise Exception("Penguins can't fly!")


def make_bird_fly(bird: Bird):
    bird.fly()


# This breaks!
penguin = Penguin()
make_bird_fly(penguin)  # 💥 Exception!
```

This violates LSP — `Penguin` cannot substitute `Bird` without causing errors.

### ✅ Good Example

```python
from abc import ABC, abstractmethod

class Bird(ABC):
    pass

class FlyingBird(Bird):
    @abstractmethod
    def fly(self):
        pass

class SwimmingBird(Bird):
    @abstractmethod
    def swim(self):
        pass


class Eagle(FlyingBird):
    def fly(self):
        print("Eagle is flying high!")

class Penguin(SwimmingBird):
    def swim(self):
        print("Penguin is swimming!")


def make_bird_fly(bird: FlyingBird):
    bird.fly()


# Now it's safe:
eagle = Eagle()
make_bird_fly(eagle)  # ✅ Works

# penguin = Penguin()
# make_bird_fly(penguin)  # ❌ Type error! Can't pass SwimmingBird to function expecting FlyingBird
```

✅ We split behaviors into separate interfaces → **no broken expectations**.

---

## 4️⃣ Interface Segregation Principle (ISP)

> **Clients should not be forced to depend on interfaces they do not use.**

Don’t make classes implement big, bloated interfaces with methods they don’t need.

### ❌ Bad Example

```python
class Worker(ABC):
    @abstractmethod
    def work(self):
        pass

    @abstractmethod
    def eat(self):
        pass

    @abstractmethod
    def sleep(self):
        pass


class Robot(Worker):
    def work(self):
        print("Robot is working...")

    def eat(self):  # 🤖 Robots don't eat!
        raise NotImplementedError("Robots don't eat!")

    def sleep(self):  # 🤖 Robots don't sleep!
        raise NotImplementedError("Robots don't sleep!")
```

Robot is forced to implement irrelevant methods → violates ISP.

### ✅ Good Example

```python
from abc import ABC, abstractmethod

class Workable(ABC):
    @abstractmethod
    def work(self):
        pass


class Eatable(ABC):
    @abstractmethod
    def eat(self):
        pass


class Sleepable(ABC):
    @abstractmethod
    def sleep(self):
        pass


class Human(Workable, Eatable, Sleepable):
    def work(self):
        print("Human is working...")

    def eat(self):
        print("Human is eating...")

    def sleep(self):
        print("Human is sleeping...")


class Robot(Workable):  # 👈 Only implements what it needs
    def work(self):
        print("Robot is working...")
```

✅ Each class only implements interfaces it actually uses → **no unnecessary dependencies**.

---

## 5️⃣ Dependency Inversion Principle (DIP)

> **High-level modules should not depend on low-level modules. Both should depend on abstractions.**  
> **Abstractions should not depend on details. Details should depend on abstractions.**

In short: **Program to interfaces, not implementations.**

### ❌ Bad Example

```python
class MySQLDatabase:
    def save(self, data):
        print(f"Saving {data} to MySQL")


class UserManager:
    def __init__(self):
        self.db = MySQLDatabase()  # 👈 Direct dependency on concrete class!

    def add_user(self, user):
        self.db.save(user)
```

If you want to switch to PostgreSQL or MongoDB later, you must change `UserManager` → tight coupling!

### ✅ Good Example

```python
from abc import ABC, abstractmethod

class Database(ABC):  # 👈 Abstraction
    @abstractmethod
    def save(self, data):
        pass


class MySQLDatabase(Database):
    def save(self, data):
        print(f"Saving {data} to MySQL")


class PostgreSQLDatabase(Database):
    def save(self, data):
        print(f"Saving {data} to PostgreSQL")


class UserManager:
    def __init__(self, db: Database):  # 👈 Depends on abstraction!
        self.db = db

    def add_user(self, user):
        self.db.save(user)


# Usage
mysql_db = MySQLDatabase()
pg_db = PostgreSQLDatabase()

user_manager1 = UserManager(mysql_db)
user_manager2 = UserManager(pg_db)

user_manager1.add_user("Alice")  # Saving Alice to MySQL
user_manager2.add_user("Bob")    # Saving Bob to PostgreSQL
```

✅ `UserManager` doesn’t care what database you use — as long as it follows `Database` interface.  
✅ Easy to swap databases, mock for tests, etc.

---

## 🎯 Summary Table

| Principle | Key Idea                       | Python Pattern                                      |
| --------- | ------------------------------ | --------------------------------------------------- |
| **S**RP   | One class, one job             | Split responsibilities into separate classes        |
| **O**CP   | Extend, don’t modify           | Use inheritance + abstract base classes             |
| **L**SP   | Subtypes must be substitutable | Design hierarchies carefully; avoid broken behavior |
| **I**SP   | Small, focused interfaces      | Break large interfaces into smaller ones            |
| **D**IP   | Depend on abstractions         | Inject dependencies via interfaces                  |

---

## 💡 Pro Tips

- Use **abstract base classes (`ABC`)** and **type hints** in Python to enforce contracts.
- Always ask: _“What happens if I need to change this?”_ → If it’s hard, you might violate SOLID.
- SOLID helps with **testability**, **maintainability**, and **team collaboration**.

---

## ✅ Bonus: Putting It All Together (Realistic Example)

```python
from abc import ABC, abstractmethod
from typing import List

# SRP + ISP + DIP
class NotificationSender(ABC):
    @abstractmethod
    def send(self, message: str):
        pass

class EmailSender(NotificationSender):
    def send(self, message: str):
        print(f"📧 Sending email: {message}")

class SMSSender(NotificationSender):
    def send(self, message: str):
        print(f"📱 Sending SMS: {message}")

# SRP + OCP
class Order:
    def __init__(self, items: List[str]):
        self.items = items

    def total_price(self):
        return sum([10 for _ in self.items])  # Simplified

# DIP + OCP
class OrderProcessor:
    def __init__(self, notifier: NotificationSender):
        self.notifier = notifier  # Injected dependency

    def process(self, order: Order):
        print(f"📦 Processing order with {len(order.items)} items")
        # ... business logic ...
        self.notifier.send(f"Order processed! Total: ${order.total_price()}")

# Usage
order = Order(["Laptop", "Mouse"])
email_notifier = EmailSender()
sms_notifier = SMSSender()

processor1 = OrderProcessor(email_notifier)
processor2 = OrderProcessor(sms_notifier)

processor1.process(order)  # Sends email
processor2.process(order)  # Sends SMS
```

✅ All 5 SOLID principles applied!

---

## 🏁 Final Thought

SOLID isn’t about being “perfect” from day one — it’s about **evolving your code toward better structure**. Start applying them where it matters most: when things get messy, complex, or hard to test.

You’ve now got a solid foundation to write **clean, maintainable Python code** 🚀

Let me know if you’d like a quiz or exercise to test your understanding!
