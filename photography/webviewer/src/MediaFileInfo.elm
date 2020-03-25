module MediaFileInfo exposing (Model, decoder, view)

import Json.Decode exposing (Decoder, map3, field, string, list)
import Html exposing (..)

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

view : Model -> Html a
view model =
    div []
        [ text model.item
        ]