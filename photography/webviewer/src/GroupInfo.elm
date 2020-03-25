module GroupInfo exposing (Model, decoder)

import Json.Decode exposing (Decoder, map2, field, string, list)
import MediaFileInfo as MediaFileInfo

type alias Model =
    { 
    tags : List String
    , items: List MediaFileInfo.Model
    }

decoder : Decoder Model
decoder =
  map2 Model
      (field "tags" (list string))
      (field "items" (list MediaFileInfo.decoder))