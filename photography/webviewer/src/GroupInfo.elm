module GroupInfo exposing (Model, decoder, reset, setItems)

import Json.Decode exposing (Decoder, map2, field, list)
import MediaFileInfo as MediaFileInfo
import Set exposing(Set)
import Tags as Tags

type alias Model =
    { 
    tags : Set String
    , items: List MediaFileInfo.Model
    }

reset: Model
reset = {
    tags = Tags.reset
    , items = []   
 }
decoder : Decoder Model
decoder =
  map2 Model
      (field "tags" Tags.toTags)
      (field "items" (list MediaFileInfo.decoder))

setItems: List MediaFileInfo.Model -> Model -> Model
setItems items model =
    { model | items = items}