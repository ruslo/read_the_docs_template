Mermaid diagram
---------------

.. seealso::

  - https://mermaid.js.org/
  - https://mermaid.live/

Flowchart
=========

.. seealso::

  - https://mermaid.js.org/syntax/flowchart.html

.. md-mermaid::
    ---
    config:
      look: handDrawn
    ---
    graph LR
      A[Start] --> B{Error?};
      B -->|Yes| C[Hmm...];
      C --> D[Debug];
      D --> B;
      B ---->|No| E[Yay!];

.. md-mermaid::
    ---
    config:
      look: handDrawn
    ---
    flowchart TD
      Start@{ shape: sm-circ }
      StartRebuild@{ shape: sm-circ }
      End@{ shape: framed-circle }
      Configure([Configure])
      Generate([Generate])
      Build([Build])
      CMakeListsChanged@{ shape: diamond, label: "?" }

      StartComment@{ shape: braces, label: "1" }
      StartComment -.- Start
      StartRebuildComment@{ shape: braces, label: "3" }
      StartRebuildComment -.- StartRebuild
      ConfigureComment@{ shape: braces, label: "2" }
      Configure -.- ConfigureComment
      CMakeListsChangedComment@{ shape: braces, label: "CMakeLists.txt changed?" }
      CMakeListsChangedComment -.- CMakeListsChanged

      classDef classData fill:yellow;

      CMakeLists.txt:::classData
      CMakeCache.txt:::classData
      Makefile:::classData
      Binaries:::classData

      Start --> Configure
      CMakeLists.txt --> Configure
      Configure --> CMakeCache.txt
      CMakeCache.txt --> Generate
      Generate --> Makefile
      Makefile --> Build
      Build --> CMakeListsChanged
      CMakeListsChanged -->|Yes| Configure
      CMakeListsChanged -->|No| Binaries
      Binaries --> End
      StartRebuild --> Build

.. note::

  - ``{1}`` The initial configuration step should be done only once by the user
  - ``{2}`` This is where ``Processing CMakeLists.txt`` printed
  - ``{3}`` You can keep using the native build tool. If ``CMakeLists.txt``
    changes, the native build tool will reconfigure automatically

Sequence diagram
================

.. seealso::

  - https://mermaid.js.org/syntax/sequenceDiagram.html

.. md-mermaid::
    sequenceDiagram
      autonumber
      Alice->>John: Hello John, how are you?
      loop Healthcheck
          John->>John: Fight against hypochondria
      end
      Note right of John: Rational thoughts!
      John-->>Alice: Great!
      John->>Bob: How about you?
      Bob-->>John: Jolly good!

State diagram
=============

.. seealso::

  - https://mermaid.js.org/syntax/stateDiagram.html

.. md-mermaid::
    ---
    title: State diagram
    ---
    stateDiagram-v2
      state fork_state <<fork>>
        [*] --> fork_state
        fork_state --> State2
        fork_state --> State3

        state join_state <<join>>
        State2 --> join_state
        State3 --> join_state
        join_state --> State4
        State4 --> [*]

Class diagram
=============

.. seealso::

  - https://mermaid.js.org/syntax/classDiagram.html

.. md-mermaid::
    classDiagram
      Person <|-- Student
      Person <|-- Professor
      Person : +String name
      Person : +String phoneNumber
      Person : +String emailAddress
      Person: +purchaseParkingPass()
      Address "1" <-- "0..1" Person:lives at
      class Student{
        +int studentNumber
        +int averageMark
        +isEligibleToEnrol()
        +getSeminarsTaken()
      }
      class Professor{
        +int salary
      }
      class Address{
        +String street
        +String city
        +String state
        +int postalCode
        +String country
        -validate()
        +outputAsLabel()
      }

Pie
===

.. seealso::

  - https://mermaid.js.org/syntax/pie.html

.. md-mermaid::
  pie title Pets adopted by volunteers
      "Dogs" : 386
      "Cats" : 85
      "Rats" : 15
