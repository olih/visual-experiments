module MediaFileInfo exposing (Model, decoder, view)

import Json.Decode exposing (Decoder, map3, field, string)
import Html exposing (..)
import Set exposing(Set)
import Tags as Tags

type alias Model =
    { item : String
    , folder : String
    , tags : Set String
    }


decoder : Decoder Model
decoder =
  map3 Model
      (field "item" string)
      (field "folder" string)
      (field "tags" Tags.toTags)

view : Model -> Html a
view model =
    div []
        [ text model.item
        ]