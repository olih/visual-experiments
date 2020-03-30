module Main exposing (Document, Model, Msg(..), init, main, subscriptions, update, view)

import Browser
import Experiment.Brush.Editor.Applicative as App
import Experiment.Brush.Editor.AppEvent exposing (UIEvent(..))
import Http
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)

type Model
  = Unloadable
  | Loading
  | Loaded App.Model


main =
    Browser.document
        { init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        }



-- MODEL

init : () -> ( Model, Cmd Msg )
init _ =
    ( Loading, fetchGeneticBrushes )


-- UPDATE


type Msg
    = OnUIEvent UIEvent
    | GotText (Result Http.Error String)


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        GotText result ->
            case result of
                Ok fullContent ->
                   case App.fromString fullContent of
                      Ok appModel ->
                        (Loaded appModel, Cmd.none )
                      Err failure ->
                        ( Unloadable, Cmd.none )

                Err _ ->
                    (Unloadable, Cmd.none)

        OnUIEvent event ->
            ( model , Cmd.none )


-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none

-- VIEW


type alias Document msg =
    { title : String
    , body : List (Html msg)
    }


view : Model -> Document Msg
view model =
    { title = "Hello Goodbye"
    , body =
        [ div []
            [ h1 [] [ text "ha" ]
           ]
        ]
    }


fetchGeneticBrushes :  Cmd Msg
fetchGeneticBrushes =
  Http.get
    { url = "/brushes.gen.txt"
    , expect = Http.expectString GotText
    }
