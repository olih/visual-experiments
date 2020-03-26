module MediaFileInfo exposing (Model, decoder, view)

import Json.Decode exposing (Decoder, map3, field, string)
import Html exposing (Html, figure, img)
import Html.Attributes as Attr exposing (src)
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
    figure [ Attr.class "image is-128x128" ]
    [ img [ [model.folder, "/small-", model.item] |> String.concat |> src]
        []
    ]