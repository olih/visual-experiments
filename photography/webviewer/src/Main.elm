module Main exposing (..)

import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http
import Json.Decode exposing (Decoder, field, string, decodeString)

-- MAIN


main =
  Browser.element
    { init = init
    , update = update
    , subscriptions = subscriptions
    , view = view
    }



-- MODEL


type Model
  = Failure
  | Loading
  | Success String


init : () -> (Model, Cmd Msg)
init _ =
  (Loading, getRandomGif)



-- UPDATE


type Msg
  = MorePlease
  | GotGif (Result Http.Error String)

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    MorePlease ->
      (Loading, getRandomGif)
    
    GotGif result ->
      case result of
        Ok url ->
          (Success url, Cmd.none)

        Err _ ->
          (Failure, Cmd.none)

-- SUBSCRIPTIONS

subscriptions : Model -> Sub Msg
subscriptions model =
  Sub.none

-- VIEW

view : Model -> Html Msg
view model =
  div []
    [ h2 [] [ text "Random image" ]
    , viewGif model
    ]


viewGif : Model -> Html Msg
viewGif model =
  case model of
    Failure ->
      div []
        [ text "I could not load a random image for some reason. "
        , button [ onClick MorePlease ] [ text "Try Again from application/json!" ]
        ]

    Loading ->
      text "Loading..."

    Success url ->
      div []
        [ button [ onClick MorePlease, style "display" "block" ] [ text "Another from application/json!" ]
        , img [ src url ] []
        ]



-- HTTP

getRandomGif : Cmd Msg
getRandomGif =
  Http.get
    { url = "http://localhost:8080/some-json.json"
    , expect = Http.expectJson GotGif gifDecoder
    }

gifDecoder : Decoder String
gifDecoder =
  field "data" (field "image_url" string)