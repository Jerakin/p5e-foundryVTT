# Extra Data
The data in these files will be used to overwrite the corresponding data in the template data.
Its useful for adding data that should be consistent between versions of this module, example of this is text such as
the flavour text when using moves. Data that isn't available in the data of the app could also be added in this way.


## JSON
Here is a small explanation of how JSON works, if this is not enough (I wrote this pretty quickly so I bet it isn't) then
please google it and read a bit, maybe even youtube it. JSON isn't a hard format to understand but it can look odd at first.
Here is a article that I skimmed quickly that looks to explain it okay https://www.digitalocean.com/community/tutorials/an-introduction-to-json

### Basic structure
The data here is stored in a format called JSON. The format of JSON is very strict but follows a couple of fairly simple rules.
* Data is represented in name/value pairs 
* Curly braces `{ }` hold objects and each name is followed by a colon `:`, the name/value pairs are separated by a comma `,`.
* Square brackets `[ ]` hold arrays and values are separated by a comma `,`.

### Keyword explinations
##### Objects
In json everything within `{ }` are a object, it's a collection of data

##### Array
In json everything within `[ ]` are a arrays, an array can contain any of the valid JSON data types

##### Values/data type
Only values in the key/value pair can hold data.
* strings - `""`, text surrounded by quotation marks
* numbers - `1`, `2`, `122` are all numbeers
* objects - `{ }`, they can be empty too!
* arrays - `[]` can store any kind of data type
* Booleans - `true` or `false`
* null - `null`, also known as "nil", "None", "nan".

##### Example
`{}` Empty object  
`{"key": "value"}` Basic key/value pair  
Nested objects 
```json
{
  "key": {
    "key": "value"
  }
}
```

Complex nested objects 
```json
{
  "Bulbasaur": {
    "data": {
      "_id": "random_string",
      "traits": {
        "size": "normal"
      }
    }
  }
}
```


## How do?
If you want to add something you first need to know where to add it. Take a look in the template file in `./assets/templates/`
to try to figure out where to add it. Let say that we want to add a `size` to Bulbasaur what we would do then is to open
up the `templates/pokemon.json` file and search for `size`, which we would find it under `"data" -> "traits" -> "size"`. Now we need to add this
exact hierarchy back into the `data\pokemon.json`.

Our end json would then look like this.
```json
{
  "Bulbasaur": {
    "data": {
      "traits": {
        "size": "medium"
       }
    }
  } 
}
```
But we have to add this into the existing `json` data that is there, for now that is only the `img` but it could be more
in the future. We have to add the `"data"` under Bulbasaur next to the `"img"` tag. Remember that the format is very important,
as this is a new line we have to add the `,` after the `"img"` line. If you are worried about your json formatting you
can always copy the whole document and use [jsonlint.com](https://www.jsonlint.com) to verify that it is correct. 

```json
{
  "Bulbasaur": {
    "img": "https://img.pokemondb.net/artwork/bulbasaur.jpg",
    "data": {
      "traits": {
        "size": "medium"
       }
    }
  } 
}
```

## Files
### move_icons.json
This store the different element icons. The `"img"` is the icon in the description **Type:** \<img\>

### moves.json
This is the data file that is overwriting the template data for every move. Here it could be nice to input a `chatFlavor`
for the moves.

### moves.json
Currently only containing the "Higher Level" text of a Move.

### pokemon.json
This is the data file that is overwriting the template data for every Pokemon. Images are already added.

### pokemon_extra.json
Currently only containing the Size of a Pokemon.

### pokemon_icon.json
This stores the different icons for the Pokemon, the `"img"` is the image that is used on the Pokemon Item. The `"token"`
is used as the token. These tokens are created by the script in `./tools/tokens/`.

