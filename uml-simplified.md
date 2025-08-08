# UML and Database Design Guide from class.

## What is UML?

UML (Unified Modeling Language) is a visual way to design and understand software systems before building them. There are two main types of diagrams we'll cover:

1. **Class Diagrams** - Show the structure of your code
2. **Entity Relationship Diagrams (ERD)** - Show the structure of your database

## Class Diagrams

### Basic Structure

A class is represented by a rectangle with three sections:

```
┌─────────────────┐
│   ClassName     │  ← Class name
├─────────────────┤
│ - attribute1    │  ← Attributes (data)
│ - attribute2    │
├─────────────────┤
│ + method1()     │  ← Methods (functions)
│ + method2()     │
└─────────────────┘
```

### Visibility

- `+` Public (accessible by anyone)
- `-` Private (only this class)
- `#` Protected (this class and subclasses)
- `~` Package (rarely used)

### Relationships

- **Inheritance** (IS-A): Open arrow →
- **Association** (USES): Simple line —
- **Aggregation** (HAS-A, parts can exist independently): Open diamond ◇
- **Composition** (HAS-A, parts cannot exist without whole): Filled diamond ◆

### Example: Zoo System

```
Animal (abstract)
├── Tortoise
├── Otter
└── SlowLoris
```

## Entity Relationship Diagrams (ERD)

### Components

1. **Entities** - Things in your database (Customer, Order, Product)
2. **Attributes** - Properties of entities (name, ID, email)
3. **Relationships** - How entities connect
4. **Cardinality** - Number constraints on relationships

### Cardinality Notation

- `1` - Exactly one
- `0..1` - Zero or one
- `1..*` - One or many
- `0..*` - Zero or many
- `*` - Many

### Keys

- **Primary Key (PK)** - Unique identifier for each record
  - Must be unique, never-changing, never-null
- **Foreign Key (FK)** - References a primary key in another table
- **Composite Key** - Multiple attributes combined to create uniqueness

### Example: E-commerce System

```
Customer (1) ←→ (0..*) Order (0..*) ←→ (1..*) Product
```

- One customer can have zero or many orders
- One order belongs to exactly one customer
- One order can contain one or many products
- One product can be in zero or many orders

### Bridge Tables

When you have a many-to-many relationship, you often need a bridge table to capture additional information about the relationship (like when an order was placed, quantity, etc.).

## Why Use These Diagrams?

### Class Diagrams Help You:

- Plan your code structure before programming
- Understand inheritance and relationships
- Communicate design with team members
- Avoid coding mistakes

### ERDs Help You:

- Design efficient databases
- Understand data relationships
- Prevent data redundancy
- Ensure data integrity
- Generate database code automatically

## Tools

You can draw these diagrams with:

- Pen and paper (simple projects)
- Lucidchart (recommended - free online tool)
- Draw.io
- Any diagramming software

## From Diagram to Code

Modern tools can:

- Generate database code from ERDs
- Create class skeletons from class diagrams
- Import existing databases to create ERDs
- Export diagrams to various database systems

This saves time and reduces errors when building real systems!

## Key Takeaway

Think of UML diagrams as blueprints for your software - just like architects create blueprints before building houses, software engineers create UML diagrams before writing code and databases.
