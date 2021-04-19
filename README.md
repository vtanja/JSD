# DSL for generating Web applications

Our language can generate Spring Boot + Angular applications. The language itself is inspired by [raml](https://github.com/raml-org/raml-spec) language. SBAG will generate admin interface for managing each entity defined in your SBAG definition and create custom paths that you can override and create fancy new features! SBAG has configured Spring Security with basic authorization and authentication.

## Grammar

Language is separathed in three main parts:
1. Configuration, where you can specify some metadata which will be used while generating your next application.
2. Entities declaration, here you define entities that will be used in your application.
3. Custom paths, here you can define custom paths that will be generated and all you have to is add business logic to generated methods.

## Example

Here is a little example, we define a library project with its entites and custom paths.

```
project: Library

entity Book:
   title: String;
   publishingYear: int;
   generes: Genre[*..*];
   authors: Author[*..*books];
   publisher: Publisher[*..1];

entity Author:
   firstName: String;
   lastName: String;
   books: Book[*..*];
   address: Address[1..1];
   
entity Genre:
   name: String;
   books: Book[*..*genres];
   
entity Publisher:
   name: String;
   books; Book[1..*publisher];

entity Address:
   city: String;
   street: String;
   number: int;

/book
   get:
         return: Book[]
   /{id}
      get:
         return: Book

/author
   get:
      return: Author[]
   /{id}
      get:
         return: Author
      /book
         get: return: Book[]
         post: return: Book
         
/custom
   get: return String
```

## Generation

1. Configuration is not required, you can ommit it. In that case a default values will be used. You can define following properties:

- project - name of the project (will be used for folder and app names)
- description - short project description (used for readme files)

2. Entities - you need to specify them, and then use them later on while specifying custom paths. From entity declaration following is generated:

- Spring boot hibernate layer with model classes
- JPA repository for each entity
- DTO objects 
- Angular components for each CRUD operation
- Controller paths for CRUD operations
- CRUD business logic in services

When defining entities you will need to specify associations between them. This is done with '[]' and some parameters depending on association type. One side is the owning side, and other side is the inverse side. We are specifying owner attribute name on the inverse side:

- One to one association:  [1..1] and [1..1\<owner attribute name\>].
- One to many: [1..*\<owner attribute name\>].
- Many to one associations: [*..1].
- Many to many association: [*..*] and [*..*\<owner attribute name\>].

3. Custom paths are not required. If you define them they will be generated in different controller based on root path:

- if root path name is an entity name, path will be generated in that entity's controller
- else a new controller will be created for that root path, and every subpath will be generated in that conroller
   For each path, an empty method is generated in appropriate service for frontend and backend services.

# Credits

Initial project layout generated with `textx startproject`.
