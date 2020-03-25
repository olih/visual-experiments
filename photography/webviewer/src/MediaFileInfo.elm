module MediaFileInfo exposing (Model, decoder)

import Json.Decode exposing (Decoder, map3, field, string, list)

type alias Model =
    { item : String
    , folder : String
    , tags : List String
    }

decoder : Decoder Model
decoder =
  map3 Model
      (field "item" string)
      (field "folder" string)
      (field "tags" (list string))
