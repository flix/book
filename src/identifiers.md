## Identifiers

Flix has several types of identifiers:

* **Uppercase name:** An identifier that starts with an uppercase letter followed by any number of uppercase and lowercase letters, underscore, and exclamation mark (`A`…`Z`, `a`…`z`, `_`, `!`).
  * e.g. `String`, `ALL_UPPER`, `Shriek!`
  * Can be used to name: namespaces, annotations, traits, effects, predicates (within datalog), tags (within enums), types
* **Lowercase name:** An identifier that starts with aa lowercase letter followed by any number of uppercase and lowercase letters, underscore, and exclamation mark (`A`…`Z`, `a`…`z`, `_`, `!`).
  * e.g. `anIdentifier`, `x`, `this_and_that`
  * Can be used to name: annotations, attributes (within datalog), functions, labels (within records), variables
* **Greek name:** An identifier consisting of any combination of letters from the Greek alphabet (the unicode range U+0370 to U+03FF).
  * e.g. `Χαίρετε`, `αναγνωριστικό`
  * Can be used to name: functions, variables
* **Math name:** An identifier consisting of any combination of math symbols (the unicode range U+2190 to U+22FF).
  * e.g. `⊆`, `√`, `⊙`
  * Can be used to name: functions, variables
* **Operator name:** An identifier of minimum length 2 consisting of any combination of `+`, `-`, `*`, `<`, `>`, `=`, `!`, `&`, `|`, `^`, and `$`.
  * e.g. `>==>`, `<*>`
  * Can be used to name: functions

Note that greek letters, math symbols, and operator letters cannot be combined within a single identifier.

## Reserved Identifiers

The following are reserved by Flix and cannot be redefined within user code:

`!=`, `**`, `..`, `::`, `:=`, `<-`, `<=`, `==`, `=>`, `>=`, `or`,
`&&&`, `<+>`, `<<<`, `<=>`, `>>>`, `???`, `^^^`, `and`, `mod`, `not`, `|||`, `~~~`,
`$DEFAULT$`, `*`, `+`, `-`, `/`, `:`, `<`,
`>`, `@`, `Absent`, `Bool`, `Impure`, `Nil`, `Predicate`, `Present`, `Pure`,
`Read`, `RecordRow`, `Region`, `SchemaRow`, `Type`, `Write`, `alias`, `case`, `catch`, `chan`,
`class`, `def`, `deref`, `else`, `enum`, `false`, `fix`, `force`,
`if`, `import`, `inline`, `instance`, `into`, `lat`, `law`, `lawful`, `lazy`, `let`, `match`,
`mod`, `null`, `opaque`, `override`, `pub`, `ref`, `region`, `reify`,
`reifyBool`, `reifyEff`, `reifyType`, `rel`, `sealed`, `set`, `spawn`, `Static`, `trait`, `true`,
`type`, `use`, `where`, `with`, `discard`, `object`, `choose`, `solve`, `inject`, `project`
