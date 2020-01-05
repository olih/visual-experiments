module Main exposing (Document, Model, Msg(..), init, main, subscriptions, update, view)

import Browser
import Dalmatian.Editor.Applicative as Applicative exposing (Model)
import Dalmatian.Editor.Schema exposing (PanelZone(..), ScreenZone(..))
import Dalmatian.Editor.AppEvent exposing (UIEvent(..))
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)


main =
    Browser.document
        { init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        }



-- MODEL


type alias Model =
    { greeting : String
    , applicative : Applicative.Model
    }


defaultModel : Model
defaultModel =
    { greeting = "Hello Goodbye"
    , applicative = Applicative.reset
    }


init : () -> ( Model, Cmd Msg )
init _ =
    ( defaultModel, Cmd.none )



-- UPDATE


type Msg
    = Hello
    | Goodbye
    | OnUIEvent UIEvent


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Hello ->
            ( { model | greeting = "I say \"hello\"" }, Cmd.none )

        Goodbye ->
            ( { model | greeting = "You say \"goodbye\"" }, Cmd.none )

        OnUIEvent event ->
            ( { model | greeting = "You say \"goodbye\"" }, Cmd.none )



{--each variant should return a model and a command message. If you are not using any command messages,
   then use "Cmd.none". This is different from what you may have done in "Browser.sandbox" if you started
   with the official guide's tutorials.
   
   For example: 
   
   Variant -> 
        ( { model | key = changeToValue }, Cmd.none ) --}
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
            [ h1 [] [ text model.greeting ]
            , button
                [ type_ "Button"
                , onClick
                    (if model.greeting == "You say \"goodbye\"" then
                        Hello

                     else
                        Goodbye
                    )
                ]
                [ text "Click me!" ]
            ]
        ]
    }

